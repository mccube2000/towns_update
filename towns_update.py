# 城镇消失创建检测 by:MC_cubes

import json
import time

import requests

url = "https://earthmc-api.herokuapp.com/towns/"
file = 'data.json'  # 数据文件目录
pause = 10  # 暂停时间 秒 开启循环后生效
loop = True  # 是否循环? False or True
level = 2  # 显示的提示信息等级 0-2 越小显示的信息越少


def printl(msg: str, l: int = -1):
    if l < level:
        print(msg)


def read() -> dict:
    try:
        with open(file, encoding='utf-8') as f:
            js = json.load(f)
    except:
        js = {}
    return js


def write(data: str) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def update() -> dict:
    printl('正在获取城镇信息, 可能需要很久......', 1)
    re = requests.get(url=url).content.decode("UTF-8")
    js = json.loads(re)
    data = {}
    for i in js:
        data[i['name']] = [i['x'], i['z']]
    return data


if __name__ == '__main__':
    if level > 2:
        level = 2
    elif level < 0:
        level = 0

    old = read()
    ol = len(old)
    printl(f'数据文件内城镇数量: {ol}', 0)
    try:
        while True:
            new = update()
            nl = len(new)
            printl(f'更新城镇数量: {nl}', 0)
            if ol != nl:
                for i in old:
                    if i not in new:
                        printl(f'{i} {old[i]} 消失')
                for i in new:
                    if i not in old:
                        printl(f'{i} {new[i]} 创建')
                old = new
                ol = len(old)
            if loop:
                printl('sleep', 1)
                for i in range(pause):
                    printl('.', 1)
                    time.sleep(1)
            else:
                break
    finally:
        write(old)
