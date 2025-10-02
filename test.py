import urllib
import bs4
from urllib import request

debut_url="https://letterboxd.com/"

jo = "https://letterboxd.com/film/one-battle-after-another/"
req = request.Request(jo, headers={"User-Agent": "Mozilla/5.0"})

request_text = request.urlopen(req).read()
#print(request_text[:1000])
page = bs4.BeautifulSoup(request_text, "lxml")

#Release Date
release_date=page.find("span",{"class" : "releasedate"})
year=release_date.a.text.strip()
print(int(year))

#Director
director=page.find("a",{"class":"contributor"})
print(director)
director_url=debut_url+director.get("href","")
print(director_url)
director_name=director.span.text.strip()
print(director_name)
