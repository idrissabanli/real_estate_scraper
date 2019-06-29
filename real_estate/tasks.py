# from __future__ import absolute_import, unicode_literals
import traceback
import re
from datetime import timedelta


from celery import shared_task

# Use celery shared_task documentation here
# http://docs.celeryproject.org/en/latest/faq.html


import requests
import time
from lxml import html

from real_estate.models import RealEstateDetail, SearchWord, PhoneNumber


def get_xpath_element_link(elements):
    if elements:
        return ['https://www.sahibinden.com{}'.format(el.get('href')) for el in elements]
    else:
        return None


def get_xpath_element_text(elements):
    if elements:
        return elements[0].text
    else:
        return None


def get_xpath_elements_text(elements):
    if elements:
        return [element_text.text for element_text in elements]
    else:
        return None


# url = 'https://www.sahibinden.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 '
                  'Safari/537.36'}

client = requests.session()


def get_real_estate_detail(url, search_word):
    try:
        print('Go to ', url)
        r = client.head(url, headers=headers)

        print('page status code ', r.status_code)

        page = client.get(url, headers=headers)

        print('Detail page opened successfully')
        tree = html.fromstring(page.content)

        phone_numbers = get_xpath_elements_text(tree.xpath('//*[@id="phoneInfoPart"]/li/span[1]'))

        phone_titles = get_xpath_elements_text(tree.xpath('//*[@id="phoneInfoPart"]/li/strong'))

        city = get_xpath_element_text(tree.xpath('//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/h2/a[1]'))
        district = get_xpath_element_text(tree.xpath('//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/h2/a[2]'))
        street = get_xpath_element_text(tree.xpath('//*[@id="classifiedDetail"]/div[1]/div[2]/div[2]/h2/a[3]'))

        print('city', city)
        print('district', district)
        print('street', street)

        agency_name = get_xpath_element_text(tree.xpath('//span[@class = "storeInfo"]'))
        realtor_name = get_xpath_element_text(tree.xpath('//div[@class = "username-info-area"]/h5'))

        print('agency_name', agency_name)
        print('realtor_name', realtor_name)

        real_estate_dict = {}

        name = get_xpath_element_text(tree.xpath('//*[@id="classifiedDetail"]/div[1]/div[1]/h1'))

        if name:
            real_estate_dict['name'] = re.sub(' +', ' ', name)
        if agency_name:
            real_estate_dict['agency_name'] = re.sub(' +', ' ', agency_name)
        if realtor_name:
            real_estate_dict['realtor_name'] = re.sub(' +', ' ', realtor_name)
        if city:
            real_estate_dict['city'] = re.sub(' +', ' ', city)
        if district:
            real_estate_dict['district'] = re.sub(' +', ' ', district)
        if street:
            real_estate_dict['street'] = re.sub(' +', ' ', street)
        real_estate_dict['url'] = url
        real_estate_dict['search_word'] = search_word

        real_estate = RealEstateDetail.objects.create(**real_estate_dict)

        counter = 0
        print('titles and header for ', name)
        if phone_numbers:
            for phone_number in phone_numbers:
                print(phone_titles[counter], phone_number)
                PhoneNumber.objects.create(title=re.sub(' +', ' ', phone_titles[counter]),
                                           phone=re.sub(' +', ' ', phone_number), real_estate=real_estate)
                counter += 1
    except:
        print('error', traceback.format_exc())
        search_word.status = 2
        search_word.save()
    return True

@shared_task
def get_new_real_estates(search_word_id, page=0):
    search_word = SearchWord.objects.get(id=search_word_id)
    url = 'https://www.sahibinden.com/emlak?cspv=true&pagingOffset={}&pagingSize=50&query_text_mf={}'\
        .format(page, search_word.word)

    r = client.head(url, headers=headers)

    print('page status code ', r.status_code)

    print('Go to ', url)

    page = client.get(url, headers=headers)

    print('Page opened successfully')
    # print(page.content)
    tree = html.fromstring(page.content)

    reate_estate_links = get_xpath_element_link(tree.xpath("//a[@class = ' classifiedTitle' ]"))

    print('reate_estate_links ', reate_estate_links)

    for reate_estate_link in reate_estate_links:
        time.sleep(3)
        get_real_estate_detail(reate_estate_link, search_word)
    if page == 1000:
        search_word.status = 3
        search_word.save()

@shared_task
def get_page_datas(search_word_id, created_time):
    page = 0
    while page <= 1000:
        print('page == ', page)
        get_new_real_estates.apply_async(args=(search_word_id, page), eta=(created_time + timedelta(minutes=1)))
        page = page + 50

# get_page_datas('djkfbsdkj')

# get_real_estate_detail('https://www.sahibinden.com/ilan/emlak-konut-satilik-duru-gayrimenkul%2Cden-yilin-firsati-2-plus1-sifir-bahce-kullanimli-704634547/detay')
