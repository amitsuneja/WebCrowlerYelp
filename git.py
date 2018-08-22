from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import copy
import pickle

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
        shop_dict = self.read_all_reviews(shop_dict)
        self.dumpdata_to_pickle_file(shop_dict)
        self.print_my_dictionary(shop_dict)
        self.write_data_to_csv_file(shop_dict)

    @staticmethod
    def dumpdata_to_pickle_file(my_dict):
        pickle_file = "D:\\YelpScrappedData\\AshishBhaiFighter.pickle"
        with open(pickle_file, 'wb') as my_picklefile:
            pickle.dump(my_dict, my_picklefile)

    @staticmethod
    def print_my_dictionary(my_dict):
        for company in my_dict.keys():
            for review in my_dict[company]["all_review"]:
                print("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(
                    company,
                    my_dict[company]["shop_star_rating"],
                    my_dict[company]["review_count"],
                    my_dict[company]["phone"],
                    my_dict[company]["address"],
                    my_dict[company]["neighbour"],
                    my_dict[company]["comment_page_count"],
                    review
                ))

    @staticmethod
    def write_data_to_csv_file(my_dict):
        csv_file = "D:\\YelpScrappedData\\AshishBhaiFighter.csv"
        with open(csv_file, "wt", encoding='utf-8') as my_file:
            print("NameOfCompany,", "Rating,", "NumberOfReviews,", "Contact,", "Address,", "Location,",
                  "NumberOfPages,", "NameOfPerson,", "LocationOfPerson,", "Date,", "review", file=my_file)
            for company in my_dict.keys():
                for review in my_dict[company]["all_review"]:
                    print("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}".format(
                        company,
                        my_dict[company]["shop_star_rating"],
                        my_dict[company]["review_count"],
                        my_dict[company]["phone"],
                        my_dict[company]["address"],
                        my_dict[company]["neighbour"],
                        my_dict[company]["comment_page_count"],
                        review[0].replace(",", "-").replace("\n", "-").replace("\r", "-"),
                        review[1].replace(",", "-").replace("\n", "-").replace("\r", "-"),
                        review[2].replace(",", "-").replace("\n", "-").replace("\r", "-"),
                        review[3].replace(",", "-").replace("\n", "-").replace("\r", "-")
                    ), file=my_file)

    @staticmethod
    def convert_selenium_driver_into_soup(my_driver):
        print(" i am in convert_selenium_driver_into_soup:")

        my_soup = BeautifulSoup(my_driver.page_source, 'lxml')
        return my_soup

    @staticmethod
    def getme_soup_of_url(url):
        print(" i am in getme_soup_of_url:")

        time.sleep(3)
        my_web_page = requests.get(url)
        my_soup = BeautifulSoup(my_web_page.text, 'html.parser')
        return my_soup

    @staticmethod
    def find_num_of_pages(my_soup):
        print(" i am in find_num_of_pages:")

        try:
            num_of_pages = my_soup.find(class_="page-of-pages")
        except (AttributeError, KeyError, TypeError) as ex:
            #  print(ex)
            num_of_pages = "Page 1 of 1"

        return int(num_of_pages.text.strip().replace("Page 1 of ", ""))

    @staticmethod
    def get_url_of_selinium_driver(my_driver):
        print(" i am in get_url_of_selinium_driver:")
        return my_driver.current_url

    @staticmethod
    def find_search_page_bottom_url(search_page_url, search_page_count):
        print(" i am in find_search_page_bottom_url:")

        list_of_all_bottom_url = [search_page_url]
        url = search_page_url[0:-4]
        for i in range(10, (search_page_count *10), 10):  # formula is *10 for testing i made it *1
            list_of_all_bottom_url.append(url + "start=" + str(i))
        return list_of_all_bottom_url

    @staticmethod
    def dictionary_cleanup(my_dict):
        print(" i am in dictionary_cleanup:")

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
        print(" i am in read_shop_details:")
        shop_dict = {}
        for shop_url in list_of_search_page_urls:
            print(shop_url)
            my_soup = MyWebSite.getme_soup_of_url(shop_url)
            shops_list = my_soup.findAll(class_="media-story")
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
                print("shop_star_rating:", shop_star_rating,
                      "shop_sub_url:", shop_sub_url,
                      "review_count:", review_count,
                      "phone:", phone ,
                      "address:", address,
                      "neighbour:", neighbour)
        clean_shop_dict = MyWebSite.dictionary_cleanup(shop_dict)
        return clean_shop_dict

    # this code can be modified in case you need more details from shop_page
    @staticmethod
    def find_all_comment_page_urls(my_dict):
        print(" i am in find_all_comment_page_urls:")

        for key in my_dict.keys():
            shop_url = yelp_index_page + my_dict[key]["shop_sub_url"]
            print(shop_url)
            shop_soup = MyWebSite.getme_soup_of_url(shop_url)
            comment_page_count = MyWebSite.find_num_of_pages(shop_soup)
            my_dict[key]["comment_page_count"] = comment_page_count
            list_of_comment_urls = [shop_url]
            if comment_page_count > 1:
                for i in range(20, comment_page_count *20, 20):   # formula is *20 for testing i made it *2
                    list_of_comment_urls.append(shop_url + "&start=" + str(i))
            my_dict[key]["comments_url_list"] = list_of_comment_urls
        return my_dict

    @staticmethod
    def read_all_reviews(my_dict):
        print(" i am in read_all_reviews:")

        for key in my_dict:
            my_dict[key]["all_review"] = list()
            for url in my_dict[key]["comments_url_list"]:
                print(url)
                comment_soup = MyWebSite.getme_soup_of_url(url)
                outer_div = comment_soup.find(class_="ylist ylist-bordered reviews")
                all_inner_div_list = outer_div.findAll(class_="review review--with-sidebar")

                for record in all_inner_div_list:
                    this_user_review = []
                    try:
                        name = record.find(class_="user-display-name js-analytics-click")
                    except (AttributeError, KeyError, TypeError) as ex:
                        name = "BlankValue"

                    try:
                        location = record.find(class_="user-location responsive-hidden-small")
                    except (AttributeError, KeyError, TypeError) as ex:
                        location = "BlankValue"

                    try:
                        date = \
                            record.find(class_="biz-rating biz-rating-large clearfix")
                    except (AttributeError, KeyError, TypeError) as ex:
                        date = "BlankValue"

                    try:
                        review = record.find('p')
                    except (AttributeError, KeyError, TypeError) as ex:
                        review = "BlankValue"

                    this_user_review.append(name.text.strip())
                    this_user_review.append(location.text.strip())
                    this_user_review.append(date.text.strip()[0:10].rstrip("\n\r"))
                    this_user_review.append(review.text.strip())
                    my_dict[key]["all_review"].append(this_user_review)
        return my_dict



K = MyWebSite("burger", "orlando, FL")
K.searching_product_in_city()