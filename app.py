import json

from flask import Flask, render_template, request, Response
import mysql.connector as sql
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'python'
app.config['MYSQL_PASSWORD'] = 'python123'
app.config['MYSQL_DB'] = 'MyDB'

mysql.init_app(app)


@app.before_first_request
def before_first_request_func():
    createrPartitionsInsertData()


@app.route('/')
def home():
    return render_template('home.html')


# @app.route('/enternew')
# def new_student():
#     return render_template('student.html')


# @app.route('/addrec', methods=['POST', 'GET'])
# def addrec():
#     if request.method == 'POST':
#         try:
#             cid = request.form['cid']
#             odate = request.form['od']
#             pid = request.form['pid']
#
#             with sql.connect(database) as con:
#                 cur = con.cursor()
#
#                 cur.execute("INSERT INTO SALES (customer_id, order_date, product_id) VALUES (?,?,?)", (cid, odate, pid))
#
#                 con.commit()
#                 msg = "Record successfully added"
#         except:
#             con.rollback()
#             msg = "error in insert operation"
#
#         finally:
#             return render_template("result.html", msg=msg)
#             con.close()

def createrPartitionsInsertData():
    # for A less than join date - (A, 2021-01-07)
    # for A join date and later - (A, MAXVALUE)
    # for B less than join date - (B, 2021-01-07)
    # for B join date and later - (B, MAXVALUE)
    # any new values such as C - (MAXVALUE , MAXVALUE)
    alter_cid = "ALTER TABLE SALES_CID PARTITION BY RANGE COLUMNS(customer_id, order_date) (" \
                "PARTITION p05 VALUES LESS THAN ('A', '2021-01-07'), " \
                "PARTITION p06 VALUES LESS THAN ('A', MAXVALUE), " \
                "PARTITION p07 VALUES LESS THAN ('B', '2021-01-09'), " \
                "PARTITION p08 VALUES LESS THAN ('B', MAXVALUE), " \
                "PARTITION p09 VALUES LESS THAN (MAXVALUE , MAXVALUE)" \
                ")"

    alter_pid = "ALTER TABLE SALES_PID PARTITION BY RANGE (product_id)(" \
                "PARTITION p0 VALUES LESS THAN(1), " \
                "PARTITION p1 VALUES LESS THAN(2), " \
                "PARTITION p2 VALUES LESS THAN(3), " \
                "PARTITION p3 VALUES LESS THAN(MAXVALUE)" \
                ")"

    # insert data into sales
    insertSalesPID = "INSERT INTO SALES_PID (customer_id, order_date, product_id) VALUES " \
                     "('A', '2021-01-01', '1'), " \
                     "('A', '2021-01-01', '2'), " \
                     "('A', '2021-01-07', '2'), " \
                     "('A', '2021-01-10', '3'), " \
                     "('A', '2021-01-11', '3'), " \
                     "('A', '2021-01-11', '3'), " \
                     "('B', '2021-01-01', '2'), " \
                     "('B', '2021-01-02', '2'), " \
                     "('B', '2021-01-04', '1'), " \
                     "('B', '2021-01-11', '1'), " \
                     "('B', '2021-01-16', '3'), " \
                     "('B', '2021-02-01', '3'), " \
                     "('C', '2021-01-01', '3'), " \
                     "('C', '2021-01-01', '3'), " \
                     "('C', '2021-01-07', '3')" \
                     "; "

    insertSalesCID = "INSERT INTO SALES_CID (customer_id, order_date, product_id) VALUES " \
                     "('A', '2021-01-01', '1'), " \
                     "('A', '2021-01-01', '2'), " \
                     "('A', '2021-01-07', '2'), " \
                     "('A', '2021-01-10', '3'), " \
                     "('A', '2021-01-11', '3'), " \
                     "('A', '2021-01-11', '3'), " \
                     "('B', '2021-01-01', '2'), " \
                     "('B', '2021-01-02', '2'), " \
                     "('B', '2021-01-04', '1'), " \
                     "('B', '2021-01-11', '1'), " \
                     "('B', '2021-01-16', '3'), " \
                     "('B', '2021-02-01', '3'), " \
                     "('C', '2021-01-01', '3'), " \
                     "('C', '2021-01-01', '3'), " \
                     "('C', '2021-01-07', '3')" \
                     "; "

    # conn = sql.connect(host="localhost", user="python", passwd="python123", database="MyDB", autocommit=True)
    # cur = conn.cursor()

    conn = sql.connect(host="localhost", user="python", passwd="python123", database="MyDB", autocommit=True)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS SALES_CID")
    cur.execute("DROP TABLE IF EXISTS SALES_PID")

    # insert on sales_pid
    cur.execute("CREATE TABLE SALES_PID LIKE SALES")
    cur.execute(alter_pid)
    cur.execute(insertSalesPID)
    print("Table sales_pid inserted successfully")

    # insert on sales_cid
    cur.execute("CREATE TABLE SALES_CID LIKE SALES")
    cur.execute(alter_cid)
    cur.execute(insertSalesCID)
    print("Table sales_cid inserted successfully")
    conn.close()

# make different endpoints containing /mostpurchased for query1 onclick would generate the table via a function
# queryParameters for future querying on this analysis can get each customer's most purchased item, cater to the
# loyal customers or even get most purchased customers from members who have highest rank
@app.route("/mostPurchased", methods=['GET', 'POST'])
def mostPurchased():
    if request.method == 'GET':
        print("THIS WAS A GET")
        name = request.args.get("customer_id")
    else:
        return Response("Record not found", status=400)

    conn = sql.connect(host="localhost", user="python", passwd="python123", database="MyDB", autocommit=True)
    cur = conn.cursor()
    d = {}

    query1 = "select * from SALES_CID where customer_id = '%s'" % name
    cur.execute(query1)

    rows = cur.fetchall()
    conn.close()

    for result in rows:
        d.update({result[0]: {"customer_id": result[0], "product_id": result[2]}})
    return json.dumps(d)


@app.route('/query1')
def querylist1():
    conn = sql.connect(host="localhost", user="python", passwd="python123", database="MyDB", autocommit=True)
    cur = conn.cursor()

    query1 = "SELECT m.product_name, count(s.product_id) as numPurchased " \
             "from SALES_PID s, MENU m " \
             "WHERE s.product_id = m.product_id " \
             "group by s.product_id " \
             "order by s.product_id desc " \
             "limit 1 "

    cur.execute(query1)

    rows = cur.fetchall()
    conn.close()
    return render_template("list.html", rows=rows)

# make different endpoints containing /memberRanking for query1
# onclick would generate the table via a function
# queryParameters for future querying on this analysis can contain cid, member. Can also use queryParameters to check
# which customer has highest ranking (is a repeating customer, will become loyal to Van Deli)
@app.route('/query2')
def querylist2():
    conn = sql.connect(host="localhost", user="python", passwd="python123", database="MyDB", autocommit=True)
    cur = conn.cursor()

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
    return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
