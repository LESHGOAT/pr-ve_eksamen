from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

env_User = os.getenv("user") 
env_Password = os.getenv("password")
env_Host = os.getenv("host")
DB_NAME = "mat_oppskrift"

app = Flask(__name__)
app.secret_key = "superhemmelig_nøkkel"

def get_db_connection():
    conn = mysql.connector.connect(
        host=env_Host,
        user=env_User,
        password=env_Password,
        database=DB_NAME
    )
    return conn


@app.route('/')
def index():
    if "username" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM oppskrift")
    recipes = cursor.fetchall()
    conn.close()
    return render_template("index.html", recipes=recipes, username=session["username"])


@app.route('/add', methods=['POST'])
def add_recipe():
    if "username" not in session:
        return redirect("/login")

    try:
        name = request.form.get('name', '').strip()
        ingredienser = request.form.get('ingredienser', '').strip()
        fremgangsmåte = request.form.get('fremgangsmåte', '').strip()
        koketid = request.form.get('koketid', '').strip()
        prsjoner = request.form.get('prsjoner', '').strip()

        if not name or not ingredienser or not fremgangsmåte:
            return "Feil: Alle felt må fylles ut.", 400

        koketid = float(koketid)
        prsjoner = int(prsjoner)

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO oppskrift (name, ingredienser, fremgangsmåte, koketid, prsjoner, added_by)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (name, ingredienser, fremgangsmåte, koketid, prsjoner, session["username"])
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        return redirect('/')
    except Exception as e:
        return f"Det oppstod en feil: {e}", 500


@app.route('/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    if "username" not in session:
        return redirect("/login")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM oppskrift WHERE id = %s", (recipe_id,))
        conn.commit()
        conn.close()
        return redirect('/')
    except Exception as e:
        return f"Kunne ikke slette oppskrift: {e}", 500


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        if not username or not password:
            return "Feil: Alle felt må fylles ut", 400

        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
        except mysql.connector.Error as err:
            return f"Feil ved registrering: {err}", 500
        finally:
            conn.close()

        return redirect("/login")

    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["username"] = username
            return redirect("/")
        else:
            return "Feil brukernavn eller passord", 401

    return render_template("log_in.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


# ── FAQ ──────────────────────────────────────────────
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    if request.method == 'POST':
        navn     = request.form.get('navn', '').strip()
        epost    = request.form.get('epost', '').strip()
        sporsmal = request.form.get('sporsmal', '').strip()

        if not navn or not epost or not sporsmal:
            flash('Alle felt må fylles ut.')
            return redirect('/faq')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO faq (navn, epost, sporsmal) VALUES (%s, %s, %s)",
            (navn, epost, sporsmal)
        )
        conn.commit()
        conn.close()

        flash('Spørsmålet ditt er sendt! Vi svarer så snart vi kan.')
        return redirect('/faq')

    return render_template('faq.html')


@app.route('/slett-data', methods=['GET', 'POST'])
def slett_data():
    print("SLETT DATA ROUTE HIT")
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            flash('Feil brukernavn eller passord. Prøv igjen.')
            conn.close()
            return redirect('/slett-data')

        epost = user["epost"]

        if epost:
            cursor.execute("""
                UPDATE faq
                SET navn = 'Slettet bruker',
                    epost = CONCAT('slettet_', id, '@eksempel.local')
                WHERE epost = %s
            """, (epost,))

        cursor.execute("DELETE FROM saved_recipes WHERE username = %s", (username,))
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))

        conn.commit()
        conn.close()

        session.pop("username", None)
        flash('Alle dine data er slettet.')
        return redirect('/login')

    return render_template('slett_data.html')


if __name__ == "__main__":
    app.run(debug=True)