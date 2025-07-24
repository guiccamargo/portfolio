import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.utils import redirect
from wtforms import StringField, FloatField
from wtforms.fields.simple import BooleanField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


load_dotenv()

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Café TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


# Add Café form
class CafeForm(FlaskForm):
    name = StringField('Café name', validators=[DataRequired()])
    location = StringField('Address', validators=[DataRequired()])
    map_url = StringField("Café Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    img_url = StringField("Photo from the Café (URL)", validators=[DataRequired(), URL()])
    has_wifi = BooleanField(label="Café has Wifi")
    has_sockets = BooleanField(label="Café has power sockets")
    can_take_calls = BooleanField(label="Can take calls")
    has_toilet = BooleanField(label="Have toilets")
    coffee_price = FloatField(label="Coffee price", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    """
    Render index page
    """
    return render_template("index.html", cafes=get_all())


def get_all():
    """
    Get all Cafés from the database
    :return: List of Cafés
    """
    with app.app_context():
        all_cafe = db.session.execute(db.select(Cafe).order_by(Cafe.id),
                                      execution_options={"prebuffer_rows": True}).scalars()
        cafes = []
        for cafe in all_cafe:
            # Convert café to dict
            dict_cafe = {"id": cafe.id, "name": cafe.name, "map_url": cafe.map_url, "img_url": cafe.img_url,
                         "location": cafe.location, "has_toilet": cafe.has_toilet, "has_wifi": cafe.has_wifi,
                         "has_sockets": cafe.has_sockets, "can_take_calls": cafe.can_take_calls,
                         "coffee_price": cafe.coffee_price, }
            cafes.append(dict_cafe)
        return cafes


@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    """
    Render add café form if method is GET, else save the new café in database and redirect to index page.
    """
    if request.method == "GET":
        return render_template("add.html", form=CafeForm())
    else:
        new_cafe = Cafe(name=request.form.get("name"), map_url=request.form.get("map_url"),
                        img_url=request.form.get("img_url"), location=request.form.get("location"),
                        has_toilet=bool(request.form.get("has_toilet")), has_wifi=bool(request.form.get("has_wifi")),
                        has_sockets=bool(request.form.get("has_sockets")),
                        can_take_calls=bool(request.form.get("can_take_calls")),
                        coffee_price=f"BRL {request.form.get('coffee_price')}")
        with app.app_context():
            db.session.add(new_cafe)
            db.session.commit()
    return redirect(url_for("home"))


@app.route("/update-price/<cafe_id>", methods=["GET", "POST"])
def update_cafe(cafe_id):
    """
    Update information from an existing Café
    :param cafe_id: Index of the café to be updated in the database.
    """
    if request.method == "GET":
        with app.app_context():
            cafe_to_update = db.session.get(Cafe, cafe_id)
            form = CafeForm()
        return render_template("update.html", form=form, cafe=cafe_to_update)
    else:
        with app.app_context():
            cafe_to_update = db.session.get(Cafe, cafe_id)
            cafe_to_update.name = request.form.get("name")
            cafe_to_update.location = request.form.get("location")
            cafe_to_update.map_url = request.form.get("map_url")
            cafe_to_update.img_url = request.form.get("img_url")
            cafe_to_update.has_wifi = bool(request.form.get("has_wifi"))
            cafe_to_update.has_toilet = bool(request.form.get("has_toilet"))
            cafe_to_update.has_sockets = bool(request.form.get("has_sockets"))
            cafe_to_update.can_take_calls = bool(request.form.get("can_take_calls"))
            cafe_to_update.coffee_price = f"BRL {request.form.get('coffee_price')}"

            db.session.commit()

    return redirect(url_for("home"))


@app.route("/report-closed/<cafe_id>", methods=["GET"])
def delete_cafe(cafe_id):
    """
    Delete a Café from database
    :param cafe_id: Index of the café in the database
    """
    with app.app_context():
        cafe_to_delete = db.session.get(Cafe, cafe_id)
        if cafe_to_delete is None:
            return redirect(url_for("home"))
        else:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
