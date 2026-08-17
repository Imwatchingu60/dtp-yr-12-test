import sqlite3

from flask import Flask, g, render_template

app = Flask(__name__, template_folder='.')

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