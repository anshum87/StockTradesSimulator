import trade
from trade import DataLoader
from objc._objc import NULL


class CurrStockData:

    class CurrStockEntry:
        stock_data_entry = NULL
        status = "NOPOS"
        curr_price = 0.0
        bench_price = 0.0
        num_days = 0
        amount = 0.0

        def __init__(self, stock_data_entry):
            self.stock_data_entry = stock_data_entry;
            self.status = "NOPOS"
            self.curr_price = 0.0
            self.num_days = 0
            self.amount = 0.0

    stock_map = dict()  # mapping from stock_name-> CurrStockEntry
    trans_date_map = dict()  # mapping from date->list(stock_name)

    def __init__(self, stock_data):
        for stock_entry in stock_data:
            self.stock_map[stock_data[stock_entry].stock_name] = \
                self.CurrStockEntry(stock_data[stock_entry])

            print stock_data[stock_entry].stock_name;

            for curr_date in stock_data[stock_entry].trans_map:
                self.trans_date_map.setdefault(curr_date, []). \
                    append(stock_data[stock_entry].stock_name)



class TradeExecutor:
           
        def BuildCurrStockData(self, stock_data):
            curr_stock_data = CurrStockData(stock_data)
            return curr_stock_data

        def ExecTrades(self, data_loader, origAmt, trade_margin, num_consec):
            curr_stock_data = self.BuildCurrStockData(data_loader.stock_data)

            n = curr_stock_data.stock_map.__len__()
            totalAmt=origAmt

            num_dates = curr_stock_data.trans_date_map.__len__();
            
            i = 0;

            
            if n < 2 :
               return totalAmt

            d=0;
            num_hold=0

            for td_date in sorted(curr_stock_data.trans_date_map):
                for stock_name in curr_stock_data.trans_date_map[td_date]:

                    stock_daily_trans =  curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date]

                    is_last_day = (td_date == max(curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map, \
                                                  curr_stock_data.stock_map[
                                                      stock_name].stock_data_entry.trans_map.get));

                    if (curr_stock_data.stock_map[stock_name].status == "NOPOS" and
                                          stock_daily_trans.low_price <= (100.0 - trade_margin) / 100 * \
                                              curr_stock_data.stock_map[stock_name].curr_price) :
                        curr_stock_data.stock_map[stock_name].amount = totalAmt / (n - i)
                        totalAmt -= totalAmt / (n - i)
                        curr_stock_data.stock_map[stock_name].curr_price= stock_daily_trans.low_price;
                        curr_stock_data.stock_map[stock_name].status = "BOUGHT"
                        curr_stock_data.stock_map[stock_name].num_days = 0
                        num_hold+=1

                    elif (is_last_day  or (curr_stock_data.stock_map[stock_name].status == "BOUGHT" and
                                                stock_daily_trans.high_price >= (100.0 + trade_margin) / 100 * \
                                                    curr_stock_data.stock_map[stock_name].curr_price)) :
                        if (curr_stock_data.stock_map[stock_name].curr_price == 0) :
                            print "0: "+ stock_name + ", " + td_date;
                        totalAmt += stock_daily_trans.high_price / (curr_stock_data.stock_map[stock_name].curr_price) * \
                                    curr_stock_data.stock_map[stock_name].amount
                        curr_stock_data.stock_map[stock_name].status = "NOPOS"
                        curr_stock_data.stock_map[stock_name].curr_price = 0
                        curr_stock_data.stock_map[stock_name].num_days = 0
                        num_hold-=1


                        
                    if curr_stock_data.stock_map[stock_name].num_days == 0 or (curr_stock_data.stock_map[stock_name].num_days == num_consec and
                                          curr_stock_data.stock_map[stock_name].status == "NOPOS"):
                        curr_stock_data.stock_map[stock_name].num_days = 1
                        curr_stock_data.stock_map[stock_name].curr_price = \
                            curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date].low_price

                    elif curr_stock_data.stock_map[stock_name].status == "NOPOS":
                        curr_stock_data.stock_map[stock_name].num_days += 1
                        curr_stock_data.stock_map[stock_name].curr_price = min( \
                            curr_stock_data.stock_map[stock_name].curr_price, \
                            curr_stock_data.stock_map[stock_name].stock_data_entry.trans_map[td_date].low_price)


                d = d+1

            return (totalAmt-origAmt)/origAmt * 100.0;
        
            
        def InitAlloc(self):
            return
        
        
trade_executor = TradeExecutor()
data_loader = trade.DataLoader()
data_loader.LoadAllStockData('/Users/apple/Downloads/quantquote_daily_sp500_83986/daily')

profitPerc = trade_executor.ExecTrades(data_loader, \
                    1000000, \
                    5, 7)

print profitPerc
                                             
            
