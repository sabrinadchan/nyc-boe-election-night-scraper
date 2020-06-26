import pandas as pd
import pathlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

##### Configuration #####

boe_url = "https://web.enrboenyc.us/index.html"

contests = [
  {'office': "Member of the Assembly", 'district': 36, 'party': "Democratic"},
  {'office': "Member of the Assembly", 'district': 51, 'party': "Democratic"},
  {'office': "Member of the Assembly", 'district': 57, 'party': "Democratic"},
  {'office': "State Senator", 'district': 18, 'party': "Democratic"},
  {'office': "State Senator", 'district': 25, 'party': "Democratic"},
  {'office': "Representative in Congress", 'district': 14, 'party': "Democratic"},
  {'office': "Representative in Congress", 'district': 15, 'party': "Democratic"},
]

data_dir = "data"
pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)

#########################

def soupify_page(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, features="lxml")
  return soup

def get_href(soup, lookup):
  a = soup.find("a", lookup)
  if a:
    return a['href']
  raise Exception("No such page could be found")

def parse_table(table, district):
  df = pd.read_html(str(table), header=[0,1])[0]
  df.dropna(axis=1, how='all', inplace=True)
  df.columns = ["ad_ed", "reporting"] + ["candidate|" + c.title() + "|" + p.replace("&nbsp", "") for c,p in df.columns[2:]]
  df = df.loc[~df.ad_ed.str.contains("Total")]
  df.ad_ed = district + "-" + df.ad_ed.str.split().str[1].astype(int).map("{:03d}".format)
  return df
  
main_page = soupify_page(boe_url)
for c in contests:
  # Depends on Democratic candidates appearing first on the page
  href = get_href(main_page, {'title': lambda x: x and x == f"By AD: {c['office']}"})
  
  if 'district' in c:
    print("Fetching", c['office'], " - District", c['district'])
    contest_url = urljoin(boe_url, href)
    contest_page = soupify_page(contest_url)
    href = get_href(contest_page, {'title': lambda x: x and c['office'] and str(c['district']) in x})
  else:
    print("Fetching", c['office'])
    
  # URL for "total" page listing AD-level results in all boroughs
  all_ad_results_url = urljoin(boe_url, href.replace("ADI0.html", "AD0.html"))
  all_ad_results_page = soupify_page(all_ad_results_url)
  ad_results = all_ad_results_page.find_all("a", title=lambda x: x and "AD" in x)

  results_dfs = []
  for a in ad_results:
    href = a['href']
    results_url = urljoin(boe_url, href)
    ad_results_page = soupify_page(results_url)
    table = ad_results_page.find("table", class_="underline")
    district = a['title'].split()[1]
    results_dfs.append(parse_table(table, district))

  df = pd.concat(results_dfs, ignore_index=True)
  fn = f"{c['office']}" +  (f" - District {c['district']}" if 'district' in c else "") + ".tsv"
  file_path = pathlib.Path.cwd() / data_dir / fn
  df.to_csv(file_path, sep="\t", index=False)