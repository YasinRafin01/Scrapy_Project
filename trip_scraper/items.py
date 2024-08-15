# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TripItem(scrapy.Item):
    hotel_id = scrapy.Field()
    name = scrapy.Field()
    hotel_type = scrapy.Field()
    scrapy_date = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    checkin_date = scrapy.Field()
    checkout_date = scrapy.Field()
    gap = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    price_un = scrapy.Field()
    price = scrapy.Field()
    star_rating = scrapy.Field()
    review_score = scrapy.Field()
    number_of_reviews = scrapy.Field()
    room_type = scrapy.Field()
    uri = scrapy.Field()