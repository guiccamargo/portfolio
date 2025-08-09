import os
from random import choice

import requests
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

URL = "https://the-one-api.dev/v2"

load_dotenv()
app = Flask(__name__)
Bootstrap5(app)


def get_list_of_movies():
    """
    Gets list of the movies from the API
    :return: list of movies.
    """
    response = requests.get(URL + "/movie", headers={"Authorization": f"Bearer {os.getenv("token")}"})
    return reversed(response.json()["docs"][1:])


def get_character(_id):
    """
    Gets the name of a character from API
    :param _id: id of the character
    :return: Name of the character.
    """
    response = requests.get(URL + f"/character/{_id}", headers={"Authorization": f"Bearer {os.getenv("token")}"})
    return response.json()["docs"][0]["name"]


@app.route("/quote")
def random_quote():
    """
    Get a random quote from the movies
    :return: render of the index template.
    """
    response = requests.get(URL + "/quote", headers={"Authorization": f"Bearer {os.getenv("token")}"})
    quote = choice(response.json()["docs"])
    dialog = quote["dialog"]
    character = get_character(quote["character"])
    return render_template("index.html", movies=get_list_of_movies(), quote=dialog, character=character)


@app.route("/")
def home():
    """
    Render the first page
    :return:  of the index template.
    """
    return render_template("index.html", movies=get_list_of_movies())


if __name__ == '__main__':
    app.run(debug=True)
