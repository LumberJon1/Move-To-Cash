import requests
import datetime

# Base URL for the API
url = "https://yh-finance.p.rapidapi.com/stock/v3/get-chart"

# Beginning and ending periods
period1 = "1496275200"
period2 = "1654041600"


# Querystring parameters
querystring_VTSAX = {"interval":"1d","symbol":"VTSAX","range":"5y","region":"US","includePrePost":"false","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split", "period1": period1, "period2": period2}
querystring_VTIAX = {"interval":"1d","symbol":"VTIAX","range":"5y","region":"US","includePrePost":"false","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split", "period1": period1, "period2": period2}
querystring_VBTLX = {"interval":"1d","symbol":"VBTLX","range":"5y","region":"US","includePrePost":"false","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split", "period1": period1, "period2": period2}
querystring_VTABX = {"interval":"1d","symbol":"VTABX","range":"5y","region":"US","includePrePost":"false","useYfid":"true","includeAdjustedClose":"true","events":"capitalGain,div,split", "period1": period1, "period2": period2}


# API Key and headers
headers = {
	"X-RapidAPI-Key": "17cf3c4677msh5f3456cbf2d6540p12003fjsna8360ab47844",
	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
}

res_VTSAX = requests.get(url, headers=headers, params=querystring_VTSAX)
res_VTIAX = requests.get(url, headers=headers, params=querystring_VTIAX)
res_VBTLX = requests.get(url, headers=headers, params=querystring_VBTLX)
res_VTABX = requests.get(url, headers=headers, params=querystring_VTABX)


# Parse the JSON API responses
data_VTSAX = res_VTSAX.json()
data_VTIAX = res_VTIAX.json()
data_VBTLX = res_VBTLX.json()
data_VTABX = res_VTABX.json()

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


# function to convert dates to readable format from UNIX time
def convertTime(unix_date):
    date = datetime.datetime.fromtimestamp(unix_date)
    month = date.strftime("%b")
    day = date.strftime("%d")
    year = date.strftime("%Y")
    return str(month+" "+day+", "+year)

# Function that will traverse the JSON response and fill the data arrays
def fill_array(response_array, timestamp_array, prices_array, mixed_array):

	for item in response_array["chart"]["result"][0]["timestamp"]:
		timestamp_array.append(item)


	for item in response_array["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]:
		prices_array.append(item)
	

	for element in range(len(timestamp_array)):
		mixed_array.append([timestamp_array[element], prices_array[element]])
    
	# Format dates
	for date in mixed_array:
		date[0] = convertTime(date[0])
      

# Run the function on each of the API responses
fill_array(data_VTSAX, VTSAX_timestamp_array, VTSAX_prices_array, VTSAX_mixed_array)
fill_array(data_VTIAX, VTIAX_timestamp_array, VTIAX_prices_array, VTIAX_mixed_array)
fill_array(data_VBTLX, VBTLX_timestamp_array, VBTLX_prices_array, VBTLX_mixed_array)
fill_array(data_VTABX, VTABX_timestamp_array, VTABX_prices_array, VTABX_mixed_array)

# Dates in readable format for use in main.py
date1 = convertTime(int(period1))
date2 = convertTime(int(period2))
