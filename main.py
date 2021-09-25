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
    company_status_in_base = 5  # 4-база 5-недозвон 6-переговоры 7-ожидаем оплаты 8-партнерка 9-оплачено 10-закрыто нереализовано
    company_date_of_creation = ''
    company_dns = ''
    company_status_add = True
    list_for_search_contact=['partnerskaya-programma','partner','contacts','contact','about','vip','admin','boss','feedback']
    list_ansver_response=[]
    def __init__(self,dns,comment,search_quest):
        global headers
        self.company_dns=dns
        self.check_company_status(headers)
        if self.company_status_add:
            self.collect_a_list_of_pages()

            for response in self.list_ansver_response:
                if not self.company_phone:
                    self.get_company_phone(response)
                if not self.company_email:
                    self.get_company_email(response)
            self.get_company_name(search_quest)
            self.company_comment(comment)
            self.get_first_lvl_domain()

    def check_company_status(self,headers):
        response=requests.get(self.company_dns,headers=headers)
        if response:
            self.list_ansver_response.append(response)
            print(f'[+] - Домен  {self.company_dns} доступен')
        else:
            print(f'[-] - Домен  {self.company_dns} НЕ РАБОТАЕТ')
            self.company_status_add=False

    def collect_a_list_of_pages(self):
        for page in self.list_for_search_contact:
            try:
                response=requests.get(f'{self.company_dns}/{page}/')
                self.list_ansver_response.append(response)
            except:
                pass

    def get_company_name(self,search_quest):
        self.company_name= f'parser {search_quest}'

    def get_company_email(self,response):
        pattern="([A-z0-9_.-]{1,})@([A-z0-9_.-]{1,}).([A-z]{2,8})"
        try:
            self.company_email=re.search(pattern,response.text)
        except:
            pass

    def get_company_phone(self,response):
        try:
            i=re.search('https://wa.me/',response.text).end()
            self.company_phone=response.text[i:i+11]
        except:
            pass
        if not self.company_phone:
            try:
                i = re.search('https://wa.me/', response.text).end()
                tel = response.text[i:i + 22]
                tel = tel.replace(' ','').replace('.','').replace('/','').replace('(','').replace(')','').replace('_','').replace('-','')
                tel=re.search(r'\d+',tel)
                tel=tel[:11]
                self.company_phone =tel
            except:
                pass

    def get_company_comment(self,comment):
        self.company_comment = comment

    def get_first_lvl_domain(self):
        url = self.company_dns.strip().replace('http://', '').replace('https://', '').replace('/', '').replace('www.', '')
        if url.count('.') > 1:
            self.company_dns= url[url.index('.') + 1:].strip()
        if 'xn--' in url:
            url = idna.decode(url)
            self.company_dns=url




def send_commercial_offer():
    pass


def form_letter():
    pass


def start_program():
    list_questions = ['']
    max_deep = 10
    print('Привет, ты находишься в парсере Lead Group версии 2.0')
    print('У Вас есть возможность напрямую влиять на его работу. ')
    print('Чем больше дадите обратной связи, тем лучше он будет работать')
    print('Для этого замечания и предложения фиксируйте в файле ')
    print('https://docs.google.com/spreadsheets/d/19Kmt0qVzaeH2I0wBkcBJXtkrmXfvHpFpKugMadLKYVg/edit?usp=sharing ')

    print('ВАЖНО')
    print('Ограничений на количество запросов и городов нет, но стоит помнить, ')
    print('что время работы программы возрастает в геометрической прогрессии (запрос*город*глубину поиска)')
    print('Нажми Enter если понятно')
    input()

    print('Введи запросы для поиска через запятую')
    print('ВАЖНО')
    print('В запросе используйте коммерческие слова ')
    print('"Купить", "Цена", "Снять в аренду", "Продать" и тд')
    print('Так же используйте более узкие запросы')
    print('Например, не "юридические услуги", а "авто юрист" или "Банкротство" ')

    while not list_questions[0]:
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
    print('формирую варианты запроса')
    search_list = generate_search_list(list_questions, city_questions)
    print('[+] - запросы сформированы')
    return search_list, deep_page


# Предложить случайную категорию
def suggest_category_for_search():
    file = requests.get('https://raw.githubusercontent.com/nesterovichps/pwrser_wr/main/top_category.csv')
    random_category = file.content.decode('UTF-8').split('\n')
    print()
    print('10 случайных категорий для поиска')
    print('**********')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print(f'{random.choices(random_category)[0]}')
    print('**********')
    print('Чтобы получить еще 10 случайных категорий нажми Enter или введи запросы для поиска через запятую')


def generate_search_list(list_questions, city_questions):
    list_questions, city_questions = list_questions, city_questions
    search_list = []
    for quest in list_questions:
        if quest:
            for city in city_questions:
                if city:
                    search_list.append(f'{quest} {city}')

    return search_list

def parse_google(response,search_quest,dns_list):

    pattern = 'http(s){0,1}:\/\/[A-zaz0-9\.-]+\/'
    soup = bs(response.content, 'html.parser')
    soup_rk=soup.__copy__()
    for div in soup.find_all('div',class_='g'):
        dns=re.match(pattern,div.a.get('href'))[0]
        dns = search_rubbish(dns)
        if dns and dns not in dns_list:
            dns_list.append(dns)
            company=Company(dns,div.a.text,search_quest)

            list_company.append(company)

    for div in soup_rk.find_all('div',class_='uEierd'):
        dns=re.match(pattern,div.a.get('data-pcu'))[0]
        dns=search_rubbish(dns)
        if dns and dns not in dns_list:
            dns_list.append(dns)
            company = Company(dns, div.a.text, search_quest)
            list_company.append(company)



def search_rubbish(url):
    file=requests.get('https://raw.githubusercontent.com/nesterovichps/pwrser_wr/main/words_of_exclusion.csv')
    list_exception_for_dns = file.content.decode('UTF-8').split('\n')
    for exept in list_exception_for_dns:
        if exept in url:
            return  None

    return url





google_link = 'https://www.google.com/search'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}
list_company = []
company_number=1
search_list=['купить айфон Москва'] #todo del
dns_list=[]
deep_page=1 #TODO del


try:
    # search_list, deep_page = (start_program()) TODO: вкл
    # print("[+] - данные для поиска получены")  TODO: вкл
    print('[+] - Начинаю искать')

    i_quest = 1
    for search_quest in search_list:
        print(f' {i_quest} запрос из {len(search_list)}, ожидайте')
        print(f' Поиск запроса {search_quest}, ожидайте')
        i_quest += 1
        for page in range(deep_page) :
            print(f'[+] - {page+1} страница из {deep_page}, ожидайте')
            time.sleep(random.randint(1, 5))
            param = {'q': search_quest,
                     'start': page * 10}
            response = requests.get(google_link, params=param, headers=headers)

            if response:
                parse_google(response,search_quest,dns_list)
                print('[+] - данные со страницы получены')







    #TODO сохранить результат
    #TODO формирую письмо
    #TODO отправить кп

    # for company in list_company:
    #
    #     save_result(list_url)
    print('Работа окончена')
except:
    print('Упс, что то не работает')









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



# и отсекал форумы и новостные сайты .
# И в идеале хочу сделать , чтобы ещё и трафик сайта пробивал, но по этому пункту пока даже приблизительно не знаю как сделать.

