import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        numerical_index = response.css('section[id=numerical-index]')
        table = numerical_index.css('tbody')
        rows = table.css('tr')
        for row in rows:
            pep_link = row.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_info = response.css('section[id=pep-content]')
        pep_title = pep_info.css('.page-title::text').get().split()
        number = int(pep_title[1])
        name = ' '.join(pep_title[3:])
        status = pep_info.css('dt:contains("Status") + dd::text').get()
        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
