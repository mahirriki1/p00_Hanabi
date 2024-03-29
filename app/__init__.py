from flask import Flask, request, render_template, session, redirect
import db_articles, db_users
import random as ran
# account to use for test:
# Kevin:1234
# hello:lol
# hi:hello

app = Flask(__name__)
# generated via terminal command: python3 -c 'import secrets; print(secrets.token_hex())'
app.secret_key = 'b52635eab6be8ca4c07bd65adc04b27d11a8e251b1e3d16825b881497b1c7af1'

@app.route("/", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return render_template('home.html')
    return render_template('login.html')

# the home page; if the user is not logged in, redirect to login page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # for logging in
        if request.form.get("sub0") == "login":
            username = request.form['username']
            password = request.form['password']
            # this set of if statements is for checking if user is in system; if in system, check if password is correct
            # if password is incorrect, return to login page and say wrong password
            if db_users.username_in_system(username):
                if db_users.get_password(username) == password:
                    session['username'] = username
                    print(session)
                    return render_template('home.html')
                else:
                    return render_template('login.html', error = "Wrong password.")
            else:
                # for blank username/password
                if "" == username or "" == password:
                    return render_template('login.html', error = "Enter a username and/or password.")
                # if the username is not found in the database, returns an error with username not in system
                return render_template('login.html', error = "Username not in system.")
        # for registering
        elif request.form.get("sub0") == "register":
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            # to check if username is already registered
            if db_users.username_in_system(new_username):
                return render_template('login.html', error = "Username in system.")
            # for blank username/password
            elif "" == new_username or "" == new_password:
                return render_template('login.html', error = "To register, enter a username and/or password.")
            # if successful, the code under runs and makes an account to the database
            else:
                db_users.signup(new_username, new_password)
                session['username'] = new_username
                print(session)
                return render_template('home.html')
    return render_template('login.html')

#give route to a random story
@app.route('/random', methods=['GET', 'POST'])
def random():
    id = db_articles.get_random_article()
    return redirect(f'/{id}/', code=302)
@app.route('/random_edit', methods=['GET', 'POST'])
def random_edit():
    id_list = db_articles.get_list_of_stories('story_id')
    username = session['username']
    story_id = db_users.get_list_of_stories(username, 'story_id')
    for element in id_list:
        if element in story_id:
            id_list.remove(element)
    if(len(id_list) == 0):
        return render_template('home.html', error = "No story to edit")
    num = ran.randint(0, len(id_list)-1)
    id = id_list[num]
    return redirect(f'/{id}/edit/', code=302)
# return the create story page
@app.route('/create_page', methods=['GET', 'POST'])
def create_page():
    return render_template('create.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    story_names = db_articles.get_list_of_stories('story_name')
    text = request.form['search']
    search_results = []
    story_id = []
    for elements in story_names:
        if(text in elements):
            search_results.append(elements)
    for x in search_results:
        temp1 = db_articles.id_from_name(x)
        story_id.append(temp1)
    length = len(story_id)
    return render_template('results.html', leng = length, a = search_results, b = story_id)

@app.route('/myStories', methods=['GET', 'POST'])
def myStories():
    username = session['username']
    story_id = db_users.get_list_of_stories(username, 'story_id')
    story_names = []
    for x in story_id:
        temp1 = db_articles.name_from_id(x)
        story_names.append(temp1)
    length = len(story_names)
    return render_template('projects.html', leng = length, a = story_names, b = story_id)

@app.route('/stories', methods=['GET', 'POST'])
def stories():
    story_names = db_articles.get_list_of_stories('story_name')
    story_id = db_articles.get_list_of_stories('story_id')
    length = len(story_names)
    # composition = []
    # for x in range(0, len(story_names)):
    #     temp1 = 
    return render_template('popular.html', leng = length, a = story_names, b = story_id)

# the webpage for creating stories
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        story = request.form['story']
        # for blank title/text
        if "" == title or "" == story:
            return render_template('create.html', error = "Enter a title and/or text.")
        # if successful, the code under runs and makes a story to the database
        else:
            db_articles.add_entry(title, story, db_users.get_id_from_username(session['username']), False)
            return redirect('/')

# webpage for displaying stories
@app.route('/<int:story_id>/', methods=['GET', 'POST'])
def display(story_id):
    text = db_articles.get_full_story_id(story_id)
    title = db_articles.name_from_id(story_id)
    return render_template( 'display.html', display = text, ARTICLE_TITLE=title, story_id=story_id)

# webpage for editing stories
@app.route('/<int:story_id>/edit/', methods=['GET', 'POST'])
def edit(story_id):
    username = session['username']
    stories = db_users.get_list_of_stories(username, 'story_id')
    story_name = db_articles.name_from_id(story_id)
    Prev = db_articles.get_newest_edit(story_name)
    title = db_articles.name_from_id(story_id)
    edited = story_id in stories
    print(edited)
    if request.method == 'POST':
        edit = request.form['story']
        # for blank text
        if "" == edit:
            return render_template('edit.html', error = "Enter an edit.")
        else:
            db_articles.add_entry(title, edit, db_users.get_id_from_username(session['username']), True)
            return redirect('/')
    return render_template('edit.html', prev = Prev, title = title, story_id = story_id, edited = edited)

@app.route('/logout')
def logout():
    # db_users.remove_user(session['username'])
    session.pop('username', None) # remove the username from the session if it's there
    return render_template('login.html', error = "Logged out.")

if __name__ == "__main__":
    app.debug = True 
    app.run() 