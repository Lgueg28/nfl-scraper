import scrapy
from datetime import datetime


class TeamDataSpider(scrapy.Spider):
    """Pulls all of the historical team passing data"""
    name = 'team-passing-nfl'
    start_urls = ['https://www.nfl.com/stats/team-stats/']

    def parse(self, response):
        current_year = datetime.now().year
        # //div[has-class("nfl-c-form__group")]/select/option/text() - does the same thing
        for year in response.xpath('//div/label[contains(text(),"Year")]/following-sibling::select/option/text()').getall():
            if year != current_year:
                passing_stats_url = f"https://www.nfl.com/stats/team-stats/offense/passing/{year}/reg/all"
                yield response.follow(passing_stats_url, self.parse_passing_stats, meta={'year': year})

    def parse_passing_stats(self, response):
        year = response.meta['year']
        # TODO - I broke this loop :(
        for team_row in response.xpath('//span[has-class("TeamLink__Logo")]/../../..').getall():
            index = team_row.xpath('@data-idx').extract_first()
            team = team_row.xpath('span[has-class("TeamLink__Logo")]/following-sibling::a/text()').extract_first()
            yield {
                'year': year,
                'name': team,
                'att': team_row.xpath('td[2]/text()').extract_first(),
                'cmp': team_row.xpath('td[3]/text()').extract_first(),
                'cmp_pct': team_row.xpath('td[4]/text()').extract_first(),
                'yds_att': team_row.xpath('td[5]/text()').extract_first(),
                'yds': team_row.xpath('td[6]/text()').extract_first(),
                'td': team_row.xpath('td[7]/text()').extract_first(),
                'int': team_row.xpath('td[8]/text()').extract_first(),
                'rate': team_row.xpath('td[9]/text()').extract_first(),
                '1st': team_row.xpath('td[10]/text()').extract_first(),
                '1st%': team_row.xpath('td[11]/text()').extract_first(),
                '20+': team_row.xpath('td[12]/text()').extract_first(),
                '40+': team_row.xpath('td[13]/text()').extract_first(),
                'Lng': team_row.xpath('td[14]/text()').extract_first(),
                'Sck': team_row.xpath('td[15]/text()').extract_first(),
                'SckY': team_row.xpath('td[16]/text()').extract_first(),
            }
