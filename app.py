import json
import os
from flask import Flask, render_template, request, Response, send_from_directory
import mysql.connector as sql
from flaskext.mysql import MySQL
import mySqlDBSetup

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'python'
app.config['MYSQL_PASSWORD'] = 'python123'
app.config['MYSQL_DB'] = 'MyDB'

mysql.init_app(app)


# insert data before any requests to initialize partitioned tables
@app.before_first_request
def before_first_request_func():
    mySqlDBSetup.createrPartitionsInsertData()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# homepage
@app.route('/')
def home():
    return render_template('home.html')


# endpoint from ajax GET request. Displays results from query 1.
# queryParameters for future querying on this analysis can get each customer's most purchased item, cater to the
# # loyal customers or even get most purchased customers from members who have highest rank
@app.route("/mostPurchased", methods=['GET', 'POST'])
def mostPurchased():
    if request.method == 'POST':
        print("THIS WAS A POST")
    if request.method == 'GET':
        print("THIS WAS A GET")
    else:
        print("THIS WAS AN ERROR")
        return Response("Record not found", status=400)

    conn = sql.connect(host="localhost", user="python", passwd="python123", database="MyDB", autocommit=True)
    cur = conn.cursor()
    d = {}

    query1 = "SELECT m.product_name, count(s.product_id) as numPurchased " \
             "from SALES_PID s, MENU m " \
             "WHERE s.product_id = m.product_id " \
             "group by s.product_id " \
             "order by s.product_id desc " \
             "limit 1 "
    cur.execute(query1)
    rows = cur.fetchall()
    conn.close()
    for result in rows:
        d.update({"mostPurchasedTable": {"product_name": result[0], "numPurchased": result[1]}})
    response = app.response_class(
        response=json.dumps(d["mostPurchasedTable"]),
        status=200,
        mimetype='application/json'
    )
    return response


# endpoint from ajax GET request. Displays results from query 2.
# queryParameters for future querying on this analysis can contain cid, member. Can also use queryParameters to check
# which customer has highest ranking (is a repeating customer, will become loyal to Van Deli) and cater to them
@app.route('/memberAndRanking', methods=['GET', 'POST'])
def memberAndRanking():
    if request.method == 'POST':
        print("THIS WAS A POST")
    if request.method == 'GET':
        print("THIS WAS A GET")
    else:
        print("THIS WAS AN ERROR")
        return Response("Record not found", status=400)

    conn = sql.connect(host="localhost", user="python", passwd="python123", database="MyDB", autocommit=True)
    cur = conn.cursor()
    d = {}

    query2 = "select t.*, DENSE_RANK() OVER (PARTITION BY t.customer_id order by t.order_date) as 'ranking' " \
             "from (" \
             "select SALES_CID.customer_id, SALES_CID.order_date, MENU.product_name, MENU.price, " \
             "CASE " \
             "WHEN SALES_CID.order_date >= MEMBERS.join_date THEN 'Y' " \
             "ELSE 'N' " \
             "END AS member " \
             "from (" \
             "(SALES_CID INNER JOIN MENU ON SALES_CID.product_id = MENU.product_id) " \
             "LEFT JOIN MEMBERS ON SALES_CID.customer_id = MEMBERS.customer_id) " \
             "order by customer_id, order_date, product_name) t "

    cur.execute(query2)
    rows = cur.fetchall()
    conn.close()
    for result in rows:
        if d.get("memberRanking") is None:
            d.update(
                {"memberRanking": [{"customer_id": result[0], "order_date": str(result[1]), "product_name": result[2],
                                    "price": result[3], "member": result[4], "ranking": result[5]}]})
        else:
            d["memberRanking"].append(
                {"customer_id": result[0], "order_date": str(result[1]), "product_name": result[2],
                 "price": result[3], "member": result[4], "ranking": result[5]})

    response = app.response_class(
        response=json.dumps(d["memberRanking"]),
        status=200,
        mimetype='application/json'
    )
    return response


# render tables.html and when clicking button Get Most Purchased, calls getMostPurchased() (ajax call - GET request)
# to /mostPurchased endpoint. When clicking Get Member And Ranking, calls getMemberAndRanking() (ajax call - GET
# request) to /memberAndRanking endpoint
@app.route('/query')
def querylist():
    return render_template("tables.html")


if __name__ == '__main__':
    app.run(debug=True)
