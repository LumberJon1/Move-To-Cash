# Organize Data Arrays
VTSAX_historical_data = [92.1, 91.1, 91.57, 89.48, 89.1, 92.32, 90.94, 91.25, 95.15, 98.04, 100.47, 101.58, 100.54, 100.21]
VTIAX_historical_data = [27.39, 27.48, 27.77, 27.36, 27.78, 28.41, 27.97, 28.09, 29.09, 29.68, 30.32, 30.53, 30.46, 30.31]
VBTLX_historical_data = [9.87, 9.84, 9.76, 9.8, 9.8, 9.77, 9.67, 9.73, 9.89, 9.97, 10.01, 9.98, 10.04, 10.06]
VTABX_historical_data = [20.01, 19.71, 19.56, 19.42, 19.56, 19.51, 19.58, 19.36, 19.51, 19.74, 19.84, 19.91, 19.98, 19.94]
VMFFX_historical_data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Define array to hold output return data
iteration_results = []

# Define variables like cash hold duration
cash_out_duration = 0

# Define beginning and ending date ranges in UNIX time and as array-iterable integers
begin_unix = 1483228800
end_unix = 1655942400

date_begin = 0
date_end = 1376

# Define beginning excluded dates
excluded_dates = []
for date in range(cash_out_duration):
	excluded_dates.append(date)

print("\nExcluded dates: ", excluded_dates)

# Define URL format for later if I want to scrape data
url = "https://finance.yahoo.com/quote/VTSAX/history?period1=1483228800&period2=1655942400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"

# Define base weights
VTSAX_weight = 0.36
VTIAX_weight = 0.24
VBTLX_weight = 0.28
VTABX_weight = 0.12
VMFFX_weight = 0.00

# Define starting portfolio balance
beginning_balance = 100000

# Function that will switch portfolio weights to the cash-pullout base weights
def set_cash_weights():
	VTSAX_weight = 0.00
	VTIAX_weight = 0.00
	VBTLX_weight = 0.00
	VTABX_weight = 0.00
	VMFFX_weight = 1.00


def set_base_weights():
	VTSAX_weight = 0.36
	VTIAX_weight = 0.24
	VBTLX_weight = 0.28
	VTABX_weight = 0.12
	VMFFX_weight = 0.00


# Function that will compute weighted portfolio change
def portfolio_change(date_index):
	# For each asset in the portfolio, compute the weighted change by subtracting the price at the current index - the price at the previous index
	# from the corresponding historical data array and dividing by the prior day change, then multiplyingf by the weight

	VTSAX_change = VTSAX_weight * ((VTSAX_historical_data[date_index] - VTSAX_historical_data[date_index - 1]) / VTSAX_historical_data[date_index - 1])
	VTIAX_change = VTIAX_weight * ((VTIAX_historical_data[date_index] - VTIAX_historical_data[date_index - 1]) / VTIAX_historical_data[date_index - 1])
	VBTLX_change = VBTLX_weight * ((VBTLX_historical_data[date_index] - VBTLX_historical_data[date_index - 1]) / VBTLX_historical_data[date_index - 1])
	VTABX_change = VTABX_weight * ((VTABX_historical_data[date_index] - VTABX_historical_data[date_index - 1]) / VTABX_historical_data[date_index - 1])
	VMFFX_change = VMFFX_weight * ((VMFFX_historical_data[date_index] - VMFFX_historical_data[date_index - 1]) / VMFFX_historical_data[date_index - 1])

	# Compute the portfolio change by summing the individual asset percent changes
	portfolio_chg = VTSAX_change + VTIAX_change + VBTLX_change + VTABX_change + VMFFX_change

	print("\nPortfolio % change: "+str(round(portfolio_chg * 100, 2))+"%")
	return portfolio_chg


# Function that will compute the resulting HPR for a portfolio
def evaluate_HPR(balance_array):
	"""Takes an array of portfolio balances, and computes HPR"""
	HPR = (balance_array[-1] - balance_array[0]) / balance_array[0]

	return round(HPR, 2)

# Functions to assign cash-out and reinvestment dates
def progress_excluded_dates(progression=1):
	"""Takes each index of excluded_dates and increments by a progression factor, which defaults to 1"""
	for date in excluded_dates:
		date += progression 
	


# Main Function that will loop through each dataset and compute % change with excluded date ranges
def iterate_return():
    
    print("Went into iterate_return function")
    
    balance = beginning_balance
    balance_array = []	

	# Will need to take a beginning and ending date - for now using length of historical data arrays
    for day in range(len(VTSAX_historical_data)):
        
        # If the date is in the excluded dates range, switch the weights
        if (day in excluded_dates):
            set_cash_weights()
            print("Setting weights to cash weights")
        else:
            set_base_weights()
            print("Using base weights")
        
        # Run portfolio_change for each date, excluding date 0
        if (day != 0):
            day_change = portfolio_change(day)
            
            # Add or subtract that change from the prior day's balance
            balance += day_change
            
            # Assign the resulting balance to a balance_array
            balance_array.append(balance)
            
    # Run the evaluate_HPR function on the balance_array
    HPR = evaluate_HPR(balance_array)
    
    # Return HPR result
    return HPR

# Loop through iterate_return, progressing the excluded dates and appending to iteration_results,
# as long as exclusion_date doesn't exceed the dataset range
for iteration in range(len(VTSAX_historical_data) - cash_out_duration):
    print("\nRunning iteration ", iteration)
    result = iterate_return()
    iteration_results.append(result)
    progress_excluded_dates()
    
print("\n\nIteration results: ", iteration_results)