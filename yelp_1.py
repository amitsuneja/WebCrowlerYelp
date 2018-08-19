from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time


my_url = "https://www.yelp.com"
shop_dict = {}


class MyWebSite(object):

    def __init__(self, product, location):
        self.product = product
        self.location = location

    def start_searching_product(self):
        my_driver = webdriver.Chrome("C:\\chromedriver_win32\\chromedriver.exe")
        my_driver.get(my_url)
        # my_driver.maximize_window()
        find_product = my_driver.find_element_by_xpath('//*[@id="find_desc"]')
        find_product.clear()
        find_product.send_keys(self.product)
        find_location = my_driver.find_element_by_xpath('//*[@id="dropperText_Mast"]')
        find_location.clear()
        find_location.send_keys(self.location)
        find_button = my_driver.find_element_by_xpath('//*[@id="header-search-submit"]/span/span[1]')
        find_button.click()
        num_of_pages = int(self.scrap_bottom_links(my_driver))
        current_url = my_driver.current_url
        list_of_all_bottom_url = self.generate_all_bootom_url(current_url, num_of_pages)
        my_driver.quit()
        complete_dict_of_shops = self.read_address_rating(list_of_all_bottom_url)
        complete_dict_of_shops_with_shop_url = self.read_shop_url(complete_dict_of_shops)
        print(complete_dict_of_shops_with_shop_url)

        

    @staticmethod
    def generate_all_bootom_url(current_url, num_of_pages):
        list_of_all_bottom_url = [current_url]
        url = current_url[0:-4]
        for i in range(10, (num_of_pages*1) - 80, 10):        # formula is *10 for testing i made it *1 and -10 as -80
            list_of_all_bottom_url.append(url + "start=" + str(i))
        return list_of_all_bottom_url

    @staticmethod
    def scrap_bottom_links(my_driver):
        my_soup = BeautifulSoup(my_driver.page_source, 'lxml')
        total_pages_list = my_soup.findAll(class_="page-of-pages")
        for item in total_pages_list:
            my_string = item.text.strip()
            return my_string[-4:]

    @staticmethod
    def read_address_rating(list_of_all_bottom_url):
        counter = 0
        for shop_url in list_of_all_bottom_url:
            print(shop_url)
            my_web_page = requests.get(shop_url)
            my_soup = BeautifulSoup(my_web_page.text, 'html.parser')
            shops_list = my_soup.findAll(class_="media-story")
            time.sleep(3)
            for shop in shops_list:
                time.sleep(3)
                counter += 1
                shop_dict[counter] = {}
                try:
                    shop_star_rating = shop.find(class_="i-stars")['title']
                except (AttributeError, KeyError, TypeError) as ex:
                    #  print(ex)
                    shop_star_rating = "BlankValue"

                try:
                    shop_sub_url = shop.find(class_="biz-name js-analytics-click")['href']
                except (AttributeError, KeyError, TypeError) as ex:
                    #  print(ex)
                    shop_sub_url = "BlankValue"

                try:
                    shop_name = shop.find(class_="biz-name js-analytics-click").text.strip()
                except (AttributeError, KeyError, TypeError) as ex:
                    #  print(ex)
                    shop_name = "BlankValue"

                try:
                    review_count = shop.find(class_="review-count rating-qualifier").text.strip()
                except (AttributeError, KeyError, TypeError) as ex:
                    #  print(ex)
                    review_count = "BlankValue"

                try:
                    phone = shop.find(class_="biz-phone").text.strip()
                except (AttributeError, KeyError, TypeError) as ex:
                    #  print(ex)
                    phone = "BlankValue"

                try:
                    address = shop.address.text.strip()
                except (AttributeError, KeyError, TypeError) as ex:
                    #  print(ex)
                    address = "BlankValue"

                try:
                    neighbour = shop.find(class_="neighborhood-str-list").text.strip()
                except (AttributeError, KeyError, TypeError) as ex:
                    #  print(ex)
                    neighbour = "BlankValue"
                shop_dict[counter] = {
                                        "shop_name": shop_name,
                                        "shop_star_rating": shop_star_rating,
                                        "shop_sub_url": shop_sub_url,
                                        "review_count": review_count,
                                        "phone": phone,
                                        "address": address,
                                        "neighbour": neighbour}
                                
        return shop_dict
    
    @staticmethod
    def read_shop_url(complete_dict_of_shops):
        for key, value in complete_dict_of_shops.items():
            if value["shop_name"] == "BlankValue" and value["shop_star_rating"] == "BlankValue" and \
                value["shop_sub_url"] == "BlankValue" and value["review_count"] == "BlankValue" and \
                    value["address"] == "BlankValue" and value["neighbour"] == "BlankValue":
                pass
            else:
                comments_url = my_url + value["shop_sub_url"]
                complete_dict_of_shops[key]["shop_full"] = comments_url
        return complete_dict_of_shops
                
                











K = MyWebSite("burger", "Orlando, FL")
X = K.start_searching_product()


