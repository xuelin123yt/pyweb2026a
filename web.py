import random
import os
import json
import firebase_admin
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from datetime import datetime
from firebase_admin import credentials, firestore

if not firebase_admin._apps:   # 防止重複初始化
    if os.path.exists('serviceAccountKey.json'):
        # 本地環境
        cred = credentials.Certificate('serviceAccountKey.json')
    else:
        # 雲端環境
        firebase_config = os.getenv('FIREBASE_CONFIG')
        cred_dict = json.loads(firebase_config)
        cred = credentials.Certificate(cred_dict)

    firebase_admin.initialize_app(cred)
app = Flask(__name__)

@app.route("/")
def index():
    link = "<h1>歡迎加入王奕翔的網站首頁</h1>"
    link += "<a href='/mis'>課程</a><hr>"
    link += "<a href='/today'>今天日期</a><hr>"
    link += "<a href='/about'>關於奕翔</a><hr>"
    link += "<a href='/welcome?nick=奕翔&dep=靜宜資管'>GET傳值</a><hr>"
    link += "<a href=/account>POST傳值(帳號密碼)</a><hr>"
    link += "<a href=/math>數學運算</a><hr>"
    link += "<a href=/cup>擲茭</a><hr>"
    link += "<a href=/read3>讀取Firestore資料</a><hr>"
    link += "<a href='/search'>老師搜尋</a><hr>"
    link += "<a href='/movie'>查詢即將上映電影</a><hr>"
    link += "<a href='/movie2'>爬取電影進資料庫</a><hr>"
    link += "<a href='/movie3'>查詢電影資料庫</a><hr>"
    return link

@app.route("/movie3", methods=["GET", "POST"])
def movie3():
    db = firestore.client()
    results = []
    keyword = ""
    
    if request.method == "POST":
        keyword = request.form.get("keyword")
        collection_ref = db.collection("電影2A")
        docs = collection_ref.get()

        for doc in docs:
            movie = doc.to_dict()
            if keyword in movie["title"]:
                results.append({
                    "title":  movie["title"],
                    "picture": movie["picture"],
                    "hyperlink": movie["hyperlink"],
                    "showDate": movie["showDate"],
                    "showLength": movie["showLength"],
                    "lastUpdate": movie["lastUpdate"]
                })

    return render_template("movie3.html", results=results, keyword=keyword)

@app.route("/movie2")
def movie2():
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".filmListAllX li")
    lastUpdate = sp.find("div", class_="smaller09").text[5:]

    for item in result:
        picture = item.find("img").get("src").replace(" ", "")
        title = item.find("div", class_="filmtitle").text
        movie_id = item.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
        hyperlink = "http://www.atmovies.com.tw" + item.find("div", class_="filmtitle").find("a").get("href")
        show = item.find("div", class_="runtime").text.replace("上映日期：", "")
        show = show.replace("片長：", "")
        show = show.replace("分", "")
        showDate = show[0:10]
        showLength = show[13:]

        doc = {
            "title": title,
            "picture": picture,
            "hyperlink": hyperlink,
            "showDate": showDate,
            "showLength": showLength,
            "lastUpdate": lastUpdate
        }

        db = firestore.client()
        doc_ref = db.collection("電影2A").document(movie_id)
        doc_ref.set(doc)    
    return "近期上映電影已爬蟲及存檔完畢，網站最近更新日期為：" + lastUpdate 

