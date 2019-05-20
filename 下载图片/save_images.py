import pymongo
import os
import requests
from hashlib import md5


def sava_image(result):
    content = result.get('content')
    content = content.replace('?', '？')
    content = content.replace('/', '')
    content = content.replace('\\', '')
    dir = './zz/' + content + result.get('_id').__str__()

    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except OSError:
            print(dir)
        for image in result.get('images'):
            try:
                response = requests.get(image)
                if response.status_code == 200:
                    file_path = '{0}/{1}.{2}'.format(dir, md5(response.content).hexdigest(), '.jpg')
                    if not os.path.exists(file_path):
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                    else:
                        print('Already Download', file_path)
            except requests.ConnectionError:
                print('Faild to Save Image')
            except requests.exceptions.MissingSchema:
                with open('error.txt', 'a', encoding='gb18030') as file:
                    file.write(dir + '\n')
                print('URL error')
            except OSError:
                print(dir)

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.kongjian
collection = db.zz
results = collection.find({'images': {'$ne': []}})
for result in results:
    sava_image(result)
print(results.count())

