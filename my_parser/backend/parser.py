import time
import datetime
import os

from .exeptions import FailedItemsGetting, FailedGetRequest
from .parser_response import ParserAvito
from .request_avito import Url, RequestHandler
from .settings import MainSettings

import csv


def write_csv(data_result, row_number):
    """
    writing result to a csv file
    :param data_result: obtained result
    :param row_number: number of element in lists of result
    """

    with open('avito.csv', 'a', encoding='utf16', newline='') as f:
        writer = csv.writer(f)

        try:
            data_row = [data_result[row][row_number] for row in data_result]
            writer.writerow(data_row)
        except IndexError:
            pass


def check_file_result():
    if os.path.exists('avito.csv'):
        os.remove('avito.csv')


def get_object_url(settings):
    url_obj = Url(settings.base_url)

    url_obj.max_price = settings.max_summ

    url_obj.min_price = settings.min_summ

    return url_obj


def send_get_request(request_avito, url, wait_flag=False):
    """
    Sends requests to the avito web server
    :param request_avito: object of the class RequestHandler
    :param url: url of the required page
    :param wait_flag: if flag = True then the programm waits for a random time
    :return: None
    """

    if wait_flag:
        request_avito.sleep_random_time()

    return request_avito.get_html(url)


def get_main_ads_data(request_avito, total_pages, url, parser_avito):
    """
    Getting the main data from an ad
    :param request_avito: object of the class RequestHandler
    :param total_pages: total numbers of the pages in the searchings result
    :param url: object of the class Url
    :param parser_avito: object of the class ParserAvito
    :return: None
    """
    for i in range(1, total_pages + 1):
        url.page_number = i
        print(i, url.url, sep=' ')
        html_data = send_get_request(request_avito, url.url)

        parser_avito.html = html_data
        parser_avito.parse_data_for_db()



def main():
    """
    main function
    """
    settings = MainSettings()

    url_obj = get_object_url(settings)

    req_avito = RequestHandler()

    print(url_obj.url)
    #print(req_avito, '\n'*3)

    html_data = send_get_request(req_avito, url_obj.url)
    #print(html_data[:100], '\n'*3)

    parser_avito = ParserAvito()
    parser_avito.html = html_data

    total_pages = parser_avito.count_page

    print('total pages: ', total_pages, '\n', datetime.datetime.now(), '\n'*3)
    #get_main_ads_data(req_avito, total_pages, url_obj, parser_avito)
    get_main_ads_data(req_avito, total_pages, url_obj, parser_avito)


    #check_file_result()

    #get_detail_ads_data(req_avito, parser_avito)


def main_with_settings(base_url, p_max, p_min):
    """
    main function

    """
    settings = MainSettings()
    settings.base_url = base_url
    settings.max_summ = p_max
    settings.min_summ = p_min

    url_obj = get_object_url(settings)

    req_avito = RequestHandler()

    print(url_obj.url)
    #print(req_avito, '\n'*3)

    html_data = send_get_request(req_avito, url_obj.url)
    #print(html_data[:100], '\n'*3)

    parser_avito = ParserAvito()
    parser_avito.html = html_data

    total_pages = parser_avito.count_page
    print('total pages: ', total_pages,'\n',datetime.datetime.now() , '\n'*3)
    #get_main_ads_data(req_avito, total_pages, url_obj, parser_avito)
    get_main_ads_data(req_avito, total_pages, url_obj, parser_avito)


if __name__ == '__main__':
    main()
