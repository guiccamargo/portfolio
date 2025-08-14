import os

import stripe
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import current_user, LoginManager, login_user, UserMixin, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash

from online_shop.forms import RegisterForm, LoginForm

app = Flask(__name__)

Bootstrap5(app)
app.config["SESSION_PERMANENT"] = False

BASE_DOMAIN = "http://127.0.0.1:5000"


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db = SQLAlchemy(model_class=Base)
db.init_app(app)
stripe.api_key = os.getenv("STRIPE_API_KEY")

# Config login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Set Database tables
class Product(db.Model):
    """
    This table stores all the products availible.
    """
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return f"<Product {self.name}>"


class User(UserMixin, db.Model):
    """
    This table stores the registered users.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship between User and Cart tables
    cart_items = db.relationship("Cart", backref="user", lazy="dynamic")

    def __init__(self, email, name, password):
        self.email = email
        self.username = name
        self.password_hash = password

    def __repr__(self):
        return f"<User {self.username}>"


class Cart(db.Model):
    """
    This table store the products that are currently on the cart.
    """
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    quantity = db.Column(db.Integer, default=1)

    # Relationship between Cart and Product tables
    product = db.relationship("Product", backref="in_carts")

    def __repr__(self):
        return f"<Cart {self.user_id} - Product {self.product_id}>"


# Create tables
with app.app_context():
    db.create_all()


def get_all():
    """
    Get all products from database
    :return: list of products
    """
    products = []
    with app.app_context():
        all_products = Product.query.all()
        for product in all_products:
            products.append({
                "id": product.id,
                "img": product.image_url,
                "name": product.name,
                "price": product.price,
            })
    return products


def sum_items() -> int:
    """
    Sum all the items at the current cart
    :return: Result of the sum.
    """
    if not current_user.is_authenticated:
        return None
    with app.app_context():
        _sum = 0
        all_items = db.session.execute(db.select(Cart).where(Cart.user_id == current_user.id)).scalars()
        for item in all_items:
            _sum += item.quantity
    return _sum


def clear_cart():
    """
    Delete all products from the current cart.
    """
    with app.app_context():
        items = Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()


@app.route("/")
def home():
    """
    Render homepage.
    """
    return render_template("index.html", product_list=get_all(), logged_in=current_user.is_authenticated,
                           total_items=sum_items())


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Render login page if request method is GET or if login was not successful else redirect to homepage.
    """
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.email == request.form.get("email"))).scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        if check_password_hash(pwhash=user.password_hash, password=request.form.get("password")):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Password incorrect, please try again.")
            return render_template("login.html", form=LoginForm(), logged_in=current_user.is_authenticated,
                                   total_items=sum_items()
                                   )
    else:
        return render_template("login.html", form=LoginForm(), logged_in=current_user.is_authenticated,
                               total_items=sum_items()
                               )


@app.route("/logout")
def logout():
    """
    Logout user and redirect to homepage.
    """
    logout_user()
    return redirect(url_for("home"))


@app.route("/cart")
def go_to_cart():
    """
    Get all the products from the current cart and render cart page.
    """
    products = []
    with app.app_context():
        all_items = db.session.execute(db.select(Cart).where(Cart.user_id == current_user.id)).scalars()
        for item in all_items:
            if item.product_id == 0:
                continue
            product = db.get_or_404(Product, item.product_id)
            products.append({"name": product.name, "img": product.image_url, "total": product.price * item.quantity,
                             "quantity": item.quantity})
    return render_template("cart.html", products=products, logged_in=True, total_items=sum_items())


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Render the register page if request method is GET or register was not successful else redirect to homepage.
    """
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.email == request.form.get("email"))).scalar()
        if user:
            flash("You’ve already signed up with that email, log in instead!")
            return redirect(url_for("login"))
        else:
            with app.app_context():
                new_user = User(email=request.form.get("email"), name=request.form.get("name"),
                                password=generate_password_hash(request.form.get("password"), method="pbkdf2:sha256",
                                                                salt_length=8))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for("home"))
    else:
        register_form = RegisterForm()
        return render_template("register.html", form=register_form, logged_in=current_user.is_authenticated, )


@app.route("/create-checkout-session", methods=["GET", "POST"])
def create_checkout_session():
    """
    Redirect user to a stripe based checkout page
    """
    all_items = db.session.execute(db.select(Cart).where(Cart.user_id == current_user.id)).scalars()
    line_items = []
    for item in all_items:
        if item.product_id == 0:
            continue
        db_product = db.get_or_404(Product, item.product_id)
        product = stripe.Product.create(name=db_product.name)
        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(db_product.price * 100),
            currency="usd",
        )
        line_items.append({"price": price.id, "quantity": item.quantity})
    try:
        checkout_session = stripe.checkout.Session.create(mode="payment",
                                                          line_items=line_items,
                                                          success_url=BASE_DOMAIN + "/success",
                                                          cancel_url=BASE_DOMAIN + "/cancel"
                                                          )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route("/product/<product_id>")
def buy_product(product_id):
    """
    Add a product to the current cart and redirect to homepage.
    :param product_id: id of the selected product.
    """
    with app.app_context():
        user_id = current_user.id
        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Cart(user_id=user_id, product_id=product_id, quantity=1)
            db.session.add(cart_item)

        db.session.commit()
    return redirect(url_for("home"))


@app.route("/cancel")
def cancel():
    """
    Render the cancel page if checkout was not successful.
    """
    return render_template("cancel.html", logged_in=True, total_items=sum_items())


@app.route("/success")
def success():
    """
    Render the success page if checkout was successful.
    """
    clear_cart()
    return render_template("success.html", logged_in=True, total_items=sum_items())


@app.route("/cart/clear")
def clear_checkout():
    """
    Clear current cart when a user clicks the delect button.
    """
    clear_cart()
    return redirect(url_for("go_to_cart"))


if __name__ == "__main__":
    app.run(debug=True)
