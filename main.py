from tkinter import*
import tkinter.font as Font
# import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import time
import requests
import json
import re
from datetime import date, datetime, timedelta


win = Tk()


#현재 시간, 날짜
ntime = int(time.strftime("%H"))
today = int(date.today().strftime("%Y%m%d"))
date = int (date.today().strftime("%d"))

def base_time():
    now = datetime.now()
    if now.minute < 45:
        now -= timedelta(hours=1)
    base_time = now.strftime("%H") + "00"
    # print(base_time)
    return base_time


시도교육청코드 = 'B10'
학교코드 = '7011489'
기본학년 = '1'
기본반 ='1'



# win.geometry("800x600")
win.title("데일리 학교 알리미")
win.resizable(False, False)

#폰트
font_small = Font.Font(family="페이퍼로지 2 ExtraLight", size=10)
font_sbjt = Font.Font(family="페이퍼로지 3 Light", size=13)
font_default = Font.Font(family="페이퍼로지 3 Light", size=12)
font_medium = Font.Font(family="페이퍼로지 4 regular", size=15)
font_temp = Font.Font(family="페이퍼로지 5 medium", size=25)
font_big = Font.Font(family="페이퍼로지 5 medium", size=18)

#api
key_sc = "571668b4449b4ba09ef972d847ee6022"

key_fc = "qrbUwwefTa221MMHn-2tVQ"




#급식 api
url_meal = "https://open.neis.go.kr/hub/mealServiceDietInfo"

params = {
    'KEY' : key_sc,
    'Type' : 'json',
    'pIndex' : '1',
    'pSize' : '100',
    'ATPT_OFCDC_SC_CODE' : 시도교육청코드,
    'SD_SCHUL_CODE' : 학교코드,
    'MLSV_YMD' : today
}

response_meal = requests.get(url_meal, params=params)
data = response_meal.json()
menu_list = []
if 'mealServiceDietInfo' in data:
    menu_data = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
    menu_list_data = menu_data.split('<br/>')
    for item in menu_list_data:
        menu = re.sub(r"\s*\(.*\)", "", item).strip()
        menu_list.append(menu)
else:
    menu_list =["급식 정보가 없습니다."]


print(menu_list)


#시간표 api
url_scj = "https://open.neis.go.kr/hub/hisTimetable"

