import hmac
import hashlib
import time
import requests
import json
import os


class CexClient():
    BASE_URL = "https://cex.io/api/"
    KEY = os.getenv('CX_API_KEY')
    SECRET = os.getenv('CX_API_SECRET')


    def __init__(self, username):
        self.username = username


    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(round(time.time() * 1000)))


    def _headers(self, path, nonce):
        string = bytes(nonce + self.username + self.KEY, 'utf-8')
        signature = hmac.new(bytes(self.SECRET, 'utf-8'), string, digestmod=hashlib.sha256).hexdigest().upper()  # create signature

        return {
            "key": self.KEY,
            "signature": signature,
            "nonce": nonce
        }


    def api_call(self, method, body={}, private=0, couple=''):  # api call (Middle level)
        nonce = self._nonce()
        path = self.BASE_URL + method + '/'
        if couple != '':
            path = path + couple + '/'  # set couple if needed
        if private:
            headers = self._headers(path, nonce)
            data = {**headers, **body}
            print("requests.post("+ path + ", data=" + str(data) + ", verify=True)")
            r = requests.post(path, data=data, verify=True)
        else:
            print("requests.post("+ path + ", verify=True)")
            r = requests.post(path, verify=True)

        if r.status_code == 200:
          return r.json()
        else:
          print(r.status_code)
          print(r)
          return ''

    def ticker(self, couple='GHS/BTC'):
        return self.api_call('ticker', {}, 0, couple)

    def order_book(self, couple='GHS/BTC'):
        return self.api_call('order_book', {}, 0, couple)

    def trade_history(self, since=1, couple='GHS/BTC'):
        return self.api_call('trade_history', {"since": str(since)}, 0, couple)

    def balance(self):
        return self.api_call('balance', {}, 1)

    def current_orders(self, couple='GHS/BTC'):
        return self.api_call('open_orders', {}, 1, couple)

    def cancel_order(self, order_id):
        return self.api_call('cancel_order', {"id": order_id}, 1)

    def place_order(self, ptype='buy', amount=1, price=1, couple='GHS/BTC'):
        return self.api_call('place_order', {"type": ptype, "amount": str(amount), "price": str(price)}, 1, couple)

    def price_stats(self, last_hours, max_resp_arr_size, couple='GHS/BTC'):
        return self.api_call(
                'price_stats',
                {"lastHours": last_hours, "maxRespArrSize": max_resp_arr_size},
                0, couple)

if __name__ == "__main__":
    # orders = []
    # orders.append(CexClient('up128740645').place_order(amount=.15, price=100 ,couple='ETH/USD'))
    # orders = CexClient('up128740645').current_orders(couple='ETH/USD')
    # print(CexClient('up128740645').cancel_order(orders[0]))
    # print(CexClient('up128740645').current_orders(couple='ETH/USD'))