import datetime
import html
import pathlib
import re
import urllib.request

url = 'https://scholar.google.com/citations?user=ERtvH7kAAAAJ&hl=en'
request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(request, timeout=30) as response:
    page = response.read().decode('utf-8')
cells = re.findall(r'class="gsc_rsb_std"[^>]*>(.*?)</td>', page)
if not cells:
    raise RuntimeError('Scholar statistics unavailable; keeping previous badge.')
count = html.unescape(re.sub('<[^>]+>', '', cells[0])).strip()
if not re.fullmatch(r'[0-9,]+', count):
    raise RuntimeError('Unexpected citation count; keeping previous badge.')
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="150" height="20" role="img" aria-label="Citations: {count}">
<title>Google Scholar citations: {count}; last checked {today} UTC</title>
<rect width="150" height="20" fill="#4285f4"/>
<rect width="95" height="20" fill="#555"/>
<g fill="white" font-family="Verdana, sans-serif" font-size="11" text-anchor="middle">
<text x="47.5" y="14">Citations</text><text x="122.5" y="14">{count}</text></g></svg>\n'''
pathlib.Path('assets/scholar-citations.svg').write_text(svg)
print(f'Google Scholar citations: {count} ({today} UTC)')
