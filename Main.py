# Define array to hold output return data
iteration_results = []

# Set cash_out_duration for use in the functions
cash_out_duration = 3

# Define beginning and ending date ranges in UNIX time and as array-iterable integers
begin_unix = 1483228800
end_unix = 1655942400

date_begin = 0
date_end = 1376

# Organize Data Arrays
VTSAX_historical_data = [92.1, 91.1, 91.57, 89.48, 89.1, 92.32, 90.94, 91.25, 95.15, 98.04, 100.47, 101.58, 100.54, 100.21]
VTIAX_historical_data = [27.39, 27.48, 27.77, 27.36, 27.78, 28.41, 27.97, 28.09, 29.09, 29.68, 30.32, 30.53, 30.46, 30.31]
VBTLX_historical_data = [9.87, 9.84, 9.76, 9.8, 9.8, 9.77, 9.67, 9.73, 9.89, 9.97, 10.01, 9.98, 10.04, 10.06]
VTABX_historical_data = [20.01, 19.71, 19.56, 19.42, 19.56, 19.51, 19.58, 19.36, 19.51, 19.74, 19.84, 19.91, 19.98, 19.94]
VMFFX_historical_data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


# Define beginning excluded dates
excluded_dates = []
for date in range(cash_out_duration):
	excluded_dates.append(date)

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


# Function that will compute weighted portfolio change
def portfolio_change(date_index, VTSAX_weight, VTIAX_weight, VBTLX_weight, VTABX_weight, VMFFX_weight):
	# For each asset in the portfolio, compute the weighted change by subtracting the price at the current index - the price at the previous index
	# from the corresponding historical data array and dividing by the prior day change, then multiplyingf by the weight

    VTSAX_change = VTSAX_weight * ((VTSAX_historical_data[date_index] - VTSAX_historical_data[date_index - 1]) / VTSAX_historical_data[date_index - 1])
    VTIAX_change = VTIAX_weight * ((VTIAX_historical_data[date_index] - VTIAX_historical_data[date_index - 1]) / VTIAX_historical_data[date_index - 1])
    VBTLX_change = VBTLX_weight * ((VBTLX_historical_data[date_index] - VBTLX_historical_data[date_index - 1]) / VBTLX_historical_data[date_index - 1])
    VTABX_change = VTABX_weight * ((VTABX_historical_data[date_index] - VTABX_historical_data[date_index - 1]) / VTABX_historical_data[date_index - 1])
    VMFFX_change = VMFFX_weight * ((VMFFX_historical_data[date_index] - VMFFX_historical_data[date_index - 1]) / VMFFX_historical_data[date_index - 1])
    
    # Sum the percent change and return
    portfolio_chg = VTSAX_change + VTIAX_change + VBTLX_change + VTABX_change + VMFFX_change
    
    return portfolio_chg


# Functions to assign cash-out and reinvestment dates  
def progress_excluded_dates(progression=1):
    for date in range(len(excluded_dates)):
        excluded_dates[date] += progression
	
def evaluate_HPR(balance_array):
    HPR = (balance_array[-1] - balance_array[0]) / balance_array[0]
    return round(HPR, 4)

# Main Function that will loop through each dataset and compute % change with excluded date ranges
def iterate_return():
    
    balance = beginning_balance
    balance_array = []	

	# Will need to take a beginning and ending date - for now using length of historical data arrays
    for day in range(len(VTSAX_historical_data)):
        
        # TODO: Check that the set weights are working correctly
        # If the date is in the excluded dates range, switch the weights
        if (day in excluded_dates):
            VTSAX_weight = 0
            VTIAX_weight = 0
            VBTLX_weight = 0
            VTABX_weight = 0
            VMFFX_weight = 0   
        else:
            VTSAX_weight = 0.36
            VTIAX_weight = 0.24
            VBTLX_weight = 0.28
            VTABX_weight = 0.12
            VMFFX_weight = 0.00
        
        # Run portfolio_change for each date, excluding date 0
        if (day != 0):
            day_change = portfolio_change(day, VTSAX_weight, VTIAX_weight, VBTLX_weight, VTABX_weight, VMFFX_weight)
            
            # Add or subtract that change from the prior day's balance
            balance = round(balance * (1 + day_change), 2)
            
            # Assign the resulting balance to a balance_array
            balance_array.append(balance)
            
    # Run the evaluate_HPR function on the balance_array
    HPR = evaluate_HPR(balance_array)
    
    # Return HPR result
    return HPR


# Run the baseline comparison for leaving the assets invested without a cash-out period
cash_out_duration = 0
base_case_HPR = iterate_return()
iteration_results.append(base_case_HPR)
print("Base Case:", iteration_results)

# Reset the cash out duration
cash_out_duration = 3

# Loop through iterate_return, progressing the excluded dates and appending to iteration_results,
# as long as exclusion_date doesn't exceed the dataset range
for iteration in range(len(VTSAX_historical_data) - cash_out_duration):
    print("\nRunning iteration ", iteration)
    result = iterate_return()
    iteration_results.append(result)
    progress_excluded_dates()
    
print("\n\nIteration results: ", iteration_results)

# Function to evaluate the percentage of iterations that over- or under-performed the base case
# where the assets were never pulled out to cash

def evaluate_successes():
    count_success = 0
    for result in iteration_results:
        if (result > iteration_results[0]):
            count_success += 1
    
    proportion_success = count_success / (len(iteration_results) - 1)
    print("\n\nProbability of outperforming the market by pulling to cash for "+str(cash_out_duration)+" days:\n")
    print(str(round(proportion_success * 100, 2))+"%")

evaluate_successes()
