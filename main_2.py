from tkinter import*
import tkinter.font as Font
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import time
import requests
import json
import re
from datetime import date, datetime, timedelta

win = Tk()



#배경사진
# image = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\bg.jpg")
# bg_image = ImageTk.PhotoImage(image)

# background_label = Label(win, image=bg_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)




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
font_DKSH = Font.Font(family="페이퍼로지 7 Bold", size=19)
#없으면 자동으로 기본 폰트 적용





#api key
key_sc = "571668b4449b4ba09ef972d847ee6022"

key_fc = "3069107dc8048e396ed96dc4ff73f4d8e34a8a6852bee46363b23899e8cfc951"


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
url_fc = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
# url_fc = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getVilageFcst"


base_time = base_time()

params_fc = {
    "serviceKey" : key_fc,
    "numOfRows" : "1000",
    "pageNo" : "1",
    "dataType" : "json",
    "base_date" : today,
    "base_time" : base_time,
    "nx" :"61",
    "ny" : "125"
}

response_fc = requests.get(url_fc, params=params_fc)

# data_fc = response_fc.json()
# fcdata = data_fc["response"]["body"]["items"]["item"]

# # 3️⃣ 현재 시간 기준으로 데이터 정리
# # 시간별, 카테고리별 딕셔너리 생성
# forecast_dict = {}
# for item in fcdata:
#     t = item['fcstTime']
#     category = item['category']
#     value = item['fcstValue']
#     forecast_dict.setdefault(t, {})[category] = value

# # 4️⃣ 현재 날씨: 첫 번째 데이터 기준 시간
# latest_time = fcdata[0]['fcstTime']
# current_weather = forecast_dict[latest_time]

# rain_type = current_weather.get("PTY")  # 강수형태
# temp      = current_weather.get("T1H")  # 기온
# humidity  = current_weather.get("REH")  # 습도


# print(current_weather)

# # 5️⃣ 현재 시각부터 12시간 후까지 1시간 간격 예보
# now = datetime.now()
# next_12h = [now + timedelta(hours=i) for i in range(0, 13)]
# next_12h_str = [dt.strftime("%H%M") for dt in next_12h]

# print("\n📊 12시간 예보 (1시간 단위):")
# for t in next_12h_str:
#     if t in forecast_dict:
#         print(t, forecast_dict[t])


print(response_fc.text)


#현재 날씨 정보
# temp = fc_dict.get('T1H')  # 기온
# humidity = fc_dict.get('REH')  # 습도
# rain_type = fc_dict.get('PTY')  # 강수형태
# rain_1h = fc_dict.get('RN1')  # 1시간 강수량

# img_weather_fc = []



#색상
blue = "#007fff"
DKSH = '#164e93'

# #메뉴 새로고침 함수
# def refresh():
#     pass

# #메뉴
# menubar = Menu(win)

# menu_file = Menu(menubar, tearoff=0)
# menu_file.add_command(label="refresh", command=refresh)
# menu_file.add_separator()
# menu_file.add_command(label="quit", command=win.quit)
# menubar.add_cascade(label="File", menu=menu_file)

# win.config(menu=menubar)




#다짐 엔트리 클릭 동작
def clear(event):
    ent_note.delete(0, END)
    ent_note.unbind("<Button-1>")
    ent_note.config(fg="black")

#시간 업데이트
def update_time():
    current_time = time.strftime("%H:%M:%S")
    lbl_time.config(text=current_time)
    win.after(100, update_time)

#윗줄 프레임
frm_top = Frame(win)
frm_top.pack(fill="x", padx=30, pady=13)

#학교 로고
img_DKSH = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\단대소고.png")
width_D = int(img_DKSH.width*0.1)
hight_D = int(img_DKSH.height*0.1)
img_rsiz_DKSH = img_DKSH.resize((width_D,hight_D), Image.LANCZOS)
img_DKSH_2 = ImageTk.PhotoImage(img_rsiz_DKSH, master=win)
lbl_img_DKSH = Label(frm_top, image=img_DKSH_2)
lbl_img_DKSH.pack(side="left")

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
img_clock = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\시계.png")
img_rsiz_clock = img_clock.resize((35, 35), Image.LANCZOS)
img_clock_2 = ImageTk.PhotoImage(img_rsiz_clock, master=win)
lbl_clock = Label(frm_top, image=img_clock_2)
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



