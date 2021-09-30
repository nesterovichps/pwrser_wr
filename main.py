import requests
from bs4 import BeautifulSoup as bs
import time
import re
import csv
import random
import os
import idna
import smtplib
from threading import *


# Создание модели стандартной компании
class Company:
    company_name = ''
    company_email = ''
    company_phone = ''
    company_comment = ''
    company_status_in_base = 5  # 4-база 5-недозвон 6-переговоры 7-ожидаем оплаты 8-партнерка 9-оплачено 10-закрыто нереализовано
    company_dns = ''
    company_status_add = True
    list_for_search_contact = ['partnerskaya-programma', 'partner', 'contacts', 'contact', 'about', 'vip', 'admin',
                               'boss', 'feedback']
    list_answer_response = []

    def __init__(self, dns, comment, search_quest):
        global headers
        self.list_answer_response.clear()
        self.company_dns = dns
        self.check_company_status(headers)
        if self.company_status_add:
            self.collect_a_list_of_pages()

            for response in self.list_answer_response:
                if not self.company_phone:
                    self.get_company_phone(response)
                if not self.company_email:
                    self.get_company_email(response)
            self.get_company_name(search_quest)
            self.get_company_comment(comment)
            self.get_first_lvl_domain()
            print('[+] - данные со страницы получены')

    def check_company_status(self, headers):

        response = requests.get(self.company_dns, headers=headers ,verify=False )
        if response:
            self.list_answer_response.append(response)
            print(f'[+] - Домен  {self.company_dns} доступен')
        else:
            print(f'[-] - Домен  {self.company_dns} НЕ РАБОТАЕТ')
            self.company_status_add = False

    def collect_a_list_of_pages(self):
        for page in self.list_for_search_contact:
            time.sleep(random.randint(1, 2))

            response = requests.get(f'{self.company_dns}{page}/',headers=headers ,verify=False)
            if response:
                self.list_answer_response.append(response)



    def get_company_name(self, search_quest):
        self.company_name = f'parser {search_quest}'

    def get_company_email(self, response):
        pattern = "([A-z0-9_.-]{1,})@([A-z0-9_.-]{1,}).([A-z]{2,8})"
        email_company=re.search(pattern, response.text)
        if email_company:
            self.company_email = email_company[0]
            print(f'   [+] - email. найден {self.company_dns}')

    def get_company_phone(self, response):

        i = re.search('https://wa.me/', response.text)
        if i:

            i=int(i.end())
            tel = response.text[i:i + 11]
            if tel:
                self.company_phone = tel
                print(f'   [+] - тел. найден {self.company_dns}')

        if not self.company_phone:

            i = re.search('tel:', response.text)
            if i:
                i = int(i.end())
                tel = response.text[i:i + 22]
                if tel:
                    tel = tel.replace(' ', '').replace('.', '').replace('/', '').replace('(', '').replace(')', '').replace(
                        '_', '').replace('-', '').replace('+', '').replace('"', '')
                    tel = re.search(r'\d+', tel)
                    if tel:
                        tel=tel[0]
                        tel = tel[:11]
                        if tel:
                            self.company_phone = tel
                            print(f'   [+] - тел. найден {self.company_dns}')


    def get_company_comment(self, comment):
        self.company_comment = comment

    def get_first_lvl_domain(self):
        url = self.company_dns.strip().replace('http://', '').replace('https://', '').replace('/', '').replace('www.',
                                                                                                               '')
        if url.count('.') > 1:
            self.company_dns = url[url.index('.') + 1:].strip()
        if 'xn--' in url:
            url = idna.decode(url)
            self.company_dns = url


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
    deep_page = int(input())
    if deep_page > max_deep:
        deep_page = 5
        print(f'Вы превысили максимальную глубину поиска ({max_deep} страниц), установлено значение {deep_page} страниц')

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

    search_list = []
    for quest in list_questions:
        if quest:
            for city in city_questions:
                if city:
                    search_list.append(f'{quest} {city}')

    return search_list


def parse_google(response, search_quest, dns_list):
    pattern = 'http(s){0,1}:\/\/[A-zaz0-9\.-]+\/'
    soup = bs(response.content, 'html.parser')

    for div in soup.find_all('div', class_='g'):
        dns = re.match(pattern, div.a.get('href'))
        if dns:

            dns = search_rubbish(dns[0])

        if dns and dns not in dns_list:
            dns_list.append(dns)

            company = Company(dns, div.a.text, search_quest)
            list_company.append(company)

    soup = bs(response.content, 'html.parser')
    for div in soup.find_all('div', class_='uEierd'):
        dns = re.match(pattern, div.a.get('data-pcu'))[0]
        dns = search_rubbish(dns)
        if dns and dns not in dns_list:
            dns_list.append(dns)
            company = Company(dns, div.a.text, search_quest)
            list_company.append(company)


