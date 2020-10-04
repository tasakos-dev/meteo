__author__ = 'tasakos'
import urllib.request
import urllib.error
import re
import os.path
import os



url = "http://www.meteo.gr/rss/news.cfm"
dir_name = 'my_forecasts'

def find_tags(t, s):
    tags = re.findall(r'<' + t + r'\b[^>]*>(.*?)</' + t + r'>', s, re.I)
    return tags

def extact_date(st):
    date = st.split()[-1]
    if re.search(r"[0-9]{2}/[0-9]{2}/[0-9]{4}",date) :
        date = date.split("/")
        date.reverse()
        date= "_".join(date)

    return date



forecast_dir = os.path.join(os.getcwd(), dir_name)
if not os.path.isdir(forecast_dir):
    os.mkdir(forecast_dir)
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        char_set = response.headers.get_content_charset()
        rss = response.read().decode(char_set)
except urllib.error.HTTPError as e:
    print('Σφάλμα HTTP:', e.code)
except urllib.error.URLError as e:
	print('Αποτυχία σύνδεσης στον server')
	print('Αιτία: ', e.reason)
else:
    rss = rss.replace('\n', '')
    items = find_tags('item', rss)
    for i in items:
        if 'ΓΕΝΙΚΗ ΠΡΟΓΝΩΣΗ ΓΙΑ:' in i:
            title = find_tags('title', i)[0]
            file_name = (extact_date(title))+'.txt'
            forecast = find_tags('description', i)
            print(title, '\n', forecast[0])
            try:
                with open(os.path.join(forecast_dir, file_name), 'w', encoding='utf-8') as f:
                    f.write(title+'\n'+forecast[0])
            except IOError as e:
                print(e)