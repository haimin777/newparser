import datetime
import locale

from bs4 import BeautifulSoup as bs
from .exeptions import FailedGettingNumberPages, FailedAdsDataGet, FailedItemsGetting
import pymorphy2
import requests

from ..models import AvitoData, AvitoPriceChange, AvitoNew




def send_bot_notification(bot_chatID, bot_message):
    bot_token = '1187651461:AAHqdGs2A5nhNsGF5I2F0F7keHaz73qF_VA'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(bot_chatID) + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

class ParserAvito:

    def __init__(self):

        self.__soup = None
        self.result_data = PageData()
        self.__number_page = 1

    @property
    def count_page(self):
        """
        Get count of pages
        :return: Count of pages: int
        """

        last_page_tag = self.__soup.find('a', class_='pagination-page', text='Последняя')

        if last_page_tag:
            href_last_page = last_page_tag.get('href')
            count_page = href_last_page.split('=')[1].split('&')[0]

        else:
            raise FailedGettingNumberPages()

        return int(count_page)

    @property
    def html(self):
        return self.html

    @html.setter
    def html(self, data_html):

        self.__soup = bs(data_html, 'lxml')

    def __get_ads(self):
        """
        Get list of the ads tags
        :return: None
        """

        ads = self.__soup.find_all('div', class_='iva-item-root-G3n7v')  #'js-catalog_serp')

        #ads = ads.find_all('div', class_='item_table')

        if not ads:
            raise FailedAdsDataGet(self.__number_page)
        else:
            return ads

    def __get_name_ad(self, ad):
        """
        Get name of the ad
        :param ad: tag of the ad
        :return: name
        """

        title = ''
        title_tag = ad.find('span', class_="title-root-395AQ").text

        if title_tag:
            title = title_tag #title_tag.text.strip()

        return title

    def __get_url_ad(self, ad):
        """
        Get url of the ad
        :param ad: tag of the ad
        :return: url
        """

        url = ''
        url_base = 'https://www.avito.ru{}'

        url_tag = ad.find('div', class_='iva-item-titleStep-2bjuh').find('a')

        if url_tag:
            url_patt = url_tag.get('href')
            url = url_base.format(url_patt)

        return url

    def __get_price_ad(self, ad):
        """
        Get price of the house in the ad
        :param ad: tag of the ad
        :return: price
        """
        price = '1111'

        #price_tag = ad.find('div', class_='about')
        price_tag = ad.find('span', class_="price-text-1HrJ_")#"snippet-price")


        if price_tag:
            price = price_tag.text.strip()

        price = price.replace(' ', '')
        return int(price[:-1])

    def __get_date_ad(self, ad): # :TODO now data in hours create convertor !!!!
        """
        Get date of the ad
        :param ad: tag of the ad
        :return: date
        """
        date = ''
        date_tag = ad.find('div', class_='js-item-date')

        if date_tag:
            date = date_tag.get('data-absolute-date').strip()
            date = self.__change_date_format(date)

        return date

    def __get_place_ad(self, ad):
        """
        Get place of the house
        :param ad: tag of the ad
        :return: date
        """

        place = ''
        place_tag = ad.find('span', class_='geo-address-9QndR')

        if place_tag:
            place = place_tag.text.strip()

        return place

    def __get_description_ad(self):
        """
        Gets a description of the house in ad
        :return: description
        """
        description = ''
        description_tag = self.__soup.find('span', class_="title-root-395AQ").text #'div', class_='item-description-text')

        if description_tag:
            description = description_tag.text.strip()

        return description

    def __get_views_ad(self):
        """
        Gets an info about the number of views
        :return: number of views
        """

        views = ''
        views_tag = self.__soup.find('div', class_='title-info-metadata-item title-info-metadata-views')

        if views_tag:
            views = views_tag.text.split(" (")[0]

        return views

    def __get_items_ads(self):
        """
        Gets items in the ad for retrieving the data about the material of the house,
        distance from the city and number of floors
        :return: items tag
        """

        items_tag = self.__soup.find_all('div', class_='iva-item-root-G3n7v') #'item-params-list-item')

        if items_tag:
            return items_tag
        else:
            raise FailedItemsGetting()

    def __get_detail_data_in_ad(self):
        """
        Gets in every ad the data about the number of floors, material of the house
        and distance from the city
        :return: data of the parameter
        """
        items = self.__get_items_ads()

        if not items:
            print ('')

        for item in items:
            key = item.find('span', class_='item-params-label').text
            value = self.__get_data_in_item(item).strip()

            assert bool(key) == True

            self.result_data.append_data(key, value)

    def __get_data_in_item(self, item):
        """
        Get more detail data in an ad
        :param item: tag of the detail data
        :return: value of the detail data
        """
        split_text = item.text.split(": ")
        text = ''

        if len(split_text) > 0:
            text = split_text[1].strip()

        return text

    def parse_main_data(self):
        """
        Retrieving data from an ad
        In the first cycle we get main data from an ad(Name of ad, url, price, date, place, metro)
        :return: None
        """

        ads = self.__get_ads()

        for ad in ads:
            data_keys = {
                'Наименование объявления': self.__get_name_ad(ad),
                'Url': self.__get_url_ad(ad),
                'Цена': self.__get_price_ad(ad),
                #'Дата': self.__get_date_ad(ad),
                'Месторасположение': self.__get_place_ad(ad)
            }

            data = [self.result_data.append_data(key, data_keys[key]) for key in data_keys]


    def parse_data_for_db(self):
        """
        Retrieving data from an ad
        In the first cycle we get main data from an ad(Name of ad, url, price, date, place, metro)
        :return: None
        """
        try:
            ads = self.__get_ads()
            #print(len(ads))

        ### 790562843 - klimov
        ### 275749097 -haimin

            bot_chat_id = 790562843

            for ad in ads:
                # get ad id from url
                ad_url = self.__get_url_ad(ad)
                #print(ad_url, '\n'*3)

                ad_id = int(ad_url.split('._')[1])


                # check if add is new
                res = AvitoData.objects.filter(ad_id=ad_id)

                if len(res) == 0:
                    # save new data
                    print('new data line \n')
                    ad_name = self.__get_name_ad(ad)

                    #rooms, square, floor = ad_name.split(',')

                    info = ad_name.split(' ')
                    rooms, square, floor = info[0], info[2], info[4]

                    ad_price = self.__get_price_ad(ad)

                    ad_place = self.__get_place_ad(ad)

                    
                    # is it Novgorod
                    ad_city = 'Район' if ad_place.startswith('д.') else 'Город'
                    av = AvitoData(ad_id=ad_id,
                                   ad_name=ad_name,
                                   ad_rooms=rooms,
                                   ad_square=square,
                                   ad_url=ad_url,
                                   ad_price=ad_price,
                                   ad_place=ad_place,
                                   ad_city=ad_city)

                    
                    av.save()
                    # add to database with new objects
                    av_new = AvitoNew(avitodata=av)
                    av_new.save()

                    # send notification about new
                    bot_message = 'Новый объект [' + av.ad_place + ']' + '(' + av.ad_url + ')'

                    send_bot_notification(bot_chat_id, bot_message)

                else:

                    ad_price = self.__get_price_ad(ad)

                    # check price change
                    if res[0].ad_price != ad_price:
                        print('price changed!!! old: {} new: {}\n'.format(res[0].ad_price, ad_price))
                        # retrieve object by pk
                        av = AvitoData.objects.get(pk=res[0].pk)
                        av.ad_price_delta = ad_price - res[0].ad_price
                        av.ad_price = ad_price
                        av.save()
                        av_change = AvitoPriceChange(avitodata=av)
                        av_change.save()

                        # send bot notification for chanded price
                        bot_message = 'Изменение цены: ' + str(av.ad_price_delta) + ' [' + av.ad_place +']'+'(' + av.ad_url + ')'

                        send_bot_notification(bot_chat_id, bot_message)

        except Exception as e:
            print(e, 'Exception from parse_data_for_db')
            # send alarm message
            send_bot_notification(275749097, 'Somthing wrong with AvitoBot')

    def parse_detail_data(self):
        """
        Getting detailed information from the search result on the avito site
        :return: None
        """

        data_keys = {
            'Описание': self.__get_description_ad(),
            'Просмотры': self.__get_views_ad(),
        }

        data = [self.result_data.append_data(key, data_keys[key]) for key in data_keys]

        self.__get_detail_data_in_ad()

    def __change_date_format(self, date):

        if "сегодня" in date.lower():
            date = datetime.datetime.today()
        elif "вчера" in date.lower():
            date = datetime.datetime.today() - datetime.timedelta(1)
        else:
            loc = locale.getlocale()
            date_str = date.split()[:2]

            locale.setlocale(locale.LC_ALL, 'ru_RU')
            m = pymorphy2.MorphAnalyzer()

            date_str[1] = m.parse(date_str[1])[0].inflect({'nomn'}).word.title()
            date = ' '.join(date_str)
            date = datetime.datetime.strptime(date + " 2019", "%d %B %Y")

            locale.setlocale(locale.LC_ALL, loc)

        date = date.strftime("%d.%m.%Y")

        return date


class PageData:

    def __init__(self):
        self.page_data = {
            'Наименование объявления': [],
            'Url': [],
            'Цена': [],
            'Дата': [],
            'Месторасположение': [],
            'Описание': [],
            'Просмотры': []
        }

    def append_data(self, key, value):
        """
        Add value of data in dictionary
        :param key: data dictionary key
        :param value: value
        :return: None
        """

        if key in self.page_data:
            self.page_data[key].append(value)
        else:
            self.page_data[key] = []
            self.page_data[key].append(value)
