# GOOGLE IMAGE SEARCH TEST (SERPAPI SERVICES)

import requests
from serpapi import GoogleSearch

#url = "https://serpapi.com/account?api_key=00608aa6196298194939714d009218033442b305aaa9d243099ea7862716b085"
#response = requests.get(url).json()

#print(response)

key = input("Provide a keyword to search: ")
API_KEY = "00608aa6196298194939714d009218033442b305aaa9d243099ea7862716b085"

params = {
    "engine": "google",
    "q": key,
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
    "tbm": "isch",                  # Image Search
    "api_key": API_KEY
}


search = GoogleSearch(params)
results = search.get_dict()
meta = requests.get(f"https://serpapi.com/account?api_key={API_KEY}")