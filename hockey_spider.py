import json
import scrapy

class HockeySpider(scrapy.Spider):
    name = 'hockey'
    start_urls = ['https://scrapethissite.com/pages/forms/']
    
    def __init__(self, *args, **kwargs):
        super(HockeySpider, self).__init__(*args, **kwargs)
        self.data = {}

    def parse(self, response):
        for row in response.css('tr.team'):
            team_name = row.css('td.name::text').get()
            year = row.css('td.year::text').get()
            wins_count = row.css('td.wins::text').get()
            
            if team_name and year and wins_count:
                team_name = team_name.strip()
                year = int(year.strip()) if year.strip().isdigit() else 0
                wins_count = int(wins_count.strip()) if wins_count.strip().isdigit() else 0
                
                # Create the clean record dictionary profile
                record = {
                    "year": year,
                    "wins": wins_count
                }
                
                # Initialize an empty list folder if the team is completely new
                if team_name not in self.data:
                    self.data[team_name] = []
                
                # CORE BUG FIX: Only append if this exact year record doesn't exist yet
                # This explicitly blocks duplicate values from being added to the JSON array
                if not any(existing_rec['year'] == year for existing_rec in self.data[team_name]):
                    self.data[team_name].append(record)

        # Dynamic pagination handling: follow the "Next" link button
        next_page = response.css('ul.pagination li a[aria-label="Next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        output_filename = 'hockey_stats.json'
        with open(output_filename, 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, indent=4, ensure_ascii=False)
        self.log(f"Successfully serialized clean data to {output_filename}")
