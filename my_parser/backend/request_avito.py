from random import uniform
from time import sleep

from urllib.parse import urlparse, urlencode, urlunsplit
import requests

from .exeptions import ErrorSummParameter, ZeroPageNumber, FailedGetRequest

import cfscrape



HEADERS = {
    'Host': 'www.avito.ru',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Cookie': 'u=2fsqtwio.hbxbka.g92ll90kjd; buyer_location_id=641270; buyer_selected_search_radius4=0_general; _ga=GA1.2.882107431.1574090029; _ym_uid=1547928531133303852; _ym_d=1607075298; cto_lwid=10483b36-9bf7-460c-8646-9771a64cbbfd; __utma=99926606.882107431.1574090029.1604599165.1607075367.40; __utmz=99926606.1599716630.30.3.utmcsr=soc_sharing|utmccn=native|utmcmd=item_page_ios; buyer_selected_search_radius0=200; buyer_selected_search_radius3=0_services; buyer_laas_location=641270; __gads=ID=d9f4b7a39971c590:T=1592848491:S=ALNI_MZEoV7J3NlWk-sLvPX88L1JXT95RA; cto_bundle=pXGqQl9BSEtWSWQzNzMxYjFmeGJwcmpjNGp5bEE1WlZranNUajRLZVE5T2glMkZ2Ull0UldVaWR4dnk3VFh1eFRac2ZvcDVJUllpMW9QSCUyQmFQMTV3JTJGMDdmT2hJeHBBb3NsNk91NFJmc01wclFjdHlQQVZWcWowN0xzTUFGNmlvdGhSUEo3d1d4eDNwWU9CYVZPbldOTXpTV2NIbUElM0QlM0Q; showedStoryIds=52-51-50-49-48-47-46-43-41-42-39-32-30; lastViewingTime=1607075297064; buyer_local_priority_v2=0; sx=H4sIAAAAAAACA02NMQ6DMAwA%2F%2BKZwUnThPKbyoBprcZKI%2BEgxN9bhkod7sa7Ha4zLmG8v%2FgiiBZqz0xSyXoYdlhhAB4zzqXkVVUNv5AwGgXulYwZOphgcBGTD84nf3RAz%2FbwJd38m6wGlCBclc30l8zL1NoWtxTreUTUSsjGclr%2BkxHRueP4AOR%2BuiqnAAAA; __cfduid=dfaa16c2759a3328cfdd2b7d5d8a314d91607075294; _gid=GA1.2.753547210.1607075298; _ym_isad=2; _nfh=271416ef19be17eb2abff22e8bc8bd5f; __utmc=99926606; buyer_popup_location=632720; no-ssr=1; abp=0; v=1607173611; luri=velikiy_novgorod; so=1607173611; dfp_group=25; sessid=e41b4d8ec0ad412557e829f445ec5a84.1607173612; _ym_visorc_34241905=b; f=5.1dd1a46efe13913d4b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fad99271d186dc1cd0143114829cf33ca7baed66fa7192f00c615ab5228c34303140e3fb81381f3591956cdff3d4067aa559b49948619279110df103df0c26013a1d6703cbe432bc2a2da10fb74cac1eab2da10fb74cac1eab03c77801b122405c2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabf722fe85c94f7d0c71e7cb57bbcb8e0f868aff1d7654931c9d8e6ff57b051a5874ddae3a7aafbbe4001fae3ab8d7e7b1021dce8db01be7bfdb738f2d696f28dd291950647ecb15689154f4aaf0a7b4f448c9619070b10c16f2cf422e086ba40a2ebf3cb6fd35a0ac0df103df0c26013a28a353c4323c7a3a140a384acbddd748a81d9c1b10ad47e43de19da9ed218fe23de19da9ed218fe2aa6f746d757dff059427383f0d84727c52d24b309942366a; _ym_visorc_419506=w; buyer_from_page=catalog',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
     'Cache-Control':'max-age=0',
    }


class Url:

    def __init__(self, base_url):
        self.base_url = base_url

        self.min_price = 0
        self.max_price = 0
        self.page_number = 1

        self.__scheme = ''
        self.__hostname = ''
        self.__path = ''

        self.__split_url()

    @property
    def url(self):
        """
        Getting new url with required parameter
        :param self.page_number: number of self.page_number
        :return: new url
        """
        self.__check_parameter()
        query_data = self.__get_query_data()

        return self.__parse_url(query_data)

    @property
    def place(self):
        """
        Get name city in url path
        :return: name of city
        """
        return self.__path.split('/')[1].replace('_', ' ')

    def __split_url(self):
        """
        split url
        :return: None
        """

        data = urlparse(self.base_url)

        self.__scheme = data.scheme
        self.__hostname = data.hostname
        self.__path = data.path

    def __parse_url(self, query_data):
        """
        parse new url
        :param query_data: required settings for url
        :return: new url
        """

        return urlunsplit((
            self.__scheme,
            self.__hostname,
            self.__path, urlencode(query_data, doseq=True),
            ''
        ))

    def __get_query_data(self):
        """
        Getting url query data
        :param self.page_number: number of self.page_number
        :return: required parameter data
        """
        query_data = {}

        if self.min_price != 0:
            query_data['pmin'] = self.min_price

        if self.max_price != 0:
            query_data['pmax'] = self.max_price

        #query_data['p'] = self.page_number
        query_data['cd'] = self.page_number


        return query_data

    def __check_parameter(self):
        """
        Validate passed parameter in urls query data
        :param self.page_number: number of self.page_number
        :return: None
        """

        if self.page_number == 0:
            raise ZeroPageNumber()



class RequestHandler:

    def __init__(self):
        self.__session = requests.session()
        self.__headers = HEADERS

    def get_session(self):
        session = requests.Session()
        session.headers = self.__headers
        return cfscrape.create_scraper(sess=session)

    def get_html(self, url):
        """
        Get html code of web page
        :param url: url of required web page
        :return: html code of web page
        """
        session = self.get_session()

        response = session.get(url)
        self.__check_result_response(response)

        return response.text

    def __check_result_response(self, response):
        if response.status_code != 200:
            raise FailedGetRequest(response.status_code)

    def sleep_random_time(self):
        sleep(uniform(10, 20))
