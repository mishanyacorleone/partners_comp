import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent


with open('partners_cmp.csv', 'w') as F:
    writer = csv.writer(F)
    writer.writerow(['Название', 'Адрес', 'Телефон', 'E-mail', 'Сайт', 'Факс'])


def scrap_links():
    agent = UserAgent()
    url = 'https://drives.ru/partnery-po-prodazham-v-promyshlennosti/'
    response = requests.get(url=url, params={
        'user-agent': f'{agent.random}'
    }).text
    soup = BeautifulSoup(response, 'lxml')
    cities_block = soup.find_all('a', class_='arrow')
    links_list = list()
    for link in cities_block:
        if 'partnery-po-prodazham-v-promyshlennosti/' in link.get('href') and link.get('href').count('/') > 3:
            links_list.append('https://drives.ru' + link.get('href'))
    return links_list


def parse():
    links_list = scrap_links()
    for link in links_list:
        agent = UserAgent()
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': f'{agent.random}',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate, lzma, sdch',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
        }
        session = requests.Session()
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        response = session.get(url=link, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        about = soup.find_all('div', class_='distr-name')
        for params in about:
            pre_params = list()
            try:
                pre_params.append(params.find_all('h3')[0].text)
                for dop in params.find_all('p'):
                    pre_params.append(dop.text)
                all_params = list()
                for param in pre_params:
                    if '\n' or '\r' or '\xa0' in param:
                        if '\n' in param:
                            param = param.replace('\n', '')
                        if '\r' in param:
                            param = param.replace('\r', '')
                        if '\xa0' in param:
                            param = param.replace('\xa0', '')
                        if '  ' in param:
                            param = param.replace('  ', '')
                    if 'Адрес' in param:
                        param = param.replace('Адрес:', '', 1).strip()
                        all_params.append(param)
                        continue
                    if 'Телефоны' in param:
                        param = param.replace('Телефоны:', '', 1).strip()
                        all_params.append(param)
                        continue
                    if 'E-mail' in param:
                        param = param.replace('E-mail:', '', 1).strip()
                        all_params.append(param)
                        continue
                    if 'Телефон' in param:
                        param = param.replace('Телефон:', '', 1).strip()
                        all_params.append(param)
                        continue
                    if 'тел' in param:
                        param = param.replace('тел:', '', 1).strip()
                        all_params.append(param)
                        continue
                    if 'Сайт' or 'Web' or 'Электронный' in param:
                        param = param.replace('Сайт:', '', 1).strip()
                        all_params.append(param)
                        continue
                    if 'Web' in param:
                        param = param.replace('Web:', '', 1).strip()
                        all_params.append(param)
                        continue
                    if 'Электронный' in param:
                        param = param.replace('Электронный магазин:', '', 1).strip()
                        all_params.append(param)
                        continue
                    if 'Факс' in param:
                        param = param.replace('Факс:', '', 1).strip()
                        all_params.append(param)
                        continue
                print(all_params)
                with open('partners_cmp.csv', 'a') as F:
                    new_writer = csv.writer(F)
                    new_writer.writerow(all_params)
            except:
                continue


def main():
    parse()


if __name__ == '__main__':
    main()