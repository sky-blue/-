from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as Font
from datetime import date
from PIL import Image, ImageTk
import requests
import time
import json
import re
import os


# 상대 경로
base_path = os.path.dirname(__file__)  # main.py 위치
img_folder = os.path.join(base_path, "아이콘")

# 창 설정
win = Tk()
win.title("데일리 학교 알리미")
win.resizable(False,False) # 창 크기 변경 불가

icon_path = os.path.join(img_folder, "아이콘.png") # 창 아이콘
icon = PhotoImage(file=icon_path)
win.iconphoto(True, icon)



# 파일 불러오기
save_file = "user_data.json"

def load_data():
    try:
        with open(save_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "date" : None,
            "note" : "오늘의 다짐",
            "grade" : 1,
            "class" : 1,
            "memo" : ""

        }
    
loaded = load_data()



# 변수
blue = "#007fff"

today = int(date.today().strftime("%Y%m%d"))
today_date = int(date.today().strftime("%d"))
cur_hour = int(time.strftime("%H"))

font_small = Font.Font(family="페이퍼로지 2 ExtraLight", size=11)
font_default = Font.Font(family="페이퍼로지 3 Light", size=12)
font_scj = Font.Font(family="페이퍼로지 3 Light", size=13)
font_medium = Font.Font(family="페이퍼로지 4 regular", size=15)
font_meal = Font.Font(family="페이퍼로지 5 medium", size=19)
font_big = Font.Font(family="페이퍼로지 5 medium", size=26)


if loaded["date"] == today:
    note = loaded["note"]
else:
    note = "오늘의 다짐"
sc_grade = loaded["grade"]
sc_class = loaded["class"]
memo = loaded["memo"]






# ---API--- # 

# KEYs
key_sc = "571668b4449b4ba09ef972d847ee6022"

# 학교 변수
시도교육청코드 = "B10"
학교코드 = "7011489"


# 시간표 API
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
    "컴퓨터 네트워크" : "임네",   # <-- ?? 다른 과목인데 같은 이름
    "데이터과학과 머신러닝" : "빅데",
    "* 빅데이터 분석 결과 시각화" : "빅데",  # <-- ?? 
    "* 탐색적 데이터 분석" : "빅데",   # <-- ???
    "공업수학의 기초" : "공수",
    "공업 일반" : "공일",
    "자료 구조" : "자구",
    "수학Ⅱ" : "수Ⅱ",
    "영어Ⅱ" : "영 Ⅱ",
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
    def scj_params(date):
        return{
        "KEY" : key_sc,
        "Type" : "json",
        "pIndex" : "1",
        "pSize" : "100",
        "ATPT_OFCDC_SC_CODE" : 시도교육청코드,
        "SD_SCHUL_CODE" : 학교코드,
        "GRADE" : sc_grade,
        "CLASS_NM" :sc_class,
        "TI_FROM_YMD" : date,
        "TI_TO_YMD" : date
        }
    params_scj_td = scj_params(today)

    params_scj_tm = scj_params(today+1)

    global scj_td, scj_tm

    response_scj_td = requests.get(url_scj,params=params_scj_td)
    data_scj_td = response_scj_td.json()

    response_scj_tm = requests.get(url_scj,params=params_scj_tm)
    data_scj_tm = response_scj_tm.json()

    def scjdata(data_scj):
        if "hisTimetable" in data_scj:
            rows = data_scj["hisTimetable"][1]["row"]
            return [scj_map.get(row["ITRT_CNTNT"],row["ITRT_CNTNT"])for row in rows]
        else:
            return ["-","-","-","-","-","-","-"]

    scj_td = scjdata(data_scj_td)

    scj_tm = scjdata(data_scj_tm)

api_scj(sc_grade, sc_class)




# 날씨 API
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
fc = data_fc["hourly"]


# 현재날시
temp = str(fc["temperature_2m"][cur_hour])+"°C"
hum = str(fc["relative_humidity_2m"][cur_hour])+"%"

def weather_code(code):
    if code == 0:
        return 0 # 맑음
    elif code in [1, 2, 3]:
        return 1 # 구름
    elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82 ,95, 96, 99]:
        return 2 # 비
    elif code in [71, 73, 75, 77, 85, 86]:
        return 3 # 눈




