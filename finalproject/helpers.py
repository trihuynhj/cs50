import os
import requests
import urllib.parse
import random
import smtplib, ssl

from flask import redirect, render_template, request, session
from functools import wraps
from serpapi import GoogleSearch