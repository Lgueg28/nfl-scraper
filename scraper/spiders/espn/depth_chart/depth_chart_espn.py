import scrapy
from datetime import datetime


class DepthChartESPNSpider(scrapy.Spider):
    """Pulls all of the current depth charts"""
    name = 'depth-chart-espn'
    start_urls = ['https://www.espn.com/nfl/story/_/id/29098001/2022-nfl-depth-charts-all-32-teams']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.1
    }

    def parse(self, response):
        # TODO: Scrape weekly?
        current_year = datetime.now().year
        query = '//a[starts-with(@href, "https://www.espn.com/nfl/team/depth/_/name/")]/@href'
        for depth_chart in response.xpath(query).getall():
            yield response.follow(depth_chart, self.parse_depth_chart, meta={'year': current_year, 'week': 1})

    def parse_depth_chart(self, response):
        year = response.meta['year']
        week = response.meta['week']
        team = response.xpath('//h1[has-class("headline")]/text()')
        offense_header = response.xpath('//div[has-class("Table__Title")]')[0].xpath('text()')
        defense_header = response.xpath('//div[has-class("Table__Title")]')[1].xpath('text()')
        off_label_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[0]
        off_player_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[1]
        def_label_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[2]
        def_player_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[3]
        st_label_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[4]
        st_player_tbody = response.xpath('//tbody[has-class("Table__TBODY")]')[5]
        yield {
            'year': year,
            'week': week,
            'team': team.extract_first().replace(' Depth Chart', ''),
            'offense': {
                'formation': offense_header.extract_first(),
                'depth_chart': self.extract_depth_chart(off_label_tbody, off_player_tbody)
            },
            'defense': {
                'formation': defense_header.extract_first(),
                'depth_chart': self.extract_depth_chart(def_label_tbody, def_player_tbody)
            },
            'special_teams': {
                'depth_chart': self.extract_depth_chart(st_label_tbody, st_player_tbody)
            },
        }

    def extract_depth_chart(self, label_tbody, player_tbody):
        depth_chart_map = {}
        for position_row in label_tbody.xpath('tr'):
            pos_idx = position_row.xpath('@data-idx').extract_first()
            position = position_row.xpath('td/span/text()').extract_first()
            player_row = player_tbody.xpath(f'tr[@data-idx={pos_idx}]')
            player_1 = player_row.xpath('td[1]/span/a/text()').extract_first()
            player_2 = player_row.xpath('td[2]/span/a/text()').extract_first()
            player_3 = player_row.xpath('td[3]/span/a/text()').extract_first()
            player_4 = player_row.xpath('td[4]/span/a/text()').extract_first()
            players = [player_1, player_2, player_3, player_4]
            players = list(filter(None, players))
            depth_chart_map[position] = players
        return depth_chart_map
