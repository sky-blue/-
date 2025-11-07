from tkinter import*
from datetime import date, datetime, timedelta
from PIL import Image, ImageTk
import requests
import re
import tkinter.font as Font
import time


win = Tk()
win.title('데일리 학교 알리미')
win.resizable(False,False)


#변수
blue = "#007fff"
DKSH = '#164e93'
today = int(date.today().strftime("%Y%m%d"))

cur_hour = int(time.strftime('%H'))

font_small = Font.Font(family="페이퍼로지 2 ExtraLight", size=10)
font_default = Font.Font(family="페이퍼로지 3 Light", size=12)
font_medium = Font.Font(family="페이퍼로지 4 regular", size=15)
font_big = Font.Font(family="페이퍼로지 5 medium", size=25)



#---API---#

#KEYs
key_sc = '571668b4449b4ba09ef972d847ee6022'

#학교 변수
시도교육청코드 = 'B10'
학교코드 = '7011489'
기본학년 = '1'
기본반 = '1'


#급식 API
url_menu = 'https://open.neis.go.kr/hub/mealServiceDietInfo'

params_menu = {
    'KEY' : key_sc,
    'Type' : 'json',
    'pIndex' : '1',
    'pSize' : '100',
    'ATPT_OFCDC_SC_CODE' : 시도교육청코드,
    'SD_SCHUL_CODE' : 학교코드,
    'MLSV_YMD' : today
}


