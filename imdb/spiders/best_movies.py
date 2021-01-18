# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating']

    rules = (
        #Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//h3[@class= 'lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a [ @ class = 'lister-page-next next-page'])[1]")),
    )# in the crwal spider the callback method is defined as string.

    def parse_item(self, response):
        yield{
            'title' : response.xpath("//div[@class= 'title_wrapper']/h1/text()").get(),
            'year' : response.xpath("//span[@id = 'titleYear']/a/text()").get(),
            'duration' : response.xpath("normalize-space((//time)[1]/text())").get(),
            #normalize-space remove extra space from xpath value
            'genre' : response.xpath("//div[@ class ='subtext']/a[1]/text()").get(),
            'rating' : response.xpath("//span[@itemprop = 'ratingValue']/text()").get(),
            'movie_url' : response.url,
        }
