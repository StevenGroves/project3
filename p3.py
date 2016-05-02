from bs4 import BeautifulSoup
import re
import urllib2

channel_name = raw_input('Enter a channel name: ')

root_url = "https://www.youtube.com"
url = urllib2.urlopen("https://www.youtube.com/user/" + channel_name + "/videos")

content = url.read()

soup = BeautifulSoup(content, "html.parser")

#searches for all 'a' tags that have "/watch" in them.
for elem in soup.find_all('a', href=re.compile('/watch')):
  print elem['href'] 