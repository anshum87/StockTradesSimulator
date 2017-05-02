import trade
from trade import DataLoader
from objc._objc import NULL

class CurrStockEntry:
        stock_data_entry = NULL
        status = "NOPOS"
        curr_price = 0.0
        amount = 0.0
        def __init__(self, stock_data_entry):
            self.stock_data_entry = stock_data_entry;
            self.status = "NOPOS"
            self.curr_price = 0.0
            self.amount = 0.0


class TradeExecutor:
           
        class CurrStockData:
            stock_map = dict()
            trans_date_map = dict()
            
            def __init__(self, stock_data):
                for stock_entry in stock_data:
                    self.stock_map[stock_data[stock_entry].stock_name] = \
                            CurrStockEntry(stock_data[stock_entry])

                    print stock_data[stock_entry].stock_name;
                    
                    for curr_date in stock_data[stock_entry].trans_map :
                        self.trans_date_map.setdefault(curr_date, []). \
                        append(stock_data[stock_entry].stock_name)
                        
            
        def ExecTrades(self, data_loader, origAmt, k, num_consec):
            curr_stock_data = self.CurrStockData(data_loader.stock_data)
            n = data_loader.stock_data.__len__()
            totalAmt=origAmt

            num_dates = curr_stock_data.trans_date_map.__len__();
            
            i = 0;

            
            if n < 2 :
               return totalAmt

            d=0;

            for td_date in sorted(curr_stock_data.trans_date_map):
                i=0
                for stock_name in curr_stock_data.trans_date_map[td_date]:

                    stock_daily_trans =  curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date]

                    if (curr_stock_data.stock_map[stock_name].status == "NOPOS" and
                                          stock_daily_trans.low_price <= (100 - k) / 100 * \
                                              curr_stock_data.stock_map[stock_name].curr_price) :
                        curr_stock_data.stock_map[stock_name].amount = totalAmt / (n - i)
                        totalAmt -= totalAmt / (n - i)
                        curr_stock_data.stock_map[stock_name].curr_price= stock_daily_trans.low_price;
                        curr_stock_data.stock_map[stock_name].status = "BOUGHT"
                        curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date].curr_date = 0
                        
                    elif (d == (num_dates - 1) and curr_stock_data.stock_map[stock_name].status == "BOUGHT")  or \
                            (curr_stock_data.stock_map[stock_name].status == "BOUGHT" and
                                                stock_daily_trans.high_price >= (100 + k) / 100 * \
                                                    curr_stock_data.stock_map[stock_name].curr_price) :
                        if (curr_stock_data.stock_map[stock_name].curr_price == 0) :
                            print "0: "+ stock_name + ", " + td_date;
                        totalAmt += stock_daily_trans.high_price / (curr_stock_data.stock_map[stock_name].curr_price) * \
                                    curr_stock_data.stock_map[stock_name].amount
                        curr_stock_data.stock_map[stock_name].status = "NOPOS"
                        curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date].curr_date = 0
                        curr_stock_data.stock_map[stock_name].curr_price = stock_daily_trans.low_price

                        
                    elif i==0 or stock_daily_trans.curr_date >= num_consec :
                        curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date].curr_date = 0
                        curr_stock_data.stock_map[stock_name].curr_price = \
                            curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date].low_price

                    elif curr_stock_data.stock_map[stock_name].status == "NOPOS" :
                        curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date].curr_date += 1

                    i= i+1;

                d = d+1

            return (totalAmt-origAmt)/origAmt * 100;
        
            
        def InitAlloc(self):
            return
        
        
trade_executor = TradeExecutor()
data_loader = trade.DataLoader()
data_loader.LoadAllStockData('/Users/apple/Downloads/quantquote_daily_sp500_83986/daily')

finalAmt = trade_executor.ExecTrades(data_loader, \
                    1000000, \
                    3, 4)

print finalAmt
                                             
            
