from bs4 import BeautifulSoup
import requests


myUrl = "https://www.yelp.com/biz/burger-21-orlando?osq=burger"
myWebPage = requests.get(myUrl)
mySoup = BeautifulSoup(myWebPage.text, 'html.parser')

# Raw data from the page
un_list = mySoup.find('ul', {'class': "ylist ylist-bordered reviews"})

list_items = un_list.findAll('div', {'class': 'review review--with-sidebar'})  # Creates a list

for i in list_items:
    u_name = i.find('a', {'class': 'user-display-name js-analytics-click'}).text.strip()
    u_location = i.find('li', {'class': 'user-location responsive-hidden-small'}).text.strip()
    u_date = str(i.find('span', {'class': 'rating-qualifier'}).text.strip()[:10].rstrip("\n\r"))
    u_review = str(i.find('p', {'lang' : 'en'}).text.strip())
    print("Name: {}\nLocation: {}\nDate: {}\nReview: {}\n{}\n".format(u_name, u_location, u_date, u_review, ("*" * 50)))
