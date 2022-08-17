import scrapy


class TeamDataSpider(scrapy.Spider):
    """Pulls all of the historical team passing data"""
    name = 'team-passing-espn'
    start_urls = ['https://www.espn.com/nfl/stats/team/_/view/offense/stat/passing/table/passing']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.1
    }

    def parse(self, response):
        # current_year = datetime.now().year
        # https://www.espn.com/nfl/stats/team/_/view/offense/stat/passing/season/2020/seasontype/2/table/passing/sort/netPassingYardsPerGame/dir/descte
        query = '//div[has-class("filters__seasonDropdown")]/select/option[contains(text(), "Regular")]/@value'
        for value in response.xpath(query).getall():
            parts = value.split('|')
            season = parts[0]
            season_type = parts[1]
            passing_stats_url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/passing/season/{season}/seasontype/{season_type}/table/passing/sort/netPassingYardsPerGame/dir/desc"
            yield response.follow(passing_stats_url, self.parse_passing_stats, meta={'year': season})

    def parse_passing_stats(self, response):
        year = response.meta['year']
        team_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[0]
        stats_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[1]
        for team_row in team_tbody.xpath('tr'):
            team_idx = team_row.xpath('@data-idx').extract_first()
            team_name = team_row.xpath('td/div/a/text()').extract_first()
            yield {
                'year': year,
                'idx': team_idx,
                'name': team_name,
                # 'att': team_row.xpath('td[2]/text()').extract_first(),
                # 'cmp': team_row.xpath('td[3]/text()').extract_first(),
                # 'cmp_pct': team_row.xpath('td[4]/text()').extract_first(),
                # 'yds_att': team_row.xpath('td[5]/text()').extract_first(),
                # 'yds': team_row.xpath('td[6]/text()').extract_first(),
                # 'td': team_row.xpath('td[7]/text()').extract_first(),
                # 'int': team_row.xpath('td[8]/text()').extract_first(),
                # 'rate': team_row.xpath('td[9]/text()').extract_first(),
                # '1st': team_row.xpath('td[10]/text()').extract_first(),
                # '1st%': team_row.xpath('td[11]/text()').extract_first(),
                # '20+': team_row.xpath('td[12]/text()').extract_first(),
                # '40+': team_row.xpath('td[13]/text()').extract_first(),
                # 'Lng': team_row.xpath('td[14]/text()').extract_first(),
                # 'Sck': team_row.xpath('td[15]/text()').extract_first(),
                # 'SckY': team_row.xpath('td[16]/text()').extract_first(),
            }
