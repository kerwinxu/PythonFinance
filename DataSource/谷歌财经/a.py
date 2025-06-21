import datetime
import pandas as pd
import pandas_datareader.data as web

import pandas_datareader as pdr
gold = pdr.get_data_fred('GOLDAMGBD228NLBM')
print(gold.head())