# 급식 API
url_menu = "https://open.neis.go.kr/hub/mealServiceDietInfo"

params_menu = {
    "KEY" : key_sc,
    "Type" : "json",
    "pIndex" : "1",
    "pSize" : "100",
    "ATPT_OFCDC_SC_CODE" : 시도교육청코드,
    "SD_SCHUL_CODE" : 학교코드,
    "MLSV_YMD" : today
}


def api_menu():
    global menulist
    menulist = []

    response_menu = requests.get(url_menu,params=params_menu)
    data_menu = response_menu.json()

    if "mealServiceDietInfo" in data_menu:
        menudata = data_menu["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        menulistdata = menudata.split("<br/>")
        for item in menulistdata:
            menu = re.sub(r"\s*\(.*\)", "", item).strip()
            menulist.append(menu)
    else:
        menulist = ["급식정보가 없습니다."]


api_menu()





# ---화면구성---# 
frm_top = Frame(win)
frm_top.pack(fill="x", padx=30, pady=10)


# 로고
img_DKSH_path = os.path.join(img_folder, "단대소고.png")
img_DKSH = Image.open(img_DKSH_path)
width_D = int(img_DKSH.width*0.1)
hight_D = int(img_DKSH.height*0.1)
img_DKSH_rsize = img_DKSH.resize((width_D,hight_D), Image.LANCZOS)
img_DKSH = ImageTk.PhotoImage(img_DKSH_rsize, master=win)
lbl_DKSH_img = Label(frm_top, image=img_DKSH)
lbl_DKSH_img.pack(side="left", padx=10, pady=10)


# 다짐 엔트리
def clear_note(event):
    ent_note.delete(0,END)
    ent_note.unbind("<Button-1>")
    ent_note.config(fg="black")

ent_note = Entry(frm_top, width=40, font=font_default)
ent_note.pack(side="left", padx=10, pady=10, ipady=3)
if note == "오늘의 다짐":
    ent_note.config(fg="gray")
    ent_note.bind("<Button-1>", clear_note)
ent_note.insert(0, note)


# 시계
def update_time():
    cur_time = time.strftime("%H:%M:%S")
    lbl_time.config(text=cur_time)
    win.after(100, update_time)

lbl_time = Label(frm_top, text="", font=font_medium)
lbl_time.pack(side="right", padx=10, pady=10)

img_clock_path = os.path.join(img_folder, "시계.png")
img_clock = Image.open(img_clock_path)
img_clock_rsize = img_clock.resize((35,35), Image.LANCZOS)
img_clock = ImageTk.PhotoImage(img_clock_rsize, master=win)
lbl_clock_img = Label(frm_top, image=img_clock)
lbl_clock_img.pack(side="right", padx=10, pady=10)

# 구분선
def line():
    frm_line = Frame(win)
    frm_line.pack(fill="x", padx=15)
    cnv_line = Canvas(frm_line, height=1, bg="gray")
    cnv_line.pack(side="top", fill="x")

line()



# 정보 프레임
frm_info = Frame(win)
frm_info.pack(fill="x", pady=10)

# 시간표 업뎃 프레임
frm_scj_update = Frame(frm_info)
frm_scj_update.grid(row=0, column=0, columnspan=3, sticky="ew", padx=40, pady=10)

# 학년선택
comb_grade = ttk.Combobox(frm_scj_update, height=5, width=10, values=list(range(1,4)), state="readonly")
comb_grade.grid(row=0, column=0, padx=5, pady=5)
comb_grade.set(sc_grade)

# 반선택
comb_class = ttk.Combobox(frm_scj_update, height=5, width=10, values=list(range(1,6)), state="readonly")
comb_class.grid(row=0, column=2, padx=5, pady=5)
comb_class.set(sc_class)

# 시간표
frm_scj = Frame(frm_info)
frm_scj.grid(row=1, column=0, rowspan=7, columnspan=3, sticky="ew", padx=(30,50))

lbl_scj = Label(frm_scj, text="시간표", font=font_medium, width=4)
lbl_scj.grid(row=0, column=0, sticky="ewsn", pady=5)

lbl_td = Label(frm_scj, text=f"오늘({today_date})", font=font_medium, width=7)
lbl_td.grid(row=0, column=1, padx=10, pady=5)
lbl_tm = Label(frm_scj, text=f"내일({today_date+1})", font=font_medium, width=7)
lbl_tm.grid(row=0, column=2, padx=10, pady=5)

for i in range(1,8):
    lbl_scj_time = Label(frm_scj, text=f"{i}교시", font=font_scj, width=7)
    lbl_scj_time.grid(row=i, column=0, sticky="ewsn", pady=10)

def scj():
    global lbl_scj_td_list, lbl_scj_tm_list
    lbl_scj_td_list, lbl_scj_tm_list = [], []
    for i,t in enumerate(scj_td, start=1):
        lbl_scj_td = Label(frm_scj, text=t, font=font_scj, width=7)
        lbl_scj_td.grid(row= i, column=1, padx=5, pady=10)
        lbl_scj_td_list.append(lbl_scj_td)
    for i,t in enumerate(scj_tm, start=1):
        lbl_scj_tm = Label(frm_scj, text=t, font=font_scj, width=7)
        lbl_scj_tm.grid(row=i, column=2, padx=5, pady=10)
        lbl_scj_tm_list.append(lbl_scj_tm)

scj()


# 시간표 검색
def update_scj():
    scj_class = comb_class.get()
    scj_grade = comb_grade.get()

    api_scj(int(scj_grade), int(scj_class))

    for lbl in lbl_scj_td_list:
        lbl.destroy()
    for lbl in lbl_scj_tm_list:
        lbl.destroy()
    scj()



btn_scj = Button(frm_scj_update, text="검색", width=4, command=update_scj)
btn_scj.grid(row=0, column=3, padx=5, pady=5)



# 날씨 프레임
frm_fc_info = Frame(frm_info)
frm_fc_info.grid(row=0, column=4, rowspan=3, sticky="ew", padx=(40,20), pady=5)

# 현재 날씨 프레임
frm_weather = Frame(frm_fc_info)
frm_weather.grid(row=0, column=0, sticky="ew")

# 날씨 아이콘 경로
weather_name = ["맑음.png", "달.png", "구름.png", "구름_달.png", "비.png", "눈.png"]
weather_imgs = {}

for name in weather_name:
    img_weather_path = os.path.join(img_folder, name)
    weather_imgs[name] = Image.open(img_weather_path)


img_weather_sun = weather_imgs["맑음.png"]
img_weather_moon = weather_imgs["달.png"]
img_weather_cloud = weather_imgs["구름.png"]
img_weather_cloud_moon = weather_imgs["구름_달.png"]
img_weather_rain = weather_imgs["비.png"]
img_weather_snow = weather_imgs["눈.png"]

# 날씨 아이콘
code_weather = weather_code(fc["weathercode"][cur_hour])
if code_weather == 0:
    if 18 < cur_hour or cur_hour < 6:
        img_weather = img_weather_moon # 달
    else:
        img_weather = img_weather_sun # 맑음
elif code_weather == 1:
    if 18 < cur_hour or cur_hour < 6:
        img_weather = img_weather_cloud_moon # 흐림 달
    else:
        img_weather = img_weather_cloud # 흐림
elif code_weather == 2:
    img_weather = img_weather_rain # 비
elif code_weather == 3:
    img_weather = img_weather_snow # 눈

img_weather_rsize = img_weather.resize((75,75), Image.LANCZOS)
img_weather = ImageTk.PhotoImage(img_weather_rsize, master=win)
lbl_weather_img = Label(frm_weather, image=img_weather)
lbl_weather_img.pack(side="left", padx=10, pady=10)

# 온습도 라벨
lbl_temp = Label(frm_weather, text=temp, font=font_big, fg=blue)
lbl_temp.pack(side="left", padx=10, pady=10)

lbl_hum = Label(frm_weather, text=f"습도:{hum}", font=font_small)
lbl_hum.pack(side="left", padx=10, pady=10)

# 날씨 예보 부모 프레임
frm_fc_container = Frame(frm_fc_info)
frm_fc_container.grid(row=1, column=0, rowspan=2, sticky="ew", pady=10)

# 날씨 예보 캔버스
cnv_fc = Canvas(frm_fc_container, height=100)
cnv_fc.pack(side="top", fill="both")

# 날씨 예보 스크롤바
scrbar_fc = ttk.Scrollbar(frm_fc_container, orient="horizontal", command=cnv_fc.xview)
scrbar_fc.pack(side="bottom", fill="x")
cnv_fc.config(xscrollcommand=scrbar_fc.set)

# 날씨 예보 프레임
frm_fc = Frame(cnv_fc)
cnv_fc.create_window((0,0), window=frm_fc, anchor="nw")

def update_scrbar_fc(event):
    cnv_fc.config(scrollregion=cnv_fc.bbox("all"))

frm_fc.bind("<Configure>", update_scrbar_fc)

# 날씨 예보 아이콘
img_weather_fc = []
for i in range(1,13):
    code_fc = weather_code(fc["weathercode"][cur_hour+i])
    hour = (cur_hour+i) % 24
    if code_fc == 0:
        if 18 < hour or hour < 6:
            img_weather_fc.append(img_weather_moon) # 달
        else:
            img_weather_fc.append(img_weather_sun) # 맑음
    elif code_fc == 1:
        if 18 < hour or hour < 6:
            img_weather_fc.append(img_weather_cloud_moon) # 흐림 달
        else:
            img_weather_fc.append(img_weather_cloud) # 흐림
    elif code_fc == 2:
        img_weather_fc.append(img_weather_rain) # 비
    elif code_fc == 3:
        img_weather_fc.append(img_weather_snow) # 눈

for i in range(12):
    hour = (cur_hour+i+1) % 24
    lbl_fc = Label(frm_fc, text=f"{hour}시", font=font_small, width=6)
    lbl_fc.grid(row=0, column=i, pady=5)

    img_fc_rsize = img_weather_fc[i].resize((30,30), Image.LANCZOS)
    img_fc = ImageTk.PhotoImage(img_fc_rsize, master=win)
    
    lbl_fc_img = Label(frm_fc, image=img_fc)
    lbl_fc_img.image = img_fc
    lbl_fc_img.grid(row=1, column=i, pady=5)

    fc_temp = str(fc["temperature_2m"][cur_hour+i]) + "°C"
    lbl_fc_temp = Label(frm_fc, text=fc_temp, font=font_small)
    lbl_fc_temp.grid(row=2, column=i, pady=5)




# 급식 프레임
frm_meal = Frame(frm_info)
frm_meal.grid(row=4, column=4, sticky="ew", padx=(40,20))

# 급식 아이콘
img_meal_path = os.path.join(img_folder, "급식.png")
img_meal = Image.open(img_meal_path)
img_meal_rsize = img_meal.resize((55,55), Image.LANCZOS)
img_meal = ImageTk.PhotoImage(img_meal_rsize, master=win)
lbl_meal_img = Label(frm_meal, image=img_meal)
lbl_meal_img.pack(side="left", padx=10, pady=5)

lbl_meal = Label(frm_meal, text="급식", font=font_meal)
lbl_meal.pack(side="left")

# 급식메뉴 프레임
frm_menu = Frame(frm_info)
frm_menu.grid(row=5, column=4, sticky="ew", padx=(40,20))

lbl_menu = Label(frm_menu, text=menulist[0:3], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)
lbl_menu = Label(frm_menu, text=menulist[3:6], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)
lbl_menu = Label(frm_menu, text=menulist[6:], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)


# 구분선
line()


# 메모 프레임
frm_memo = Frame(win)
frm_memo.pack(side="top", fill="x", padx=40, pady=20)

# 메모
txt_memo = Text(frm_memo, height=12, width=68, font=font_default, wrap="word") # 단어 단위로 줄 바꿈
txt_memo.pack(side="left", fill="both")
txt_memo.insert("1.0", memo)

# 메모 스크롤바
scrbar_memo = ttk.Scrollbar(frm_memo, command=txt_memo.yview)
scrbar_memo.pack(side="right", fill="y")

txt_memo.config(yscrollcommand=scrbar_memo.set)



# 파일로 저장
def save_data():
    user_data = {
        "date" : today,
        "note" : ent_note.get(),
        "grade" : comb_grade.get(),
        "class" : comb_class.get(),
        "memo"  : txt_memo.get("1.0", "end-1c")
    }
    with open(save_file, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)
    
    win.destroy()


win.protocol("WM_DELETE_WINDOW", save_data)

update_time()

win.mainloop()
