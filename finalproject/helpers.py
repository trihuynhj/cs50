import os
import requests
import urllib.parse
import random
import smtplib, ssl

from flask import redirect, render_template, request, session
from functools import wraps
from serpapi import GoogleSearch
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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