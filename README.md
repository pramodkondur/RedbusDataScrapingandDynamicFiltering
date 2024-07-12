# Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

## Overview

The **Redbus Data Scraping and Filtering with Streamlit Application** project is designed to transform the transportation industry by automating the collection, analysis, and visualization of bus travel data. This project leverages Selenium for web scraping, Python for data manipulation, SQL for data storage, and Streamlit for creating an interactive application to visualize and filter the data.

## Skills and Technologies

- **Web Scraping**: Selenium
- **Programming Language**: Python
- **Data Analysis & Visualization**: Streamlit
- **Data Storage**: SQL
- **Domain**: Transportation

## Problem Statement

The project aims to streamline the process of collecting and analyzing bus travel information from the Redbus website. By automating data extraction and providing a user-friendly interface for data exploration, the project seeks to improve operational efficiency, support market analysis, and enhance customer service in the transportation industry.

## Business Use Cases

This solution can be applied in various scenarios including:

- **Travel Aggregators**: Offering real-time bus schedules and seat availability for customers.
- **Market Analysis**: Studying travel patterns and preferences for strategic planning.
- **Customer Service**: Providing customized travel options and improving user experience.
- **Competitor Analysis**: Comparing pricing and service levels with other providers.

## Approach

### Data Scraping

- **Tool**: Selenium
- **Objective**: Automate the extraction of detailed bus travel information from Redbus.
- **Data Collected**: Bus routes, schedules, prices, seat availability, etc.

### Data Storage

- **Tool**: SQL
- **Objective**: Store scraped data in a structured SQL database for efficient querying and analysis.

### Streamlit Application

- **Tool**: Streamlit
- **Objective**: Develop an interactive web application to filter and display the scraped data.
- **Features**:
  - Filters for bus type, route, price range, star rating, and availability.
  - Data visualization and interactive user interface.

### Data Analysis/Filtering

- **Tool**: SQL queries within Streamlit
- **Objective**: Retrieve and filter data based on user inputs.

## Results

The project aims to achieve the following objectives:

- **Scrape Data**: Collect data from at least 10 Government State Bus Transport routes from the Redbus website, along with private bus information.
- **Store Data**: Organize data in a structured SQL database.
- **Develop Application**: Create a functional and user-friendly Streamlit application for data filtering.
- **User Experience**: Ensure the application is intuitive and responsive.

## Project Evaluation Metrics

- **Data Scraping Accuracy**: Completeness and correctness of the scraped data.
- **Database Design**: Effectiveness of the database schema for data storage and retrieval.
- **Application Usability**: User experience and functionality of the Streamlit application.
- **Filter Functionality**: Efficiency and responsiveness of the data filters.
- **Code Quality**: Adherence to coding standards and best practices.

## Technical Tags

- Web Scraping
- Selenium
- Streamlit
- SQL
- Data Analysis
- Python
- Interactive Application

## Data Set

- **Source**: Redbus website [https://www.redbus.in/](https://www.redbus.in/)
- **Format**: SQL database
- **Fields**:
  - **Bus Routes Name**: Start and end locations of the bus journey.
  - **Bus Routes Link**: Detailed link for the route.
  - **Bus Name**: Name of the bus or service provider.
  - **Bus Type**: Type of bus (e.g., Sleeper, Seater, AC, Non-AC).
  - **Departing Time**: Scheduled departure time.
  - **Duration**: Total journey time.
  - **Reaching Time**: Expected arrival time.
  - **Star Rating**: Passenger rating of the bus service.
  - **Price**: Ticket price.
  - **Seat Availability**: Number of available seats.

## Database Schema

| Column Name      | Data Type | Description                                      |
|------------------|----------|--------------------------------------------------|
| id               | INT      | Primary Key (Auto-increment)                    |
| route_name       | TEXT     | Bus Route information                           |
| route_link       | TEXT     | Link to the route details                        |
| busname           | TEXT     | Name of the bus                                 |
| bustype          | TEXT     | Type of the bus (Sleeper/Seater/AC/Non-AC)      |
| departing_time   | DATETIME | Departure time                                   |
| duration         | TEXT     | Duration of the journey                          |
| reaching_time    | DATETIME | Arrival time                                     |
| star_rating      | FLOAT    | Rating of the bus                                |
| price            | DECIMAL   | Ticket price                                     |
| seats_available  | INT      | Number of seats available                       |
