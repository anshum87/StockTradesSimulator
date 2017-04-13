import trade
from trade import DataLoader
from objc._objc import NULL

class CurrStockEntry:
        stock_data_entry = NULL
        status = "NOPOS"
        last_trans = "000000"
        amount = 0.0
        def __init__(self, stock_data_entry):
            self.stock_data_entry = stock_data_entry;


class TradeExecutor:
           
        class CurrStockData:
            stock_map = dict()
            trans_date_map = dict()
            
            def __init__(self, stock_data):
                for stock_entry in stock_data:
                    self.stock_map[stock_data[stock_entry].stock_name] = \
                            CurrStockEntry(stock_entry)
                    
                    for stock_daily_trans in stock_data[stock_entry].trans_map :
                        self.trans_date_map.setdefault(stock_daily_trans.curr_date, []). \
                        append((stock_data[stock_entry].stock_name, stock_daily_trans))
                        
            
        def ExecTrades(self, data_loader, totalAmt, k):
            curr_stock_data = self.CurrStockData(data_loader.stock_data)
            n = data_loader.size()
            amt = totalAmt / n
            
            i = 0;
            
            if n < 2 :
               return totalAmt
           
            for td_date in sorted(curr_stock_data.trans_date_map):
                for stock_name_trans in curr_stock_data.trans_date_map:
                    
                    print totalAmt
                            
                    if i == 0 or (curr_stock_data.stock_map[stock_name_trans[0]][td_date].status == "NOPOS" and
                            curr_stock_data.trans_date_map[stock_name_trans[0]][td_date].low_price <= (100 - k) / 100 * \
                                curr_stock_data.stock_map[stock_name_trans[0]][td_date].amount) :
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].amount = totalAmt / (n - i)
                        totalAmt -= totalAmt / (n - i)
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].status = "BOUGHT"
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].curr_date = td_date
                        
                    elif i == n - 1 or (curr_stock_data.stock_map[stock_name_trans[0]][td_date].status == "NOPOS" and
                            curr_stock_data.trans_date_map[td_date].high_price >= (100 + k) / 100 * \
                                curr_stock_data.stock_map[stock_name_trans[0]][td_date].amount) :
                        totalAmt += curr_stock_data.stock_map[td_date].amount
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].amount = 0
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].status = "NOPOS"
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].curr_date = td_date
                        
                    elif (curr_stock_data.stock_map[stock_name_trans[0]][td_date].status == "NOPOS" and
                            curr_stock_data.trans_date_map[td_date].low_price != \
                            curr_stock_data.stock_map[stock_name_trans[0]][td_date].amount) :
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].curr_date = td_date
                        
                    elif td_date - curr_stock_data.stock_map[stock_name_trans[0]][td_date].curr_date >= k :
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].curr_date = td_date
                        curr_stock_data.stock_map[stock_name_trans[0]][td_date].amount = \
                            curr_stock_data.stock_map[stock_name_trans[0]][td_date].low_price
                                 
            return totalAmt       
                       
            
            
        def InitAlloc(self):
            return
        
        
trade_executor = TradeExecutor()
data_loader = trade.DataLoader()
data_loader.LoadAllStockData('/Users/apple/Downloads/quantquote_daily_sp500_83986/daily')

finalAmt = trade_executor.ExecTrades(data_loader, \
                    100000, \
                    5)

print finalAmt
                                             
            
