# NYC BOE Election Night Results Scraper
The NYC Board of Elections publishes unofficial election night results on a different page than certified results. The unofficial results can be tedious to fetch manually, especially for city-wide and congressional races, as election-district-level results for each contest are displayed on separate pages for each assembly district.

## Use
Set `data_dir` to the name of the directory where you want the data to be saved. The script will automatically create the directory if it does not exist. Configure the `contests` list to include a dictionary for each of the elections you wish to scrape with values for the following keys: `office`, `district`, and `party`. If the office is not districted, omit `district`. The office name must match the BOE website exactly. See an example configuration below.

```python
contests = [
  {'office': "President", 'party': "Democratic"},
  {'office': "Member of the Assembly", 'district': 36, 'party': "Democratic"},
  {'office': "Judge of the Civil Court - District", 'district': 'Bronx', 'party': "Democratic"},
]

```

Possible values for `office` include:
```
President
Delegate to National Convention
Judge of the Civil Court - County
Borough President
Representative in Congress
State Senator
Member of the Assembly
Judge of the Civil Court - District
Female State Committee
Male State Committee
Female District Leader
Male District Leader
Delegate to Judicial Convention
Alternate Delegate to the Judicial Convention
```

## Notes
At the moment, this scraper only fetches data for candidates running on the Democratic ballot line.