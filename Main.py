# import HistoricalData

# Define array to hold output return data
iteration_results = []

# Set cash_out_duration for use in the functions
cash_out_duration = 90

# Define beginning and ending date ranges in UNIX time and as array-iterable integers
begin_unix = 1483228800
end_unix = 1655942400

date_begin = 0
date_end = 1376

# Organize Data Arrays
# VTSAX_historical_data = HistoricalData.VTSAX_prices_array
# VTIAX_historical_data = HistoricalData.VTIAX_prices_array
# VBTLX_historical_data = HistoricalData.VBTLX_prices_array
# VTABX_historical_data = HistoricalData.VTABX_prices_array
# VMFXX_historical_data = []

# Fill VMFXX with $1 entries for the length of the other arrays
for entry in range(len(VTSAX_historical_data)):
    VMFXX_historical_data.append(1)


# Define beginning excluded dates
excluded_dates = []
for date in range(cash_out_duration):
	excluded_dates.append(date)


# Define base weights
VTSAX_weight = 0.36
VTIAX_weight = 0.24
VBTLX_weight = 0.28
VTABX_weight = 0.12
VMFXX_weight = 0.00

# Define starting portfolio balance
beginning_balance = 100000


# Function that will compute weighted portfolio change
def portfolio_change(date_index, VTSAX_weight, VTIAX_weight, VBTLX_weight, VTABX_weight, VMFXX_weight):
	# For each asset in the portfolio, compute the weighted change by subtracting the price at the current index - the price at the previous index
	# from the corresponding historical data array and dividing by the prior day change, then multiplyingf by the weight

    VTSAX_change = VTSAX_weight * ((VTSAX_historical_data[date_index] - VTSAX_historical_data[date_index - 1]) / VTSAX_historical_data[date_index - 1])
    VTIAX_change = VTIAX_weight * ((VTIAX_historical_data[date_index] - VTIAX_historical_data[date_index - 1]) / VTIAX_historical_data[date_index - 1])
    VBTLX_change = VBTLX_weight * ((VBTLX_historical_data[date_index] - VBTLX_historical_data[date_index - 1]) / VBTLX_historical_data[date_index - 1])
    VTABX_change = VTABX_weight * ((VTABX_historical_data[date_index] - VTABX_historical_data[date_index - 1]) / VTABX_historical_data[date_index - 1])
    VMFXX_change = VMFXX_weight * ((VMFXX_historical_data[date_index] - VMFXX_historical_data[date_index - 1]) / VMFXX_historical_data[date_index - 1])
    
    # Sum the percent change and return
    portfolio_chg = VTSAX_change + VTIAX_change + VBTLX_change + VTABX_change + VMFXX_change
    
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
        
        # If the date is in the excluded dates range, switch the weights
        if (day in excluded_dates):
            VTSAX_weight = 0
            VTIAX_weight = 0
            VBTLX_weight = 0
            VTABX_weight = 0
            VMFXX_weight = 0   
        else:
            VTSAX_weight = 0.36
            VTIAX_weight = 0.24
            VBTLX_weight = 0.28
            VTABX_weight = 0.12
            VMFXX_weight = 0.00
        
        # Run portfolio_change for each date, excluding date 0
        if (day != 0):
            day_change = portfolio_change(day, VTSAX_weight, VTIAX_weight, VBTLX_weight, VTABX_weight, VMFXX_weight)
            
            # Add or subtract that change from the prior day's balance
            balance = round(balance * (1 + day_change), 2)
            
            # Assign the resulting balance to a balance_array
            balance_array.append(balance)
            
    # Run the evaluate_HPR function on the balance_array
    HPR = evaluate_HPR(balance_array)
    
    # Return HPR result
    return HPR
          

# Function to generate the base_data chart for data visualization
def generate_chart_data():
    balance = beginning_balance
    balance_array = []
    
    VTSAX_weight = 0.36
    VTIAX_weight = 0.24
    VBTLX_weight = 0.28
    VTABX_weight = 0.12
    VMFXX_weight = 0.00
    
    for day in range(len(VTSAX_historical_data)):
        if (day != 0):
            day_change = portfolio_change(day, VTSAX_weight, VTIAX_weight, VBTLX_weight, VTABX_weight, VMFXX_weight)
            
            # Add or subtract that change from the prior day's balance
            balance = round(balance * (1 + day_change), 2)
            
            # Assign the resulting balance to a balance_array
            balance_array.append([HistoricalData.convertTime(HistoricalData.VTSAX_timestamp_array[day]), "$"+str(balance)])
    
    return balance_array  


# Run the baseline comparison for leaving the assets invested without a cash-out period
cash_out_duration = 0
base_case_HPR = iterate_return()
iteration_results.append(base_case_HPR)

# Reset the cash out duration
cash_out_duration = 90

# Loop through iterate_return, progressing the excluded dates and appending to iteration_results,
# as long as exclusion_date doesn't exceed the dataset range
for iteration in range(len(VTSAX_historical_data) - cash_out_duration):
    result = iterate_return()
    iteration_results.append(result)
    progress_excluded_dates()
    
# print("\n\nIteration results: ", iteration_results)


# Function to evaluate the percentage of iterations that over- or under-performed the base case
# where the assets were never pulled out to cash

def evaluate_successes():
    count_success = 0
    for result in iteration_results:
        if (result > iteration_results[0]):
            count_success += 1
    
    # Compute statistics for the dataset of iteration results
    best_performance = 0
    worst_performance = 1
    beginning_date = HistoricalData.date1
    ending_date = HistoricalData.date2
    
    for element in iteration_results:
        if element > best_performance:
            best_performance = element
        elif element < worst_performance:
            worst_performance = element
        
        sum_iterations = sum(iteration_results)
        mean_performance = sum_iterations / len(iteration_results)
    
    
    proportion_success = count_success / (len(iteration_results) - 1)
    print("\n------------------------------------------------------------\n")
    print("Time period analyzed: "+beginning_date+" to "+ending_date)
    print("Base case HPR:", str((base_case_HPR * 100))+"%")
    print("\nProbability of outperforming the market by pulling to cash for "+str(cash_out_duration)+" days:")
    print(str(round(proportion_success * 100, 2))+"%\n")
    print("Best cash-out scenario return:", str(round((best_performance * 100), 2))+"%")
    print("Worst cash-out scenario return", str(round((worst_performance * 100), 2))+"%")
    print("Average cash-out scenario return", str(round(mean_performance * 100, 2))+"%")

# evaluate_successes()
