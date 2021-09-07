import mysql.connector as mysql


# must commit when using transactional storage - mine is InnoDB
# autocommit is useful in ad-hoc execution of SQL, not desirable for high transaction volumes bc an error can occur
# along the way where you should rollback
# for the purpose of this assignment, since only small amount of data I will use autocommit
# TODO: - load data from a csv and make only alphabetic characters for cid in SALES and MEMBERS
def initializeMembersAndMenu(database):
    # create tables Sales, Menu, Members
    print("Start creating database " + database + ", tables SALES, MEMBERS, and MENU will be created in " + database)
    conn = mysql.connect(host="localhost", user="python", passwd="python123", database=database, autocommit=True)
    cursor = conn.cursor()

    # create members
    # need join_date to be joined with order_date, part of primary key
    # customer_name not necessary to be defined
    createMembers = "CREATE TABLE MEMBERS (" \
                    "customer_id VARCHAR(1) NOT NULL, " \
                    "customer_name VARCHAR(4), " \
                    "join_date TIMESTAMP NOT NULL, " \
                    "PRIMARY KEY(customer_id, join_date)" \
                    "); "
    cursor.execute(createMembers)
    print("Table members created successfully")
    # insert data into members
    insertMembers = "INSERT INTO MEMBERS (customer_id, customer_name, join_date) VALUES " \
                    "('A', 'Anne', '2021-01-07'), " \
                    "('B', 'Bob', '2021-01-09')" \
                    "; "
    cursor.execute(insertMembers)
    print("Table members inserted successfully")

    # create menu
    # product_name not necessary to be defined
    createMenu = "CREATE TABLE MENU (" \
                 "product_id INTEGER NOT NULL PRIMARY KEY, " \
                 "product_name VARCHAR(5), " \
                 "price INTEGER NOT NULL" \
                 "); "
    cursor.execute(createMenu)
    print("Table menu created successfully")
    # insert data into menu
    insertMenu = "INSERT INTO MENU (product_id, product_name, price) VALUES " \
                 "('1', 'sushi', '10'), " \
                 "('2', 'curry', '15'), " \
                 "('3', 'ramen', '12')" \
                 "; "
    cursor.execute(insertMenu)
    print("Table menu inserted successfully")

    # Cannot make foreign key bc not supported in mysql with partitions
    # customer_id and product_id will be linked, only max amount of products at a small company
    # disregarding invalid characters, so only take alphabet characters
    # Creating no partitions for Sales, will create relevant partitions in SALES_CID and SALES_PID
    # will link to the primary key since it's unique. No primary keys here since duplicate entries
    # (which are valid since you can order on the same day)

    createSales = "CREATE TABLE SALES (" \
                  "customer_id VARCHAR(1) NOT NULL, " \
                  "order_date DATE NOT NULL, " \
                  "product_id INTEGER NOT NULL check (product_id>=0)" \
                  "); "

    cursor.execute(createSales)
    print("Table sales created successfully")

    conn.close()


def initializeDBAndTables(database):
    # create database
    conn = mysql.connect(user='python', password='python123',
                         host='127.0.0.1', autocommit=True)  # using python user and python123 for password created
    print("Successfully connected")
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES LIKE '" + database + "'")
    dbExists = cursor.fetchall()
    if len(dbExists) != 0:
        while True:
            result = str(input("The database already exists. Would you like to override? (y/n) "))
            if (result.lower() != 'y') & (result.lower() != 'n'):
                print("Sorry, valid inputs must be (y/Y) or (n/N), try again")
                continue
            else:
                break

        if result.lower() == "y":
            print("Dropping previous database " + database + "...")
            cursor.execute("DROP DATABASE " + database)
            print("Creating new database " + database)
            cursor.execute("CREATE DATABASE " + database)
            print("Opened database successfully")
            conn.close()
            initializeMembersAndMenu(database)
        elif result.lower() == "n":
            print("Using existing database " + database + " and its tables")
    else:
        cursor.execute("CREATE DATABASE " + database)
        print("Opened new database successfully")
        conn.close()
        initializeMembersAndMenu(database)


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
                "PARTITION p0 VALUES LESS THAN(2), " \
                "PARTITION p1 VALUES LESS THAN(3), " \
                "PARTITION p2 VALUES LESS THAN(4), " \
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

    conn = mysql.connect(host="localhost", user="python", passwd="python123", database="MyDB", autocommit=True)
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


if __name__ == '__main__':
    db = input("Enter the name of the database to create: ")
    # delete any previous db created
    initializeDBAndTables(db)
