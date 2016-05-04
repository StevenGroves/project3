from bs4 import BeautifulSoup
import re
import urllib2

channel_name = raw_input('Enter a channel name: ')

root_url = "https://www.youtube.com"
url = urllib2.urlopen("https://www.youtube.com/user/" + channel_name + "/videos")

content = url.read()

soup = BeautifulSoup(content, "html.parser")
list_of_links = []

#searches for all 'a' tags that have "/watch" in them.
for elem in soup.find_all('a', href=re.compile('/watch')):
	list_of_links.append(root_url + elem['href'])

#This loop gets rid of duplicate links
i = 0
while i < len(list_of_links):
   if list_of_links[i] == list_of_links[i+1]:
       list_of_links.remove(list_of_links[i])
       i += 1

print("Links for the %d most recent videos:" % len(list_of_links))

for x in range(len(list_of_links)):
	print(list_of_links[x])


#This function will go to each link and scrape data of subscribers, views, likes and dislikes
def get_data(list_of_links = []):

 	for x in range(len(list_of_links)):

 		url = urllib2.urlopen(list_of_links[x])
 		link_content = url.read()
 		link_soup = BeautifulSoup(link_content, "html.parser")

 		views = link_soup.find('div', {'class' : 'watch-view-count'})
 		views = views.get_text()
 		print(views)

 		likes = link_soup.find('button', {'class' : "yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip"})
 		likes = likes.get_text()
 		print("%s likes" % likes)

 		dislikes = link_soup.find('button', {'class' : "yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip"})
 		dislikes = dislikes.get_text()
 		print("%s dislikes" % dislikes)
 		print(" ")
 	
	subscribers = link_soup.find('span', {'class' : "yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count"})
	subscribers = subscribers.get_text()
	print("%s subscribers" % subscribers)

get_data(list_of_links)
