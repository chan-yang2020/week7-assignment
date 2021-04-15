from flask import Flask, request, render_template, redirect, session, url_for, jsonify
import json
import mysql.connector

app = Flask(__name__)

# session key
app.secret_key = "l;f2j;fs/.masdopff"

# 連接database website
website = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="website",
)

# 執行SQL語法
cursor = website.cursor()

@app.route("/api/users", methods=["get"])
def api():
    account=request.args.get("username")
    SQL_statement = "select id,name,username from user where username=%s"
    username_data = (account, )
    cursor.execute(SQL_statement, username_data)
    data_account = cursor.fetchone()
    if data_account is not None:
        return jsonify({"data":{"id":int(data_account[0]),"name":str(data_account[1]),"username":str(data_account[2])}})
    else:
        return jsonify({"data":None})




@app.route("/")
def home():
    if "status" in session:
        return redirect("http://127.0.0.1:3000/member")
    return render_template("home.html")


@app.route("/signup", methods=["POST"])
def signup():
    # 從網頁讀取資料 POST
    username = request.form["username"]
    account = request.form["account"]
    password = request.form["password"]
    # check account
    SQL_statement = "select username from user where username=%s"
    username_data = (account, )
    cursor.execute(SQL_statement, username_data)
    data_account = cursor.fetchone()
    if data_account is not None:  # 判斷是否為空陣列
        # 等同於/error/?message=帳號已經被註冊
        return redirect(url_for("error", message="帳號已經被註冊"))
    # insert data
    else:
        insert_data = "insert into user (name, username, password) VALUES (%s, %s, %s)"
        current_data = (username, account, password)
        cursor.execute(insert_data, current_data)
        return redirect("http://127.0.0.1:3000")


@app.route("/signin", methods=["POST"])
def signin():
    # 從網頁讀取資料 POST
    account = request.form["account"]
    password = request.form["password"]
    SQL_statement = "select username from user where username=%s and password=%s"
    data = (account, password)
    cursor.execute(SQL_statement, data)
    data_account = cursor.fetchone()
    if data_account is not None:  # 判斷是否為空陣列
        SQL_statement = "select name from user where username = %s"
        username_data = (account, )
        cursor.execute(SQL_statement, username_data)
        name = cursor.fetchone()  # fetchone只取一個
        session["status"] = "".join(name)  # 把name存進session
        return redirect("http://127.0.0.1:3000/member")
    else:
        # 等同於/error/?message=帳號或密碼輸入錯誤
        return redirect(url_for("error", message="帳號或密碼輸入錯誤"))


@app.route("/member/")
def member():
    if "status" not in session:
        return redirect("http://127.0.0.1:3000")
    
    return render_template("right.html", data=session["status"])# 把name從session中抓出來


@app.route("/error/", methods=["get"])
def error():
    text = request.args.get("message")  # 用get method讀取message
    return render_template("wrong.html", data=text)


@app.route("/loggedout")
def loggedout():
    session.pop("status", None)
    return redirect("http://127.0.0.1:3000")


app.run(port=3000)
