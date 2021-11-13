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
    
        # Check the usability of the keys
        for key in keys:
            meta = requests.get(f"https://serpapi.com/account?api_key={key}").json()
            if meta["total_searches_left"] > 0:
                API_KEY = key
                break
        
        # Google Search for Images API
        params = {
            "engine": "google",
            "q": keyword,
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "tbm": "isch",                  # Image Search
            "safe": "off",
            "api_key": API_KEY
        }
        if safesearch == 1:
            params["safe"] = "active"

        search = GoogleSearch(params)
    
    except requests.RequestException:
        return None

    # Parse response
    try:
        # Initialize a random seed
        random.seed()
        results = search.get_dict()["images_results"]

        # Make sure to not randomly choose the same image more than once
        image_already_chosen = True;
        while image_already_chosen:
            random_int = random.randint(0, len(results) - 1)
            if not search_history:
                image_already_chosen = False
                break
            for search in search_history:
                if random_int != search["result_position"]:
                    image_already_chosen = False
        
        response = results[random_int]
        return {
            "position": response["position"],
            "title": response["title"],
            "link": response["link"],
            "original": response["original"],
            "thumbnail": response["thumbnail"]
        }

    except (KeyError, TypeError, ValueError):
        return None


def send_email(user, receiver_email, response, time):
    """Send the random image to the specified receiver's email."""

    # Parse response
    title = response["title"]
    original = response["original"]

    