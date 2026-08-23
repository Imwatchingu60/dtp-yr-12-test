import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for


app = Flask(
    __name__,
    template_folder=".",
    static_folder="static",
    static_url_path="/static",
)

DATABASE = "database.db"


def get_db():
    """Open one database connection for the current request."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close the request's database connection, if one was opened."""
    db = getattr(g, "_database", None)
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


def get_form_choices(db):
    """Read the rows used by the two database-backed select controls."""
    colours = db.execute(
        "SELECT id, name FROM colours ORDER BY name"
    ).fetchall()
    categories = db.execute(
        "SELECT id, name FROM categories ORDER BY name"
    ).fetchall()
    return colours, categories


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
        form.get("category_id", ""),
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/flowers")
def flowers():
    db = get_db()
    colours, categories = get_form_choices(db)

    conditions = []
    values = []

    name = request.args.get("name", "").strip()
    if name:
        conditions.append("(flowers.name LIKE ? OR flowers.latin LIKE ?)")
        values.append("%" + name + "%")
        values.append("%" + name + "%")

    seasons = request.args.getlist("season")
    if seasons:
        season_parts = []
        for season in seasons:
            season_parts.append("flowers.season LIKE ?")
            values.append("%" + season + "%")
        conditions.append("(" + " OR ".join(season_parts) + ")")

    for key in ("colour_id", "category_id", "sunlight", "watering", "difficulty"):
        chosen = request.args.getlist(key)
        if chosen:
            marks = ", ".join("?" * len(chosen))
            conditions.append("flowers." + key + " IN (" + marks + ")")
            values.extend(chosen)

    sql = """
        SELECT flowers.*,
               colours.name AS colour,
               categories.name AS category
        FROM flowers
        JOIN colours
          ON flowers.colour_id = colours.id
        JOIN categories
          ON flowers.category_id = categories.id
        """
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY flowers.name"

    flower_list = db.execute(sql, values).fetchall()

    return render_template(
        "flowers.html",
        flowers=flower_list,
        colours=colours,
        categories=categories,
        filters=request.args,
    )


@app.route("/flower/<int:id>")
def flower_detail(id):
    db = get_db()
    flower = db.execute(
        """
        SELECT flowers.*,
               colours.name AS colour,
               categories.name AS category
        FROM flowers
        JOIN colours
          ON flowers.colour_id = colours.id
        JOIN categories
          ON flowers.category_id = categories.id
        WHERE flowers.id = ?
        """,
        (id,),
    ).fetchone()

    if flower is None:
        return "Flower not found", 404

    return render_template("flower.html", flower=flower)


@app.route("/add", methods=["GET", "POST"])
def add_flower():
    db = get_db()
    colours, categories = get_form_choices(db)

    if request.method == "POST":
        errors = validate_flower(request.form)
        if errors:
            return render_template(
                "flower_form.html",
                action="Add",
                errors=errors,
                flower=request.form,
                colours=colours,
                categories=categories,
                picked_seasons=request.form.getlist("season"),
            )

        db.execute(
            """
            INSERT INTO flowers
                (name, latin, season, sunlight, watering, difficulty,
                 colour_id, category_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            submitted_flower(request.form),
        )
        db.commit()
        return redirect(url_for("flowers"))

    return render_template(
        "flower_form.html",
        action="Add",
        errors=[],
        flower={},
        colours=colours,
        categories=categories,
        picked_seasons=[],
    )


@app.route("/flower/<int:id>/edit", methods=["GET", "POST"])
def edit_flower(id):
    db = get_db()
    flower = db.execute(
        "SELECT * FROM flowers WHERE id = ?",
        (id,),
    ).fetchone()

    if flower is None:
        return "Flower not found", 404

    colours, categories = get_form_choices(db)

    if request.method == "POST":
        errors = validate_flower(request.form)
        if errors:
            return render_template(
                "flower_form.html",
                action="Edit",
                errors=errors,
                flower=request.form,
                colours=colours,
                categories=categories,
                picked_seasons=request.form.getlist("season"),
            )

        db.execute(
            """
            UPDATE flowers
            SET name = ?, latin = ?, season = ?, sunlight = ?,
                watering = ?, difficulty = ?, colour_id = ?, category_id = ?
            WHERE id = ?
            """,
            submitted_flower(request.form) + (id,),
        )
        db.commit()
        return redirect(url_for("flower_detail", id=id))

    return render_template(
        "flower_form.html",
        action="Edit",
        errors=[],
        flower=dict(flower),
        colours=colours,
        categories=categories,
        picked_seasons=flower["season"].split("-"),
    )


if __name__ == "__main__":
    app.run(debug=True)
