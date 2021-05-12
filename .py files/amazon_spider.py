import scrapy
from ..items import AmazonItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    # start_urls = ['https://www.amazon.in/s?bbn=10983941031&rh=n%3A976389031%2Cn%3A%211318447031%2Cn%3A%211318449031%2Cn%3A%2120348517031%2Cn%3A10983941031%2Cp_85%3A10440599031&pf_rd_i=10983941031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=99c1d4b3-23e5-4aba-9e5f-c8217cfd92a3&pf_rd_r=FJY4HZFC0DFNK5XDCFN7&pf_rd_s=merchandised-search-1&pf_rd_t=101&ref=s9_acsd_hps_bw_c2_x_c2cl']
    start_urls = ['https://www.amazon.in/s?rh=n%3A23033693031&fs=true&ref=lp_23033693031_sar']
    count = 0

    def parse(self, response):
        items = AmazonItem()
        product_list = response.xpath(
            './/*[@class="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16"]')

        for book in product_list:
            if AmazonSpiderSpider.count <= 5000:
                book_name = book.css('a.a-link-normal .a-color-base.a-text-normal::text').extract()
                book_type = book.xpath('.//a[@class="a-size-base a-link-normal a-text-bold"]/text()').extract()
                book_price = book.css('.a-price-whole::text').extract()
                book_author = book.css('.a-color-secondary .a-size-base:nth-child(2) , .a-color-secondary .a-size-base.a-link-normal').css('::text').extract()

                items['book_name'] = book_name
                items['book_author'] = book_author
                items['book_type'] = book_type
                items['book_price'] = book_price

                AmazonSpiderSpider.count += 1
                print(AmazonSpiderSpider.count)
                yield items

            else:
                break

        next_url = response.xpath('.//li[@class="a-last"]/a/@href').get()
        if response.xpath('.//li[@class="a-last"]/a/text()').get() == 'Next':
            yield response.follow(next_url, callback=self.parse)



