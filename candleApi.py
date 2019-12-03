def getTickers():
    from poloniex import Poloniex
    polo = Poloniex()
    ticker = polo.returnTicker()
    return ticker


database = 'CotacoesCriptomoedas.db'

def addTicker(ticker):
    import time
    import sqlite3
    import uuid

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    for t in ticker:
        id = str(uuid.uuid1())
        last = ticker[t]['last']
        date = time.time()
        cur.execute('INSERT INTO TickerData (id, Name, Last, Date) VALUES (?, ?, ?, ?)',
                    (id, t , last, date))


    conn.commit()
    conn.close()

def getTicker(currentPair):
    import sqlite3

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("select * from TickerData where Name = ? order by date", (currentPair,))
    data = cur.fetchall() 
    conn.close()
    return data



def generateDataToPlot():
    import time

    count = 0
    while True:
        count += 1
        tickers = getTickers()
        addTicker(tickers)
        time.sleep(1)
        if count == 100000000:
            break


def createCandle(currentPair, timeCandle):
    from datetime import datetime

    tickerPlotar = getTicker(currentPair)
    dateOpenFloat = float(tickerPlotar[0][3]) 
    dateOpen = datetime.utcfromtimestamp(dateOpenFloat).strftime("%m/%d/%Y, %H:%M:%S")
    open = tickerPlotar[0][2]
    high = open
    low = open
    close = open
    dateClose = dateOpen

    candles = []
    for t in tickerPlotar:
        if t[2] > high:
            high = t[2]
        if t[2] < low:
            low = t[2]
        if float(t[3]) - dateOpenFloat >= timeCandle:
            close = t[2]
            dateClose = datetime.utcfromtimestamp(float(t[3])).strftime("%m/%d/%Y, %H:%M:%S")
            candles.append([open, high, low, close, dateOpen, dateClose])    

            dateOpenFloat = float(t[3])
            dateOpen = datetime.utcfromtimestamp(dateOpenFloat).strftime("%m/%d/%Y, %H:%M:%S")            
            open = t[2]
            high = open
            low = open
            close = open
            dateClose = dateOpen
    
    return candles

def main():

    candles1Min = createCandle("USDT_BTC", 60)
    print(candles1Min)

main()
#datetime.datetime.utcfromtimestamp(a).strftime("%m/%d/%Y, %H:%M:%S")
#a = time.time()
#time.sleep(2)
#b = time.time()
#
#c = b-a
#
#print(c)
#print(c > 3)

