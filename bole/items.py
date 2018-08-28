import scrapy


class MmItem(scrapy.Item):
    images_url = scrapy.Field()
    images_path = scrapy.Field()