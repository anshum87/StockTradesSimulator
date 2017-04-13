import csv
from os import listdir
from os import path


class StockDataEntry:
    trans_map = list()
    stock_name = ""
    
    class StockDailyTrans:
        curr_date = 0
        open_price = 0
        high_price = 0
        low_price = 0
        close_price = 0
        volume = 0
        def __init__(self, curr_date, open_price, high_price, low_price, close_price, volume):
            self.curr_date = curr_date
            self.open_price = open_price
            self.high_price = high_price
            self.low_price = low_price
            self.close_price = close_price
            self.volume = volume
            
    def __init__(self, stock_name):
        self.stock_name = stock_name
    
    def AddDailyTrans(self, datenum, timenum, open_price, low_price, high_price,
                      close_price, volume):
        self.trans_map.append(self.StockDailyTrans(int(datenum), float(open_price), float(high_price), float(low_price),
                      float(close_price), float(volume)))
        
    

class DataLoader:
        stock_data = dict()
        def LoadIndividualStockData(self, stock_data_file_name):
            with open(stock_data_file_name, 'rb') as stock_file_data:
                csv_reader = csv.reader(stock_file_data)
                stock_name = path.basename(stock_data_file_name)
                stock_de = StockDataEntry(stock_name)
                for row in csv_reader:
                    stock_de.AddDailyTrans(row[0], row[1], row[2], row[3], row[4],
                                                     row[5], row[6]);
                    # print row
                self.stock_data[stock_name] = stock_de;
                
        
        def LoadAllStockData(self, stock_data_dir):
            [self.LoadIndividualStockData(path.join(stock_data_dir, fname)) for fname in listdir(stock_data_dir)];
            

dl = DataLoader()
dl.LoadAllStockData('/Users/apple/Downloads/quantquote_daily_sp500_83986/daily')

                
