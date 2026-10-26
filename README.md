# NHL Hockey Statistics JSON Persistence Engine

An automated, asynchronous web crawling backend engine built in Python utilizing the Scrapy framework. The engine programmatically traverses interactive pagination layouts, extracts historical statistics from a live sandbox database, and formats the elements into a custom, hierarchical in-memory schema utilizing dictionary mapping and list aggregation before serializing the dataset to JSON.

## Key Engineering Accomplishments
* Asynchronous Processing: Built using Scrapy's event-driven runtime to perform non-blocking web request rounds across multi-page tables.
* Recursive Pagination Tracking: Programmatic link-following logic that parses UI pagination blocks (ul.pagination li a) to track live URL modifications automatically.
* Hierarchical State Management: Avoided overwriting recurring dictionary records by pairing unique team string keys directly with an appending list array of annual nested records.
* Runtime Deduplication Engine: Includes an automated lookahead guard check (if not any(...)) that evaluates the global memory dictionary array during execution to block duplicate entries from entering the final file format.

## System Architecture & Logic Breakdown

### 1. In-Memory Persistent State Engine
An empty structural tracking dictionary is bound to the core crawler instance utilizing Python's initialization constructor:
```python
def __init__(self, *args, **kwargs):
    super(HockeySpider, self).__init__(*args, **kwargs)
    self.data = {} # Centralized dictionary cache preserved throughout crawling life cycles
```

### 2. Hierarchical Node Aggregation & Deduplication Guard
The parser extracts textual elements from table rows. If a team name does not exist yet inside our memory cache, a fresh list array container is instantiated. Yearly records are checked for duplication before being appended:
```python
record = {
    "year": int(year) if year.isdigit() else 0,
    "wins": int(wins_count) if wins_count.isdigit() else 0
}

if team_name not in self.data:
    self.data[team_name] = [] # Instantiate folder list container

# Deduplication Filter: Check existing array records before appending
if not any(existing_rec['year'] == year for existing_rec in self.data[team_name]):
    self.data[team_name].append(record) # Slip record into the folder array safely
```

### 3. Recursive Pagination Callback Loop
The engine targets the navigation interface elements, extracts the link layer source parameters, and passes execution loops forward continuously:
```python
next_page = response.css('ul.pagination li a[aria-label="Next"]::attr(href)').get()
if next_page is not None:
    yield response.follow(next_page, callback=self.parse)
```

## Setup & Execution Instructions

### Deployment
Execute the crawler spider locally from the root folder directory using your terminal execution command:
```bash
python3 -m scrapy runspider hockey_spider.py --set HTTPCACHE_ENABLED=False
```

### Serialized Data Output Structure
Upon pipeline completion, the engine exports a structured, completely deduplicated hockey_stats.json timeline file tracking historical years seamlessly:
```json
{
    "Boston Bruins": [
        { "year": 1990, "wins": 44 },
        { "year": 1991, "wins": 36 },
        { "year": 1992, "wins": 51 }
    ]
}
```
## cat hockey_stats.json was run in the terminal to ensure json file formatting.

