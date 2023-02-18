import sqlite3

# lenght of table border
lines_lenght = 8 + 50 + 20 + 8 + 3 + 1

# print table with records included in data_
def print_data(data_):
    #print(20 * "=")
    for row in data_:
            print("+" + lines_lenght * "-" + "+")
            # print(F'|{row[0]}' + (8 - len(str( row[0]) ) ) * "." + F'| {row[1]}' + (50 - len(str( row[1]) ) ) * "." + F'|{row[2]}' + (20 - len(str( row[2]) ) ) * "." + F'|{row[3]}' + (8 - len(str( row[3]) ) ) * "." + "|")
            print(F'|{row[0]}' + (8 - len(str( row[0]) ) ) * " " + F'| {row[1]}' + (50 - len(str( row[1]) ) ) * " " + F'|{row[2]}' + (20 - len(str( row[2]) ) ) * " " + F'|{row[3]}' + (8 - len(str( row[3]) ) ) * " " + "|")
    print("+" + lines_lenght * "-" + "+")
    input("Press enter to continue.")
    print()

# add record to the database
def add_record():
        # add book to database
        # request data
        print("Enter the new ebook to database:")
        id  = get_int("Enter ID: ")
        title = input("Enter title: ")
        author = input("Enter author: ")
        qty = get_int("Enter quanity: ")

        # add requested data to database
        try:
            cursor.execute(""" INSERT INTO ebookstore(ID, TITLE, AUTHOR, QTY) VALUES (?,?,?,?)""", (id, title, author, qty))
            db.commit()
            print("Added to stock:")
            # print added ebook
            print_data( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY FROM ebookstore WHERE ID = ?""",(id,)) )
        except Exception:
            print("The ebook with the given ID already exists in the database.")
            input("Press enter to continue.")
            print("\n" + lines_lenght * "-" )

def get_int(request):
    while True:
        try:
            int_num = int(input(request))
            break
        except Exception:
            print("Something's wrong. Try again. Enter the integer number.")
    return int_num

# read elements from record  and return reqested
def get_item(record , num_of_requsted):
    counter = 0
    result = ""
    for col in record:
        if counter == num_of_requsted:
            result = col
        counter += 1
    return result


def update_ebook(data_):
    # reading records from selected row
    old_data = []
    for row in data_:
        old_data.append(row)
        new_data = []

    # request user to enter new data
    # print_data( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY from ebookstore WHERE ID IS ?""",(search,)) )
    try:
        print("Press enter if you don't want to make any changes.\nCurrent ID: ", old_data[0][0])
        new_data.append(input("New ID: ") )
        print("Current title: ", old_data[0][1])
        new_data.append( input("New title: ") )
        print("Current author: ", old_data[0][2])
        new_data.append( input("New author: ") )
        print("Quantity: ",old_data[0][3])
        new_data.append( input("New quantity: ") )

        # writing new data
        # replacment "" with old record
        for col in range(0, len(new_data)):
            if new_data[col] == "":
                new_data[col] = old_data[0][col]

        # adding old id to create tuple
        new_data.append(old_data[0][0])

        cursor.executemany (""" UPDATE ebookstore SET ID = ?, TITLE = ?,AUTHOR = ?,QTY = ? WHERE ID IS ?""",(new_data,))
    except Exception:
        print("Entered id not exist.")


# open the database
# connect to the database
try:
    db = sqlite3.connect("database.db")
    # get a coursor object
    cursor = db.cursor()
except Exception:
    print("Can't open database. End of program.")
    exit()
# creation of table
try:
    # create column: ID TITLE AUTHOR QTY
    cursor.execute(""" CREATE TABLE ebookstore(ID INTEGER PRIMARY KEY, TITLE text, AUTHOR text, QTY INTEGER)  """)
except Exception:
    pass
    # databese already exist

# print main menu
while True:
    print("""Select option:
    1 - Enter book,
    2 - Update book,
    3 - Delete book,
    4 - Search book,
    0 - Exit""")
    option = input("Choice: ")

    if option == "1":
        add_record()    

    elif option == "2":
        # update book
        # request id from user
        print("Update ebook by id.\nEnter the id of ebook: ");
        search = input("Choice: ")
        update_ebook( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY from ebookstore WHERE ID IS ?""",(search,)) )
            
        
    elif option == "3":
        print("Delete ebook by id.")
        search = input("Choice: ")
        # asking for id, nummer 3
        if get_item( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY from ebookstore WHERE ID IS ?""",(search,)), 0) != "":        
            print_data( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY from ebookstore WHERE ID IS ?""",(search,)) )

            if input("Confirm: yes / no: " ).lower() == "yes":
                cursor.execute( """DELETE FROM ebookstore WHERE ID = ? """, (search,) )
        else:
            print("There isn't a ebook with id: ", search, ".")
	
	
    elif option == "4":
        while True:
            option = input("""\t1 - Print all stock,
        2 - Search book by id,
        3 - Search by title,
        4 - Search by author,
        5 - Search by quntity,
        0 - back to main menu.
        Choice: """)

            if option == "1":
                # print all database
                print_data( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY from ebookstore  """) )
            elif option == "2":
                # search book by id
                search = input("Enter the id: ")
                print_data( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY from ebookstore  WHERE ID IS ?""",(search,)) )
            elif option == "3":
                # search book by title
                search = input("Enter the title: ")
                print_data( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY from ebookstore  WHERE TITLE IS ?""",(search,)) )
            elif option == "4":
                # search book by author
                search = input("Enter the author: ")
                print_data( cursor.execute(""" SELECT ID, TITLE, AUTHOR, QTY from ebookstore  WHERE AUTHOR IS ?""",(search,)) )
            elif option == "5":
                # search book by quantity
                search = input("Enter the : quantity: ")
                print(F"""\t\t1 - equal to {search},
            \t2 - less than {search},
            \t3 - equal to or less than {search},
            \t4 - equal to or greater than {search},
            \t5 - more than {search},
            \t0 - back to search menu.""")
                method = input("\t\tChoice: ")
                if method == "1":
                    print_data( cursor.execute('''SELECT ID, TITLE, AUTHOR, QTY FROM ebookstore WHERE QTY = ?''', (search, )) )
                elif method == "2":
                    print_data( cursor.execute('''SELECT ID, TITLE, AUTHOR, QTY FROM ebookstore WHERE QTY < ?''', (search, )) )
                elif method == "3":
                    print_data( cursor.execute('''SELECT ID, TITLE, AUTHOR, QTY FROM ebookstore WHERE QTY <= ?''', (search, )) )
                elif method == "4":
                    print_data( cursor.execute('''SELECT ID, TITLE, AUTHOR, QTY FROM ebookstore WHERE QTY >= ?''', (search, )) )
                elif method == "5":
                    print_data( cursor.execute('''SELECT ID, TITLE, AUTHOR, QTY FROM ebookstore WHERE QTY > ?''', (search, )) )
                elif method == "0":
                    pass
                else:
                    print("Opps, try again.")
                

            elif option == "0":
                # back to main menu
                # reset the option value
                option == ""
                break


    elif option == "0":
        print("End of program.")
        # writing all changes
        db.commit()
        exit()