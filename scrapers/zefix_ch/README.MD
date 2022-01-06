# Zefix.ch Scraper

###### About the project

A robust scraper on [https://www.zefix.ch/en/search/entity/welcome](https://www.zefix.ch/en/search/entity/welcome). Built by: `python requests`.

Zefix.ch API leads to several external links, but the most of the configurations are somewhat the same [link](https://www.zefix.ch/ZefixREST/api/v1/appConfigData.json), and there are three distinct configurations.

1. `chregister.ch`
2. `ge.ch/hrcintapp/`
3. `prestations.vd.ch`

Each configurations needs a different scraper code(which in this case a module), because they are different in nature.

`main.py`
![Alt text](image/README/threeConfig.jpg?raw=true "Title")

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

##### Flags

--output_dir=`directory of the output file where you want to save, including the filename and extensions. Default: output.jsonl`

--output_file=`filename of the output, this wont be used if output_dir flag is true. Default: output.jsonl`

--page_size=`number of page results Default: 20`

--errorlog_file=`Name of the errorlog file Default: error.log`

## Table Data Algorithm (Parsing data for every table of a webpage)

For getting data from a table, we can immediately tell that its easy to get our output (dict) if we make the table header `<th>Value </th>` as the key and the value of TD `<tr><td>value</td></tr>.` This is true to a very simple table **BUT** for Complex table has a lot of rows and `<th>` can sometimes take more than one column `"colspan"`, this is where things gets complicated.

To fix the issue:
I decided to create three python Lists variable.

1. parent_keys = this is the list that contains the values of every TH in a table, if there are two (2) `<tr><th>` in a table. The topmost TH values are the called parent_keys, if there is only one TH row in a table parent_keys is automatically a null.
2. keys = this is the list that that contains the values `<tr><th>` in a table.
3. values = this contains all the values of `<td>` for every row in a table that is not part of an table header.

Example:

![Alt text](image/README/tableSample.jpg?raw=true "Title")

Breakdown:

|     parent_keys = |      | JOURNAL | JOURNAL    | PUBLICATION FOSC | PUBLICATION FOSC |
| ----------------: | ---- | ------- | ---------- | ---------------- | ---------------- |
| **parent_keys =** | Ref. | Numero  | Date       | Date             | Page/Id          |
|      **values =** | 1    | 1883    | 09.09.2002 | 13.09.2002       | 6                |
|      **values =** | 3    |         | Complément | 03.10.2018       | 1004468146       |

In this example some parent_keys took `colspan=2` thats why it was repeated in parent_keys list to achieve our desired output. With a little bit of mapping for every indexes for our three lists variables we can achieve our desired output.

Output in json:

```
{
            "": [
                {
                    "Ref.": [
                        "1",
                        "3"
                    ]
                }
            ],
            "JOURNAL": [
                {
                    "Number": [
                        "1883",
                        ""
                    ]
                },
                {
                    "Date": [
                        "09.09.2002",
                        "Complément"
                    ]
                }
            ],
            "SOGC PUBLICATION": [
                {
                    "Date": [
                        "13.09.2002",
                        "19.12.2013"
                    ]
                },
                {
                    "Page/Id": [
                        "6",
                        "7225826"
                    ]
                }
            ]
        },
```