def search_rubbish(url):
    file = requests.get('https://raw.githubusercontent.com/nesterovichps/pwrser_wr/main/words_of_exclusion.csv')
    list_exception_for_dns = file.content.decode('UTF-8').split('\n')
    for ex in list_exception_for_dns:
        if ex in url:
            return None

    return url


def save_result(list_company):
    file_number = 1
    try:
        for i in range(1, 100):
            os.remove(f'result{i}.csv')
    except:
        pass

    while list_company:
        with open(f'result{file_number}.csv', 'w', encoding='UTF-8', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            i = 0
            while i < 200 and list_company:
                company = list_company.pop()
                filewriter.writerow([company.company_name,
                                     company.company_email,
                                     company.company_phone,
                                     company.company_comment,
                                     '',
                                     '',
                                     company.company_dns])
                i += 1
        file_number += 1


def create_email_list(list_company):
    email_list_for_send = []
    for company in list_company:
        if company.company_email:
            email_list_for_send.append(company.company_email)
    return email_list_for_send


def mail_teamplate(first_name_manager, last_name_manager, logo_masagerov, tel_company, tel_manager, sait_company,
                   logo_company):
    mail = f'''
Здравствуйте, Меня зовут {last_name_manager}.
Мы готовы поставлять Вам клиентов с гарантией. Стоимость одного заинтересованного клиента будет от 42 до 93 руб . Если контакт пустой, то стоит 0 рублей.

Тестовые 3-5 клиентов, которые подтвердят свой интерес, дадим бесплатно . причем Вам даже звониь никому не нужно. Мы определим 10 посетителей с Вашего сайта, сами с ними свяжемся и передадим Вам уже подтвержденных клиентов, которые будут ждать от Вас звонка.

А теперь расскажу , почему это письмо стоит Вашего внимания.

Мы сделали и запатентовали продукт, который позволяет определять телефонные номера посетителей, которые заходили на ваш сайт, интересовались вашим продуктом,но в итоге ушли и заявку не оставили.
Важно, само по себе подключение продукта, его использование или техническая поддержка стоит 0 рублей! Вы платите только за конкретный результат, в виде телефонных номеров новых потенциальных клиентов. При этом, все это не просто красивые слова- все эти условия мы фиксируем с вами в договоре. Если вы позвонили по номеру, но не дозвонились до клиента, либо клиент не заинтересован, то такие номера меняются. В видео без воды, подробно рассказано как работает технология https://www.youtube.com/watch?v=MJ3NB-Zg5i0

Лучше всего о нашей работе расскажут результаты наших клиентов в цифрах https://disk.yandex.uz/i/kQQP67REEhesww

Крупнейшие компании России уже являются нашими клиентами https://docs.google.com/spreadsheets/d/1f4z0zePJgpCsbsLCQl16C6NeveFn-4Jfl9ccty0QS6s/edit#gid=0
Нам доверяет уже более 26 000 компаний по всей РФ из различных сфер https://crm.wantresult.ru/site/public-categories
ВТБ выпустил пресс-релиз, в котором назвал Нашу технологию лучшей из 190 IT продуктов https://www.rvc.ru/press-service/media-review/rvk/146546/

Министерство экономического развития, своместно с Сбербанком создало специальную платформу знаний и сервисов для бизнеса «Деловая среда». Цель этой платформы - помочь предпринимателям в более эффективном запуске и управлению бизнесом. «Деловая среда» выбрала нас официальным партнером по направлению «Маркетинг» https://dasreda.ru/services/tarif-start

Сбербанк на своем официальном сайте размещает информацию о нас https://www.sberbank.ru/ru/s_m_business/franchises/detail/want-result

Так же Мы являемся резидентами Сколково https://navigator.sk.ru/orn/1124137

Нет ресурсов\ времени обрабатывать наши Лиды?

Тоже не проблема. Наши менеджеры могут обрабатывать поток клиентов и передавать Вам уже тех клиентов, которые подтвердили интерес по телефону. Можем даже разработать небольшой скрипт , чтобы прогонять по воронке и сразу отсекать тех клиентов, которые не подошли под Ваши первичные требования.

---
С уважением к Вам и Вашему бизнесу, ведущий специалист отдела развития регионального бизнеса {first_name_manager} {last_name_manager}, Lead Group
{logo_masagerov}
{tel_manager}
{tel_company}
Сайт: {sait_company}
"Экономить на рекламе всё равно, что остановить часы с целью экономии времени."
(с)Томас Джефферсон
{logo_company}
'''
    print('[+] Письмо сформировано')
    return mail


def connect_server(EMAIL_LOGIN, EMAIL_PASS, SMTP):
    server = smtplib.SMTP_SSL(SMTP)
    server.login(EMAIL_LOGIN, EMAIL_PASS)
    print('[+] Подключение успешно')
    return server


def send_mail(email_letter, send_server, email_from, email_to, email_subgect):
    email_subgect = random.choice(email_subgect)
    header = f'''From: {email_from}
To: {email_to}
Subject: {email_subgect}
    '''

    email_letter = header + email_letter
    email_letter = email_letter.encode('utf-8')
    try:
        send_server.sendmail(email_from, email_to, email_letter)
        print(f'[+] Письмо на почту {email_to} отправлено')
    except:
        print(f'[-] Письмо на почту {email_to} НЕ отправлено')


google_link = 'https://www.google.com/search'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Referer': 'https://www.google.com/',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}


list_company = []
company_number = 1
dns_list = []
EMAIL_LOGIN = 'leadgroup@internet.ru'
EMAIL_PASS = 'DSB2HknauTt77ZeTGa1p'
SMTP = 'smtp.mail.ru:465'
email_from = 'leadgroup@internet.ru'
email_to = 'leadgroup@internet.ru'
email_subject = ['Для руководства', 'Для Директора']
first_name_manager = 'Нестерович'
last_name_manager = 'Петр'
logo_massager = ''
tel_company = '8 995 333 60 21'
tel_manager = 'Тел.: 8 950 333 33 43'
url_company = 'result55.ru'
logo_company = ''
potok=10
potok_list=[]
search_list, deep_page = (start_program())
print("[+] - данные для поиска получены")
print('[+] - Начинаю искать')

i_quest = 1


for search_quest in search_list:
    print(f' {i_quest} запрос из {len(search_list)}, ожидайте')
    print(f' Поиск запроса {search_quest}, ожидайте')
    i_quest += 1
    for page in range(deep_page):
        print(f'[+] - {page + 1} страница из {deep_page} , ожидайте')

        time.sleep(random.randint(1, 5))
        param = {'q': search_quest,
                 'start': page * 10}
        response = requests.get(google_link, params=param, headers=headers)

        if response:
            for _ in range(potok):
                pt = Thread(target=parse_google, args=(response, search_quest, dns_list,))
                potok_list.append(pt)

            for pt in potok_list:
                if pt:
                    pt.start()
            # parse_google(response, search_quest, dns_list)
            for pt in potok_list:
                if pt:
                    pt.join()
            potok_list.clear()


save_result(list_company)
print('[+] - результаты сохранены')

print('Работа окончена')

f = 0
while f != '1' and f != '2':
    print('Хочешь отправить Коммерческое предложение по всем собранным емэйлам???')
    print('выбери один из вариантов')
    print('1 - да, отправить кп')
    print('2 - нет, закончить работу программы')
    f = input()

    print('[+] - ответ принят' if (f == '1' or f == '2') else '[-] ответ не принят, выбери из доступных вариантов')

if f == 1:
    print('[+] - рассылка кп запущена')
    print('Формирую список для емейл рассылки')
    email_list_for_send = create_email_list(list_company)
    if email_list_for_send:
        print(f'[+] список рассылки сформирован. Подготовлено {len(email_list_for_send)}адресов для рассылки')
        email_letter = mail_teamplate(first_name_manager, last_name_manager, logo_massager,
                                      tel_company, tel_manager, url_company, logo_company)
        try:
            print('Подключаюсь к почтовому серверу')
            send_server = connect_server(EMAIL_LOGIN, EMAIL_PASS, SMTP)
        except:
            print('[-] Не удалось подключится к серверу, неверный логин и пароль от почты, завершаю работу')

        print('Пробую отправить письмо из .')
        i_send = 1
        for email_to_send in email_list_for_send:
            print(f'Пробую отправить {i_send} из {len(email_list_for_send)} адресов ')
            try:
                send_mail(email_letter, send_server, email_from, email_to_send, email_subject)
            except:
                print('[-] ошибка с отправкой сообщения')
        send_server.quit()
        print('[+] Рассылка закончена')

    else:
        print('[-] - Список емейлов пуст, завершаю работу')
print('[+] - работа программы закончена. отличного дня.')

# и отсекал форумы и новостные сайты .
# И в идеале хочу сделать , чтобы ещё и трафик сайта пробивал, но по этому пункту пока даже приблизительно не знаю как сделать.
