import requests
import json
import datetime
import logging

class DailyupProxy(object):

    def __init__(self):
        self.session = requests.sessions.Session()
        self.cookies = {}

    def login(self, username, password):
        url = 'https://xxcapp.xidian.edu.cn/uc/wap/login/check'
        form_data = {'username': username, 'password': password}
        res = self.session.post(url, data=form_data)
        if '"e":0' in res.text:
            logging.info(username + ' login.')
            self.cookies = requests.utils.dict_from_cookiejar(res.cookies)
            return True
        else:
            logging.warning(username + ' login fail.')
            return False

    def query_string_stringify(self, json_name):
        cur_time = datetime.datetime.now()
        date = cur_time.date()
        flag = cur_time.hour // 6 - 1
        with open(json_name, 'r', encoding='utf-8') as f:
            form_data = json.loads(f.read())
        form_data['date'] = date
        form_data['flag'] = flag
        query_string = ''
        for key in form_data:
            query_string += key + '=' + (str(form_data[key]) if form_data[key] != None else '') + '&'
        return query_string[0:-1]

    def submit(self):
        url = 'https://xxcapp.xidian.edu.cn/xisuncov/wap/xidian/ulists'
        query_string = self.query_string_stringify('conditions.json')
        res = self.session.get(url + '?' + query_string, cookies=self.cookies)
        users = json.loads(res.text)['d']['lists']
        for user in users:
            number = user['role']['number']
            url = 'https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save'
            with open('data.json', 'r', encoding='utf-8') as f:
                form_data = json.loads(f.read())
            form_data['xgh'] = number
            res = self.session.post(url, data=form_data, cookies=self.cookies)
            if '"e":0' in res.text:
                logging.info(number + ' submit.')
            else:
                logging.error(number + ' submit fails.')
