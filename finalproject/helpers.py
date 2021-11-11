import os
import requests
import urllib.parse
import random
import smtplib, ssl

from flask import redirect, render_template, request, session
from functools import wraps
from serpapi import GoogleSearch
from email.mime.text import MIMEText
from email.mime.    multipart import MIMEMultipart


def error(message, code=400):
    """Render an error message to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Contact SerpAPI, search images and return a random image from the search result
def random_image(keyword, search_history, safesearch=0):
    """Return search results from SerpAPI."""

    # Contact API
    try:
        # Prepared keys for SerpAPI services
        keys = ["00608aa6196298194939714d009218033442b305aaa9d243099ea7862716b085", #tri.********@gmail.com
                "24a5a550527b18c291309c572da9069b07d1eeab978bb61e7bfdbcf9120ee1e0", #picprank.cs50@gmail.com
                "e3fea8857bf4d3855db7c7739ac7fb905105a5492a03004623ae1b5d1e166c28"] #ur.*******@gmail.com
        API_KEY = ""