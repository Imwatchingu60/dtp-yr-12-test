import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__, template_folder='.', static_folder="static", static_url_path="/static",)

DATABASE = "database.db"

def get_db():
    """Open one database connection fot the current request."""
    db= getattr(g,"_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_kets = ON")
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close the request's database connection, if one was opened"""
    db = getattr(g,"_database", None)
    if db is not None:
        db.close()

def validate_flower(form):
    """Return one message for each invalid field."""
    errors = []

    name = form.get("name", "").strip()
    if not name:
        errors.append("Name is required.")
    elif len(name) > 50:
        errors.append("Name must be 50 characters or fewer.")

    if len(form.get("latin", "").strip()) > 80:
        errors.append("Latin name must be 80 characters or fewer.")

    if not form.getlist("season"):
        errors.append("Choose at least one bloom season.")

    if not form.get("colour_id", ""):
        errors.append("Choose a colour.")
    if not form.get("category_id", ""):
        errors.append("Choose a category.")

    return errors

deef get_form_choices(db):
    """Read the rows used by the two database-backed select controls."""
    colours = db.execute(
        "SELECT id, name FROM colours ORDER BY name"
    ).fetchall()
    categories = db.execute(
        "SELECT id, name FROM categories ORDER BY name"
    ).fetchall()
    return colours, categorie

def submitted_flower(form):
    """Put the submitted values in the same order as the SQL columns."""
    return (
        form.get("name", "").strip(),
        form.get("latin", "").strip(),
        "-".join(form.getlist("season")),
        form.get("sunlight", ""),
        form.get("watering", ""),
        form.get("difficulty", ""),
        form.get("colour_id", ""),
        form.get("category_id", "")
        
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/flowers")
def flowers():
    db = get_db()
    flower_list = db.execute(
        """
        SELECT *,
               colours.name AS category
        FROM flowers
        JOIN colours
          ON flowers.colour_id = colours.id
        JOIN categories
          ON flowers.category_id = categories.id
        ORDER BY flowers.name
        """
    ).fetchall()

    return render_template('flowers.html',flowers=flower_list)


@app.route("/flower/<int:id>")
def flower_detail(id):
    db = get_db()
    flower = db.execute(
        """
        SELECT flowers.*,
               colours.name AS category
        FROM flowers
        JOIN colours
          ON flowers.colour_id = colours.id
        JOIN categories
          ON flowers.category_id = categories.id
        WHERE flowers.id = ?
        """,
        (id,),

    ).fetchone()
    
    return render_template('flower.html', flower=flower)

if __name__ =='__main__':
    app.run(debug=True)