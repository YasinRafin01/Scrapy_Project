# Trip.com Hotel Scraper

This project is a Scrapy spider designed to scrape hotel information from Trip.com and store it in a PostgreSQL database.

## Features

- Scrapes hotel data from Trip.com including:
  - hote_id
  - hotel_name
  - hotel_url
  - hotel_location
  - latitude
  - longitude
  - rating
  - image_url
  - price
  - city
  - section(Header)
- Stores data in a PostgreSQL database using SQLAlchemy
- Automatically creates database tables


## Prerequisites

- Python 3.7+
- PostgreSQL
- pip
- Scrapy

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/YasinRafin01/Scrapy_Project.git
   ```

2. Create a virtual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  
   ```
3. Set up your PostgreSQL database and update the connection details in `config.py`.
   ```
   DATABASE_URL = "postgresql://username:password@localhost:port/database_name"
   ```

## Usage
To install require dependencies:
```
pip install -r requirements.txt
```

To run the spider, use the following command:

```
cd trip_scraper
scrapy crawl trip_spider
```

This will start the scraping process, storing data in the database and saving images to the `images` directory.

## Project Structure

- `trip_scraper/` - Main project directory
  - `spiders/` - Contains the Scrapy spider
      - `__init__.py`
      - `trip_spider.py`
  - `__init__.py`
  - `hotel_model.py` 
  - `items.py` - Defines the structure of scraped items
  -  `middlewares.py`- Defines the middlewares
  - `pipelines.py` - Handles data processing and storage
  - `settings.py` - Project settings including database configuration


## Configuration

Update the `hotel_model.py` file to configure:
- Database connection details

Update the `settings.py` file to configure:
- Scraping behavior (e.g., request delays, concurrent requests)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
