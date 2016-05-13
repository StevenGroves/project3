from flask import Flask, request, render_template, url_for
from bs4 import BeautifulSoup
import re
import urllib2
from bokeh.charts import Bar, output_file, show, hplot, color, marker
from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, show

app = Flask(__name__)
@app.route('/')
def mainPage():
	
	return render_template('resultsPage.html')

@app.route('/results')
def robots():
	

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

		#print("Links for the %d most recent videos:" % len(list_of_links))

		#for x in range(len(list_of_links)):
			#print(list_of_links[x])

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

	 		#print("Video number: %d" % (x+1))
	 		views = link_soup.find('div', {'class' : 'watch-view-count'})
	 		views = views.get_text()
	 		views = views.replace(",", "")
	 		views = views.replace(" views", "")
	 		data['total_views'] += int(views)
	 		#print("%s views" % views)

	 		likes = link_soup.find('button', {'class' : "yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip"})
	 		likes = likes.get_text()
	 		likes = likes.replace(",", "")
	 		data['total_likes'] += int(likes)
	 		#print("%s likes" % likes)

	 		dislikes = link_soup.find('button', {'class' : "yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target   yt-uix-tooltip"})
	 		dislikes = dislikes.get_text()
	 		dislikes = dislikes.replace(",", "")
	 		data['total_dislikes'] += int(dislikes)
	 		#print("%s dislikes" % dislikes)
	 		#print(" ")
	 	
		subscribers = link_soup.find('span', {'class' : "yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count"})
		subscribers = subscribers.get_text()
		subscribers = subscribers.replace(",", "")
		data['total_subscribers'] = int(subscribers)

		return data

	name1 = request.args['example']
	name2 = request.args['example2']

	ch1 = name1
	ch2 = name2

	channel1 = retrieve_links(ch1)
	channel2 = retrieve_links(ch2)

	channel1_data = get_data(channel1)
	channel2_data = get_data(channel2)

	#*************************************************************************************************
	#Graphing functions added here:

	# Puts integer values into variables to be used in bokeh graphing:
	ch1TotalViews = channel1_data["total_views"]
	ch2TotalViews = channel2_data["total_views"]

	ch1TotalLikes = channel1_data["total_likes"]
	ch2TotalLikes = channel2_data["total_likes"]

	ch1TotalDislikes = channel1_data["total_dislikes"]
	ch2TotalDislikes = channel2_data["total_dislikes"]

	ch1TotalSubscribers = channel1_data["total_subscribers"]
	ch2TotalSubscribers = channel2_data["total_subscribers"]

	# Data to be used for graphone ordered into groups
	data = {
	    'Numbers': ['Dislikes', 'Likes', 'Subscribers', 'Total Views', 'Dislikes', 'Likes', 'Subscribers', 'Total Views'],
	    'Channels': [ch1, ch1, ch1, ch1, ch2, ch2, ch2, ch2],
	    'Total': [ch1TotalDislikes, ch1TotalLikes, ch1TotalSubscribers, ch1TotalViews, ch2TotalDislikes, ch2TotalLikes, ch2TotalSubscribers, ch2TotalViews]   
	}

	# Puts all the data into a format which may be graphed with correct parameters:
	bar = Bar(data, values='Total', label=['Channels', 'Numbers'],agg = 'sum',
	           title="Comparing two Youtube Channels", width=500, height = 1000,
	           group = 'Numbers', tools=['hover', 'resize', 'box_zoom', 'wheel_zoom', 'pan'])

	# Allows the hover tool to function:
	hover = bar.select(dict(type=HoverTool))
	hover.tooltips = [('Value of Channel',' $x'),('Value of Total',' @height')]

	# outputs a file with the data for the graph:
	output_file("stacked_bar.html")

	# Shows the graph:
	show(hplot(bar))
	#
	#End of graphing functions code!
	#**************************************************************************************

	return render_template("resultsPage.html")

if __name__ == '__main__':
	app.run()