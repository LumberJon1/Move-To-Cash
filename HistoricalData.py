import requests
import datetime

# Base URL for the API
url = "https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data"
url2 = "https://yh-finance.p.rapidapi.com/stock/v3/get-chart"

querystring2 = {"interval":"1d","symbol":"VTSAX","range":"5y","region":"US","includePrePost":"false","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split", "period1": "1496275200", "period2": "1654041600"}

# Querystring parameters
querystring_VTSAX = {"symbol":"VTSAX"}
querystring_VTIAX = {"symbol":"VTIAX"}
querystring_VBTLX = {"symbol":"VBTLX"}
querystring_VTABX = {"symbol":"VTABX"}

# API Key and headers
headers = {
	"X-RapidAPI-Key": "17cf3c4677msh5f3456cbf2d6540p12003fjsna8360ab47844",
	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
}

# res_VTSAX = requests.get(url, headers=headers, params=querystring_VTSAX)
# res_VTIAX = requests.get(url, headers=headers, params=querystring_VTIAX)
# res_VBTLX = requests.get(url, headers=headers, params=querystring_VBTLX)
# res_VTABX = requests.get(url, headers=headers, params=querystring_VTABX)

res2 = requests.request("GET", url2, headers=headers, params=querystring2)
data2 = res2.json()

# Arrays to hold data and timestamps for each analyzed asset
VTSAX_mixed_array = []
VTSAX_timestamp_array = []
VTSAX_prices_array = []

VTIAX_mixed_array = []
VTIAX_timestamp_array = []
VTIAX_prices_array = []

VBTLX_mixed_array = []
VBTLX_timestamp_array = []
VBTLX_prices_array = []

VTABX_mixed_array = []
VTABX_timestamp_array = []
VTABX_prices_array = []



# Function that will traverse the JSON response and fill the data arrays
def fill_array(response_array, timestamp_array, prices_array):

	for item in response_array["chart"]["result"][0]["timestamp"]:
		timestamp_array.append(item)


	for item in response_array["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]:
		prices_array.append(item)
	

	for element in range(len(timestamp_array)):
		mixed_array.append([timestamp_array[element], prices_array[element]])
    

# function to convert dates to readable format from UNIX time
def convertTime(unix_date):
    date = datetime.datetime.fromtimestamp(unix_date)
    month = date.strftime("%b")
    day = date.strftime("%d")
    year = date.strftime("%Y")
    return str(month+" "+day+", "+year)


# Format dates
for date in mixed_array:
    date[0] = convertTime(date[0])
    
print(mixed_array[:50])


# Parse the JSON API response
# data_VTSAX = res_VTSAX.json()
# data_VTIAX = res_VTIAX.json()
# data_VBTLX = res_VBTLX.json()
# data_VTABX = res_VTABX.json()


    
    
# Array to hold adjusted closing prices and their associated dates
# historical_data_VTSAX = []
# historical_data_VTIAX = []
# historical_data_VBTLX = []
# historical_data_VTABX = []

# Append the items in a response to an array
def fill_array(response_array, target_array):
	for item in response_array["prices"]:
		if "adjclose" in item:
			# For now, we will only append the price.  The date may come in handy later.
			# target_array.append([convertTime(item["date"]), item["adjclose"]])
			target_array.append(item["adjclose"])
        

# Run the function on each of the API responses
# fill_array(data_VTSAX, historical_data_VTSAX)
# fill_array(data_VTIAX, historical_data_VTIAX)
# fill_array(data_VBTLX, historical_data_VBTLX)
# fill_array(data_VTABX, historical_data_VTABX)


# Modified array to pass to Main.py which just contains prices
price_data = []
# for item in historical_data:
#     if (item[0] != "No price data"):
#     	price_data.append(item[1])
    

# print("\n\nPrices only: ", price_data[:30])

