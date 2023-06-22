from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import subprocess, uuid, os
import httpretty
from score import Scoreboard
from password_strength import check_password_strength

app = Flask(__name__, static_folder='static')
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'Admin1232022' 
app.config['MYSQL_DB'] = 'laro_tayo' 
app.secret_key = 'LV.s.$nIxC]!u@A'

print("MySQL Configuration:")
print("Host:", app.config['MYSQL_HOST'])
print("User:", app.config['MYSQL_USER'])
print("Database:", app.config['MYSQL_DB'])

mysql = MySQL(app)
game_process = None
scoreboard = Scoreboard()
   
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/sign_up', methods=['GET', 'POST']) # Inserts user input into players table
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        password_strength = check_password_strength(password) # password criteria
        
        if password_strength == 'Weak':
            return render_template('sign_up.html', error_message='Password is weak. Must be 8 characters long, and consists of uppercase and lowercase letters, numbers, and special characters.', email=email)
        
        elif password_strength == 'Fair':
            return render_template('sign_up.html', error_message='Password is fair. Must be 8 characters long, and consists of uppercase and lowercase letters, numbers, and special characters.', email=email)
        
        elif password_strength == 'Strong':
            uid = str(uuid.uuid4())
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO players (id, email, password) VALUES (%s, %s, %s)", (uid, email, password))
            mysql.connection.commit()
            cur.close()
            
            # Set the session variable for the logged-in user
            session['id'] = uid
            
            return redirect('/home')
        
    else:
        return render_template('sign_up.html')

    return render_template('sign_up.html')


@app.route('/log_in', methods=['GET', 'POST']) # Verifies if user input matches players data
def log_in():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM players WHERE email = %s AND password = %s", (email, password))
        player = cur.fetchone()
        cur.close()
        
        if player:
            session['id'] = player[0] 
            return redirect ('/home')
        else:
            return render_template('log_in.html')
        
    return render_template('log_in.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/launch_game')
def launch_game():
    subject = request.args.get('subject')
    global game_process
    
    if game_process is not None and game_process.poll() is None:
        return redirect ('/home')
    
    if 'id' in session:
        id = session.get('id')

        if subject == 'Mathematics':
            game_path = os.path.join(app.root_path, 'main.py')
            game_process = subprocess.Popen(['python', game_path, str(session.get('id')), str(mysql_conn), 'math_score'], cwd=app.root_path) # Launches the game
        elif subject == 'Science':
            game_path = os.path.join(app.root_path, 'main_s.py')
            game_process = subprocess.Popen(['python', game_path, str(session.get('id')), str(mysql_conn), 'science_score'], cwd=app.root_path)

        session['score'] = 0
        return redirect('/home')
    else:
        return redirect('log_in')

current_score = 0

@app.route('/submit_score', methods=['POST'])
def submit_score():
    user_id = session['id']
    math_score = request.form.get('math_score')
    science_score = request.form.get('science_score')

    if 'id' in session:
        if math_score is not None:
            scoreboard.insert_math_score(mysql.connection, int(math_score), user_id) # calls the function from the score.py
        if science_score is not None:
            scoreboard.insert_science_score(mysql.connection, int(science_score), user_id)
        return "Score(s) inserted"
    else:
        return "Failed to insert score(s)"

@app.route('/update_score', methods=['POST'])
def update_score():
    action = request.form.get('action')

    if 'id' in session:
        
        httpretty.register_uri( # mock HTTP
            httpretty.POST,
            'http://localhost/submit_score',
            body='Score inserted',
            status=200
        )

        if action == 'restart':
            session['score'] = 0


    return redirect('/home')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/scores')
def scores():
    if 'id' in session:
        user_id = session['id']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT math_score, total_time FROM score WHERE user_id = %s AND math_score != 0", (user_id,))
        math_scores = cur.fetchall()

        cur.execute("SELECT science_score, total_time FROM score WHERE user_id = %s AND science_score != 0", (user_id,))
        science_scores = cur.fetchall()

        cur.close()

        return render_template('scores.html', math_scores=math_scores, science_scores=science_scores)
    else:
        return redirect('/log_in')
    
@app.route('/guest_home')
def guest_home():
    return render_template('guest_home.html')

if __name__ == '__main__':
    mysql_conn = mysql.connection
    app.run(debug=True)
