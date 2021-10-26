import proxy
import json
import logging
import yagmail
import datetime

def main_handler():
    cur_time = datetime.datetime.now()
    date = str(cur_time.date())
    flag = cur_time.hour // 6 - 1
    kv = {0: '晨检', 1: '午检', 2: '晚检'}
    filename = date + kv[flag] + '.log'
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', filename=filename, filemode='a')
    dailyup_proxy = proxy.DailyupProxy()
    with open('superusers.json', 'r', encoding='utf-8') as f:
        superusers = json.loads(f.read())
    for superuser in superusers:
        if dailyup_proxy.login(superuser['username'], superuser['password']):
            dailyup_proxy.submit()
    with open("smtp.json", "r", encoding="utf-8") as f:
        smtp = json.loads(f.read())
    yag = yagmail.SMTP(user=smtp['user'], password=smtp['password'], host=smtp['host'])
    yag.send('admin@admin.com', date + kv[flag], '', filename)

main_handler()