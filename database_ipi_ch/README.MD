# Database.ipi.ch Scraper

###### About the project

A simple scraper on [https://database.ipi.ch/database-client/search/query/chmarke](https://database.ipi.ch/database-client/search/query/chmarke "https://database.ipi.ch/database-client/search/query/chmarke"). Built by: `python requests` only.

There is a hidden api that we can target [https://database.ipi.ch/database/resources/query/fetch?ps=8]()

###### Problems encountered when building the scraper:

It was lucky to have a hidden API, but the problem is when we move to another page. There is no exact parameter that make this possible. But I studied the results of the API then I learn that they give a cursor that can be use to make our request as a starting point for our next request.

###### Problems when running the scraper:

None yet

## Getting Started

###### Prerequisites

`python3` installed in your system

###### Installation

1. Clone the repo (if you don't have yet in your computer)
   ```
   git clone https://github.com/deepjudge-ai/scrapers.git
   ```
2. Install the dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run main.py file

##### Important Functions or Files

`def post_data(items_size,cursor):`	is the function that sets up our request to ipi.ch API. `items_size` is the size of how many results we want and `cursor` is the key that gives us a starting point of our query which defaults to asterisk '*' .

##### Filters

For final scraping it is better to scrape by Registration Date from oldest to latest (ascending). To avoid issues on newly registered data.

##### Flags

--output_dir=`<directory of the output file where you want to save, including the filename and extensions.  
Default: output.jsonl 
Shortname: --od	>`

--output_file=`<filename of the output, this wont be used if output_dir flag is true. 
Default: output.jsonl  
shortname: --of>`

--page_size=`<number of page results>
Choices:8,16,32,64   Default: 64  shortname: --ps`

example:
needs **sudo** because you are creating the output in root directory of the system

```
sudo python3 main.py --output_dir=/home/data/output.jsonl --page_size=64 
is the same as:
sudo python3 main.py --od=/home/data/output.jsonl --ps=64

```
