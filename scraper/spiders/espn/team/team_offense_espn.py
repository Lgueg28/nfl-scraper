import scrapy


class TeamTotalOffenseDataESPNSpider(scrapy.Spider):
    """Pulls all of the historical team total offense data"""
    name = 'team-total-offense-espn'
    start_urls = ['https://www.espn.com/nfl/stats/team']
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
            # https://www.espn.com/nfl/stats/team/_/season/2020/seasontype/2
            total_offense_stats_url = f"https://www.espn.com/nfl/stats/team/_/season/{season}/seasontype/{season_type}"
            yield response.follow(total_offense_stats_url, self.parse_total_offense_stats, meta={'year': season})

    def parse_total_offense_stats(self, response):
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
                'yds': team_row.xpath('td[2]/div/text()').extract_first(),
                'yds_gm': team_row.xpath('td[3]/div/text()').extract_first(),
                'pass_yds': team_row.xpath('td[4]/div/text()').extract_first(),
                'pass_yds_gm': team_row.xpath('td[5]/div/text()').extract_first(),
                'rush_yds': team_row.xpath('td[6]/div/text()').extract_first(),
                'rush_yds_gm': team_row.xpath('td[7]/div/text()').extract_first(),
                'pts': team_row.xpath('td[8]/div/text()').extract_first(),
                'pts_gm': team_row.xpath('td[9]/div/text()').extract_first()
            }