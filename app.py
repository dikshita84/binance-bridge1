import json, config, time
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *
app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)

def order(side1, quantity1, symbol1,order_type1, price1, timeInForce = 'GTC'):
    try:
        print(f"sending order {order_type1} - {side1} {quantity1} {symbol1}")
        order = client.futures_create_order(symbol=symbol1, side=side1, type=order_type1, quantity=quantity1, price = price1, timeInForce= 'GTC')
        print(order)
    except BinanceAPIException as e:
        print("an exception occured {}".format(e))
        
        return False
    return order


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods = ['POST'])
def webhook():
    data1 = json.loads(request.data)
    #print(data["passphrase"])
    print(data1[0]["SIDE"])
    print(len(data1))
    for i in range(len(data1)):
        if data1[i]['TYPE'] == 'LIMIT':
            side1 = data1[i]["SIDE"]
            quantity1 = data1[i]["Q"]
            symbol1 = data1[i]["TS"]
            order_type1 = data1[i]["TYPE"]
            price1 = data1[i]["PRICE"]
            order_response = order(side1, quantity1, symbol1, order_type1, price1, timeInForce = 'GTC')
            print(order_response)
            time.sleep(1)
        elif data1[i]['TYPE'] == 'CANCEL':
            try:
                order_response1 = client.futures_cancel_all_open_order(symbol = data1[i]['TS'])
                print(order_response1)
                #order_response=client._delete('openOrders', True, data={'symbol': data[i]['TS']})
            except BinanceAPIException as e:
                print(e)

        elif data1[i]['TYPE'] == 'STOP_MARKET':
            try:
                order_response2 = client.futures_create_order(side = data1[i]['SIDE'], quantity= data1[i]['Q'],symbol = data1[i]['TS'],
                type = data1[i]['TYPE'], stopPrice = data1[i]['PRICE'])
                print(order_response2)
            except BinanceAPIException as e:
                print(e)
        else:
            pass

    if order_response:
        return {"code": "success",
                    "message":"order executed"}
    else:
        print("order failed")
        return {"code":"error",
                "message":"order failed"}