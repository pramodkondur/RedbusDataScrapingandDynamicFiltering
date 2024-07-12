from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import pandas as pd
import mysql.connector

# use pip install webdriver-manager also which is needed

# Setup MYSQL connection
# utilize your preferred database
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="expert789",
    database="RedBus"
)

cursor = con.cursor()

# Query to Create Table
query = """CREATE TABLE if not exists bus_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name TEXT,
    route_link TEXT,
    busname TEXT,
    bustype TEXT,
    departing_time DATETIME,
    duration TEXT,
    reaching_time DATETIME,
    star_rating FLOAT,
    price DECIMAL(10, 2),
    seats_available INT
    )"""
cursor.execute(query)

# Truncate Table
query = "TRUNCATE TABLE bus_routes"
cursor.execute(query)


# Function to scroll to end of page to get all buses
def scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for page to load

        time.sleep(.2)

        # Calculate new scroll height and compare with last scroll height

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


# Function to get bus details
def get_bus_details_for_route(url):
    driver.get(url)
    route_info = (driver.find_element(By.CLASS_NAME, 'D136_h1').text).replace(' Bus', '')

    dayelem = driver.find_element(By.XPATH, '//*[@id="searchDat"]')
    dayvar = (dayelem.get_attribute('value')) + " 2024"

    # waiting for page to load
    time.sleep(4)

    # Expanding all the buses section if it has 'view buses' button
    # Adding an exception block if it is unable to click view buses button
    try:
        tourismBusesAgency = driver.find_elements(By.CLASS_NAME, 'gmeta-data.clearfix')

        for agency in tourismBusesAgency:
            btn_var = agency.find_element(By.CLASS_NAME, "button")
            btn_var.click()
    except ElementClickInterceptedException:
        print(url, 'view-buses in this url not clickable')

    # Scrolling so all the bus data gets loaded
    scroll()

    # Creating empty list to store the details of the buses
    buses_list = []

    # Getting all the buses group so that we can get all the bus details for each of them i.e. states and private buses
    busesgroup = driver.find_elements(By.CLASS_NAME, 'bus-items')

    for buses in busesgroup:
        buseslist = buses.find_elements(By.CLASS_NAME, 'clearfix.bus-item')

        #print("buses number:", len(buseslist))

        # Gets all the required bus details in the selected group

        for bus in buseslist:
            busname = bus.find_element(By.CLASS_NAME, 'travels.lh-24.f-bold.d-color').text
            # print(busname)
            bustype = bus.find_element(By.CLASS_NAME, 'bus-type.f-12.m-top-16.l-color.evBus').text
            departing_time = dayvar + " " + bus.find_element(By.CLASS_NAME, 'dp-time.f-19.d-color.f-bold').text + ":00"
            duration = bus.find_element(By.CLASS_NAME, 'dur.l-color.lh-24').text

            # Some buses have reaching date as the next day, so we are using try and exception to get these values
            try:
                bus.find_element(By.CLASS_NAME, 'next-day-dp-lbl.m-top-16') != 0
                new_date = ((bus.find_element(By.CLASS_NAME, 'next-day-dp-lbl.m-top-16').text).replace("-",
                                                                                                       " ")) + " 2024"
                reaching_time = new_date + " " + bus.find_element(By.CLASS_NAME,
                                                                  'bp-time.f-19.d-color.disp-Inline').text + ":00"

            except NoSuchElementException:
                reaching_time = dayvar + " " + bus.find_element(By.CLASS_NAME,
                                                                'bp-time.f-19.d-color.disp-Inline').text + ":00"

            star_rating = (((bus.find_element(By.CLASS_NAME, 'column-six.p-right-10.w-10.fl').text).replace("New",
                                                                                                            "0")).replace(
                " ", "0"))[0:3]
            price = (bus.find_element(By.CLASS_NAME, 'fare.d-block').text).replace("INR ", "")
            seats_available = (bus.find_element(By.CLASS_NAME, 'column-eight.w-15.fl').text)[0:2]

            # print(bus_name, bus_type, departing_time, duration, reaching_time, star_rating, price, seats_available)

            bus_item = {
                'route_name': route_info,
                'route_link': url,
                'busname': busname,
                'bustype': bustype,
                'departing_time': datetime.strptime(departing_time, "%d %b %Y %H:%M:%S"),
                'duration': duration,
                'reaching_time': datetime.strptime(reaching_time, "%d %b %Y %H:%M:%S"),
                'star_rating': float(star_rating),
                'price': float(price),
                'seats_available': float(seats_available[0:2])

            }

            buses_list.append(bus_item)

    # Once all details of the buses are got for a route, we convert it to a dataframe so that we can write it to the db
    df = pd.DataFrame(buses_list)
    return (df)


# Function to write the scrapped data into database
def write_into_db(df):
    query = """insert into bus_routes (route_name,route_link,busname,bustype,departing_time,duration,reaching_time,star_rating,price,seats_available) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
             """
    result = []

    for index in df.index:
        row_data = list(df.loc[index].values)
        result.append(row_data)
    cursor.executemany(query,
                       result)  # execute many and storing data in list as it connects to the db once it finishes getting input rather than each time
    con.commit()


# A list to store all the route urls for each state transportation
routes_urls = []


# Function to get all the routes url for the selected state transportation
def get_urls(url):
    driver.get(url)
    time.sleep(2)

    routes_list_to_get_urls = driver.find_elements(By.CLASS_NAME, 'route_link')
    # This line used for checking no.of routes fetched from the page --> print(len(routes_list_to_get_urls))
    # Gets all routes for page 1
    for routes in routes_list_to_get_urls:
        url_to_extract = routes.find_element(By.TAG_NAME, 'a')
        url_extracted = url_to_extract.get_attribute('href')
        #print(url_extracted)
        routes_urls.append(url_extracted)

    # To handle pagination
    page_elements = driver.find_elements(By.CLASS_NAME, 'DC_117_pageTabs')

    for page in page_elements:
        try:
            page.click()
            print(page.text)
            time.sleep(.2)
            routes_list_to_get_urls = driver.find_elements(By.CLASS_NAME, 'route_link')
            # This line used for checking no.of routes fetched from the page --> print(len(routes_list_to_get_urls))
            # Gets all routes for page 2 to end
            for routes in routes_list_to_get_urls:
                url_to_extract = routes.find_element(By.TAG_NAME, 'a')
                url_extracted = url_to_extract.get_attribute('href')
                #print(url_extracted)
                routes_urls.append(url_extracted)
        # Usually the page 1 is not clickable since it is active, so we need to catch the exception
        except ElementClickInterceptedException:
            print('the page is not not clickable')


list_of_state_tourism_url = ['https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile',
                             'https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile',
                             'https://www.redbus.in/online-booking/astc/?utm_source=rtchometile',
                             'https://www.redbus.in/online-booking/pepsu/?utm_source=rtchometile',
                             'https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile',
                             'https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile',
                             'https://www.redbus.in/online-booking/jksrtc',
                             'https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile',
                             'https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile',
                             'https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile'
                             ]

# Collecting all the urls for routes from the state tourism urls
for url in list_of_state_tourism_url:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    get_urls(url)

# Collects all the bus details data from each route url we collected and writes to db
for url in routes_urls:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    df = get_bus_details_for_route(url)
    write_into_db(df)

con.close()
