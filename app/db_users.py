import sqlite3
db = sqlite3.connect("users.db", check_same_thread=False)
global c
c = db.cursor()
c.execute("CREATE TABLE if not exists main(user_id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
def _select_from(table, data_want, datagive, datatype_give):
    temp = ((c.execute(f"SELECT {data_want} FROM {table} WHERE {datatype_give} = '{datagive}'")).fetchall())
    if(len(temp) > 0):
        return temp[0][0]
    else:
        return 0
#check if username is in name
def username_in_system(username):
    temp = list(c.execute("SELECT username FROM main").fetchall())
    for element in temp:
        for element2 in element:
            if username == element2:
                return True
    return False
#gets the password
def get_password(username):
    return(_select_from("main", "password", username, "username"))
#adds username-password pair to db. Return 0 if not added(because username already exit and 1 if added successfully)
def signup(username, password):
    c.execute("CREATE TABLE if not exists main(user_id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    if(username_in_system(username)):
        return False
    else:
        temp2 = c.execute(f'SELECT user_id FROM main').fetchall()
        user_id = len(temp2) + 1
        c.execute("INSERT INTO main VALUES (?,?,?)", (user_id, username, password))
        c.execute(f'CREATE TABLE {username}(story_id INTEGER, edit_id INTEGER)')
    db.commit()
    return True #save changes
   # db.close()  #close database
#return username given an user id
def get_username_from_id(user_id):
    return(_select_from("main", "username", user_id, "user_id"))
#returns user_id given an username
def get_id_from_username(username):
    return(_select_from("main", "user_id", username, "username"))

#you can add using username or user_id

def add_into_user_db(username, story_id, edit_id):
    user_id = get_id_from_username(username)
    if(username_in_system(username)):
        print("achieved")
        c.execute(f'INSERT INTO {username} VALUES (?, ?)',(story_id, edit_id))
        print("done")
    db.commit() #save changes
    #db.close()  #close database
# def add_into_user_db(user_id, story_id, edit_id):
#     username = get_username_from_id(user_id)
#     if(username_in_system(username)):
#         c.execute(f'INSERT INTO {username} VALUES ({story_id}, {edit_id})')
#     db.commit() #save changes
#     #db.close()  #close database
# def get_list_of_stories(username):
    stories = list(c.execute(f'SELECT story_id FROM {username}').fetchall())
    return stories
#returns a list of all stories_id the user has edited
def get_list_of_stories(username, type):
    stories = list(c.execute(f'SELECT {type} FROM {username}').fetchall())
    returnlist = []
    for x in stories:
        returnlist.append(x[0])
    return returnlist

def change_password(username, new_password):
    c.execute(f'UPDATE main SET password = "{new_password}" WHERE username = "{username}"')
    db.commit() #save changes
    #db.close()  #close database

def remove_user(username):
    c.execute(f'DELETE FROM main WHERE username = "{username}"')
    c.execute(f'DROP TABLE {username}')
    db.commit() #save changes
    #db.close()  #close database
#print(get_username_from_id(1))
#c.execute("DROP TABLE")
#print(c.execute('SELECT * FROM main').fetchall())
#signup("Kevin", "1234")
# print(c.execute('SELECT * FROM main').fetchall())
# print(username_in_system("Kevin3"))
# add_into_user_db("Kevin3", 1, 1)
#print(c.execute('SELECT * FROM Kevin3').fetchall())
# # remove_user("Kevin")
#print(c.execute('SELECT * FROM main').fetchall())