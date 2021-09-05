import mysql.connector as mysql


# must commit when using transactional storage - mine is InnoDB
# autocommit is useful in ad-hoc execution of SQL, not desirable for high transaction volumes bc an error can occur
# along the way where you should rollback
# for the purpose of this assignment, since only small amount of data I will use autocommit
def initializeMembersAndMenu(database):
    # create tables Sales, Menu, Members
    print("Start creating database " + database + ", tables SALES, MEMBERS, and MENU will be created in " + database)
    conn = mysql.connect(host="localhost", user="python", passwd="python123", database=database, autocommit=True)
    cursor = conn.cursor()

    # create members
    # join_date can be null, but not for query 2 where it needs to be joined with order_date
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

    # create sales even though common columns, cannot make foreign key for customer_id bc child table (sales) has a
    # customer_id not part of parent table and will throw error. No foreign key either on product_id bc for cascading
    # purposes turned on you dont want to delete the product either
    # cascading will be turned off anyways, mysql doesnt support foreign keys
    # will link to the primary key since it's unique

    createSales = "CREATE TABLE SALES (" \
                  "customer_id VARCHAR(1) NOT NULL, " \
                  "order_date DATE NOT NULL, " \
                  "product_id INTEGER NOT NULL check (product_id>=0)" \
                  "); "

    # createSales = "CREATE TABLE SALES (" \
    #               "customer_id VARCHAR(1) NOT NULL, " \
    #               "order_date DATE NOT NULL, " \
    #               "product_id INTEGER NOT NULL, " \
    #               "FOREIGN KEY (product_id) REFERENCES MENU(product_id)" \
    #               "); "

    # createSales = "CREATE TABLE SALES (" \
    #               "customer_id VARCHAR(1) NOT NULL, " \
    #               "order_date DATE NOT NULL, " \
    #               "product_id INTEGER NOT NULL check (product_id>=0)) " \
    #               "PARTITION_BY RANGE (product_id)(" \
    #               "PARTITION p01 VALUES LESS THAN(2), # with pid 1" \
    #               "PARTITION p02 VALUES LESS THAN(3), # with pid 2" \
    #               "PARTITION p03 VALUES LESS THAN(4), # with pid 3" \
    #               "PARTITION p04 VALUES LESS THAN(MAXVALUE) # extra in case more values get added" \
    #               "); "

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


if __name__ == '__main__':
    db = input("Enter the name of the database to create: ")
    # delete any previous db created
    initializeDBAndTables(db)