#시간표 업데이트 프레임
frm_sc = Frame(frm_info)
frm_sc.grid(row=0, column=0, columnspan=3, sticky=E+W, padx=40, pady=15)



#학년 선택
grade = [1,2,3]
combox_grade = ttk.Combobox(frm_sc, height=5, width=10, values=grade, state="readonly")
combox_grade.grid(row=0, column=0, padx=5, pady=5)
combox_grade.set("학년")

#반 선택
sc_class = [1,2,3,4,5]
combox_class = ttk.Combobox(frm_sc, height=5, width=10, values=sc_class, state="readonly")
combox_class.grid(row=0, column=1, padx=5, pady=5)
combox_class.set("반")




#시간표 프레임
frm_scj = Frame(frm_info, relief="solid", bd=0)
frm_scj.grid(row=1, column=0, rowspan=8, columnspan=3, sticky=E+W, padx=(30,50), pady=0)

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
btn_sbjt = Button(frm_sc, text="검색", width=4, command=btn_sbjt_cmd)
btn_sbjt.grid(row=0,column=2, padx=5, pady=5)




# url = "https://api.open-meteo.com/v1/forecast"
# params = {
#     "latitude": 37.2971,
#     "longitude": 127.1293,
#     "hourly": "temperature_2m,weathercode,relative_humidity_2m,wind_direction_10m,precipitation_probability",
#     "timezone": "Asia/Seoul",
#     "forecast_days": 1,
# }

# response = requests.get(url, params=params)
# data = response.json()

# print(data)

# fc = data["hourly"]

# # print(fc)

# def weather(code):
#     if code == 0:
#         return 0 #맑음
#     elif code in [1, 2, 3]:
#         return 1 #구름
#     elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
#         return 2 #비
#     elif code in [71, 73, 75, 77, 85, 86]:
#         return 3 #눈


# #현재 날씨 정보
# temp = str(fc["temperature_2m"][ntime])+"°C"
# humidity = str(fc["relative_humidity_2m"][ntime])+"%"
# wind_dir = str(fc["wind_direction_10m"][ntime])+"°"
# precip_prob = str(fc["precipitation_probability"][ntime])+"%"



#날씨 정보 프레임
frm_weather_info = Frame(frm_info)
frm_weather_info.grid(row=0, column=7, rowspan=3, sticky=E+W, padx=(40,20), pady=5)


#온도 프레임
frm_weather = Frame(frm_weather_info)
frm_weather.grid(row=0, column=0, sticky=E+W, padx=0, pady=0)


#날씨 아이콘 경로
img_weather0 = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\맑음.png")
img_weather1 = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\구름.png")
img_weather2 = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\비.png")
img_weather3 = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\눈.png")
img_weather4 = Image.open(r"D:\hajun\개인\VScode\pythonworkspace\.vscode\단대소고\사진\바람.png")

#날씨 아이콘
# if rain_type == "0":
#     img_weather = img_weather0 # 맑음
# elif rain_type == "1"or"4":
#     img_weather = img_weather2 # 비
# elif rain_type == "2"or"3":
#     img_weather = img_weather3 # 눈

img_weather = img_weather0 # 임시 맑음

img_resized_weather = img_weather.resize((75, 75), Image.LANCZOS)
img_weather = ImageTk.PhotoImage(img_resized_weather, master=win)
lbl_weather = Label(frm_weather, image=img_weather)
lbl_weather.pack(side="left", padx=10, pady=10)





temp = "25°C"  # 임시 기온
humidity = "60"  # 임시 습도

#안내라벨
lbl_temp = Label(frm_weather, text=temp, font=font_temp, fg=blue)
lbl_temp.pack(side='left', padx=10, pady=10)

lbl_humidity = Label(frm_weather, text=("습도: "+humidity+"%"), font=font_small)
lbl_humidity.pack(side='left', padx=10, pady=10)

# lbl_ment = Label(frm_weather, text="", font=font_default)   #<-- 날씨에 따라 멘트 변경
# lbl_ment.pack(side="left", padx=10, pady=10)


