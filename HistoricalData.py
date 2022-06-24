import requests
from bs4 import BeautifulSoup

# Base URL for the API
url = "https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data"

# Querystring parameters
querystring = {"symbol":"VTSAX"}

# API Key and headers
headers = {
	"X-RapidAPI-Key": "17cf3c4677msh5f3456cbf2d6540p12003fjsna8360ab47844",
	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text[:10000])

# Parse the data with BeautifulSoup

