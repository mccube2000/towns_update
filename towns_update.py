# 城镇消失创建检测 by:MC_cubes

import json
import logging
import logging.config
import time

import requests

url = "http://earthmc-api.herokuapp.com/towns/"
file = 'data.json'  # 数据文件目录
pause = 10  # 暂停时间 秒 开启循环后生效
loop = True  # 是否循环? False or True
retry = 10  # 下载失败重试次数
timeout = 30  # 下载超时时间
show_speed = True  # 是否显示下载速度? False or True

# logging.json 14 19 26行 level 可设置为 DEBUG INFO WARN
#              21 28   行 filename 为输出文件，可写相对/绝对路径

with open('logging.json') as f:
    config = json.load(f)
logging.config.dictConfig(config)
logger = logging.getLogger("towns")


def printr(plan: float, speed: str) -> None:
    if show_speed:
        print('\r',
              '{:.1f}'.format(plan),
              '%  ',
              speed,
              end='    ',
              flush=True)


retry_count = 0
speed_info = [{
    'lvl': 'K',
    'lim': 1024**1
}, {
    'lvl': 'M',
    'lim': 1024**2
}, {
    'lvl': 'G',
    'lim': 1024**3
}, {
    'lvl': 'T',
    'lim': 1024**4
}]


def calc_size(speed: int, is_sp=True) -> str:
    for sp in speed_info:
        limit = sp['lim']
        lvl = sp['lvl']
        if speed < (limit * 1024):
            break
    return '{:.1f}'.format(
        speed / limit) + ' ' + lvl + ('B/s' if is_sp else '')


def download():
    global retry_count
    if retry_count < retry:
        logger.debug('正在获取数据大小......')
        with requests.get(url, timeout=timeout, stream=True) as req:
            total_size = int(req.headers['content-length'])
            logger.debug(f'数据大小: {calc_size(total_size, False)}')
            content_size = 0
            plan = 0
            temp_size = 0
            data = b''
            start_time = time.time()
            try:
                for content in req.iter_content(chunk_size=1024):
                    data += content
                    content_size += len(content)
                    plan = (content_size / total_size) * 100
                    speed = total_size
                    if time.time() - start_time > 1:
                        start_time = time.time()
                        speed = content_size - temp_size
                        temp_size = content_size
                        printr(plan, calc_size(speed))
            except:
                logger.info(f'正在重试 {retry_count}......')
                retry_count += 1
                return download()
        printr(plan, calc_size(speed))
        print()
        return data
    return None


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
    try:
        global retry_count
        retry_count = 0
        js = json.loads(download())
    except:
        logger.info('获取数据失败!')
        return None
    data_dict = {}
    try:
        # 如果获取的是原网站数据, 取出需要的数据即可
        for i in js:
            data_dict[i['name']] = [i['x'], i['z']]
        return data_dict
    except:
        # 如果获取的不是原网站数据, 上面会报错, 返回原始数据
        return js


def pos8(data):
    return [int(data[0] / 8), int(data[1] / 8)]


if __name__ == '__main__':
    old = read()
    ol = len(old)
    logger.debug(f'数据文件内城镇数量: {ol}')
    try:
        while True:
            new = update()
            nl = len(new)
            logger.debug(f'更新城镇数量: {nl}')
            if ol != nl:
                for i in old:
                    if i not in new:
                        logger.warning(f'{i} {old[i]} 消失 地狱位置：{pos8(old[i])}')
                for i in new:
                    if i not in old:
                        logger.info(f'{i} {new[i]} 创建 地狱位置：{pos8(new[i])}')
                old = new
                ol = len(old)
            if loop:
                logger.debug(f'暂停{pause}s')
                for i in range(pause):
                    time.sleep(1)
            else:
                break
    finally:
        write(old)
