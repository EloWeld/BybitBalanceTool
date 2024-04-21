import json
import os
import sys
from urllib import request
from PyQt5.QtCore import QSize, QThread, pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem, QPushButton, QMessageBox, QLineEdit, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
import requests

from components.token_panel import TokenPanel
from pyui.main_window import Ui_BBTMainWindow
from pybit.unified_trading import HTTP
from pybit.exceptions import InvalidRequestError
from PyQt5.QtCore import QTimer

def dec(number):
    return number[:-1] + str(int(number[-1])-1)


class MainForm(Ui_BBTMainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.qsettings = QSettings("no_company", "no_app")

        self.bbapi = None
        self.token_panels: list[TokenPanel] = []

        self.init_values()
        self.connect_signals()

        self.try_connect_account()

    def init_values(self):
        self.le_bybit_api_key.setText(
            self.qsettings.value("bybit_api_key", ""))
        self.le_bybit_api_secret.setText(
            self.qsettings.value("bybit_api_secret", ""))
        self.le_cmc_api_key.setText(
            self.qsettings.value("cmc_api_key", ""))

    def connect_signals(self):
        self.btn_connect.clicked.connect(self.on_connect_clicked)
        self.btn_refresh.clicked.connect(self.try_connect_account)
        self.btn_save.clicked.connect(self.on_save_clicked)

    def try_connect_account(self):
        key = self.qsettings.value("bybit_api_key", "")
        secret = self.qsettings.value("bybit_api_secret", "")

        if (not key) or (not secret):
            return

        self.lbl_connecting_status.setText("Connecting...")
        self.lbl_connecting_status.setStyleSheet("color:blue")

        self.bbapi = HTTP(
            testnet=False,
            api_key=key,
            api_secret=secret,
        )

        try:
            self.bbapi.get_account_info()
            self.lbl_connecting_status.setText("SUCCESS")
            self.lbl_connecting_status.setStyleSheet("color:green")
        except InvalidRequestError as e:
            self.lbl_connecting_status.setText(f"FAILED: {e.message}")
            self.lbl_connecting_status.setStyleSheet("color:red")
            self.bbapi = None

        # If connect is successfull
        if self.bbapi:
            balances = self.bbapi.get_wallet_balance(accountType="UNIFIED")
            print(json.dumps(balances, indent=4))

            # Set total usd
            self.lbl_total_usd.setText(f"{float(balances['result']['list'][0]['totalEquity']):.2f} $")

            # Clear list of tokens
            self.token_panels = []
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(0)  # Get the item at index 0
                self.listWidget.takeItem(0)  # Remove the item from the QListWidget
                del item  # Delete the item from memory

            # Fill list of tokens
            for coin in balances['result']['list'][0]['coin']:
                token_name = coin['coin']
                t = TokenPanel(token_name=token_name, 
                               equidity=coin['equity'], 
                               usd_value=coin['usdValue'], 
                               total_usd=balances['result']['list'][0]['totalEquity'],
                               callback_change_sliders=self.on_change_sliders,
                               )
                token_icon_path = os.path.join('src', f"{token_name}.png")
                if not os.path.exists(token_icon_path):
                    token_icon_web_addr = self.get_token_logo(token_name)
                    if not token_icon_web_addr:
                        # Owerride token icon path to unknown token icon
                        token_icon_path = os.path.join('src', f"unknown_token.png")
                    else:
                        r = requests.get(token_icon_web_addr)
                        with open(token_icon_path, 'wb') as f:
                            f.write(r.content)
                
                t.lbl_token_icon.setPixmap(QPixmap(token_icon_path))
                
                try:
                    tickers_resp = self.bbapi.get_tickers(category="spot", symbol=token_name+"USDT")
                    t.lbl_price.setText(f"{float(tickers_resp['result']['list'][0]['lastPrice']):,} $")
                except Exception as e:
                    print(e)
                    t.lbl_price.setText('-')

                self.token_panels.append(t)
                item = QListWidgetItem(self.listWidget)
                item.setSizeHint(QSize(100, 90))
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, t)

    def get_token_logo(self, symbol):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        parameters = {
            'symbol': symbol,
            'aux': 'logo',
        }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.qsettings.value("cmc_api_key", ""),
        }

        try:
            response = requests.get(url, headers=headers, params=parameters)
            data = response.json()
            
            # Check if data contains token info
            if 'data' in data and symbol.upper() in data['data']:
                return data['data'][symbol.upper()]['logo']
            else:
                return None
        except Exception as e:
            print(f"Error while download icon: {e}")
            return None
        
    def on_change_sliders(self, curr_token_panel: TokenPanel, new_percent):
        for t in self.token_panels:
            print(t.current_percent)
        print("+")
        non_fixed_sliders = [panel for panel in self.token_panels if not panel.btn_fix.isChecked()]

        # Exclude the current panel from the total sum calculation
        total_sum = sum(panel.slider_balance.value() for panel in self.token_panels if panel is not curr_token_panel)

        # Calculate the remaining percentage to distribute among non-fixed sliders
        remaining_percent = 100 - new_percent

        # Distribute the remaining percentage among non-fixed sliders proportionally
        for tp in non_fixed_sliders:
            if tp is curr_token_panel:
                continue
            if total_sum == 0:
                # If the total sum is zero, distribute the remaining percentage equally
                tp.update_percent(remaining_percent / len(self.token_panels))
            else:
                # Otherwise, distribute the remaining percentage proportionally based on each slider's current percentage
                current_percent = tp.slider_balance.value()
                current_ratio = current_percent / total_sum
                tp.update_percent(current_ratio * remaining_percent)
        for tp in non_fixed_sliders:
            tp.slider_balance.repaint()
        ttp = sum(tp.current_percent for tp in self.token_panels)
        self.lbl_total_percent.setText(f"Total percent: {ttp:.2f}%")
        self.lbl_total_percent.setStyleSheet("color: red" if ttp > 100 else "color:green")

    def on_save_clicked(self):

        # Выполняем конвертацию валют с помощью pybybit
        self.convert_balances()

        # Обновляем интерфейс с полученными значениями
        self.try_connect_account()

    def convert_balances(self):
        # Проходим по каждому токену и его балансу
        for token_panel in self.token_panels:
            token_name = token_panel.token_name
            
            if token_name in ['USDT']:
                continue

            # Получаем баланс токена на бирже
            balance = self.bbapi.get_coin_balance(accountType="UNIFIED", coin=token_name)['result']['balance']['transferBalance']

            # Sell all of tokens to usdt
            retry = True
            precision = 7
            # We can get an error "Order qty has too many decs" so decrement precision until it'll gone
            while retry:
                try:
                    balance = f"{float(balance):.{precision}f}"
                    buy_result = self.bbapi.place_order(
                        category="spot",
                        symbol=token_name+"USDT",
                        side="Sell", # Sell,
                        orderType="Market", # Limit
                        qty=balance, # In USDT
                        # marketUnit="quoteCoin", # quoteCoin when buy and baseCoin when sell, and all qty in USDT
                        # baseCoin when buy and quoteCoin when sell, and all qty in TOKEN
                    )
                    print(buy_result)
                    retry = False
                except Exception as e:
                    print(f"Cant sell coin {token_name}: {e}")
                    if "Order quantity has too many decimals" in e.message:
                        retry = True
                        precision -= 1
                    elif "Insufficient balance" in e.message:
                        retry = True
                        balance = dec(balance)
                    else:
                        retry = False

        total_usdt_amount = float(self.bbapi.get_coin_balance(accountType="UNIFIED", coin="USDT")['result']['balance']['transferBalance'])

        # Проходим по каждому токену и покупаем его
        for token_panel in self.token_panels:
            token_name = token_panel.token_name
            curr_percent = token_panel.current_percent
            
            if token_name in ['USDT']:
                continue

            # Sell all of tokens to usdt
            retry = True
            precision = 7
            # We can get an error "Order qty has too many decs" so decrement precision until it'll gone
            while retry:
                try:
                    buy_result = self.bbapi.place_order(
                        category="spot",
                        symbol=token_name+"USDT",
                        side="Buy", # Sell,
                        orderType="Market", # Limit
                        qty=f"{float(curr_percent/100*total_usdt_amount*0.999):.7f}", # In USDT
                        marketUnit="quoteCoin", # quoteCoin when buy and baseCoin when sell, and all qty in USDT
                        # baseCoin when buy and quoteCoin when sell, and all qty in TOKEN
                    )
                    print(buy_result)
                    retry = False
                except Exception as e:
                        print(f"Cant buy coin {token_name}: {e}")
                        if "Order quantity has too many decimals" in e.message:
                            retry = True
                            precision -= 1
                        elif "Insufficient balance" in e.message:
                            retry = True
                            balance = dec(balance)
                        else:
                            retry = False


    def on_connect_clicked(self):

        self.qsettings.setValue("bybit_api_key", self.le_bybit_api_key.text())
        self.qsettings.setValue("bybit_api_secret", self.le_bybit_api_secret.text())
        self.qsettings.setValue("cmc_api_key", self.le_cmc_api_key.text())
        
        self.try_connect_account()    


def main():
    app = QApplication(sys.argv)

    w = MainForm()
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
