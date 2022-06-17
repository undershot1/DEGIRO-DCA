import datetime
import os
import math
import degiroapi
from degiroapi.product import Product
from degiroapi.order import Order

DEGIRO_USER = os.environ['DEGIRO_USER']
DEGIRO_PASS = os.environ['DEGIRO_PASS']
PRODUCT = os.environ['PRODUCT']
REGULAR_AMOUNT = float(os.environ['REGULAR_AMOUNT'])

degiro = degiroapi.DeGiro()
degiro.login(DEGIRO_USER, DEGIRO_PASS)

cashfunds = degiro.getdata(degiroapi.Data.Type.CASHFUNDS)
balance = float([s for s in cashfunds[0].split()][1])
investment_amount = min(balance, REGULAR_AMOUNT, 0)

products = degiro.search_products(PRODUCT)
product_id = Product(products[0]).id
product_price = degiro.real_time_price(product_id, degiroapi.Interval.Type.One_Day)[0]['data']['lastPrice']

if investment_amount >= product_price:
    qty = math.floor(investment_amount / product_price)
    degiro.buyorder(Order.Type.MARKET, product_id, 1, qty)
    print('%s - ORDER SUBMITTED FOR %i @ EUR %.2f = EUR %.2f' % (datetime.date.today(), product_price, qty, qty * product_price))
else:
    print('%s - NOT ENOUGH FUNDS AVAILABLE (EUR %.2f), MIN. REQUIRED = EUR %.2f' % (datetime.date.today(), investment_amount, product_price))

degiro.logout()