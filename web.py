from flask import Flask, render_template, request
from datetime import datetime
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
    return link

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
    
if __name__ == "__main__":
    app.run()
