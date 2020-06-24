import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time


def write_csv_header():  # обновляет файл, добавляя в него заголовки
    with open('vk_parser.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Город', 'Сообщество', 'Ссылка на сообщество', 'Наименование товара', 'Ссылка на товар',
                         'Цена товара', 'Изображение товара', 'Дата добавления товара'))


def write_csv(data):  # записывает данные в файл csv
    with open('vk_parser.csv', 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        row = (data['city'], data['group'], data['group_ref'], data['product_name'], data['product_ref'],
                         data['product_price'], data['image'], data['time'])
        writer.writerow(row)


def main():
    driver = webdriver.Chrome()
    driver.get("https://vk.com/market?city=2&country=1&groups=1&q=%D0%BA%D1%83%D1%80%D1%81%D1%8B%20%D0%B1%D1%80%D0%BE%D0%B2%D0%B8%D1%81%D1%82%D0%B0&sort=101")

    time.sleep(40)  #необходимо для того, чтобы успеть авторизоваться и прокрутить до конца страницу
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')

    row_names = soup.find_all('div', class_='market_row_inner_cont')
    write_csv_header()
    for obj in row_names:
        product_name = obj.find('div', class_='market_row_name').text
        product_price = obj.find('div', class_='market_row_price').text
        group_name = obj.find('div', class_='market_row_user').text
        group_reference = obj.find('div', class_='market_row_user').find('a').get('href')
        dat = obj.find('div', class_='market_row_time').text
        image = obj.find('img', class_='market_row_img').get('src')
        image_ref = obj.find('div', class_='market_row_photo bordered-thumb').find('a').get('href')
        group_reference = 'https://vk.com' + str(group_reference)
        image_reference = 'https://vk.com/market' + str(image_ref)
        data = {'city': 'Санкт-Петербург',
                'group': group_name,
                'group_ref': group_reference,
                'product_name': product_name,
                'product_ref': image_reference,
                'product_price': product_price,
                'image': image,
                'time': dat
                }
        write_csv(data)
        print(product_name + ' ' + product_price + ' ' + group_name + ' ' + group_reference + ' ' + dat + ' ' + str(
            image) + ' ' + image_reference)

if __name__ == '__main__':
    main()
