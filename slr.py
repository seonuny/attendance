#!/home/hugh/UTIL/python_3.6.5/bin/python3
# -*- coding: utf-8 -*-
# parser.py

import requests
from bs4 import BeautifulSoup as bs
import random
from time import sleep
from datetime import datetime
import sys
import os
import logging

# requests와 beautifulsoup 설치 필요
#  $ pip install requests 
#  $ pip install beautifulsoup4.  
#  $ pip install bs4  

# telegram define
TOKEN='561033107:AAFRKMLeEghQgfZf13a1hHMFo0aJRMGeVe4'
CHAT_ID='454993046'
MSG_URL='/sendMessage?chat_id='

# logging 
filename = '/home/hugh/SCRIPT/LOG/{0}_{1}.log'.format(os.path.basename(os.path.splitext(sys.argv[0])[0]),datetime.now().strftime('%Y%m%d'))
logging.basicConfig(filename=filename, level=logging.INFO,format='%(asctime)s %(message)s',datefmt='[%Y.%m.%d %I:%M:%S]')
logging.info('Started')

if len(sys.argv) != 1 :
    bSleep = True
    bAttendance = True
else :
    bSleep = False
    bAttendance = False 
sleep_min = 1
sleep_max = 30

if bSleep :
    num = random.randint(sleep_min,sleep_max)
    logging.info('sleep sec:{0}'.format(num))
    sleep(num)

# 로그인할 유저정보를 넣어주자 (모두 문자열)
LOGIN_INFO = {
        'user_id': 'hughK',
        'password': 'qwertyu1',
        }

bFlag = False
try :
    # Session 생성, with 구문 안에서 유지
    with requests.Session() as s:
        # HTTP POST request: 로그인을 위해 POST url와 함께 전송될 data를 넣어주자.
        r = s.post('https://www.slrclub.com/login/process.php', data=LOGIN_INFO)
        logging.info(r.status_code)
        logging.info(r.text)
        r = s.get('http://www.slrclub.com/')
       #msg = r.text.encode('utf-8')
        msg = r.text
        for line in msg.splitlines():
            if bFlag == True:
                find_start = line.find('>')+1
                find_end   = line.find('<',find_start)
                msg_detail += line[find_start:find_end]
                if len(line[find_start:find_end]) >= 1:
                    msg_detail +='\n'
            if bFlag==False and '"login"' in line:
                msg_detail = ""
                bFlag = True
            if bFlag==True and 'login-article' in line:
                bFlag = False

        logging.info(msg_detail)
        if bAttendance == True :
           #텔레그램 전송.
            MSG='{0}'.format(msg_detail)
            telegram_bot_url='https://api.telegram.org/bot{0}{1}{2}&text={3}'.format(TOKEN,MSG_URL,CHAT_ID,MSG)
            r = s.get(telegram_bot_url)
            logging.info('텔레그램 전송 결과:%d',r.status_code)
            if bSleep :
                num = random.randint(sleep_min,sleep_max)
                logging.info('sleep sec:{0}'.format(num))
                sleep(num)
       #r = s.get('http://www.slrclub.com/bbs/zboard.php?id=today_pictures')    
       #print type(r)
       #print r.request
       #print r.headers
       #for line in r.iter_lines():
       #    print line
       #    break
    

except TypeError as inst :
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    logging.error('{0}:{1}:{2} type:{3},args:{4},inst:{5}'.format(filename,lineno,line.strip(),type(inst),inst.args,inst))
except UnicodeEncodeError as inst :
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    logging.error('{0}:{1}:{2} type:{3},args:{4},inst:{5}'.format(filename,lineno,line.strip(),type(inst),inst.args,inst))
except Exception as inst :
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    logging.error('{0}:{1}:{2} type:{3},args:{4},inst:{5}'.format(filename,lineno,line.strip(),type(inst),inst.args,inst))
except :
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    logging.info('{0}:{1}:{2} Unexpected error:'.format(filename,lineno,line.strip(),tb[0]))
finally:
    logging.info("Finished")