def menu():
    menulist = []

    response_menu = requests.get(url_menu,params=params_menu)
    data_menu = response_menu.json()

    if 'mealServiceDietInfo' in data_menu:
        menudata = data_menu['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        menulistdata = menudata.split('<br/>')
        for item in menulistdata:
            menu = re.sub(r'\s*\(.*\)', '', item)
            menulist.append(menu)
    else:
        menulist = ['급식정보가 없습니다.']

    print(menulist)

menu()


#시간표 API
url_sbjt = "https://open.neis.go.kr/hub/hisTimetable"

sbjt_map = {
    "인공지능 수학": "인수",
    "진로와 직업": "직업",
    "진로활동" : "진로",
    "컴퓨터 구조" : "컴구",
    "공통국어2" : "국어",
    "공통수학2" : "수학",
    "정보 통신" : "정통",
    "공통영어2" : "영어",
    "토익연습일반" : "토익",
    "임베디드 소프트웨어 공학" : "임네",
    "공업수학의 기초" : "공수",
    "공업 일반" : "공일",
    "자료 구조" : "자구",
    "수학Ⅱ" : "수Ⅱ",
    "영어Ⅱ" : "영 Ⅱ",
    "데이터과학과 머신러닝" : "빅데",
    "4차 산업혁명과 윤리" : "윤리",
    "성공적인 직업생활" : "성직",
    "운영체제" : "운체",
    "물리학Ⅰ" : "물 Ⅰ",
    "봉사활동" : "자율",
    "알고리즘" : "알고",
    "자율·자치활동" : "창독",
    "자율활동" : "창독",
    "스포츠 생활" : "스생",
    "토익연습실무" : "토익",
    "통합사회2" : "통사",
    "* 프로그래밍 언어 활용" : "응프",
    "체육2" : "체육",
    "통합과학2" : "통과",
    "음악 감상과 비평" : "음악",
    "* 시스템SW 운영관리" : "시프",
    "실무국어" : "실국",
    "한국사" : "한국",
    "확률과 통계" : "확통",
    "영어회화": "영회",
    "한국지리": "한지",
    "동아리활동" : "창체"
}

def sbjt(sc_grade,sc_class):
    params_sbjt_td = {
        'KEY' : key_sc,
        'Type' : 'json',
        'pIndex' : '1',
        'pSize' : '100',
        'ATPT_OFCDC_SC_CODE' : 시도교육청코드,
        'SD_SCHUL_CODE' : 학교코드,
        'GRADE' : sc_grade,
        'CLASS_NM' :sc_class,
        'TI_FROM_YMD' : today,
        'TI_TO_YMD' : today
        }

    params_sbjt_tm = {
        'KEY' : key_sc,
        'Type' : 'json',
        'pIndex' : '1',
        'pSize' : '100',
        'ATPT_OFCDC_SC_CODE' : 시도교육청코드,
        'SD_SCHUL_CODE' : 학교코드,
        'GRADE' : sc_grade,
        'CLASS_NM' : sc_class,
        'TI_FROM_YMD' : today+1,
        'TI_TO_YMD' : today+1
        }

    global sbjt_td,sbjt_tm

    response_sbjt_td = requests.get(url_sbjt,params=params_sbjt_td)
    data_sbjt_td = response_sbjt_td.json()

    if 'hisTimetable' in data_sbjt_td:
        rows = data_sbjt_td['hisTimetable'][1]['row']
        sbjt_td = [sbjt_map.get(row['ITRT_CNTNT'],row['ITRT_CNTNT'])for row in rows]
    else:
        sbjt_td = ['-','-','-','-','-','-','-']
    print(sbjt_td)

    response_sbjt_tm = requests.get(url_sbjt,params=params_sbjt_tm)
    data_sbjt_tm = response_sbjt_tm.json()

    if 'hisTimetable' in data_sbjt_tm:
        rows = data_sbjt_tm['hisTimetable'][1]['row']
        sbjt_tm = [sbjt_map.get(row['ITRT_CNTNT'],row['ITRT_CNTNT'])for row in rows]
    else:
        sbjt_tm = ['-','-','-','-','-','-','-']
    print(sbjt_tm)

sbjt(기본학년,기본반)



#날씨 API
url_fc = "https://api.open-meteo.com/v1/forecast"
params_fc = {
    "latitude": 37.4956,
    "longitude":127.0577,
    "hourly": "temperature_2m,weathercode,relative_humidity_2m",
    "timezone": "Asia/Seoul",
    "forecast_days": 2,
}

response_fc = requests.get(url_fc,params_fc)
data_fc = response_fc.json()
print(data_fc)
fc = data_fc['hourly']

#현재날시
temp = str(fc['temperature_2m'][cur_hour])+"°C"
hum = str(fc['relative_humidity_2m'][cur_hour])+"%"

def weather(code):
    if code == 0:
        return 0 #맑음
    elif code in [1, 2, 3]:
        return 1 #구름
    elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82 ,95, 96, 99]:
        return 2 #비
    elif code in [71, 73, 75, 77, 85, 86]:
        return 3 #눈





#---화면구성---#

#로고
img_DKSH = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\단대소고.png")
width_D = int(img_DKSH.width*0.1)
hight_D = int(img_DKSH.height*0.1)
img_resize_DKSH = img_DKSH.resize((width_D,hight_D), Image.LANCZOS)
img_DKSH2 = ImageTk.PhotoImage(img_resize_DKSH, master=win)
lbl_DKSH = Label(win, image=img_DKSH2)
lbl_DKSH.pack(side='left', padx=10, pady=10)


#다짐 엔트리
def clear_note(event):
    ent_note.delete(0,END)
    ent_note.unbind("<Button-1>")
    ent_note.config(fg="black")

ent_note = Entry(win, width=40, font=font_default)
ent_note.pack(side='left', padx=10, pady=10, ipady=3)
ent_note.config(fg="gray")
ent_note.bind("<Button-1>", clear_note)
ent_note.insert(0, "오늘의 다짐")


#시간 라벨
def update_time():
    cur_time = time.strftime("%H:%M:%S")
    lbl_time.config(text=cur_time)
    win.after(100, update_time)

lbl_time = Label(win, text="", font=font_medium)
lbl_time.pack(side='left', padx=10, pady=10)



update_time()

win.mainloop()