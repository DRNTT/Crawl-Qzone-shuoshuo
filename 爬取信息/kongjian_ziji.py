from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import time
import json
import pymongo


browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.kongjian


def index_page(page):
    #  进入主页
    try:
        if page > 1:
            print('正在爬取', page, '页')
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#pager .textinput')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#pager .bt_tx2')))
            input.clear()
            input.send_keys(page)
            submit.click()

        get_info()
    except TimeoutException:
        index_page(page)


def get_info():
        # 若能展开，则展开所有说说的原文
        time.sleep(1)
        # 也可以设置一个较大的数，一下到底
        js = "var q=document.documentElement.scrollTop=10000" # javascript语句
        browser.execute_script(js)
        time.sleep(3)

        btn_ap_ss = browser.find_elements_by_css_selector('.f_toggle a')
        for btn_ap_s in btn_ap_ss:
            if btn_ap_s.text == '展开查看全文':
                if btn_ap_s.is_displayed():
                    time.sleep(2)
                    browser.execute_script("arguments[0].click();", btn_ap_s)
                    # 该方法无效
                    # btn_ap_s.click()
        time.sleep(2)

        # 在获取一次html源代码
        html = browser.page_source
        # print(html)
        doc = pq(html)
        items = doc('#msgList .feed').items()

        for item in items:
            pic = []
            images = item.find('.md img').items()
            times = item.find('.ft .info')
            if times.size() == 2:
                time_ss = 1
            else:
                time_ss = 0
            for image in images:
                pic.append(image.attr('data-src'))
            ss = {
                'author': item.find('.bd .qz_311_author').text(),
                'content': item.find('.bd .content').text(),
                'images': pic,
                'time': times.eq(time_ss).text()
            }
            collection_s = db.ss
            collection_s.insert_one(ss)
            # 有转载内容
            if time_ss == 1:
                pic_zz = []
                images_zz = item.find('.md .md img').items()
                for image in images_zz:
                    pic_zz.append(image.attr('data-src'))
                zz = {
                    'author': item.find('.md .bd .qz_311_author').text(),
                    'content': item.find('.md .bd pre').text(),
                    'images': pic_zz,
                    'time': times.eq(0).text()
                }
                collection_z = db.zz
                collection_z.insert_one(zz)


def save_to_txt(ss):
    with open('zz.txt', 'a', encoding='gb18030') as file:
        file.write(json.dumps(ss, ensure_ascii=False) + '\n')


MAX_PAGE = 294

if __name__ == '__main__':
    url = 'https://user.qzone.qq.com/qq号/311'
    browser.get(url)
    time.sleep(5)
    browser.switch_to.frame('app_canvas_frame')
    for page in range(1, MAX_PAGE + 1):
        index_page(page)