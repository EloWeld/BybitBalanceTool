import json
import os
import requests
from pyui.token_panel_widget import Ui_TokenPanelWidgetUI
from PyQt5.QtCore import QSize, QThread, pyqtSignal, QSettings, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem, QPushButton, QMessageBox, QLineEdit, QMainWindow

class TokenPanel(Ui_TokenPanelWidgetUI, QWidget):
    def __init__(self, token_name, equidity, usd_value, total_usd, callback_change_sliders=None) -> None:
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.call_callback)
        self.lbl_token_name.setText(token_name)
        self.lbl_equidity.setText(equidity)
        self.lbl_usd_value.setText(f"~{usd_value} USD")

        ratio = float(usd_value) / float(total_usd) * 100
        self.pressed_val = ratio
        self.slider_balance.setValue(int(self.pressed_val * 10))
        self.sb_balance.setValue(ratio)
        
        self.token_name = token_name
        self.equidity = float(equidity)
        self.usd_value = float(usd_value)
        self.total_usd = float(total_usd)
        self.current_percent = ratio
        self.callback_change_sliders = callback_change_sliders

        self.slider_balance.sliderMoved.connect(self.on_slider_percentage_changed)
        self.slider_balance.sliderPressed.connect(self.on_slider_pressed)
        self.sb_balance.editingFinished.connect(self.on_sb_percentage_changed)
        self.slider_balance.sliderReleased.connect(self.on_slider_released)

    def on_slider_released(self):
        self.current_percent = self.sb_balance.value()
        self.on_slider_percentage_changed()
        self.repaint()
        self.timer.start(100)

    def call_callback(self):
        self.callback_change_sliders(self, self.current_percent)
        self.timer.stop()
        
        
    def on_slider_pressed(self):
        self.pressed_val = self.slider_balance.value()

    def update_percent(self, new_value):
        print(new_value)
        self.slider_balance.setValue(int(new_value * 10))
        self.sb_balance.setValue(new_value)
        self.current_percent = new_value
        self.global_change_percent(self.current_percent)

    def on_slider_percentage_changed(self):
        value = self.slider_balance.value() / 10
        self.sb_balance.setValue(value)
        self.global_change_percent(value)

    def on_sb_percentage_changed(self):
        # Calculate the new values based on the proportion of slider value to total USD
        value = self.sb_balance.value()
        self.slider_balance.setValue(int(value * 10))
        self.global_change_percent(value)
        
        self.callback_change_sliders(self, self.current_percent)

    def global_change_percent(self, value):
        new_equidity = f"{(value / 100) * float(self.total_usd) * (float(self.equidity) / float(self.usd_value)):.4f}"
        new_usd_value = f"{(value / 100) * float(self.total_usd):.4f}"
        
        self.lbl_equidity.setText(new_equidity)
        self.lbl_usd_value.setText(f"~{new_usd_value} USD")

        self.current_percent = value

    