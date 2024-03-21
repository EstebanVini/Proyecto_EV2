import requests
import os
import json
import dotenv
from dotenv import load_dotenv
from app.models.models import Movie, TitlePosterImageModel


def search_movie(title):
    url = "https://imdb146.p.rapidapi.com/v1/find/"

    querystring = {"query": title}

    headers = {
        "X-RapidAPI-Key": "fe7738f036mshfe1b74affad0815p18ae28jsn3d82bbce7921",
        "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()

    results = response['titleResults']['results']
    results = json.dumps(results)
    return results

