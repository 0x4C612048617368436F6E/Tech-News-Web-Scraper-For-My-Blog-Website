# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscraperItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    DateAndTime = scrapy.Field()
    ExtractedInformation = scrapy.Field()
