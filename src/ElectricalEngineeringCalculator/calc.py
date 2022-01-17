from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ElectronicsCalculator import electronics_calculator as ec
from ElectronicsCalculator import scale_factors as sf

class Ui_MainWindow(object):
    def __init__(self):
        self.centralwidget = None
        self.menubar = None
        self.statusbar = None
        self.txtPower = None
        self.txtCurrent = None
        self.txtVoltage = None
        self.txtResistance = None
        self.lblInstruction = None
        self.lblPower = None
        self.lblCurrent = None
        self.lblVoltage = None
        self.lblResistance = None
        self.lcdPower = None
        self.lcdCurrent = None
        self.lcdVoltage = None
        self.lcdResistance = None
        self.cmdCalculate = None

    def setup_ui(self, main_window):
        """Defines and configures UI elements"""
        main_window.setObjectName("main_window")
        main_window.resize(371, 372)
        main_window.setAutoFillBackground(False)
        main_window.setStyleSheet("background-color: rgb(43, 43, 43);")

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # Power textbox
        self.txtPower = QtWidgets.QLineEdit(self.centralwidget)
        self.txtPower.setGeometry(QtCore.QRect(202, 90, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.txtPower.setFont(font)
        self.txtPower.setStyleSheet("background-color: rgb(255, 255, 127); text-align: right;")
        self.txtPower.setObjectName("txtPower")

        # Resistance textbox
        self.txtResistance = QtWidgets.QLineEdit(self.centralwidget)
        self.txtResistance.setGeometry(QtCore.QRect(202, 240, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.txtResistance.setFont(font)
        self.txtResistance.setStyleSheet("background-color: rgb(255, 255, 127); text-align: right;")
        self.txtResistance.setObjectName("txtResistance")

        # Voltage textbox
        self.txtVoltage = QtWidgets.QLineEdit(self.centralwidget)
        self.txtVoltage.setGeometry(QtCore.QRect(202, 190, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.txtVoltage.setFont(font)
        self.txtVoltage.setStyleSheet("background-color: rgb(255, 255, 127); text-align: right;")
        self.txtVoltage.setObjectName("txtVoltage")

        # Current textbox
        self.txtCurrent = QtWidgets.QLineEdit(self.centralwidget)
        self.txtCurrent.setGeometry(QtCore.QRect(202, 140, 51, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.txtCurrent.setFont(font)
        self.txtCurrent.setStyleSheet("background-color: rgb(255, 255, 127); text-align: right;")
        self.txtCurrent.setObjectName("txtCurrent")

        # Power label
        self.lblPower = QtWidgets.QLabel(self.centralwidget)
        self.lblPower.setGeometry(QtCore.QRect(10, 90, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPower.setFont(font)
        self.lblPower.setAccessibleDescription("")
        self.lblPower.setStyleSheet("color: rgb(85, 255, 127);")
        self.lblPower.setObjectName("lblPower")

        # Resistance label
        self.lblResistance = QtWidgets.QLabel(self.centralwidget)
        self.lblResistance.setGeometry(QtCore.QRect(10, 240, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblResistance.setFont(font)
        self.lblResistance.setAccessibleDescription("")
        self.lblResistance.setStyleSheet("color: rgb(85, 255, 127);")
        self.lblResistance.setObjectName("lblResistance")

        # Voltage label
        self.lblVoltage = QtWidgets.QLabel(self.centralwidget)
        self.lblVoltage.setGeometry(QtCore.QRect(10, 190, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblVoltage.setFont(font)
        self.lblVoltage.setAccessibleDescription("")
        self.lblVoltage.setStyleSheet("color: rgb(85, 255, 127);")
        self.lblVoltage.setObjectName("lblVoltage")

        # Current label
        self.lblCurrent = QtWidgets.QLabel(self.centralwidget)
        self.lblCurrent.setGeometry(QtCore.QRect(10, 140, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblCurrent.setFont(font)
        self.lblCurrent.setAccessibleDescription("")
        self.lblCurrent.setStyleSheet("color: rgb(85, 255, 127);")
        self.lblCurrent.setObjectName("lblCurrent")

        # Power result LCD
        self.lcdPower = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdPower.setGeometry(QtCore.QRect(273, 90, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcdPower.setFont(font)
        self.lcdPower.setStyleSheet("background-color: '#0000ff'; text-align: right;")
        self.lcdPower.setObjectName("lcdPower")

        # Current result LCD
        self.lcdCurrent = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdCurrent.setGeometry(QtCore.QRect(273, 140, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcdCurrent.setFont(font)
        self.lcdCurrent.setStyleSheet("background-color: '#0000ff'; text-align: right;")
        self.lcdCurrent.setObjectName("lcdCurrent")

        # Voltage result LCD
        self.lcdVoltage = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdVoltage.setGeometry(QtCore.QRect(273, 190, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcdVoltage.setFont(font)
        self.lcdVoltage.setStyleSheet("background-color: '#0000ff'; text-align: right;")
        self.lcdVoltage.setObjectName("lcdVoltage")

        # Resistance result LCD
        self.lcdResistance = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdResistance.setGeometry(QtCore.QRect(273, 240, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcdResistance.setFont(font)
        self.lcdResistance.setStyleSheet("background-color: '#0000ff'; text-align: right;")
        self.lcdResistance.setObjectName("lcdResistance")

        # Button
        self.cmdCalculate = QtWidgets.QPushButton(self.centralwidget)
        self.cmdCalculate.setGeometry(QtCore.QRect(120, 290, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cmdCalculate.setFont(font)
        self.cmdCalculate.setStyleSheet("background-color: '#A6A6A6';")
        self.cmdCalculate.setObjectName("cmdCalculate")

        # Top instruction label
        self.lblInstruction = QtWidgets.QLabel(self.centralwidget)
        self.lblInstruction.setGeometry(QtCore.QRect(10, -10, 351, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblInstruction.setFont(font)
        self.lblInstruction.setStyleSheet("color: rgb(0, 170, 127);")
        self.lblInstruction.setWordWrap(True)
        self.lblInstruction.setObjectName("lblInstruction")

        # Menu bar
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 371, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)

        QtCore.QMetaObject.connectSlotsByName(main_window)

        # Tab order
        main_window.setTabOrder(self.txtPower, self.txtCurrent)
        main_window.setTabOrder(self.txtCurrent, self.txtVoltage)
        main_window.setTabOrder(self.txtVoltage, self.txtResistance)
        main_window.setTabOrder(self.txtResistance, self.cmdCalculate)

        # Button event handler assignment
        self.cmdCalculate.clicked.connect(self.cmdcalculate_clicked)

    def retranslate_ui(self, main_window):
        """Sets up UI display"""
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Electronics Calculator"))
        self.lblPower.setText(_translate("main_window", "Power (Watts):"))
        self.lblResistance.setText(_translate("main_window", "Resistance (Ohms):"))
        self.lblVoltage.setText(_translate("main_window", "Voltage (Volts):"))
        self.lblCurrent.setText(_translate("main_window", "Current (Amperes):"))
        self.cmdCalculate.setText(_translate("main_window", "Calculate"))
        self.lblInstruction.setText(
            _translate("main_window", "Enter any two of the following values to compute the remainder:"))
        self.clear_lcd()

    def cmdcalculate_clicked(self):
        """Button click event handler"""
        power = current = voltage = resistance = 0.0

        if self.txtPower.text() != '':
            power = float(self.txtPower.text())

        if self.txtCurrent.text() != '':
            current = float(self.txtCurrent.text())

        if self.txtVoltage.text() != '':
            voltage = float(self.txtVoltage.text())

        if self.txtResistance.text() != '':
            resistance = float(self.txtResistance.text())

        inputs = self.count_inputs(power, current, voltage, resistance)
        count = inputs

        if count > 2:
            # too many inputs
            self.messagebox('Too many inputs')
            self.clear_lcd()
        elif count < 2:
            # insufficient number of inputs
            self.messagebox('Insufficient number of inputs')
            self.clear_lcd()
        else:
            # correct number of inputs
            if power == 0.0:
                power = ec.power(current, voltage, resistance)

            if current == 0.0:
                current = ec.current(power, voltage, resistance)

            if voltage == 0.0:
                voltage = ec.voltage(power, current, resistance)

            if resistance == 0.0:
                resistance = ec.resistance(power, current, voltage)

            self.lcdPower.display(power)
            self.lcdCurrent.display(current)
            self.lcdVoltage.display(voltage)
            self.lcdResistance.display(resistance)

    def clear_lcd(self):
        """Resets LCD boxes to default values"""
        self.lcdPower.display('0.0')
        self.lcdCurrent.display('0.0')
        self.lcdVoltage.display('0.0')
        self.lcdResistance.display('0.0')

    @staticmethod
    def messagebox(message):
        """Generates error dialog"""
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Information)
        mb.setText(message)
        mb.setWindowTitle('Input Error')
        mb.setInformativeText("Exactly two items should be entered")
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mb.exec_()

    @staticmethod
    def count_inputs(p, i, e, r):
        """Counts the number of input boxes that were filled with values"""
        retval = 0

        if p != 0:
            retval += 1

        if i != 0:
            retval += 1

        if e != 0:
            retval += 1

        if r != 0:
            retval += 1

        return retval


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
