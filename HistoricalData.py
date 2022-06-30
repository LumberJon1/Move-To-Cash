import requests
import json

# Base URL for the API
url = "https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data"

# Querystring parameters
querystring = {"symbol":"VTSAX"}

# API Key and headers
headers = {
	"X-RapidAPI-Key": "17cf3c4677msh5f3456cbf2d6540p12003fjsna8360ab47844",
	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
}

res = requests.get(url, headers=headers, params=querystring)

# Parse the JSON API response
data = res.json()


# Print out the results
for item in data["prices"]:
    if "adjclose" in item:
        print("\n\nItem: ", item, "\n")
        print("Adjusted Close: ", item["adjclose"])
    else:
        print("No price data")


