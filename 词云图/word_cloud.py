import pymongo
import re
from wordcloud import WordCloud
import jieba
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import collections
import json

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.kongjian
collection = db.ss


# 选取内容不为空的说说
def get_content():
    results = collection.find({'content': {'$ne' : ''}})
    for result in results:
        with open('process.txt', 'a', encoding='gb18030') as file:
            file.write(result.get('content'))


# 删除文本中的字符
def process_content():
    with open('process.txt', 'r', encoding='gb18030') as file:
        text = file.read()
        # 若需要删除数字与字符则在[]*中最后加上[a-zA-Z0-9]
        pattern = re.compile(r'[=～@：‥…%{}<>\"、\'“”\?！!~,，。#（）【】\[\]？\\./]*')
        text = re.sub(pattern, '', text)
        # 可以选择再把处理后的数据再写入文件，但是存在字符编码的问题
        # with open('result.txt', 'a', encoding='gb18030') as result:
        #     result.write(text)
        return text


# 判断字符是否为中文
def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


# 获取一定出现频率的词
def get_word_dict(text):
    # 分词
    seg_list_exact = jieba.cut(text, cut_all = False)
    # 存储所有的分词
    object_list = []
    # kick_words_first = [' ', '我', '的', '了', '在', '你', '是',
    #                     '有', '也', '都', '好', '说', '就', '不', '要']
    # 要剔除的分词
    kick_words_sec = []
    for word in seg_list_exact: # 循环读出每个分词
        object_list.append(word)
    # 统计词频
    words = collections.Counter(object_list)
    # 存储词频在一定频率的字词
    for word in words:
        if words.get(word) > 100:
            kick_words_sec.append(word)
        elif not is_Chinese(word):
            kick_words_sec.append(word)

    # 删除这些频率的字词
    for word in kick_words_sec:
            words.pop(word)
    return words


# 生成词云
def generate_word_cloud(words):
    # 词云图背景
    alice_mask = np.array(Image.open('ciyun.jpg'))
    # 词云图生成
    word_cloud = WordCloud(font_path='fzfs.ttf', background_color='white', max_words=200, max_font_size=80,
                          mask=alice_mask)
    word_cloud.generate_from_frequencies(words)
    # interpolation: 插值法
    plt.imshow(word_cloud, interpolation='bilinear')
    # 去坐标轴
    plt.axis('off')
    plt.savefig('word_cloud.png')
    plt.show()


# 主函数
if __name__ == '__main__':
    # get_content()
    text = process_content()
    words = get_word_dict(text)
    print(words)
    generate_word_cloud(words)
