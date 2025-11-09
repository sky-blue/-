from tkinter import*
from datetime import date, datetime, timedelta
from PIL import Image, ImageTk
import requests
import re
import tkinter.font as Font
import tkinter.ttk as ttk
import time


win = Tk()
win.title('데일리 학교 알리미')
win.resizable(False,False)


#변수
blue = "#007fff"
DKSH = '#164e93'

today = int(date.today().strftime("%Y%m%d"))
date = int(date.today().strftime('%d'))
cur_hour = int(time.strftime('%H'))

font_small = Font.Font(family="페이퍼로지 2 ExtraLight", size=10)
font_default = Font.Font(family="페이퍼로지 3 Light", size=12)
font_scj = Font.Font(family="페이퍼로지 3 Light", size=13)
font_medium = Font.Font(family="페이퍼로지 4 regular", size=15)
font_meal = Font.Font(family="페이퍼로지 5 medium", size=18)
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


def api_menu():
    global menulist
    menulist = []

    response_menu = requests.get(url_menu,params=params_menu)
    data_menu = response_menu.json()

    if 'mealServiceDietInfo' in data_menu:
        menudata = data_menu['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        menulistdata = menudata.split('<br/>')
        for item in menulistdata:
            menu = re.sub(r'\s*\(.*\)', '', item).strip()
            menulist.append(menu)
    else:
        menulist = ['급식정보가 없습니다.']

    print(menulist)

api_menu()


#시간표 API
url_scj = "https://open.neis.go.kr/hub/hisTimetable"

scj_map = {
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

def api_scj(sc_grade,sc_class):
    params_scj_td = {
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

    params_scj_tm = {
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

    global scj_td,scj_tm

    response_scj_td = requests.get(url_scj,params=params_scj_td)
    data_scj_td = response_scj_td.json()

    if 'hisTimetable' in data_scj_td:
        rows = data_scj_td['hisTimetable'][1]['row']
        scj_td = [scj_map.get(row['ITRT_CNTNT'],row['ITRT_CNTNT'])for row in rows]
    else:
        scj_td = ['-','-','-','-','-','-','-']
    print(scj_td)

    response_scj_tm = requests.get(url_scj,params=params_scj_tm)
    data_scj_tm = response_scj_tm.json()

    if 'hisTimetable' in data_scj_tm:
        rows = data_scj_tm['hisTimetable'][1]['row']
        scj_tm = [scj_map.get(row['ITRT_CNTNT'],row['ITRT_CNTNT'])for row in rows]
    else:
        scj_tm = ['-','-','-','-','-','-','-']
    print(scj_tm)

api_scj(기본학년,기본반)



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
fc = data_fc['hourly']

print(fc['temperature_2m'])
print(fc['relative_humidity_2m'])

#현재날시
temp = str(fc['temperature_2m'][cur_hour])+"°C"
hum = str(fc['relative_humidity_2m'][cur_hour])+"%"

def weather_code(code):
    if code == 0:
        return 0 #맑음
    elif code in [1, 2, 3]:
        return 1 #구름
    elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82 ,95, 96, 99]:
        return 2 #비
    elif code in [71, 73, 75, 77, 85, 86]:
        return 3 #눈





#---화면구성---#

frm_top = Frame(win)
frm_top.pack(fill='x', padx=30, pady=10)

#로고
img_DKSH = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\단대소고.png")
width_D = int(img_DKSH.width*0.1)
hight_D = int(img_DKSH.height*0.1)
img_DKSH_rsize = img_DKSH.resize((width_D,hight_D), Image.LANCZOS)
img_DKSH = ImageTk.PhotoImage(img_DKSH_rsize, master=win)
lbl_DKSH_img = Label(frm_top, image=img_DKSH)
lbl_DKSH_img.pack(side='left', padx=10, pady=10)


#다짐 엔트리
def clear_note(event):
    ent_note.delete(0,END)
    ent_note.unbind("<Button-1>")
    ent_note.config(fg="black")

ent_note = Entry(frm_top, width=40, font=font_default)
ent_note.pack(side='left', padx=10, pady=10, ipady=3)
ent_note.config(fg="gray")
ent_note.bind("<Button-1>", clear_note)
ent_note.insert(0, "오늘의 다짐")


#시계
def update_time():
    cur_time = time.strftime("%H:%M:%S")
    lbl_time.config(text=cur_time)
    win.after(100, update_time)

lbl_time = Label(frm_top, text="", font=font_medium)
lbl_time.pack(side='right', padx=10, pady=10)

img_clock = Image.open(r'D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\시계.png')
img_clock_rsize = img_clock.resize((35,35), Image.LANCZOS)
img_clock = ImageTk.PhotoImage(img_clock_rsize, master=win)
lbl_clock_img = Label(frm_top, image=img_clock)
lbl_clock_img.pack(side='right', padx=10, pady=10)

#구분선
def line():
    frm_line = Frame(win)
    frm_line.pack(fill='x', padx=15)
    cnv_line = Canvas(frm_line, height=1, bg='gray')
    cnv_line.pack(side='top', fill='x')

line()



#정보 프레임
frm_info = Frame(win)
frm_info.pack(fill='x', pady=10)

#시간표 업뎃 프레임
frm_scj_update = Frame(frm_info)
frm_scj_update.grid(row=0, column=0, columnspan=3, sticky='ew', padx=40, pady=10)

#학년선택
scj_grade = [1,2,3]
comb_grade = ttk.Combobox(frm_scj_update, height=5, width=10, values=scj_grade, state='readonly')
comb_grade.grid(row=0, column=0, padx=5, pady=5)
comb_grade.set('학년')

#반선택
scj_class = [1,2,3,4,5]
comb_class = ttk.Combobox(frm_scj_update, height=5, width=10, values=scj_class, state='readonly')
comb_class.grid(row=0, column=2, padx=5, pady=5)
comb_class.set('반')

#시간표
frm_scj = Frame(frm_info)
frm_scj.grid(row=1, column=0, rowspan=7, columnspan=3, sticky='ew', padx=(30,50))

lbl_scj = Label(frm_scj, text='시간표', font=font_medium, width=4)
lbl_scj.grid(row=0, column=0, sticky='ewsn', pady=5)

lbl_td = Label(frm_scj, text=f'오늘({date})', font=font_medium, width=7)
lbl_td.grid(row=0, column=1, padx=10, pady=5)
lbl_tm = Label(frm_scj, text=f'오늘({date+1})', font=font_medium, width=7)
lbl_tm.grid(row=0, column=2, padx=10, pady=5)

for i in range(1,8):
    lbl_scj_time = Label(frm_scj, text=f'{i}교시', font=font_scj, width=7)
    lbl_scj_time.grid(row=i, column=0, sticky='ewsn', pady=10)

def scj():
    global lbl_scj_td, lbl_scj_tm
    for i,t in enumerate(scj_td, start=1):
        lbl_scj_td = Label(frm_scj, text=t, font=font_scj, width=7)
        lbl_scj_td.grid(row= i, column=1, padx=5, pady=10)
    for i,t in enumerate(scj_tm, start=1):
        lbl_scj_tm = Label(frm_scj, text=t, font=font_scj, width=7)
        lbl_scj_tm.grid(row=i, column=2, padx=5, pady=10)

scj()


#시간표 검색
def update_scj():
    api_scj(comb_grade.get(), comb_class.get())
    lbl_scj_td.destroy()
    lbl_scj_tm.destroy()
    scj()

btn_scj = Button(frm_scj_update, text='검색', width=4, command=update_scj)
btn_scj.grid(row=0, column=3, padx=5, pady=5)



#날씨 프레임
frm_fc_info = Frame(frm_info)
frm_fc_info.grid(row=0, column=4, rowspan=3, sticky='ew', padx=(40,20), pady=5)

#온도 프레임
frm_weather = Frame(frm_fc_info)
frm_weather.grid(row=0, column=0, sticky='ew')

#날씨 아이콘 경로
img_weather_sun = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\맑음.png")
img_weather_moon = Image.open(r'D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\달.png')
img_weather_cloud = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\구름.png")
img_weather_rain = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\비.png")
img_weather_snow = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\눈.png")

#날씨 아이콘
code_weather = weather_code(fc['weathercode'][cur_hour])
if code_weather == 0:
    if 20 < cur_hour or cur_hour < 6:
        img_weather = img_weather_moon #달
    else:
        img_weather = img_weather_sun # 맑음
elif code_weather == 1:
    img_weather = img_weather_cloud # 구름
elif code_weather == 2:
    img_weather = img_weather_rain # 비
elif code_weather == 3:
    img_weather = img_weather_snow # 눈

img_weather_rsize = img_weather.resize((75,75), Image.LANCZOS)
img_weather = ImageTk.PhotoImage(img_weather_rsize, master=win)
lbl_weather_img = Label(frm_weather, image=img_weather)
lbl_weather_img.pack(side='left', padx=10, pady=10)

#온습도 라벨
lbl_temp = Label(frm_weather, text=temp, font=font_big, fg=blue)
lbl_temp.pack(side='left', padx=10, pady=10)

lbl_hum = Label(frm_weather, text=hum, font=font_small)
lbl_hum.pack(side='left', padx=10, pady=10)

#날씨 예보 부모 프레임
frm_fc_container = Frame(frm_fc_info)
frm_fc_container.grid(row=1, column=0, sticky='ew', pady=10)

#날씨 예보 캔버스
canv_fc = Canvas(frm_fc_container, height=100)
canv_fc.pack(side='top', fill='both')

#날씨 예보 스크롤바
scrbar_fc = ttk.Scrollbar(frm_fc_container, orient='horizontal', command=canv_fc.xview)
scrbar_fc.pack(side='bottom', fill='x')
canv_fc.config(xscrollcommand=scrbar_fc.set)

#날씨 예보 프레임
frm_fc = Frame(canv_fc)
canv_fc.create_window((0,0), window=frm_fc, anchor='nw')

def update_scrbar_fc(event):
    canv_fc.config(scrollregion=canv_fc.bbox('all'))

frm_fc.bind('<Configure>', update_scrbar_fc)

#날씨 예보 아이콘
img_weather_fc = []
for i in range(1,13):
    code_fc = weather_code(fc['weathercode'][cur_hour+i])
    hour = (cur_hour+i) % 24
    if code_fc == 0:
        if 20 < hour or hour < 6:
            img_weather_fc.append(img_weather_moon) #달
        else:
            img_weather_fc.append(img_weather_sun) # 맑음
    elif code_fc == 1:
        img_weather_fc.append(img_weather_cloud) # 구름
    elif code_fc == 2:
        img_weather_fc.append(img_weather_rain) # 비
    elif code_fc == 3:
        img_weather_fc.append(img_weather_snow) # 눈

for i in range(12):
    hour = (cur_hour+i+1) % 24
    lbl_fc = Label(frm_fc, text=f'{hour}시', font=font_small, width=6)
    lbl_fc.grid(row=0, column=i, pady=5)

    img_fc_rsize = img_weather_fc[i].resize((30,30), Image.LANCZOS)
    img_fc = ImageTk.PhotoImage(img_fc_rsize, master=win)
    
    lbl_fc_img = Label(frm_fc, image=img_fc)
    lbl_fc_img.image = img_fc
    lbl_fc_img.grid(row=1, column=i, pady=5)

    fc_temp = str(fc['temperature_2m'][cur_hour+i]) + "°C"
    lbl_fc_temp = Label(frm_fc, text=fc_temp, font=font_small)
    lbl_fc_temp.grid(row=2, column=i, pady=5)



#급식 프레임
frm_meal = Frame(frm_info)
frm_meal.grid(row=4, column=4, sticky='ew', padx=(40,20))

#급식 아이콘
img_meal = Image.open(r'D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\급식.png')
img_meal_rsize = img_meal.resize((55,55), Image.LANCZOS)
img_meal = ImageTk.PhotoImage(img_meal_rsize, master=win)
lbl_meal_img = Label(frm_meal, image=img_meal)
lbl_meal_img.pack(side='left', padx=10, pady=5)

lbl_meal = Label(frm_meal, text='급식', font=font_meal)
lbl_meal.pack(side='left')

#급식메뉴 프레임
frm_menu = Frame(frm_info)
frm_menu.grid(row=5, column=4, sticky='ew', padx=(40,20))

lbl_menu = Label(frm_menu, text=menulist[0:3], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)
lbl_menu = Label(frm_menu, text=menulist[3:6], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)
lbl_menu = Label(frm_menu, text=menulist[6:], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)


#구분선
line()


#개인 프레임
frm_user = Frame(win)
frm_user.pack(side='top', fill='x', padx=10)

#메모 프레임
frm_memo = Frame(frm_user)
frm_memo.grid(row=0, column=0, rowspan=10, padx=30, pady=20)

#메모
txt_memo = Text(frm_memo, height=12, width=35, font=font_default, wrap='word')
txt_memo.pack(side='left', fill='both')

#메모 스크롤바
scrbar_memo = ttk.Scrollbar(frm_memo, command=txt_memo.yview)
scrbar_memo.pack(side='right', fill='y')

txt_memo.config(yscrollcommand=scrbar_memo.set)




#할일 추가 엔트리
def clear_todo(event):
    ent_todo.delete(0, END)
    ent_todo.unbind('<Button-1>')
    ent_todo.config(fg='black')

ent_todo = Entry(frm_user, font=font_default)
ent_todo.grid(row=0, column=1, sticky='ew', padx=30, pady=(10,20), ipadx=3)
ent_todo.config(fg='gray')
ent_todo.insert(0, '할 일 (enter로 추가)')
ent_todo.bind('<Button-1>', clear_todo)


#할일 부모 프레임


update_time()

win.mainloop()
