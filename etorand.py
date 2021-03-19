#!/bin/python3
# -*- coding: utf-8 -*-
# parser.py

import requests
from bs4 import BeautifulSoup as bs
import random
from time import sleep
from datetime import datetime
from datetime import timedelta
import sys
import os
import logging
import urllib.parse

# telegram define
TOKEN='561033107:AAFRKMLeEghQgfZf13a1hHMFo0aJRMGeVe4'
CHAT_ID='454993046'
MSG_URL='/sendMessage?chat_id='

# requests와 beautifulsoup 설치 필요
#  $ pip install requests 
#  $ pip install beautifulsoup4.  
#  $ pip install bs4  

os.chdir('./')
filename = './LOG/{0}_{1}.log'.format(os.path.splitext(os.path.basename(sys.argv[0]))[0],datetime.now().strftime('%Y%m%d'))
logging.basicConfig(filename=filename, level=logging.INFO,format='[%(funcName)s:%(lineno)05d] %(asctime)s %(message)s',datefmt='[%Y.%m.%d %I:%M:%S]')
logging.info('Started')
yesterday = (datetime.now() + timedelta(days=-1)).strftime('%m-%d')




def func(user,passwd,bFlag,sleep_min,sleep_max):
    bSleep = bFlag
    bAttendance = bFlag
   #bPoint = bFlag
    bPoint = True
    bFirst1 = True
    bFirst2 = True
    bFirst3 = True
    bFirst4 = True
    bFirst5 = True

    if bSleep :
        num = random.randint(sleep_min,sleep_max)
        logging.info('sleep sec:{0}'.format(num))
        sleep(num)

    # 로그인할 유저정보를 넣어주자 (모두 문자열)
    LOGIN_INFO = {
            'mb_id': user,
            'mb_password': passwd,
            }
    
    nDate = int(datetime.now().strftime('%Y%m%d'))
    logging.info("current date:{0}".format(nDate))
    msg_detail = None
    
    try :
        # Session 생성, with 구문 안에서 유지
        with requests.Session() as s:
    
            # HTTP POST request: 로그인을 위해 POST url와 함께 전송될 data를 넣어주자.
           #url_login = 'https://etoland.co.kr/bbs/login_check2.php'
            url_login = 'https://www.etoland.co.kr/bbs/login_check2020.php'
            r = s.post(url_login, data=LOGIN_INFO)
            logging.info('login result : {0}'.format(r.status_code))
            logging.info(r.text)
        
            # 로그인이 되지 않으면 경고를 띄운다.
            if r.status_code != 200:
               raise Exception('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요.')
            logging.info("로그인 성공")
        
           #r = s.get('http://etoland.co.kr/bbs/download_et.php?bo_table=data_hit&wr_id=23931&no=0',allow_redirects=True)
           #open('MV.mp4.torrent','wb').write(r.content)
           #exit()
    
            if bSleep :
                num = random.randint(sleep_min,sleep_max)
                logging.info('sleep sec:{0}'.format(num))
                sleep(num)
    
            try :
                if True:
                   #포인트 확인.
                    url_point = 'http://www.etoland.co.kr/bbs/point.php'
                    r = s.get(url_point)
                    contents = bs(r.text, 'html.parser') # Soup으로 만들어 줍시다.
                    logging.info(contents)
                    point_before = contents.find_all("b")[-1].text
                    logging.info(point_before)
            except TypeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except UnicodeEncodeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except IndexError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except Exception as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except :
                logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        
            if bAttendance :
                # -- 여기에서부터는 로그인 된 세션이 유지된다. 
                # 출석체크로 이동.... 
                #출첵 문자열 가져와서 만들어보자
                url_attendance = 'https://www.etoland.co.kr/check/index.php'
                r = s.get(url_attendance) #출첵
                soup = bs(r.text, 'html.parser') 
                table = soup.find_all("input", {'class' : 'ed'})
                attend_temp=str(table[0])
                attend_temp=attend_temp.split("value=")
                attend_temp=attend_temp[1].split("\"")
                logging.info('출석체크 문자열:{0}'.format(attend_temp[1]))
                #"출석체크문자열/"
                attend_str = str(attend_temp[1])
                
                CHECK_INFO = {
                   #'at_memo': (attend_str.decode('utf-8')).encode('euc-kr')
                    'at_memo': attend_str.encode('euc-kr')
                }
                #실제 출석체크 
                r = s.post('https://www.etoland.co.kr/check/attendance-update.php', data=CHECK_INFO) # 출첵 이후 .. 시험 완료. 
                logging.info("result:[{0}]".format(r.text))
                soup = bs(r.text, 'html.parser') 
                logging.info(soup.find_all('alert'))
                msg = soup.find_all('script')[-1].text
                logging.info(msg)
                str_start = '출석'
                str_end = '니다'
                find_start = msg.find(str_start)
                find_end = msg.find(str_end,find_start)+len(str_end)
                logging.info("find [{0}:{1}]".format(find_start,find_end))
                msg_detail = msg[find_start:find_end]
                msg_detail = msg_detail.replace('\n','')
                logging.info('출석 result : {0}:{1}'.format(r.status_code,msg_detail))
                if bSleep :
                    num = random.randint(sleep_min,sleep_max)
                    logging.info('sleep sec:{0}'.format(num))
                    sleep(num)
        
            if bPoint == True :
                try:
                    url_point1 = 'http://www.etoland.co.kr/bbs/board.php?bo_table=point1'
                    r = s.get(url_point1)
                    soup = bs(r.text,'html.parser')
                    td_list = soup.find_all('td')
                    free_points = soup.select('#mw_basic > div:nth-of-type(1) > div')
                   #i = 0
                    dic_site = {}
                    for free_point in free_points:
                       #i = i + 1
                       #logging.info("idx[{0}]".format(i))
                        link_uri = free_point.find_all('div',onclick=True)
                        if len(link_uri) == 1:
                            divs = free_point.find_all('div')
                            url = urllib.parse.urljoin(url_point1,link_uri[0]['onclick'].replace("window.open('",'').replace("');",''))
                            title = divs[1].text
                            dic_site[title] = url

                    for key in dic_site.keys():
                        r = s.post(dic_site[key])
                        logging.info("{0}:{1}:{2}".format(r.status_code,key,dic_site[key]))
                        if bSleep :
                            num = random.randint(sleep_min,sleep_max)
                            logging.info('sleep sec:{0}'.format(num))
                            sleep(num)
                    market_item = soup.find_all('div',{ 'class':'market_div_item'})
                    for item in market_item:
                        a = item.find_all('a')
                        item_txt = a[1].find('font').text
                        item_url = urllib.parse.urljoin(url_point1,a[1]['href'])
                        r = s.post(item_url)
                        logging.info("{0}:{1}:{2}".format(r.status_code,item_txt,item_url))
                        if bSleep :
                            num = random.randint(sleep_min,sleep_max)
                            logging.info('sleep sec:{0}'.format(num))
                            sleep(num)
                except TypeError as inst :
                    logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                    logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                except UnicodeEncodeError as inst :
                    logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                    logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                except IndexError as inst :
                    logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                    logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                except Exception as inst :
                    logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                    logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                except :
                    logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                    logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

           #if bPoint == True :
            if False:
                array_site = [
                         ['복권임'     ,19761021,'https://www.etoland.co.kr/bok.pop.php'                                       ]
                        ,['네티켓'     ,20181231,'http://www.etoland.co.kr/bbs/link.php?bo_table=point1&wr_id=3942&no=1&page=0']
                        ,['스포라이브' ,20181231,'http://www.etoland.co.kr/bbs/link.php?bo_table=point1&wr_id=3805&no=1&page=0']
                        ,['풀티비'     ,20181231,'http://www.etoland.co.kr/bbs/link.php?bo_table=point1&wr_id=3803&no=1&page=0']
                        ,['설문참여'   ,20191231,'http://www.etoland.co.kr/bbs/link.php?bo_table=point1&wr_id=4433&no=1&page=0']
                        ,['남성스타일' ,20191231,'http://www.etoland.co.kr/bbs/link.php?bo_table=point1&wr_id=4314&no=1&page=0']
                        ,['와니폰'     ,20191231,'http://www.etoland.co.kr/bbs/link.php?bo_table=point1&wr_id=4026&no=1&page=0']
                        ,['대출직거래' ,20191231,'http://www.etoland.co.kr/bbs/link.php?bo_table=point1&wr_id=4714&no=1&page=0']
                        ,['바나나몰'   ,20191231,'http://www.etoland.co.kr/bbs/link.php?bo_table=point1&wr_id=3802&no=1&page=0']
                        ];
                for site in array_site:
                    logging.info("{name}:{date}:{url}".format(name=site[0],date=site[1],url=site[2]))
                    if site[1] >= nDate:
                        r = s.post(site[2])
                        logging.info('{0} result : {1}'.format(site[0],r.status_code))
                        if bSleep :
                            num = random.randint(sleep_min,sleep_max)
                            logging.info('sleep sec:{0}'.format(num))
                            sleep(num)

            logging.info("게시판읽기")

            try :
                # 성인 용품.
                url_19ad='http://www.etoland.co.kr/bbs/board.php?bo_table=19ad'
                r = s.get(url_19ad)
                bsoap  = bs(r.text,'html.parser')
                tr_list = bsoap.findAll("tr")
                for tr in tr_list:
                    td_list = tr.find_all('td',{'mw_basic_list_datetime','mw_basic_list_subject'})
                    if(len(td_list)>1):
                        if (td_list[1].text ==  yesterday):
                            td = td_list[0].find_all('a','mw_basic_list_comment_count',href=True)
                            if(len(td)>0):
                               #url = "{0}/{1}".format('http://www.etoland.co.kr/bbs',td[0]['href'])
                                url = urllib.parse.urljoin(url_19ad,td[0]['href'])
                                logging.info("{0}:{1}".format(td_list[0].text,url))
                                r = s.get(url)
                                if(r.status_code != 200):
                                    break
                                soup = bs(r.text,'html.parser')
                                td_list = soup.find_all('td','mw_basic_view_link')
                               #print (len(td_list))
                                if( len(td_list) > 0):

                                    for td in td_list:
                                        href = td.find('a').get('href')
                                        get_url = urllib.parse.urljoin(url_19ad,href)
                                        logging.info(get_url)
                                        s.get(get_url)
                               #if bFirst2 == True:
                               #    bFirst2 = False
                               #    soup = bs(r.text,'html.parser')
                               #    forms = soup.find_all('form')

                               #    for form in forms:
                               #        if(form['name'] == 'fviewcomment'):
                               #            logging.info(form['name'])
                               #            fields = form.find_all('input')
                               #            fields += form.find_all('textarea')

                               #            formdata = dict((field.get('name'),field.get('value'))  for field in fields)
                               #            logging.info(formdata)
                               #            formdata['wr_content'] = 'wow'
                               #            logging.info(formdata)
                               #            url_post = urllib.parse.urljoin(url_19ad,form['action'])
                               #            logging.info(url_post)
                               #            r = s.post(url_post,data=formdata)
                                if bSleep :
                                    num = random.randint(sleep_min,sleep_max)
                                    logging.info('sleep sec:{0}'.format(num))
                                    sleep(num)
            except TypeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except UnicodeEncodeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except IndexError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except Exception as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except :
                logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))


            try :
                # 남성 스타일.
                url_market_style = 'http://www.etoland.co.kr/bbs/board.php?bo_table=market_style'
                r = s.get(url_market_style)
                bsoap  = bs(r.text,'html.parser')
                tr_list = bsoap.findAll("tr")
                for tr in tr_list:
                    td_list = tr.find_all('td',{'mw_basic_list_datetime','mw_basic_list_subject'})
                    if(len(td_list)>0):
                        if (td_list[1].text ==  yesterday):
                            a_list = td_list[0].find_all('a',href=True)
                            if(len(a_list)>0):
                               #url = "{0}/{1}".format('http://www.etoland.co.kr/bbs',a_list[1]['href'])
                                url = urllib.parse.urljoin(url_market_style,a_list[1]['href'])
                                span = a_list[1].find('span')
                                logging.info("{0}:{1}".format(span.text,url))
                                r = s.get(url)
                                if(r.status_code != 200):
                                    break
                                soup = bs(r.text,'html.parser')
                                td_list = soup.find_all('td','mw_basic_view_link')
                                if( len(td_list) > 0):

                                    for td in td_list:
                                        href = td.find('a').get('href')
                                        get_url = urllib.parse.urljoin(url_market_style,href)
                                        logging.info(get_url)
                                        s.get(get_url)
                               #if bFirst4 == True :
                               #    bFirst4 = False
                               #    soup = bs(r.text,'html.parser')
                               #    forms = soup.find_all('form')

                               #    for form in forms:
                               #        if(form['name'] == 'fviewcomment'):
                               #            logging.info(form['name'])
                               #            fields = form.find_all('input')
                               #            fields += form.find_all('textarea')

                               #            formdata = dict((field.get('name'),field.get('value'))  for field in fields)
                               #            logging.info(formdata)
                               #            formdata['wr_content'] = 'good'
                               #            logging.info(formdata)
                               #            url_post = urllib.parse.urljoin(url_market_style,form['action'])
                               #            logging.info(url_post)
                               #            r = s.post(url_post,data=formdata)
                                
                                if bSleep :
                                    num = random.randint(sleep_min,sleep_max)
                                    logging.info('sleep sec:{0}'.format(num))
                                    sleep(num)
            except TypeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except UnicodeEncodeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except IndexError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except Exception as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except :
                logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

            try :
                if False:
                    # 나눔이벤트
                    url_point_event = 'http://www.etoland.co.kr/bbs/board.php?bo_table=point_event'
                    r = s.get(url_point_event)
                    bsoap  = bs(r.text,'html.parser')
                    table_list = bsoap.findAll("table")
                    logging.info(len(table_list))
                    for table in table_list:
                       #logging.info(table.text)
                        tr_list = table.select('//*[@id="mw_basic"]/form[1]/table[2]/tbody/tr[1]/td[1]/table/tbody/tr[3]/td/table/tbody')
                        logging.info(tr_list)
                        for tr in tr_list:
                           #logging.info(tr)
                            td_list = tr.find_all('td',{'mw_basic_list_datetime','mw_basic_list_subject'})
                            if(len(td_list)>0):
                                logging.info("나눔")
                                logging.info(td_list[1].text)
                                if (td_list[1].text ==  yesterday):
                                    a_list = td_list[0].find_all('a',href=True)
                                    if(len(a_list)>0):
                                        url = urllib.parse.urljoin(url_point_event,a_list[1]['href'])
                                        span = a_list[1].find('span')
                                        logging.info("{0}:{1}".format(span.text,url))
                                        r = s.get(url)
                                        if(r.status_code != 200):
                                            break
                                        soup = bs(r.text,'html.parser')
                                        td_list = soup.find_all('td','mw_basic_view_link')
                                        if( len(td_list) > 0):

                                            for td in td_list:
                                                href = td.find('a').get('href')
                                                get_url = urllib.parse.urljoin(url_point_event,href)
                                                logging.info(get_url)
                                                s.get(get_url)
                                        
                                        if bSleep :
                                            num = random.randint(sleep_min,sleep_max)
                                            logging.info('sleep sec:{0}'.format(num))
                                            sleep(num)
            except TypeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except UnicodeEncodeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except IndexError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except Exception as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except :
                logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

            try :
                if False:
                    # 성인 웹툰.
                    url_19toon = 'http://www.etoland.co.kr/bbs/board.php?bo_table=19toon'
                    r = s.get(url_19toon)
                    bsoap  = bs(r.text,'html.parser')
                    tr_list = bsoap.findAll("tr")
                    for tr in tr_list:
                        td_list = tr.find_all('td',{'mw_basic_list_datetime','mw_basic_list_subject'})
                        if(len(td_list)>1):
                            if (td_list[1].text == yesterday):
                                td = td_list[0].find_all('a','mw_basic_list_comment_count',href=True)
                                if(len(td)>0):
                                   #url = "{0}/{1}".format('http://www.etoland.co.kr/bbs',td[0]['href'])
                                    url = urllib.parse.urljoin(url_19toon,td[0]['href'])
                                    logging.info("{0}:{1}".format(td_list[0].text,url))
                                    r = s.get(url)
                                    if(r.status_code != 200):
                                        break
                                   #if bFirst1 == True:
                                   #    bFirst1 = False
                                   #    soup = bs(r.text,'html.parser')
                                   #    forms = soup.find_all('form')

                                   #    for form in forms:
                                   #        if(form['name'] == 'fviewcomment'):
                                   #            logging.info(form['name'])
                                   #            fields = form.find_all('input')
                                   #            fields += form.find_all('textarea')

                                   #            formdata = dict((field.get('name'),field.get('value'))  for field in fields)
                                   #            logging.info(formdata)
                                   #            formdata['wr_content'] = 'wow'
                                   #            logging.info(formdata)
                                   #            url_post = urllib.parse.urljoin(url_19toon,form['action'])
                                   #            logging.info(url_post)
                                   #            r = s.post(url_post,data=formdata)
                                    if bSleep :
                                        num = random.randint(sleep_min,sleep_max)
                                        logging.info('sleep sec:{0}'.format(num))
                                        sleep(num)
            except TypeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except UnicodeEncodeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except IndexError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except Exception as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except :
                logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

            try :
                if False:
                    # 자동차 업체.
                    url_market_car = 'http://www.etoland.co.kr/bbs/board.php?bo_table=market_car'
                    r = s.get(url_market_car)
                    bsoap  = bs(r.text,'html.parser')
                    tr_list = bsoap.findAll("tr")
                    for tr in tr_list:
                        td_list = tr.find_all('td',{'mw_basic_list_datetime','mw_basic_list_subject'})
                        if(len(td_list)>1):
                            if (td_list[1].text ==  yesterday):
                                a_list = td_list[0].find_all('a',href=True)
                               #for alist in a_list:
                               #   #logging.info(alist)
                               #    span = alist.find('span')
                               #    if span != None:
                               #        logging.info(span.text)
                               #    logging.info("alist:{0}".format(alist['href']))
                                if(len(a_list)>0):
                                   #url = "{0}/{1}".format('http://www.etoland.co.kr/bbs',a_list[1]['href'])
                                    url = urllib.parse.urljoin(url_market_car,a_list[1]['href'])
                                    span = a_list[1].find('span')
                                    logging.info("{0}:{1}".format(span.text,url))
                                    r = s.get(url)
                                    if(r.status_code != 200):
                                        break
                                    try :
                                       #if bFirst3 == True :
                                       #    bFirst3 = False
                                       #    soup = bs(r.text,'html.parser')
                                       #    forms = soup.find_all('form')

                                       #    for form in forms:
                                       #        if(form['name'] == 'fviewcomment'):
                                       #            logging.info(form['name'])
                                       #            fields = form.find_all('input')
                                       #            fields += form.find_all('textarea')

                                       #            formdata = dict((field.get('name'),field.get('value'))  for field in fields)
                                       #            logging.info(formdata)
                                       #            formdata['wr_content'] = str('잘보았습니다.').encode('euc-kr')
                                       #            logging.info(formdata)
                                       #            url_post = urllib.parse.urljoin(url_market_car,form['action'])
                                       #            logging.info(url_post)
                                       #            r = s.post(url_post,data=formdata)
                                       #            logging.info(r.text)
                                        if bSleep :
                                            num = random.randint(sleep_min,sleep_max)
                                            logging.info('sleep sec:{0}'.format(num))
                                            sleep(num)
                                    except TypeError as inst :
                                        logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                                        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                                    except UnicodeEncodeError as inst :
                                        logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                                        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                                    except IndexError as inst :
                                        logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                                        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                                    except Exception as inst :
                                        logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                                        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                                    except :
                                        logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                                        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except TypeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except UnicodeEncodeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except IndexError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except Exception as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except :
                logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            try :
                if False:
                    # 성인포토
                    url_19board = 'http://www.etoland.co.kr/bbs/board.php?bo_table=19board'
                    r = s.get(url_19board)
                    bsoap  = bs(r.text,'html.parser')
                    tr_list = bsoap.findAll("tr")
                    for tr in tr_list:
                        td_list = tr.find_all('td',{'mw_basic_list_datetime','mw_basic_list_subject'})
                        if(len(td_list)>0):
                            logging.info(td_list[1].text)
                            if (td_list[1].text ==  yesterday):
                                a_list = td_list[0].find_all('a',href=True)
                                if(len(a_list)>0):
                                   #url = "{0}/{1}".format('http://www.etoland.co.kr/bbs',a_list[1]['href'])
                                    url = urllib.parse.urljoin(url_19board,a_list[1]['href'])
                                    
                                    span = a_list[1].find('span')
                                    logging.info("{0}:{1}".format(span.text,url))
                                    r = s.get(url)
                                    if(r.status_code != 200):
                                        break
                                   #if bFirst5 == True :
                                   #    bFirst5 = False
                                   #    soup = bs(r.text,'html.parser')
                                   #    forms = soup.find_all('form')

                                   #    for form in forms:
                                   #        if(form['name'] == 'fviewcomment'):
                                   #            logging.info(form['name'])
                                   #            fields = form.find_all('input')
                                   #            fields += form.find_all('textarea')

                                   #            formdata = dict((field.get('name'),field.get('value'))  for field in fields)
                                   #            logging.info(formdata)
                                   #            formdata['wr_content'] = str('감사합니다.').encode('euc-kr')
                                   #            logging.info(formdata)
                                   #            url_post = urllib.parse.urljoin(url_19board,form['action'])
                                   #            logging.info(url_post)
                                   #            r = s.post(url_post,data=formdata)
                                    
                                    if bSleep :
                                        num = random.randint(sleep_min,sleep_max/2)
                                        logging.info('sleep sec:{0}'.format(num))
                                        sleep(num)
            except TypeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except UnicodeEncodeError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except IndexError as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except Exception as inst :
                logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            except :
                logging.info('Unexpected error:'.format(sys.exc_info()[0]))
                logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

           #포인트 확인.
            r = s.get(url_point)
            contents = bs(r.text, 'html.parser') # Soup으로 만들어 줍시다.
            point_after = contents.find_all("b")[-1].text
            logging.info(point_after)
    
            # 텔레그램 전송.
            if bAttendance == True :
                if msg_detail is None :
                    MSG='{0}{1}'.format(point_before,point_after)
                else :
                    detail = ''
                    msg_array = msg_detail.split('\n')
                    for idx,value in enumerate(msg_array):
                        detail += '{0}{1}'.format(value,' ' if idx+1 == len(msg_array) else '\n')
                    MSG='{0}\n{1}\n{2}'.format(point_before,point_after,detail)
                telegram_bot_url='https://api.telegram.org/bot{0}{1}{2}&text={3}'.format(TOKEN,MSG_URL,CHAT_ID,MSG)
                r = s.get(telegram_bot_url)
                logging.info('텔레그램 전송 결과:%d',r.status_code)
    
    except TypeError as inst :
        logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    except UnicodeEncodeError as inst :
        logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    except IndexError as inst :
        logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    except Exception as inst :
        logging.error('type:{0},args:{1},inst:{2}'.format(type(inst),inst.args,inst))
        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    except :
        logging.info('Unexpected error:'.format(sys.exc_info()[0]))
        logging.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    finally:
        logging.info("Finished")


if __name__ == "__main__":
    bFlag = False
    if len(sys.argv) != 1 :
        bFlag = True

    func('hugh76k','qwertyu1',bFlag,1,300) 
    func('seonuny','qwertyu1',bFlag,1,300) 