@app.route("/movie", methods=["GET", "POST"])
def movie():
    db = firestore.client()

    # 👉 第一次進來（GET）→ 自動爬蟲
    if request.method == "GET":
        url = "http://www.atmovies.com.tw/movie/next/"
        Data = requests.get(url)
        Data.encoding = "utf-8"

        sp = BeautifulSoup(Data.text, "html.parser")
        result = sp.select(".filmListAllX li")

        for item in result:
            try:
                picture = item.find("img").get("src").strip()

                # ⭐ 關鍵修正：補完整網址
                if picture.startswith("/"):
                    picture = "http://www.atmovies.com.tw" + picture

                title = item.find("div", class_="filmtitle").text.strip()

                link = item.find("a").get("href")
                movie_id = link.replace("/", "").replace("movie", "")

                hyperlink = "http://www.atmovies.com.tw" + link

                show = item.find("div", class_="runtime").text
                show = show.replace("上映日期：", "").replace("片長：", "").replace("分", "")

                showDate = show[0:10]
                showLength = show[13:]

                doc = {
                    "title": title,
                    "picture": picture,
                    "hyperlink": hyperlink,
                    "showDate": showDate,
                    "showLength": showLength
                }

                db.collection("電影").document(movie_id).set(doc)

            except Exception as e:
                print("錯誤:", e)

        return render_template("movie.html", movies=None)

    # 👉 查詢（POST）
    else:
        keyword = request.form["MovieTitle"]

        docs = db.collection("電影").get()

        movies = []
        for doc in docs:
            data = doc.to_dict()

            if keyword in data.get("title", ""):
                movies.append(data)

        return render_template("movie.html", movies=movies)

@app.route("/search", methods=["GET", "POST"])
def search():
    Result = ""

    if request.method == "POST":
        keyword = request.form.get("name", "")

        db = firestore.client()
        collection_ref = db.collection("靜宜資管")    
        docs = collection_ref.get()

        for doc in docs:
            data = doc.to_dict()
            teacher = data.get("name", "")
            lab = data.get("lab", "")

            # 模糊搜尋
            if keyword in teacher:
                Result += f"老師：{teacher}，研究室：{lab}<br>"

        if Result == "":
            Result = "查無資料"

    return render_template("search.html", result=Result)

@app.route("/read3")
def read3():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("靜宜資管")    
    docs = collection_ref.order_by("lab", direction=firestore.Query.DESCENDING).limit(4).get()
    for doc in docs:         
        Result += str(doc.to_dict()) + "<br>"    

    return Result

@app.route("/mis")
def course():
    return '<h1>資訊管理導論</h1><a href="/">回到網站首頁</a>'

@app.route("/today")
def today():
    now = datetime.now()
    
    year = now.year
    month = now.month
    day = now.day
    
    date = f"{year}年{month}月{day}日"
    
    return render_template("today.html", datetime=date)

@app.route("/about")
def about():
    return render_template("MIS2A.html")

@app.route("/welcome", methods=["GET"])
def welcome():
    user = request.values.get("nick", "王奕翔")
    dep = request.values.get("dep", "靜宜資管")
    return render_template("welcome.html", name=user, dep=dep)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/math", methods=["GET", "POST"])
def math():
    if request.method == "POST":
        x = int(request.form["x"])
        opt = request.form["opt"]
        y = int(request.form["y"])      
        result = "您輸入的是：" + str(x) + opt + str(y)
        
        if (opt == "/" and y == 0):
            result += "，除數不能為0"
        else:
            match opt:
                case "+":
                    r = x + y
                case "-":
                    r = x - y
                case "*":
                    r = x * y
                case "/":
                    r = x / y  # 修正：之前誤寫為 x - y
                case _:
                    return "未知運算符號"
            result += "=" + str(r)  + "<br><a href=/>返回首頁</a>"          
        return result
    else:
        return render_template("math.html")

@app.route('/cup', methods=["GET"])
def cup():
    # 檢查網址是否有 ?action=toss
    #action = request.args.get('action')
    action = request.values.get("action")
    result = None
    
    if action == 'toss':
        # 0 代表陽面，1 代表陰面
        x1 = random.randint(0, 1)
        x2 = random.randint(0, 1)
        
        # 判斷結果文字
        if x1 != x2:
            msg = "聖筊：表示神明允許、同意，或行事會順利。"
        elif x1 == 0:
            msg = "笑筊：表示神明一笑、不解，或者考慮中，行事狀況不明。"
        else:
            msg = "陰筊：表示神明否定、憤怒，或者不宜行事。"
            
        result = {
            "cup1": "/static/" + str(x1) + ".jpg",
            "cup2": "/static/" + str(x2) + ".jpg",
            "message": msg
        }
        
    return render_template('cup.html', result=result)

if __name__ == "__main__":
    app.run()
