import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        for pep_link in response.css(
                'section#numerical-index td a::attr(href)'
        ).getall():
            yield response.follow(pep_link + '/', callback=self.parse_pep)

    def parse_pep(self, response):
        pep_number, name = response.css(
            'h1.page-title::text'
        ).get().split(' – ')
        yield PepParseItem(
            number=pep_number.split()[1],
            name=name,
            status=response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get(),
        )
