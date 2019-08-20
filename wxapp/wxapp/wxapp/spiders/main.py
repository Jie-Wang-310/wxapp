# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem


class MainSpider(CrawlSpider):
    name = 'main'
    allowed_domains = ['www.wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(
            allow=r'.+mod=list&catid=2&page=\d'),
            follow=True),
        Rule(LinkExtractor(allow=r".+article-.+\.html"),
             callback="parse_detail", follow=False)
    )

    def parse_detail(self, response):
        item = WxappItem()
        title = response.xpath('//div/h1[@class="ph"]/text()').get()
        author_p = response.xpath('//div/p[@class="authors"]')
        author = author_p.xpath('.//a/text()').get()
        pub_time = author_p.xpath('.//span[@class="time"]/text()').get()
        artitcle_content = response.xpath('//td[@id="article_content"]//text()').getall()
        content = "".join(artitcle_content).strip()     # 将其转换为字符串，并去掉空白

        item['title'] = title
        item['author'] = author
        item['pub_time'] = pub_time
        item['content'] = content

        yield item



