import scrapy


class TeamRushingOffenseESPNSpider(scrapy.Spider):
    """Pulls all of the historical team rushing data"""
    name = 'team-rushing-offense-espn'
    start_urls = ['https://www.espn.com/nfl/stats/team/_/view/offense/stat/rushing/table/rushing']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.1
    }

    def parse(self, response):
        query = '//div[has-class("filters__seasonDropdown")]/select/option[contains(text(), "Regular")]/@value'
        for value in response.xpath(query).getall():
            parts = value.split('|')
            season = parts[0]
            season_type = parts[1]
            # https://www.espn.com/nfl/stats/team/_/view/offense/stat/rushing/season/2020/seasontype/2/table/rushing
            rushing_stats_url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/rushing/season/{season}/seasontype/{season_type}/table/rushing"
            yield response.follow(rushing_stats_url, self.parse_rushing_stats, meta={'year': season})

    def parse_rushing_stats(self, response):
        year = response.meta['year']
        team_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[0]
        stats_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[1]
        for team_row in team_tbody.xpath('tr'):
            team_idx = team_row.xpath('@data-idx').extract_first()
            team_name = team_row.xpath('td/div/a/text()').extract_first()
            team_row = stats_tbody.xpath(f'tr[@data-idx={team_idx}]')
            yield {
                'year': year,
                'name': team_name,
                'gp': team_row.xpath('td[1]/div/text()').extract_first(),
                'att': team_row.xpath('td[2]/div/text()').extract_first(),
                'yds': team_row.xpath('td[3]/div/text()').extract_first(),
                'avg': team_row.xpath('td[4]/div/text()').extract_first(),
                'yds_gm': team_row.xpath('td[5]/div/text()').extract_first(),
                'lng': team_row.xpath('td[6]/div/text()').extract_first(),
                'td': team_row.xpath('td[7]/div/text()').extract_first(),
                'fum': team_row.xpath('td[8]/div/text()').extract_first(),
                'lst': team_row.xpath('td[9]/div/text()').extract_first()
            }
