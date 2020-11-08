from random import uniform
from time import sleep

from urllib.parse import urlparse, urlencode, urlunsplit
import requests

from .exeptions import ErrorSummParameter, ZeroPageNumber, FailedGetRequest

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', #  '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Cookie': 'u=2fsqtwio.hbxbka.g92ll90kjd; buyer_location_id=641270; buyer_selected_search_radius4=0_general; __cfduid=df5bac2ed7e3a84a74f75bc242ad9a7431574090026; _ga=GA1.2.882107431.1574090029; _ym_uid=1547928531133303852; _ym_d=1590224426; _fbp=fb.1.1574090030547.349367158; cto_lwid=10483b36-9bf7-460c-8646-9771a64cbbfd; __utma=99926606.882107431.1574090029.1604542419.1604599165.39; __utmz=99926606.1599716630.30.3.utmcsr=soc_sharing|utmccn=native|utmcmd=item_page_ios; buyer_selected_search_radius0=200; buyer_selected_search_radius3=0_services; buyer_laas_location=641270; __gads=ID=d9f4b7a39971c590:T=1592848491:S=ALNI_MZEoV7J3NlWk-sLvPX88L1JXT95RA; cto_bundle=pXGqQl9BSEtWSWQzNzMxYjFmeGJwcmpjNGp5bEE1WlZranNUajRLZVE5T2glMkZ2Ull0UldVaWR4dnk3VFh1eFRac2ZvcDVJUllpMW9QSCUyQmFQMTV3JTJGMDdmT2hJeHBBb3NsNk91NFJmc01wclFjdHlQQVZWcWowN0xzTUFGNmlvdGhSUEo3d1d4eDNwWU9CYVZPbldOTXpTV2NIbUElM0QlM0Q; showedStoryIds=46-44-45-43-41-42-39-32-31-30-25; lastViewingTime=1602141381794; buyer_local_priority_v2=0; _gcl_au=1.1.1669520200.1599387141; sx=H4sIAAAAAAACA1XRwXKCUAwF0H95axcBAgT%2FRgPEGtoU4xCdTv%2B9sTN27D7vvNybr8Ln21u99kN94XAERRU3ibCy%2Fypb2Zf%2BfR5uutHUGWl4BDojEwOQqkrZlansqw5wwL5t6HtX2hlOOB7epVGAHCcRVuegJ9nW61JdNpmrYJLEVIPUchYc0F7JFvsuyY7re%2B0XndTNwwLVMd8wPsnr4Tgv48B6zJ0yAgubiYVCsuAvZN23PSbZX95oOOC4nk0FXZlBjP1P9GYYz820Lsf86ZFa2UOygUcLyv%2BXHOoUcTndR5VD88EhaNkjcoZ3eJKf83bt206vqzu5EmSAcAOKbEfpP0m%2FS2623AZcPpMi8sxlTBgYfyRN8VFV7VwTYASQkYAmLU6I%2Bkp2j%2Bt8%2FwDsqQnd8gEAAA%3D%3D; _nfh=271416ef19be17eb2abff22e8bc8bd5f; __utmc=99926606; buyer_popup_location=632720; no-ssr=1; abp=0; luri=velikiy_novgorod; sessid=68dcd95327ba57dcf9e972648433d9ed.1604818856; _gid=GA1.2.750893903.1604818864; _ym_isad=2; f=5.1dd1a46efe13913d4b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fad99271d186dc1cd0143114829cf33ca7baed66fa7192f00c615ab5228c34303140e3fb81381f3591956cdff3d4067aa572a0378f24244a7a2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab868aff1d7654931c9d8e6ff57b051a5874ddae3a7aafbbe4001fae3ab8d7e7b1021dce8db01be7bfdb738f2d696f28dd291950647ecb15689154f4aaf0a7b4f4be2ab26116054022b6b2a31718397abd2ebf3cb6fd35a0ac0df103df0c26013a28a353c4323c7a3a140a384acbddd748b59dc1a170e735b73de19da9ed218fe23de19da9ed218fe2aa6f746d757dff059427383f0d84727c52d24b309942366a; v=1604859076; so=1604861139; _ym_visorc_34241905=b; _ym_visorc_419506=w; _ym_visorc_188382=w; _ym_visorc_106253=w; _ym_visorc_42093449=b',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0' #'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
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

        query_data['p'] = self.page_number

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

    def get_html(self, url):
        """
        Get html code of web page
        :param url: url of required web page
        :return: html code of web page
        """

        response = requests.get(url, headers=self.__headers, verify=False)
        self.__check_result_response(response)

        return response.text

    def __check_result_response(self, response):
        if response.status_code != 200:
            raise FailedGetRequest(response.status_code)

    def sleep_random_time(self):
        sleep(uniform(1, 7))
