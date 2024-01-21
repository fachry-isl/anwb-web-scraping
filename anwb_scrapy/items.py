# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnwbScrapyItem(scrapy.Item):
    carname = scrapy.Field()
    manufacturer = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    chassis = scrapy.Field()
    fuel_type = scrapy.Field()
    detailed_url = scrapy.Field()
