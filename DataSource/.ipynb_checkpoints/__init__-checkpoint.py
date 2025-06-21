from .resource import *
from .baostock.datasource import get_data as stock_get_data
from .baostock.datasource import get_codes as stock_get_codes
from .baostock.datasource import get_zz500_codes as stock_get_zz500_codes

default_datasource = 'baostock'


def get_data(code):
	if default_datasource == 'baostock':
		return stock_get_data(code)


def get_codes():
	if default_datasource == 'baostock':
		return stock_get_codes()


def get_zz500_codes():
	if default_datasource == 'baostock':
		return stock_get_zz500_codes()