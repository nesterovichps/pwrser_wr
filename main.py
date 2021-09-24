import requests
from bs4 import BeautifulSoup as bs
import time
import re
import csv
import random
import os
import idna


# Создание модели стандартной компании
class Company:
    company_name = ''
    company_email = ''
    company_phone = ''
    company_comment = ''
    company_amount = ''
    company_status_in_base = ''  # 4-база 5-недозвон 6-переговоры 7-ожидаем оплаты 8-партнерка 9-оплачено 10-закрыто нереализовано
    company_date_of_creation = ''
    company_dns = ''
    company_status_add = True

    def __init__(self):
        pass

    def get_company_name(self):
        pass

    def get_company_email(self):
        pass

    def get_company_phone(self):
        pass

    def get_company_comment(self):
        pass

    def get_company_amount(self):
        pass

    def get_company_date_of_creation(self):
        pass

    def get_company_dns(self):
        pass

    # проверяет активный ли сайт (домен привязан не привязан)
    def check_company_status(self):
        pass


def send_commercial_offer():
    pass


def form_letter():
    pass


# Когда не знаешь кого собрать система предлагала варианты запросов , из списка дорогих кликов или из ниш
def suggest_category_for_search():
    pass


def start_program():
    list_questions = ''
    max_deep = 10
    print('Привет, ты находишься в парсере Lead Group версии 2.0'
          'У Вас есть возможность напрямую влиять на его работу. '
          'Чем больше дадите обратной связи, тем лучше он будет работать'
          'Для этого замечания и предложения фиксируйте в файле '
          'https://docs.google.com/spreadsheets/d/19Kmt0qVzaeH2I0wBkcBJXtkrmXfvHpFpKugMadLKYVg/edit?usp=sharing ')

    print('ВАЖНО')
    print('Ограничений на количество запросов и городов нет, но стоит помнить, '
          'что время работы программы возрастает в геометрической прогрессии (запрос*город*глубину поиска)')
    print('Нажми Enter если понятно')
    input()
    print('Введи запросы для поиска через запятую'
          'ВАЖНО'
          'В запросе используйте коммерческие слова '
          '"Купить", "Цена", "Снять в аренду", "Продать" и тд'
          'Так же используйте более узкие запросы'
          'Например, не "юридические услуги", а "авто юрист" или "Банкротство" ')
    while not list_questions:
        suggest_category_for_search()
    list_questions = [i.strip() for i in input().split(',')]

    print('Введи города, через запятую')
    city_questions = [i.strip() for i in input().split(',')]

    print(f'Сколько первых страниц просматриваем? максимум {max_deep} стр')
    try:
        deep_page = int(input())
        if deep_page > max_deep:
            deep_page = 5
            print(
                f'Вы превысили максимальную глубину поиска ({max_deep} страниц), установлено значение {deep_page} страниц')
    except:
        deep_page = 5
        print(f'Вы неверно указали глубину поиска, установлено значение {deep_page} страниц')

    search_list = generate_serch_list(list_questions, city_questions)

    return search_list, deep_page


# Предложить случайную категорию
def suggest_a_random_category():
    random_category=[]
    file = requests.get('https://raw.githubusercontent.com/nesterovichps/pwrser_wr/main/words_of_exclusion.csv')
    file = file.content.decode('UTF-8').split()
    print(''
          '**********'
          '10 случайных категорий для поиска'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          f'{str(random.choices(file))}'
          '**********')
    print('Чтобы получить еще 10 случайных категорий нажми Enter или введи запросы для поиска через запятую')

def generate_serch_list(list_questions, city_questions):
    list_questions, city_questions = list_questions, city_questions
    search_list = []
    for quest in list_questions:
        if quest:
            for city in city_questions:
                if city:
                    search_list.append(f'{quest} {city}')

    return search_list


search_list, deep_page=(start_program())






# def search_google(search_quest, deep_page, google_link, headers, list_url):
#     search_quest, deep_page, google_link, headers, list_url = search_quest, deep_page, google_link, headers, list_url
#     i = 0
#     for page in range(deep_page):
#         print(f'поиск на странице №{i} из {deep_page}')
#         i += 1
#         time.sleep(random.randint(1, 4))
#         param = {'q': search_quest,
#                  'start': page * 10}
#         r = requests.get(google_link, params=param, headers=headers)
#         if r.status_code == 200:
#             try:
#                 parse_google(r, list_url)
#             except:
#                 return list_url
#     return list_url
#
#
# def parse_google(r, list_url):
#     list_url = list_url
#     pattern = 'http(s){0,1}:\/\/[A-zaz0-9\.-]+\/'
#     soup = bs(r.text, 'html.parser')
#     soup = soup.find('div', id='search')
#     for link in soup.find_all('a'):
#         link = re.match(pattern, str(link.get('href')))
#         if link:
#             list_url.append(link[0])
#     return list_url
#
#

# def save_result(list_url):
#     list_url = list_url
#     file_number = 1
#     try:
#         for i in range(1, 100):
#             os.remove(f'result{i}.csv')
#     except:
#         pass
#
#     while list_url:
#         with open(f'result{file_number}.csv', 'w', encoding='UTF-8', newline='') as csvfile:
#             filewriter = csv.writer(csvfile, delimiter=',',
#                                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             i = 0
#             while i < 200 and list_url:
#                 filewriter.writerow(['parser', '', '', '', '', '', list_url.pop(0)])
#                 i += 1
#         file_number += 1
#
#
# def search_rubbish(list_url):
#     result = []
#     except_list = (
#         'blog', 'google', 'avito', 'ozon', 'yandex', 'lenta', 'tiu', 'drom.ru', 'vk.com', '2gis.ru', 'zoon.ru',
#         'instagram')
#     list_url = list_url
#     flag = True
#     for url in list_url:
#         for ex in except_list:
#             if ex in url:
#                 flag = False
#                 break
#         if flag:
#             url = search_first_lvl_domain(url)
#             if url not in result:
#                 result.append(url)
#         else:
#             flag = True
#     return result
#
#
# def search_first_lvl_domain(url):
#     url = url.strip().replace('http://', '').replace('https://', '').replace('/', '').replace('www.', '')
#     if url.count('.') > 1:
#         url = url[url.index('.') + 1:].strip()
#     if 'xn--' in url:
#         url = idna.decode(url)
#     return url
#
#

#
#
# list_url = []
# list_questions = []
# city_questions = []
# deep_page = 3
# google_link = 'https://www.google.com/search'
# yandex_link = 'https://yandex.ru/search/'
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
# }
# try:
#     start()
#     print('Начинаю искать')
#     print('формирую варианты запроса')
#     search_list = generate_serch_list(list_questions, city_questions)
#     i = 1
#     for search_quest in search_list:
#         print(f'Ищу в гугле {i} запрос из {len(search_list)}, ожидайте')
#         print(f'Поиск запроса {search_quest}, ожидайте')
#
#         i += 1
#         list_url = search_google(search_quest, deep_page, google_link, headers, list_url)
#     # list_url=search_yandex(search_list[0], deep_page, yandex_link, headers,list_url) TODO: yandex pars doit
#     list_url = search_rubbish(list_url)
#     save_result(list_url)
#     print('Работа окончена')
# except:
#     print('Упс, что то не работает')

# и отсекал форумы и новостные сайты .
# и дать возможность скидывать лажовые сайты и стоп-слова .
# И в идеале хочу сделать , чтобы ещё и трафик сайта пробивал, но по этому пункту пока даже приблизительно не знаю как сделать.


if __name__ == '__main__':
    pass
