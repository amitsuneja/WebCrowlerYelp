from bs4 import BeautifulSoup
import requests

my_url = "https://www.yelp.com/biz/burger-21-orlando?osq=burger"
my_html = requests.get(my_url)

my_soup = BeautifulSoup(my_html.text, "html.parser")

outer_div = my_soup.find(class_="ylist ylist-bordered reviews")


All_inner_div_list = outer_div.findAll(class_="review review--with-sidebar")

for record in All_inner_div_list:
    name = record.find(class_="user-display-name js-analytics-click")
    location = record.find(class_="user-location responsive-hidden-small")
    date = record.find(class_="biz-rating biz-rating-large clearfix")
    review = record.find('p')
    print("Name: {}".format(name.text.strip()))
    print("Location: {}".format(location.text.strip()))
    print("Date: {}".format(date.text.strip()[0:10].rstrip("\n\r")))
    print("Review: {}".format(review.text.strip()))
    print("______________________________________________________")
