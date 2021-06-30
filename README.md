**Please read all the questions before starting the test**

For this exercise, you are not allowed to use any exchange connector Python modules to acces Kraken trade records.

The solution has to be coded in Python 3.9.
 

1. You have been provided with a Kraken (https://www.kraken.com/) trade file, you will find inside a list of trades.
The trader needs to know what his total exposure is. Read the file and calculate what his position is in each traded currency.

2. Some information in the trade file are wrong, you have to reconcile it against the Kraken exchange API. Provide us a csv file containing only the corrected orders.

3. We asked you to not use any exchange connector modules. Can you explain why it could be the case in a real project scenario ?

 
#### Requirements: 

The code must be packaged in a docker image.

The program needs to take as an input a command: `calculateExposure` or `reconcile`.

The program will take as command-line argument `--t` which will be the path to the trade file containing orders to reconcile.

The program must output a file exposure.csv with the exposure.

The program must output a file reconciled_trades.csv with corrected orders.

The code has to be delivered in a GitHub repository.
