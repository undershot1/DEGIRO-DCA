import datetime
import os
import math
import degiroapi
from degiroapi.product import Product
from degiroapi.order import Order

# set key parameters
DEGIRO_USER = os.environ['DEGIRO_USER']
DEGIRO_PASS = os.environ['DEGIRO_PASS']
PRODUCT = os.environ['PRODUCT']
REGULAR_AMOUNT = float(os.environ['REGULAR_AMOUNT'])

if __name__ == "__main__":
    # login
    degiro = degiroapi.DeGiro()
    degiro.login(DEGIRO_USER, DEGIRO_PASS)

    cashfunds = degiro.getdata(degiroapi.Data.Type.CASHFUNDS)
    # get current available balance
    balance = float([s for s in cashfunds[0].split()][1])
    # determine the investment amount which will be the minimum of the current
    # balance and the regular amount to invest
    investment_amount = min(balance, REGULAR_AMOUNT)

    # retrieve product information
    products = degiro.search_products(PRODUCT)
    product_id = Product(products[0]).id
    product_price = degiro.real_time_price(product_id, degiroapi.Interval.Type.One_Day)[0]['data']['lastPrice']

    # run purchase
    if investment_amount >= product_price:
        # determine quantity
        qtyfloor = math.floor(investment_amount / product_price)
        qtyceil = math.ceil(investment_amount / product_price)

        # set quantity to buy by cross ref with balance
        if qtyceil * product_price > balance:
            qty = qtyfloor
        else:
            qty = qtyceil

        # create the buy order
        degiro.buyorder(Order.Type.MARKET, product_id, 1, qty)
        # output
        print('%s - ORDER SUBMITTED FOR %i @ EUR %.2f = EUR %.2f' % (
        datetime.date.today(), qty, product_price, qty * product_price))
    else:
        # you ain't got enough brass
        print('%s - NOT ENOUGH FUNDS AVAILABLE (EUR %.2f), MIN. REQUIRED = EUR %.2f' % (
        datetime.date.today(), balance, product_price))

    degiro.logout()
