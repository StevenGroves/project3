from bs4 import BeautifulSoup
import re
import urllib2

def choose_channel():
	channel_name = raw_input('Enter a channel name: ')
	return channel_name

def retrieve_links(name_of_channel):
	
	root_url = "https://www.youtube.com"
	url = urllib2.urlopen("https://www.youtube.com/user/" + name_of_channel + "/videos")

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

	return list_of_links


#This function will go to each link and scrape data of subscribers, views, likes and dislikes
def get_data(list_of_links = []):
	
	data = {}
	data['total_views'] = 0
	data['total_likes'] = 0
	data['total_dislikes'] = 0
	data['total_subscribers'] = 0
	

 	for x in range(len(list_of_links)):

 		url = urllib2.urlopen(list_of_links[x])
 		link_content = url.read()
 		link_soup = BeautifulSoup(link_content, "html.parser")

 		print("Video number: %d" % (x+1))
 		views = link_soup.find('div', {'class' : 'watch-view-count'})
 		views = views.get_text()
 		views = views.replace(",", "")
 		views = views.replace(" views", "")
 		data['total_views'] += int(views)
 		print("%s views" % views)

 		likes = link_soup.find('button', {'class' : "yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip"})
 		likes = likes.get_text()
 		likes = likes.replace(",", "")
 		data['total_likes'] += int(likes)
 		print("%s likes" % likes)

 		dislikes = link_soup.find('button', {'class' : "yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip"})
 		dislikes = dislikes.get_text()
 		dislikes = dislikes.replace(",", "")
 		data['total_dislikes'] += int(dislikes)
 		print("%s dislikes" % dislikes)
 		print(" ")
 	
	subscribers = link_soup.find('span', {'class' : "yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count"})
	subscribers = subscribers.get_text()
	subscribers = subscribers.replace(",", "")
	data['total_subscribers'] = int(subscribers)

	return data

channel1 = retrieve_links(choose_channel())
channel2 = retrieve_links(choose_channel())

channel1_data = get_data(channel1)
channel2_data = get_data(channel2)
print(channel1_data)
print(channel2_data)