#날씨 예보 부모 프레임
frm_forecast_container = Frame(frm_weather_info)
frm_forecast_container.grid(row=6, column=0, rowspan=4, sticky=E+W, padx=0, pady=10)

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



img_weather_fc = [img_weather0,img_weather1,img_weather2,img_weather3,img_weather4] #임시 아이콘 리스트



for i in range(1, 13):
    if i+ntime <= 24:
        lbl_forecast = Label(frm_forecast, text=f"{i+ntime}시", font=font_small, width=6)
    else:
        lbl_forecast = Label(frm_forecast, text=f"{i+ntime-24}시", font=font_small, width=6)
    lbl_forecast.grid(row=0, column=i-1, padx=0, pady=5)
    
    img_resized = img_weather_fc[i % 5].resize((30, 30), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized, master=win)
    img_weather_fc.append(img_tk)  # 참조 유지
    
    lbl_forecast_img = Label(frm_forecast, image=img_tk)
    lbl_forecast_img.grid(row=1, column=i-1, padx=0, pady=5)
    
    lbl_forecast_temp = Label(frm_forecast, text="25°C", font=font_small)
    lbl_forecast_temp.grid(row=2, column=i-1, padx=0, pady=5)




#급식 프레임
frm_meal = Frame(frm_info, relief="solid", bd=0)
frm_meal.grid(row=3, column=7, sticky=E+W, padx=(40,20), pady=0)

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
frm_menu.grid(row=4, column=7, sticky=E+W, padx=(40,20), pady=0)

#급식 메뉴
lbl_menu = Label(frm_menu, text=menu_list[0:3], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)
lbl_menu = Label(frm_menu, text=menu_list[3:6], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)
lbl_menu = Label(frm_menu, text=menu_list[6:], font=font_default)
lbl_menu.pack(anchor="w", padx=10, pady=5)




# 구분선 프레임
frm_line = Frame(win, bg="white")
frm_line.pack(fill="x", padx=10, pady=0)

# 프레임 위쪽에 선 그리기
canvas_line = Canvas(frm_line, height=1, bg="gray", highlightthickness=0)
canvas_line.pack(side="top", fill="x")



#개인 프레임
frm_user = Frame(win)
frm_user.pack(side="top", fill="x", padx=10, pady=0)

#메모 프레임
# frm_memo = Frame(frm_user)
# frm_memo.grid(row=0,column=0, padx=10, pady=20)

txt_memo = Text(frm_user, height=13, width=35, font=font_default)
txt_memo.grid(row=0, column=0, rowspan=6, padx=30, pady=20)

def clear_todo(event):
    ent_todo.delete(0, END)
    ent_todo.unbind("<Button-1>")
    ent_todo.config(fg="black")



#할일 추가 엔트리
ent_todo = Entry(frm_user, font=font_default)
ent_todo.grid(row=0, column=1, sticky=E+W, padx=30, pady=20, ipady=3)
ent_todo.config(fg="gray")
ent_todo.insert(0, "할 일 (enter로 추가)")
ent_todo.bind("<Button-1>", clear_todo)


# 할일 부모 프레임
frm_todo_container = Frame(frm_user, relief="sunken", bd=3)
frm_todo_container.grid(row=1, column=1, padx=30, pady=0)

# 할일 스크롤바
xscrollbar_todo = ttk.Scrollbar(frm_todo_container, orient="horizontal")
xscrollbar_todo.pack(side="bottom", fill="x")

yscrollbar_todo = ttk.Scrollbar(frm_todo_container, orient="vertical")
yscrollbar_todo.pack(side="right", fill="y")

# 할일 캔버스
canvas_todo = Canvas(frm_todo_container, width=300, height=190, yscrollcommand=yscrollbar_todo.set, xscrollcommand=xscrollbar_todo.set)
canvas_todo.pack(side="left", fill="both", expand=True)

# 스크롤바 연결
yscrollbar_todo.config(command=canvas_todo.yview)
xscrollbar_todo.config(command=canvas_todo.xview)

# 할일 프레임
frm_todo = Frame(canvas_todo)
canvas_todo.create_window((0, 0), window=frm_todo, anchor="nw")

# 스크롤 영역 갱신
frm_todo.bind("<Configure>", lambda e: canvas_todo.configure(scrollregion=canvas_todo.bbox("all")))

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