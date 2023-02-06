# Move-To-Cash
The Move to Cash Tool tests the likelihood that over a given period of historical stock or
Mutual Fund/ETF data, any rolling period of pulling the investments out to cash would yield
a higher or lower return than the base case of leaving the money invested.

## Methodology
Historical data is taken (for example, from Yahoo Finance) and loaded into arrays.  A weight is then
assigned to each of the asset arrays that will total 100%.  A substitute set of weights is also loaded,
which will be used for any designated periods where the investor pulls the money out to a more conservative asset mix.  This could be 100% cash, or simply a safer mix of alternate investments.  The length of a move to cash is also defined, and must be less than the length of the historical data arrays.  A calculation is then run to compute a hypothetical $100,000 starting portfolio's growth over the length of the historical data, using the portfolio weights assigned.  This calculation is run multiple times, and on each iteration, the beginning and ending dates of any cash out event are progressed forward.  For example, a cash out period of 10 days might be assumed to begin at index 0, and lasting for the first 10 days of the historical data, after which the portfolio weights would switch to their more aggressive base weights.  Then on the second iteration the calculations would run again, this time beginning the cash out on index 1 and lasting through day 11.  This process is repeated until the cash out event spans the last days of the historical data.  The Holding Period Return is then assigned to an array after each iteration, and compared to find the number of scenarios where the cash out would have been more beneficial than holding the assets in the investments for the entire duration, vs. how many would have underperformed the base case.

## Screenshot


## Development
* Built originally using notepad and excel to test data
* Transferred to VS Code and compiled/run in Python
* By Jonathan Williams (GitHub.com/LumberJon1)