from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from jianshu.items import JianshuItem

class jianshu(CrawlSpider):
    name='jianshu'
    start_urls=['https://www.jianshu.com/c/20f7f4031550?order_by=added_at&page=1']

    def parse(self,response):
        item=JianshuItem()
        selector=Selector(response)
        infos=selector.xpath('//ul[@class="note-list"]/li')

        for info in infos:
            user=info.xpath('div/div[1]/div/a/text()').extract()[0]
            time = info.xpath('div/div[1]/div/span/@data-shared-at').extract()[0]
            title = info.xpath('div/a/text()').extract()[0]
            view = info.xpath('div/div[2]/a[1]/text()').extract()[1].strip()
            comment = info.xpath('div/div[2]/a[2]/text()').extract()[1].strip()
            like = info.xpath('div/div[2]/span[1]/text()').extract()[0].strip()
            gain = info.xpath('div/div[2]/span[2]/text()').extract()
            if gain:
                gain=gain[0].strip()
            else:
                gain='0'

            item['user']=user
            item['time'] = time
            item['title'] = title
            item['view'] = view
            item['comment'] = comment
            item['like'] = like
            item['gain'] = gain
            yield item

        urls=['https://www.jianshu.com/c/20f7f4031550?order_by=added_at&page={}'.format(str(i)) for i in range(2,5)]
        for url in urls:
            yield Request(url,callback=self.parse)
