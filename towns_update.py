# 城镇消失创建检测 by:MC_cubes

import json
import time
import requests

url = "https://earthmc-api.herokuapp.com/towns/"
file = 'data.json'  # 数据文件目录
pause = 10          # 暂停时间
loop = False        # 是否循环? False or True


def read() -> list:
    try:
        with open(file, encoding='utf-8') as f:
            js = json.load(f)
            data = []
            for i in js:
                data.append({'name': i['name'], 'x': i['x'], 'z': i['z']})
        return data
    except:
        with open(file, 'w', encoding='utf-8') as f:
            data = []
            json.dump(data, f)
        return data


def write(data: str) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def update() -> list:
    re = requests.get(url=url).content.decode("UTF-8")
    js = json.loads(re)
    data = []
    for i in js:
        data.append({'name': i['name'], 'x': i['x'], 'z': i['z']})
    return data


if __name__ == '__main__':
    old = read()
    ol = len(old)
    try:
        while True:
            print(ol)
            new = update()
            nl = len(new)
            if ol != nl:
                # dis = [i for i in old if i not in new]
                # cre = [i for i in new if i not in old]
                for i in old:
                    if i not in new:
                        print(f'{i} 消失')
                for i in new:
                    if i not in old:
                        print(f'{i} 创建')
                old = new
                ol = len(old)
            if loop:
                print('sleep')
                for i in range(pause):
                    print('.')
                    time.sleep(1)
            else:
                break
    finally:
        write(old)
