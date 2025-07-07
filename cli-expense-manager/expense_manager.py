from datetime import datetime

pwd = input("enter the password: ")

if pwd == "heta1234":

    # sql connection
    import mysql.connector
    
    db_host = "localhost"
    db_user = "root"
    db_pwd = "root"
    db_name = "expense_manager"

    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pwd,
            database=db_name
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL database!\n")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL: {error}")
        exit()

    # match case
    print("1. add expense\n2. case two\n3. exit")
    ch = int(input("enter your choice: "))

    match ch:

        case 1: 
            category = input("Enter the category (eg: food, travel, fees...): ")
            amount = float(input("Enter amount (rupees): "))
            note = input("Enter note (optional): ")
            date = datetime.today().strftime('%D-%m-%y')

            try: 
                sql = "insert into expenses (category, amount, note, date) values (%s, %s, %s, %s)"
                values = (category, amount, note, date)
                cursor.execute(sql, values)
                conn.commit()
                print("Expense added successfully!!")

            except mysql.connector.Error as err:
                print(f"Error inserting expense: {err}")

        case 2: print("case two..")
        case 3: print("exiting..")

else:
    print("incorrect password!! exiting..")
    exit