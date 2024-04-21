# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BBTMainWindow(object):
    def setupUi(self, BBTMainWindow):
        BBTMainWindow.setObjectName("BBTMainWindow")
        BBTMainWindow.resize(680, 654)
        self.centralwidget = QtWidgets.QWidget(BBTMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.setObjectName("tabs")
        self.tab_balance = QtWidgets.QWidget()
        self.tab_balance.setObjectName("tab_balance")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_balance)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_refresh = QtWidgets.QToolButton(self.tab_balance)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/../src/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_refresh.setIcon(icon)
        self.btn_refresh.setObjectName("btn_refresh")
        self.horizontalLayout.addWidget(self.btn_refresh)
        self.label_7 = QtWidgets.QLabel(self.tab_balance)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.lbl_total_usd = QtWidgets.QLabel(self.tab_balance)
        self.lbl_total_usd.setObjectName("lbl_total_usd")
        self.horizontalLayout.addWidget(self.lbl_total_usd)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_add_token = QtWidgets.QPushButton(self.tab_balance)
        self.btn_add_token.setObjectName("btn_add_token")
        self.horizontalLayout.addWidget(self.btn_add_token)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.lbl_total_percent = QtWidgets.QLabel(self.tab_balance)
        self.lbl_total_percent.setMaximumSize(QtCore.QSize(16777215, 15))
        self.lbl_total_percent.setObjectName("lbl_total_percent")
        self.verticalLayout_2.addWidget(self.lbl_total_percent)
        self.listWidget = QtWidgets.QListWidget(self.tab_balance)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.btn_save = QtWidgets.QPushButton(self.tab_balance)
        self.btn_save.setObjectName("btn_save")
        self.verticalLayout_2.addWidget(self.btn_save)
        self.tabs.addTab(self.tab_balance, "")
        self.tab_settings = QtWidgets.QWidget()
        self.tab_settings.setObjectName("tab_settings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_settings)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.tab_settings)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.le_bybit_api_key = QtWidgets.QLineEdit(self.tab_settings)
        self.le_bybit_api_key.setMinimumSize(QtCore.QSize(400, 0))
        self.le_bybit_api_key.setObjectName("le_bybit_api_key")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_bybit_api_key)
        self.label_5 = QtWidgets.QLabel(self.tab_settings)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.le_bybit_api_secret = QtWidgets.QLineEdit(self.tab_settings)
        self.le_bybit_api_secret.setMinimumSize(QtCore.QSize(400, 0))
        self.le_bybit_api_secret.setObjectName("le_bybit_api_secret")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_bybit_api_secret)
        self.label_6 = QtWidgets.QLabel(self.tab_settings)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.le_cmc_api_key = QtWidgets.QLineEdit(self.tab_settings)
        self.le_cmc_api_key.setMinimumSize(QtCore.QSize(400, 0))
        self.le_cmc_api_key.setObjectName("le_cmc_api_key")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.le_cmc_api_key)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.btn_connect = QtWidgets.QPushButton(self.tab_settings)
        self.btn_connect.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_connect.sizePolicy().hasHeightForWidth())
        self.btn_connect.setSizePolicy(sizePolicy)
        self.btn_connect.setObjectName("btn_connect")
        self.verticalLayout_3.addWidget(self.btn_connect)
        self.lbl_connecting_status = QtWidgets.QLabel(self.tab_settings)
        self.lbl_connecting_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_connecting_status.setObjectName("lbl_connecting_status")
        self.verticalLayout_3.addWidget(self.lbl_connecting_status)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10000, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.tabs.addTab(self.tab_settings, "")
        self.verticalLayout.addWidget(self.tabs)
        BBTMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(BBTMainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(BBTMainWindow)

    def retranslateUi(self, BBTMainWindow):
        _translate = QtCore.QCoreApplication.translate
        BBTMainWindow.setWindowTitle(_translate("BBTMainWindow", "Bybit Balance Tool"))
        self.btn_refresh.setText(_translate("BBTMainWindow", "..."))
        self.label_7.setText(_translate("BBTMainWindow", "Total USD:"))
        self.lbl_total_usd.setText(_translate("BBTMainWindow", "~999USD"))
        self.btn_add_token.setText(_translate("BBTMainWindow", "Add Token"))
        self.lbl_total_percent.setText(_translate("BBTMainWindow", "Total percent: 100%"))
        self.btn_save.setText(_translate("BBTMainWindow", "Save"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_balance), _translate("BBTMainWindow", "Balance"))
        self.label_4.setText(_translate("BBTMainWindow", "BB Api Key"))
        self.label_5.setText(_translate("BBTMainWindow", "BB Api Secret"))
        self.label_6.setText(_translate("BBTMainWindow", "CMC Api Key"))
        self.btn_connect.setText(_translate("BBTMainWindow", "Connect"))
        self.lbl_connecting_status.setText(_translate("BBTMainWindow", "Connecting status"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_settings), _translate("BBTMainWindow", "Settings"))