subject_map = {
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

def api_sbjt(grade,sc_class):
    params_sbjt_td = {
        'KEY' : key_sc,
        'Type' : 'json',
        'pIndex' : '1',
        'pSize' : '100',
        'ATPT_OFCDC_SC_CODE' : 시도교육청코드,
        'SD_SCHUL_CODE' : 학교코드,
        'GRADE' : grade,
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
        'GRADE' : grade,
        'CLASS_NM' : sc_class,
        'TI_FROM_YMD' : today+1,
        'TI_TO_YMD' : today+1
    }

    global sbjt_td, sbjt_tm
    response_scj = requests.get(url_scj, params=params_sbjt_td)
    data_sbjt_td = response_scj.json()
    if 'hisTimetable' in data_sbjt_td:
        rows = data_sbjt_td['hisTimetable'][1]['row']
        sbjt_td = [subject_map.get(row['ITRT_CNTNT'],row['ITRT_CNTNT']) for row in rows]
    else:
        sbjt_td = ['-','-','-','-','-','-','-']
    print(sbjt_td)

    response_scj = requests.get(url_scj, params=params_sbjt_tm)
    data_sbjt_tm = response_scj.json()
    if 'hisTimetable' in data_sbjt_tm:
        rows = data_sbjt_tm['hisTimetable'][1]['row']
        sbjt_tm = [subject_map.get(row['ITRT_CNTNT'],row['ITRT_CNTNT']) for row in rows]
    else:
        sbjt_tm = ['-','-','-','-','-','-','-']
    print(sbjt_tm)

api_sbjt(1,1)



#날씨 API
url_fc = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtFcst"

base_time = base_time()

params_fc = {
    "serviceKey" : key_fc,
    "numOfRows" : "100",
    "pageNo" : "1",
    "dataType" : "XML",
    "base_date" : today,
    "base_time" : base_time,
    "nx" :"61",
    "ny" : "125"
}

response_fc = requests.get(url_fc, params=params_fc)
# data_fc = response_fc.json()
# print(data_fc)

print(response_fc.text[:500])



#색상
blue = "#007fff"

def refresh():
    pass

#메뉴
menubar = Menu(win)

menu_file = Menu(menubar, tearoff=0)
menu_file.add_command(label="refresh", command=refresh)
menu_file.add_separator()
menu_file.add_command(label="quit", command=win.quit)

menubar.add_cascade(label="File", menu=menu_file)

win.config(menu=menubar)

#다짐 엔트리 클릭 동작
def clear(event):
    ent_note.delete(0, END)
    ent_note.unbind("<Button-1>")
    ent_note.config(fg="black")

#시간 업데이트
def update_time():
    current_time = time.strftime("%H:%M:%S")
    lbl_time.config(text=current_time)
    win.after(1000, update_time)

#윗줄 프레임
frm_top = Frame(win)
frm_top.pack(fill="x", padx=30, pady=13)

#다짐 엔트리
ent_note = Entry(frm_top, width=50, font=font_default)
ent_note.pack(side="left", padx=10, pady=10, ipady=3)
ent_note.config(fg="gray")
ent_note.bind("<Button-1>", clear)
ent_note.insert(0, "오늘의 다짐")

#시간 라벨
lbl_time = Label(frm_top, font=font_medium)
lbl_time.pack(side="right", padx=10, pady=10)

#시계아이콘
img = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\시계.png")
img_resized = img.resize((35, 35), Image.LANCZOS)
img_clock = ImageTk.PhotoImage(img_resized, master=win)
lbl_clock = Label(frm_top, image=img_clock)
lbl_clock.pack(side="right")

# 구분선 프레임
frm_line = Frame(win, bg="white")
frm_line.pack(fill="x", padx=10, pady=0)

# 프레임 위쪽에 선 그리기
canvas_line = Canvas(frm_line, height=1, bg="gray", highlightthickness=0)
canvas_line.pack(side="top", fill="x")


#정보 프레임
frm_info = Frame(win, relief="solid", bd=0)
frm_info.pack(fill="x", padx=0, pady=10)

#학년 선택
grade = [1,2,3]
combox_grade = ttk.Combobox(frm_info, height=5, width=10, values=grade, state="readonly")
combox_grade.grid(row=0, column=0, padx=20, pady=15)
combox_grade.set("학년")

#반 선택
sc_class = [1,2,3,4,5]
combox_class = ttk.Combobox(frm_info, height=5, width=10, values=sc_class, state="readonly")
combox_class.grid(row=0, column=1, padx=20, pady=15)
combox_class.set("반")




#시간표 프레임
frm_scj = Frame(frm_info, relief="solid", bd=0)
frm_scj.grid(row=1, column=0, rowspan=8, columnspan=3, padx=30, pady=0)

#1교시~7교시
# frm_sbjt_time = Frame(frm_scj)
# frm_scj.grid(row=0, column=0, padx=10, pady=0)
lbl_sbjt = Label(frm_scj, text="시간표", font=font_medium, width=3)
lbl_sbjt.grid(row=0, column=0, sticky="nsew", padx=0, pady=5)
times = ["1교시", "2교시", "3교시", "4교시", "5교시", "6교시", "7교시"]
for i, t in enumerate(times):
    lbl_sbjt_time = Label(frm_scj, text=t, font=font_sbjt, width=7)
    lbl_sbjt_time.grid(row=i+1, column=0, sticky="nsew", padx=0, pady=10)


#시간표
def sbjt():
    global lbl_sbjt_td, lbl_sbjt_tm
    # frm_sbjt = Frame(frm_scj)
    # frm_scj.grid(row=0, column=1, padx=10, pady=0)
    lbl_today = Label(frm_scj, text=f"오늘({date})", font=font_medium, width=7)
    lbl_today.grid(row=0, column=1, sticky="nw", padx=10, pady=5)
    lbl_tomorrow = Label(frm_scj, text=f"내일({date+1})", font=font_medium, width=7)
    lbl_tomorrow.grid(row=0, column=2, sticky="ne", padx=10, pady=5)
    for i, t in enumerate(sbjt_td, start=1):
        lbl_sbjt_td = Label(frm_scj, text=t, font=font_sbjt, width=7)
        lbl_sbjt_td.grid(row=i, column=1, padx=5, pady=10)
    for i, t in enumerate(sbjt_tm, start=1):
        lbl_sbjt_tm = Label(frm_scj, text=t, font=font_sbjt, width=7)
        lbl_sbjt_tm.grid(row=i, column=2, padx=5, pady=10)

sbjt()

#검색
def btn_sbjt_cmd():
    api_sbjt(combox_grade.get(),combox_class.get())
    lbl_sbjt_td.destroy()
    lbl_sbjt_tm.destroy()
    sbjt()

#검색 버튼
btn_sbjt = Button(frm_info, text="검색", width=4, command=btn_sbjt_cmd)
btn_sbjt.grid(row=0,column=2, padx=20, pady=15)

#날씨 정보 프레임
frm_weather_info = Frame(frm_info)
frm_weather_info.grid(row=0, column=6, rowspan=3, sticky=E+W, padx=20, pady=5)


#온도 프레임
frm_weather = Frame(frm_weather_info)
frm_weather.grid(row=0, column=0, sticky=E+W, padx=20, pady=0)


#날씨 아이콘 경로
img_weather_sun = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\맑음.png")
img_weather_cloud = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\구름.png")
img_weather_rain = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\비.png")
img_weather_snow = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\눈.png")
img_weather_wind = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\바람.png")

#날씨 아이콘
img_weather = img_weather_snow
img_resized_weather = img_weather.resize((75, 75), Image.LANCZOS)
img_weather = ImageTk.PhotoImage(img_resized_weather, master=win)
lbl_weather = Label(frm_weather, image=img_weather)
lbl_weather.pack(side="left", padx=10, pady=10)

val_temp = "25°C"
#온도 라벨
lbl_temp = Label(frm_weather, text=val_temp, font=font_temp, fg=blue)
lbl_temp.pack(side="left", padx=10, pady=10)
lbl_ment = Label(frm_weather, text="우산을 챙기세요", font=font_default)
lbl_ment.pack(side="left", padx=10, pady=10)

#날씨 예보 부모 프레임
frm_forecast_container = Frame(frm_weather_info)
frm_forecast_container.grid(row=6, column=0, rowspan=4, sticky=E+W, padx=10, pady=10)

#날씨 예보 캔버스
canvas_forecast = Canvas(frm_forecast_container, height=100)
canvas_forecast.pack(side="top", fill="both", expand=True)

#날씨 예보 스크롤바
scrollbar_forecast = ttk.Scrollbar(frm_forecast_container, orient="horizontal", command=canvas_forecast.xview)
scrollbar_forecast.pack(side="bottom", fill="x")
canvas_forecast.configure(xscrollcommand=scrollbar_forecast.set)

#날씨 예보 프레임
frm_forecast = Frame(canvas_forecast)
canvas_forecast.create_window((0, 0), window=frm_forecast, anchor="nw")

def update_forecast_scrollregion(event):
    canvas_forecast.config(scrollregion=canvas_forecast.bbox("all"))

frm_forecast.bind("<Configure>", update_forecast_scrollregion)


img_weather_forecast = [img_weather_sun, img_weather_cloud, img_weather_rain, img_weather_snow, img_weather_wind]

for i in range(1, 13):
    if i+ntime <= 24:
        lbl_forecast = Label(frm_forecast, text=f"{i+ntime}시", font=font_small, width=6)
    else:
        lbl_forecast = Label(frm_forecast, text=f"{i+ntime-24}시", font=font_small, width=6)
    lbl_forecast.grid(row=0, column=i-1, padx=0, pady=5)
    
    img_resized = img_weather_forecast[i % 5].resize((30, 30), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized, master=win)
    img_weather_forecast.append(img_tk)  # 참조 유지
    
    lbl_forecast_img = Label(frm_forecast, image=img_tk)
    lbl_forecast_img.grid(row=1, column=i-1, padx=0, pady=5)
    
    lbl_forecast_temp = Label(frm_forecast, text="25°C", font=font_small)
    lbl_forecast_temp.grid(row=2, column=i-1, padx=0, pady=5)




#급식 프레임
frm_meal = Frame(frm_info, relief="solid", bd=0)
frm_meal.grid(row=3, column=6, sticky=E+W, padx=20, pady=0)

#급식 아이콘
img_meal = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\급식.png")
img_resized_meal = img_meal.resize((55,55), Image.LANCZOS)
img_meal=ImageTk.PhotoImage(img_resized_meal, master= win)
lbl_meal_img= Label(frm_meal, image=img_meal)
lbl_meal_img.pack(side="left", padx=10, pady=5)

#급식 라벨
lbl_meal = Label(frm_meal, text="급식", font=font_big)
lbl_meal.pack(side="left")

#급식 메뉴 프레임
frm_menu = Frame(frm_info)
frm_menu.grid(row=4, column=6, sticky=E+W, padx=20, pady=0)

#급식 메뉴
lbl_menu = Label(frm_menu, text=menu_list[0:3], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)
lbl_menu = Label(frm_menu, text=menu_list[3:6], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)
lbl_menu = Label(frm_menu, text=menu_list[6:], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)


#개인 프레임
frm_user = Frame(win, relief="solid", bd=2)
frm_user.pack(side="top", fill="x", padx=10, pady=0)

#메모 프레임
frm_memo = Frame(frm_user)
frm_memo.pack(side="left", padx=10, pady=20)

txt_memo = Text(frm_memo, width=30, height=10, font=font_default)
txt_memo.pack(padx=10, pady=10)

def clear_todo(event):
    ent_todo.delete(0, END)
    ent_todo.unbind("<Button-1>")
    ent_todo.config(fg="black")

#할일 추가 엔트리
ent_todo = Entry(frm_user, width=20, font=font_default)
ent_todo.pack(side="top", padx=10, pady=10, ipady=3)
ent_todo.config(fg="gray")
ent_todo.insert(0, "할 일 (enter로 추가)")
ent_todo.bind("<Button-1>", clear_todo)


# 할일 부모 프레임
frm_todo_container = Frame(frm_user, relief="sunken", bd=3)
frm_todo_container.pack(side="right", padx=20, pady=0)

# 할일 캔버스
canvas_todo = Canvas(frm_todo_container, width=210, height=200)
canvas_todo.pack(side="left", fill="y", expand=True)

# 할일 스크롤바
scrollbar_todo = ttk.Scrollbar(frm_todo_container, orient="vertical", command=canvas_todo.yview)
scrollbar_todo.pack(side="right", fill="y")

canvas_todo.configure(yscrollcommand=scrollbar_todo.set)
canvas_todo.bind("<Configure>", lambda e: canvas_todo.configure(scrollregion=canvas_todo.bbox("all")))

# 할일 프레임
frm_todo = Frame(canvas_todo, width=230, height=200, bg="white")
canvas_todo.create_window((0,0), window=frm_todo, anchor="nw")

# 할일
todo_list = []

def add_todo(event):
    todo = ent_todo.get()
    if todo and todo != "할 일 (enter로 추가)":
        todo_list.append(todo)
        chkb_todo = Checkbutton(frm_todo, text=todo, font=font_default)
        chkb_todo.pack(anchor="w", padx=10, pady=5)
        ent_todo.delete(0, END)
        
        canvas_todo.update_idletasks()
        canvas_todo.configure(scrollregion=canvas_todo.bbox("all"))
        canvas_todo.yview_moveto(1) # 스크롤을 맨 아래로 이동


ent_todo.bind("<Return>", add_todo)



update_time()

win.mainloop()