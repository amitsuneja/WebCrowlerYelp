from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import copy


yelp_index_page = "https://www.yelp.com"
exe_for_chrome_web_drive = "C:\\chromedriver_win32\\chromedriver.exe"


class MyWebSite(object):

    def __init__(self, product, location):
        self.product = product
        self.location = location

    def searching_product_in_city(self):
        my_driver = webdriver.Chrome(exe_for_chrome_web_drive)
        my_driver.get(yelp_index_page)
        find_product = my_driver.find_element_by_xpath('//*[@id="find_desc"]')
        find_product.clear()
        find_product.send_keys(self.product)
        find_location = my_driver.find_element_by_xpath('//*[@id="dropperText_Mast"]')
        find_location.clear()
        find_location.send_keys(self.location)
        find_button = my_driver.find_element_by_xpath('//*[@id="header-search-submit"]/span/span[1]')
        find_button.click()
        search_page_url = self.get_url_of_selinium_driver(my_driver)
        my_soup = self.convert_selenium_driver_into_soup(my_driver)
        my_driver.quit()
        search_page_count = self.find_num_of_pages(my_soup)
        list_of_search_page_urls = self.find_search_page_bottom_url(search_page_url, search_page_count)
        shop_dict = self.read_shop_details(list_of_search_page_urls)
        shop_dict = self.find_all_comment_page_urls(shop_dict)





        self.print_my_dictionary(shop_dict)

    @staticmethod
    def print_my_dictionary(my_dict):
        print("        ")
        for key, value in my_dict.items():
            print(key, value)
            print("        ")

    @staticmethod
    def convert_selenium_driver_into_soup(my_driver):
        my_soup = BeautifulSoup(my_driver.page_source, 'lxml')
        return my_soup

    @staticmethod
    def getme_soup_of_url(url):
        my_web_page = requests.get(url)
        my_soup = BeautifulSoup(my_web_page.text, 'html.parser')
        return my_soup

    @staticmethod
    def find_num_of_pages(my_soup):
        num_of_pages = my_soup.find(class_="page-of-pages")
        return int(num_of_pages.text.strip().replace("Page 1 of ", ""))

    @staticmethod
    def get_url_of_selinium_driver(my_driver):
        return my_driver.current_url

    @staticmethod
    def find_search_page_bottom_url(search_page_url, search_page_count):
        list_of_all_bottom_url = [search_page_url]
        url = search_page_url[0:-4]
        for i in range(10, (search_page_count*1) - 80, 10):  # formula is *10 for testing i made it *1 and -10 as -90
            list_of_all_bottom_url.append(url + "start=" + str(i))
        return list_of_all_bottom_url

    @staticmethod
    def dictionary_cleanup(my_dict):
        my_dict_copy = copy.deepcopy(my_dict)
        for major_key in my_dict_copy.keys():
            for minor_key in my_dict_copy[major_key].keys():
                if my_dict_copy[major_key][minor_key] == "BlankValue":
                    shop_test = 1
                else:
                    shop_test = 0
            if "ad_business_id" in my_dict_copy[major_key]['shop_sub_url']:
                shop_test = 1
            if shop_test == 1:
                del my_dict[major_key]
        del my_dict_copy
        return my_dict

    @staticmethod
    def read_shop_details(list_of_search_page_urls):
        shop_dict = {}
        for shop_url in list_of_search_page_urls:
            print(shop_url)
            my_soup = MyWebSite.getme_soup_of_url(shop_url)
            shops_list = my_soup.findAll(class_="media-story")
            time.sleep(3)
            for shop in shops_list:
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
                shop_dict[shop_name] = {
                                        "shop_star_rating": shop_star_rating,
                                        "shop_sub_url": shop_sub_url,
                                        "review_count": review_count,
                                        "phone": phone,
                                        "address": address,
                                        "neighbour": neighbour}
        clean_shop_dict = MyWebSite.dictionary_cleanup(shop_dict)
        return clean_shop_dict

# this code can be modified incase you need more details from shop_page
    @staticmethod
    def find_all_comment_page_urls(my_dict):
        for key in my_dict.keys():
            shop_url = yelp_index_page + my_dict[key]["shop_sub_url"]
            shop_soup = MyWebSite.getme_soup_of_url(shop_url)
            comment_page_count = MyWebSite.find_num_of_pages(shop_soup)
            my_dict[key]["comment_page_count"] = comment_page_count
            list_of_comment_urls = [shop_url]
            if comment_page_count > 1:
                for i in range(20, comment_page_count*20, 20):
                    list_of_comment_urls.append(shop_url + "&start=" + str(i))
            my_dict[key]["comments_url_list"] = list_of_comment_urls
        return my_dict


































K = MyWebSite("burger", "Orlando, FL")
X = K.searching_product_in_city()
