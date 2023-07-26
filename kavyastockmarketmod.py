import pandas as pd
import numpy as np
import time
from datetime import datetime
from functools import reduce



# Create an initial list of sample stock data from the given details
samplestockdata = {'StockSymbol':['TEA', 'POP', 'ALE', 'GIN', 'JOE'],
        'Type':['Common', 'Common','Common','Preferred','Common'],
        'LastDividend':[0, 8, 23, 8,13],
        'FixedDividend':['','', '', '2', ''],
        'ParValue':[100, 100, 60, 100, 250]}

# Converting sample stock data to a DataFrame Format
stockdf = pd.DataFrame(samplestockdata)
print ("Sample Stock data is \n",stockdf)

 
def cal_divyield_peratio(stock,price):

    """
    Function to Calculate the dividend yield and PERatio for a given stock
    Arguments:
        a: stock
        b: price
    Returns:None
    """
    
    stocksymbol = stock
    stocktype=stockdf.loc[stockdf['StockSymbol'] == stocksymbol, 'Type'].iloc[0]
    stocktlastdiv=int(stockdf.loc[stockdf['StockSymbol'] == stocksymbol, 'LastDividend'].iloc[0])
    stockfixdiv=int(stockdf.loc[stockdf['StockSymbol'] == stocksymbol, 'FixedDividend'].iloc[0])
    stockparval=int(stockdf.loc[stockdf['StockSymbol'] == stocksymbol, 'ParValue'].iloc[0])
    stockprice = price
    
    if stocktype == 'Common':
            dividendyield= stocktlastdiv / stockprice if stockprice != 0 else 0
    elif stocktype == 'Preferred':
            dividendyield= ((stockfixdiv/100) * stockparval) / stockprice if stockprice != 0 else 0

    peratio = stockprice / stocktlastdiv if stocktlastdiv != 0 else 0
    
    print ("For the Given Stock",stocksymbol ,"and price ",stockprice,"\n")
    print ("STOCKTYPE :",stocktype, "LASTDIVIDEND:" ,stocktlastdiv ,"FIXEDDIVIDEND:", stockfixdiv ,"PARVALUE:" ,stockparval,"\n")
    print ("Dividend Yield for the given stock is " , dividendyield,"\n")
    print ("PE Ratio for the given stock is " , peratio,"\n")



# List to store sample trades 
sampletrades = []

def record_trade(stocksymbol,quantity, buy_sell,price):
    """
    function to record trade transactions
    Arguments:
        a: stocksymbol
        b: quantity
        c: buy_sell
        d: price
    Returns:None
    """
    
    timestamp = time.time()
    sampletrades.append((timestamp, stocksymbol, quantity, buy_sell,price))
        
#Adding few trade records
record_trade("TEA",10, "buy",100)
record_trade("GIN",20, "sell",200)
record_trade("POP",30, "buy",300)
record_trade("TEA",40, "sell",400)

# Output the sample trades
print(" \n\nThe list of sample trades are\n", sampletrades,"\n")
 
def cal_vol_weightedstockprice():

    """
    function to calculate the Volume Weighted Stock Price
    Arguments: None
    Returns:None
    """
    
    now = time.time()
    past_fifteenmins = now - 15 * 60
  
    validtrades = [trade for trade in sampletrades if past_fifteenmins <= trade[0] <= now]
    if not validtrades:
        return 0
    total_qtyprice = sum([trade[2] * trade[4] for trade in validtrades])
    total_qty = sum([trade[2] for trade in validtrades])
    vol_weightedstockprice = total_qtyprice / total_qty if total_qty != 0 else 0
    print ("based on trades in past 15 minutes Volume Weighted Stock Price is  " , vol_weightedstockprice)

def cal_vol_weightedsinglestockprice(stock):

    """
    function to calculate the Volume Weighted Stock Price for a single stock
    Arguments: stock
    Returns:vol_weightedstockprice
    """
    
    stock = stock
    total_qty = 0
    total_price = 0
    stocktrade = []
    
    for i in range((len(sampletrades))):
        if sampletrades[i][1]==stock:
            result = sampletrades[i]
            stocktrade.append(result)

    #print("\n The stock trades are \n",stocktrade)
    
    total_qtyprice = sum([trade[2] * trade[4] for trade in stocktrade])
    total_qty = sum([trade[2] for trade in stocktrade])
    vol_weightedstockprice = total_qtyprice / total_qty if total_qty != 0 else 0
    print (" Volume Weighted Stock Price for a given stock ",stock,"is",vol_weightedstockprice)
    return vol_weightedstockprice
 
def cal_gbce_allshareindex():

    """
    function to calculate the GBCE All Share Index using the geometric mean of prices for all stocks
    Arguments: None
    Returns:gbce_allshareindex
    """
    
    prices = []
    stocklist = stockdf["StockSymbol"].tolist()
    print("\n\n\n")
    print(" The list of stocks are",stocklist)
    for stock in stocklist:
        prices.append(cal_vol_weightedsinglestockprice(stock))
        
    nonzero_prices = [price for price in prices if price != 0]
    print ("Non Zero prices are " ,nonzero_prices)
    
    if not nonzero_prices:
        return 0

    gbce_allshareindex = reduce(lambda x, y: x * y, nonzero_prices) ** (1 / len(nonzero_prices))
    print ("GBCE All share Index for all stocks is ",gbce_allshareindex)
    return gbce_allshareindex
   
    
##########CALLING FUNCTIONS#########################
    
#Calculate dividend yield of stock of your choice
cal_divyield_peratio("GIN",50)

cal_vol_weightedstockprice()

#cal_vol_weightedsinglestockprice("TEA")
cal_gbce_allshareindex()






