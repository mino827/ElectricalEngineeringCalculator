import os
import sys

from PyQt5 import QtCore
from bs4 import BeautifulSoup
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (QDesktopWidget, QMainWindow, QLabel, QStatusBar, QApplication, QLCDNumber, QComboBox,
                             QPushButton, QLineEdit, QAction, QMessageBox)
import ElectronicsCalculator.electronics_calculator as ec
import ElectronicsCalculator.scale_factors as sf
from inspect import signature

# GLOSSARY =========================================================================================================== #
# Unit Type     - Any of the following: Capacitance, Inductance, Resistance, Frequency, Current, Power, Voltage,
#               Distance, and Time. These are the top-level classifications of the values used in electronics
#               calculations.
#
# Unit Scale    - These are the specific scales of values under each unit type. An example of unit scales under the
#               Capacitance unit type are: Farads, Millifarads, Microfarads, Nanofarads and Picofarads. All unit types
#               have numerous unit scales that they use to make it easier for a human to perform calculations.
#
# Scale Factor  - Each of these unit scales equate to a specific order of magnitude for conversion of input or output
#               values. For instance, for the Resistance unit type there are three unit scales: Ohms, Kilohms and
#               Megaohms. The scale factor for these are 0, 3 and 6 orders of magnitude, respectively. In other words,
#               the original unit value multiplied or divided by 10 to the power of the scale factor or by 1, 1000, and
#               1000000, respectively. This helps to avoid long numbers needing to be entered for calculations.
# ==================================================================================================================== #

StyleSheet = '''
QMainWindow {
    background-color: #303030; 
    color: #FFFFFF;
    border-radius: 5px;
}

QLabel {
    color: #14BC57;
}

QMessageBox {
    background-color: #303030; 
    font-size: 16px;
}

QStatusBar, QMenuBar {
    background-color: #3D3D3D; 
    color: #FFFFFF;
    border: 1px solid #212121;
}

QComboBox {
    border-radius: 5px;
    padding-left: 5px; 
    border: 1px solid #212121; 
    background-color: #3D3D3D;
    selection-background-color: #3D3D3D;
    color: orange;
}

/*
QComboBox::drop-down {
    border-radius: 5px;
    margin: 2px; 
    border: 1px solid #212121;
}

QComboBox::down-arrow {
    image: url(:/icons/down_arrow.png)
}
*/

QAbstractItemView {             
    background-color: #3D3D3D;
    selection-background-color: #555555;
    color: orange;
    selection-color: yellow;
}

QComboBox#cmbChangeOutputUnit {
    padding: 2px 0px 2px 5px;
}

QLCDNumber {
    border: 1px solid #212121; 
    border-radius: 5px;
    padding-left: 120px;
    padding-right: 50px
}

QLineEdit {
    background-color: #3D3D3D; 
    color: orange; 
    padding: 0px 5px 2px 5px; 
    border: 1px solid #212121;
    border-radius: 5px;
}
                                              
QMenuBar::item:selected {
    background-color: #212121;
    color: yellow;
}

QMenu {
    background-color: #303030;   
    color: #FFFFFF;
    border: 1px solid #212121;
}

QMenu::item {
    background-color: transparent;
}

QMenu::item:selected { 
    background-color: #3D3D3D;
    color: orange;
}

QLCDNumber, QLabel#lblOutputUnitValue, QLabel#lblOutputUnit, QLabel#lblOutput {
    background-color: #C0D5C0; 
    color: #000000;
}

QLabel#lblImg, QLabel#lblFormulaDescription {
    border: 1px solid #212121; 
    background-color: #3D3D3D;
    color: orange;
    border-radius: 5px;
}

QLabel#lblErrorDisplay {
    align: top; 
    padding: 10px;
}

QLabel#lblFormulaDescription {
    align: top; 
    padding: 30px 10px 10px 10px;
}

QLabel#lblErrorDisplay {
    background-color: #212121; 
    border: 1px solid #FF0000; 
    color: yellow;
    border-radius: 5px;
}

QPushButton {
    border-radius: 5px;        
    background-color: #3D3D3D; 
    color: orange; 
    padding: 5px; 
    border: 1px solid #212121;
}

QPushButton:hover {
    background-color: orange;
    color: #555555;
}

QPushButton:pressed {
    background-color: #3D3D3D;
    color: #14BC57;
}

QPushButton:focus, QLineEdit:focus, QComboBox:focus {
    border: 1px solid #FF0000;
}

'''


class App(QMainWindow):
    """GUI class that interacts with the ElectronicsCalculator package"""

    def scaleParameter(self, parameterValue, inputUnitType, inputUnitScale):
        retval = 0.0

        if parameterValue != "":
            try:
                parameterValue = float(parameterValue)
                scaleInput = self.mapUnitToEnum(inputUnitType)
                factorInput = scaleInput[inputUnitScale]
                retval = sf.scale_in(parameterValue, factorInput)
            except ValueError:
                self.set_lblErrorDisplay("All inputs must be numeric")

        return retval

    def calculate(self):
        """Directly interfaces with the electronics_calculator module to perform the calculations"""

        self.lblErrorDisplay.clear()
        self.lblErrorDisplay.hide()
        tupleVersion = None
        retval = 0.0
        inputValue_1 = self.txtParameter_1.text().strip()
        inputValue_2 = self.txtParameter_2.text().strip()
        inputValue_3 = self.txtParameter_3.text().strip()
        inputValue_4 = self.txtParameter_4.text().strip()
        inputValue_5 = self.txtParameter_5.text().strip()

        parameter_1 = self.scaleParameter(inputValue_1, self.inputUnitType_1, self.cmbUnitOptions_1.currentText())
        parameter_2 = self.scaleParameter(inputValue_2, self.inputUnitType_2, self.cmbUnitOptions_2.currentText())
        parameter_3 = self.scaleParameter(inputValue_3, self.inputUnitType_3, self.cmbUnitOptions_3.currentText())
        parameter_4 = self.scaleParameter(inputValue_4, self.inputUnitType_4, self.cmbUnitOptions_4.currentText())
        parameter_5 = self.scaleParameter(inputValue_5, self.inputUnitType_5, self.cmbUnitOptions_5.currentText())

        # Execute appropriate function in electronics_calculator module
        try:
            func = getattr(ec, self.methodName)
            sig = signature(func)
            parameterCount = len(sig.parameters)

            if parameterCount == 5:
                retval = func(parameter_1, parameter_2, parameter_3, parameter_4, parameter_5)
            elif parameterCount == 4:
                retval = func(parameter_1, parameter_2, parameter_3, parameter_4)
            elif parameterCount == 3:
                retval = func(parameter_1, parameter_2, parameter_3)
            elif parameterCount == 2:
                retval = func(parameter_1, parameter_2)
            elif parameterCount == 1:
                if inputValue_5 != "":
                    tupleVersion = (parameter_1, parameter_2, parameter_3, parameter_4, parameter_5)
                elif inputValue_4 != "":
                    tupleVersion = (parameter_1, parameter_2, parameter_3, parameter_4)
                elif inputValue_3 != "":
                    tupleVersion = (parameter_1, parameter_2, parameter_3)
                elif inputValue_2 != "":
                    tupleVersion = (parameter_1, parameter_2)
                elif inputValue_1 != "":
                    tupleVersion = (parameter_1,)

                if str(sig).find("tuple") > 0:
                    retval = func(tupleVersion)
                else:
                    retval = func(parameter_1)
        except Exception as e:  # Handles exceptions that the electronics_module throws
            self.set_lblErrorDisplay(e)

        # Get enum for scale_factor
        scaleOutput = self.mapUnitToEnum(self.outputUnitType)
        factorOutput = scaleOutput[self.outputUnitScale]  # extract value of the scale for use as the factor
        retval = sf.scale_out(retval, factorOutput)  # apply scale factor to the calculation output

        return retval

    def mapUnitToEnum(self, unitType):
        """Get Enum for scale factor"""
        scale = None

        for moduleItem in dir(sf):  # search through all classes in module
            if unitType == moduleItem:  # find the class that matches outputUnitType
                scale = getattr(sf, moduleItem)  # apply this Enum as the scale
                break

        return scale

    def set_lblErrorDisplay(self, message):
        message = "ERROR: %s" % message
        self.lblErrorDisplay.setText(message)
        self.lblErrorDisplay.show()

        return

    def set_UnitAbbreviations_Combined(self):
        """Gets a combined dictionary of all scales of all unit types. This is used for doing lookups."""

        capacitance = self.set_UnitAbbreviations_Capacitance()
        inductance = self.set_UnitAbbreviations_Inductance()
        resistance = self.set_UnitAbbreviations_Resistance()
        frequency = self.set_UnitAbbreviations_Frequency()
        current = self.set_UnitAbbreviations_Current()
        power = self.set_UnitAbbreviations_Power()
        voltage = self.set_UnitAbbreviations_Voltage()
        distance = self.set_UnitAbbreviations_Distance()
        time = self.set_UnitAbbreviations_Time()
        angle = self.set_UnitAbbreviations_Angle()
        gainDB = self.set_UnitAbbreviations_GainDB()
        gainA = self.set_UnitAbbreviations_GainA()

        # Merge all individual scale dictionaries into one
        combinedFactorAbbreviations = {
            **capacitance,
            **inductance,
            **resistance,
            **frequency,
            **current,
            **power,
            **voltage,
            **distance,
            **time,
            **angle,
            **gainDB,
            **gainA,
        }

        return combinedFactorAbbreviations

    def set_UnitAbbreviations_Capacitance(self):
        """Maps all scales for capacitance units to their equivalent abbreviations."""

        capacitance = {
            "FARADS": "F",
            "MILLIFARADS": "mF",
            "MICROFARADS": "µF",
            "NANOFARADS": "nF",
            "PICOFARADS": "pF"
        }

        return capacitance

    def set_UnitAbbreviations_Inductance(self):
        """Maps all scales for inductance units to their equivalent abbreviations."""

        inductance = {
            "HENRIES": "H",
            "MILLIHENRIES": "mH",
            "MICROHENRIES": "µH"
        }

        return inductance

    def set_UnitAbbreviations_Resistance(self):
        """Maps all scales for resistance units to their equivalent abbreviations."""

        resistance = {
            "OHMS": "Ω",
            "KILOHMS": "KΩ",
            "MEGAOHMS": "MΩ"
        }

        return resistance

    def set_UnitAbbreviations_Frequency(self):
        """Maps all scales for frequency units to their equivalent abbreviations."""

        frequency = {
            "HERTZ": "Hz",
            "KILOHERTZ": "KHz",
            "MEGAHERTZ": "MHz",
            "GIGAHERTZ": "GHz"
        }

        return frequency

    def set_UnitAbbreviations_Current(self):
        """Maps all scales for current units to their equivalent abbreviations."""

        current = {
            "AMPERES": "A",
            "MILLIAMPERES": "mA",
            "MICROAMPERES": "µA"
        }

        return current

    def set_UnitAbbreviations_Power(self):
        """Maps all scales for power units to their equivalent abbreviations."""

        power = {
            "WATTS": "W",
            "MEGAWATTS": "MW",
            "MILLIWATTS": "mW",
            "MICROWATTS": "µW"
        }

        return power

    def set_UnitAbbreviations_Voltage(self):
        """Maps all scales for voltage units to their equivalent abbreviations."""

        voltage = {
            "VOLTS": "V",
            "KILOVOLTS": "KV",
            "MILLIVOLTS": "mV",
            "MICROVOLTS": "µV"
        }

        return voltage

    def set_UnitAbbreviations_Distance(self):
        """Maps all scales for distance units to their equivalent abbreviations."""

        distance = {
            "METERS": "m",
            "CENTIMETERS": "cm",
            "MILLIMETERS": "mm",
            "KILOMETERS": "Km"
        }

        return distance

    def set_UnitAbbreviations_Time(self):
        """Maps all scales for time units to their equivalent abbreviations."""

        time = {
            "SECONDS": "s",
            "MILLISECONDS": "ms",
            "MICROSECONDS": "µs"
        }

        return time

    def set_UnitAbbreviations_Angle(self):
        """Maps all scales for angle units to their equivalent abbreviations."""

        angle = {
            "DEGREES": "°"
        }

        return angle

    def set_UnitAbbreviations_GainA(self):
        """Maps all scales for Gain (ratio) units to their equivalent abbreviations."""

        gaindb = {
            "RATIO": "A"
        }

        return gaindb

    def set_UnitAbbreviations_GainDB(self):
        """Maps all scales for gain (dB) units to their equivalent abbreviations."""

        gaina = {
            "DECIBELS": "dB"
        }

        return gaina

    def set_Parameters(self, selectedIndex):
        """Controls the appearance of the input parameters for the calculations"""

        if selectedIndex != -1:
            displayName = self.get_DisplayName(selectedIndex)

            # Get dictionary of all parameters for this calculation, along with their default unit types
            parameters = self.get_Data("parameters", displayName)
            parameterCount = len(parameters) / 2

            if parameterCount == 5:
                self.lblParameter_5.show()
                self.txtParameter_5.show()
                self.cmbUnitOptions_5.show()
                self.inputUnitOptions_5 = self.get_UnitDictionary(parameters["inputUnitScale_5"], "parameter_5")
                self.cmbUnitOptions_5.addItems(self.inputUnitOptions_5)
                self.lblParameter_5.setText(parameters["parameter_5"] + ":")

                self.lblParameter_4.show()
                self.txtParameter_4.show()
                self.cmbUnitOptions_4.show()
                self.inputUnitOptions_4 = self.get_UnitDictionary(parameters["inputUnitScale_4"], "parameter_4")
                self.cmbUnitOptions_4.addItems(self.inputUnitOptions_4)
                self.lblParameter_4.setText(parameters["parameter_4"] + ":")

                self.lblParameter_3.show()
                self.txtParameter_3.show()
                self.cmbUnitOptions_3.show()
                self.inputUnitOptions_3 = self.get_UnitDictionary(parameters["inputUnitScale_3"], "parameter_3")
                self.cmbUnitOptions_3.addItems(self.inputUnitOptions_3)
                self.lblParameter_3.setText(parameters["parameter_3"] + ":")

                self.lblParameter_2.show()
                self.txtParameter_2.show()
                self.cmbUnitOptions_2.show()
                self.inputUnitOptions_2 = self.get_UnitDictionary(parameters["inputUnitScale_2"], "parameter_2")
                self.cmbUnitOptions_2.addItems(self.inputUnitOptions_2)
                self.lblParameter_2.setText(parameters["parameter_2"] + ":")

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
                self.inputUnitOptions_1 = self.get_UnitDictionary(parameters["inputUnitScale_1"], "parameter_1")
                self.cmbUnitOptions_1.addItems(self.inputUnitOptions_1)
                self.lblParameter_1.setText(parameters["parameter_1"] + ":")

            elif parameterCount == 4:
                self.lblParameter_5.hide()
                self.txtParameter_5.hide()
                self.cmbUnitOptions_5.hide()

                self.lblParameter_4.show()
                self.txtParameter_4.show()
                self.cmbUnitOptions_4.show()
                self.inputUnitOptions_4 = self.get_UnitDictionary(parameters["inputUnitScale_4"], "parameter_4")
                self.cmbUnitOptions_4.addItems(self.inputUnitOptions_4)
                self.lblParameter_4.setText(parameters["parameter_4"] + ":")

                self.lblParameter_3.show()
                self.txtParameter_3.show()
                self.cmbUnitOptions_3.show()
                self.inputUnitOptions_3 = self.get_UnitDictionary(parameters["inputUnitScale_3"], "parameter_3")
                self.cmbUnitOptions_3.addItems(self.inputUnitOptions_3)
                self.lblParameter_3.setText(parameters["parameter_3"] + ":")

                self.lblParameter_2.show()
                self.txtParameter_2.show()
                self.cmbUnitOptions_2.show()
                self.inputUnitOptions_2 = self.get_UnitDictionary(parameters["inputUnitScale_2"], "parameter_2")
                self.cmbUnitOptions_2.addItems(self.inputUnitOptions_2)
                self.lblParameter_2.setText(parameters["parameter_2"] + ":")

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
                self.inputUnitOptions_1 = self.get_UnitDictionary(parameters["inputUnitScale_1"], "parameter_1")
                self.cmbUnitOptions_1.addItems(self.inputUnitOptions_1)
                self.lblParameter_1.setText(parameters["parameter_1"] + ":")

            elif parameterCount == 3:
                self.lblParameter_5.hide()
                self.txtParameter_5.hide()
                self.cmbUnitOptions_5.hide()

                self.lblParameter_4.hide()
                self.txtParameter_4.hide()
                self.cmbUnitOptions_4.hide()

                self.lblParameter_3.show()
                self.txtParameter_3.show()
                self.cmbUnitOptions_3.show()
                self.inputUnitOptions_3 = self.get_UnitDictionary(parameters["inputUnitScale_3"], "parameter_3")
                self.cmbUnitOptions_3.addItems(self.inputUnitOptions_3)
                self.lblParameter_3.setText(parameters["parameter_3"] + ":")

                self.lblParameter_2.show()
                self.txtParameter_2.show()
                self.cmbUnitOptions_2.show()
                self.inputUnitOptions_2 = self.get_UnitDictionary(parameters["inputUnitScale_2"], "parameter_2")
                self.cmbUnitOptions_2.addItems(self.inputUnitOptions_2)
                self.lblParameter_2.setText(parameters["parameter_2"] + ":")

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
                self.inputUnitOptions_1 = self.get_UnitDictionary(parameters["inputUnitScale_1"], "parameter_1")
                self.cmbUnitOptions_1.addItems(self.inputUnitOptions_1)
                self.lblParameter_1.setText(parameters["parameter_1"] + ":")

            elif parameterCount == 2:
                self.lblParameter_5.hide()
                self.txtParameter_5.hide()
                self.cmbUnitOptions_5.hide()

                self.lblParameter_4.hide()
                self.txtParameter_4.hide()
                self.cmbUnitOptions_4.hide()

                self.lblParameter_3.hide()
                self.txtParameter_3.hide()
                self.cmbUnitOptions_3.hide()

                self.lblParameter_2.show()
                self.txtParameter_2.show()
                self.cmbUnitOptions_2.show()
                self.inputUnitOptions_2 = self.get_UnitDictionary(parameters["inputUnitScale_2"], "parameter_2")
                self.cmbUnitOptions_2.addItems(self.inputUnitOptions_2)
                self.lblParameter_2.setText(parameters["parameter_2"] + ":")

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
                self.inputUnitOptions_1 = self.get_UnitDictionary(parameters["inputUnitScale_1"], "parameter_1")
                self.cmbUnitOptions_1.addItems(self.inputUnitOptions_1)
                self.lblParameter_1.setText(parameters["parameter_1"] + ":")

            elif parameterCount == 1:
                self.lblParameter_5.hide()
                self.txtParameter_5.hide()
                self.cmbUnitOptions_5.hide()

                self.lblParameter_4.hide()
                self.txtParameter_4.hide()
                self.cmbUnitOptions_4.hide()

                self.lblParameter_3.hide()
                self.txtParameter_3.hide()
                self.cmbUnitOptions_3.hide()

                self.lblParameter_2.hide()
                self.txtParameter_2.hide()
                self.cmbUnitOptions_2.hide()

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
                self.inputUnitOptions_1 = self.get_UnitDictionary(parameters["inputUnitScale_1"], "parameter_1")
                self.cmbUnitOptions_1.addItems(self.inputUnitOptions_1)
                self.lblParameter_1.setText(parameters["parameter_1"] + ":")

        else:
            self.lblParameter_5.hide()
            self.txtParameter_5.hide()
            self.cmbUnitOptions_5.hide()

            self.lblParameter_4.hide()
            self.txtParameter_4.hide()
            self.cmbUnitOptions_4.hide()

            self.lblParameter_3.hide()
            self.txtParameter_3.hide()
            self.cmbUnitOptions_3.hide()

            self.lblParameter_2.hide()
            self.txtParameter_2.hide()
            self.cmbUnitOptions_2.hide()

            self.lblParameter_1.hide()
            self.txtParameter_1.hide()
            self.cmbUnitOptions_1.hide()

        return

    def set_lblOutput(self, selectedIndex):
        """Sets the text displayed in the label at the top-left of the lcd"""
        if selectedIndex > -1:
            displayName = self.get_DisplayName(selectedIndex)
            outputName = str(self.get_Data("outputName", displayName)).upper()
        else:
            outputName = ""

        self.lblOutput.setText(outputName)

        return

    def set_lblOutputUnitValue(self, selectedIndex):
        """Sets the lblOutputUnitValue control with the abbreviation of the currently selected output unit"""

        displayName = self.get_DisplayName(selectedIndex)
        self.outputUnitScale = str(self.get_Data("outputUnitScale", displayName))
        unitAbbreviation = self.get_UnitAbbreviation_Combined(self.outputUnitScale)
        self.lblOutputUnitValue.setText(unitAbbreviation)
        self.lblOutputUnitValue.show()

        return

    def set_inputUnitValues(self, selectedIndex):
        displayName = self.get_DisplayName(selectedIndex)
        self.inputUnitOptions_1 = str(self.get_Data("inputUnitScale_1", displayName))
        self.inputUnitOptions_2 = str(self.get_Data("inputUnitScale_2", displayName))
        self.inputUnitOptions_3 = str(self.get_Data("inputUnitScale_3", displayName))
        self.inputUnitOptions_4 = str(self.get_Data("inputUnitScale_4", displayName))
        self.inputUnitOptions_5 = str(self.get_Data("inputUnitScale_5", displayName))

        return

    def get_Data(self, dataItem, displayName):
        """Extracts data from self.calculations list of dictionaries"""

        retval = object

        for calculation in self.calculations:
            if calculation["displayName"] == displayName:
                retval = calculation[dataItem]
                break

        return retval

    def get_DisplayName(self, selectedIndex):
        return self.listDisplayNames[selectedIndex]

    def get_UnitAbbreviation_Combined(self, unit):
        """
        Does a lookup for a given unit and returns its appropriate output scaling abbreviation value

        Input:
            unit [str] - The unit whose abbreviation we are seeking

        Output:
            unitAbbreviations[unit] [str] - The abbreviation
        """
        retval = ""

        if unit != "-- Change Unit --":
            unitAbbreviations = self.set_UnitAbbreviations_Combined()
            retval = unitAbbreviations[unit]

        return retval

    def get_UnitDictionary(self, unit, purpose):
        """
        Gets a dictionary specific to the unit type that was passed in. This contains all scales of that particular
        unit type. Also populates a specific variable for scaling purposes.

        Inputs:
            unit [str] - The default unit for a unit type

            purpose [str] - The reason we are calling the method, so we can populate the correct variable

        Output:
            unitDictionary[str, str]
        """

        unitType = ""
        unitDictionary = {}

        capacitance = self.set_UnitAbbreviations_Capacitance()
        inductance = self.set_UnitAbbreviations_Inductance()
        resistance = self.set_UnitAbbreviations_Resistance()
        frequency = self.set_UnitAbbreviations_Frequency()
        current = self.set_UnitAbbreviations_Current()
        power = self.set_UnitAbbreviations_Power()
        voltage = self.set_UnitAbbreviations_Voltage()
        distance = self.set_UnitAbbreviations_Distance()
        time = self.set_UnitAbbreviations_Time()
        angle = self.set_UnitAbbreviations_Angle()
        gainDB = self.set_UnitAbbreviations_GainDB()
        gainA = self.set_UnitAbbreviations_GainA()

        # Check which unit type contains the default scale passed in
        if unit in capacitance:
            unitDictionary = capacitance
            unitType = "Capacitance"

        elif unit in inductance:
            unitDictionary = inductance
            unitType = "Inductance"

        elif unit in resistance:
            unitDictionary = resistance
            unitType = "Resistance"

        elif unit in frequency:
            unitDictionary = frequency
            unitType = "Frequency"

        elif unit in current:
            unitDictionary = current
            unitType = "Current"

        elif unit in power:
            unitDictionary = power
            unitType = "Power"

        elif unit in voltage:
            unitDictionary = voltage
            unitType = "Voltage"

        elif unit in distance:
            unitDictionary = distance
            unitType = "Distance"

        elif unit in time:
            unitDictionary = time
            unitType = "Time"

        elif unit in angle:
            unitDictionary = angle
            unitType = "Angle"

        elif unit in gainDB:
            unitDictionary = gainDB
            unitType = "GainDB"

        elif unit in gainA:
            unitDictionary = gainA
            unitType = "GainA"

        if purpose == "output":
            self.outputUnitType = unitType

        elif purpose == "parameter_1":
            self.inputUnitType_1 = unitType

        elif purpose == "parameter_2":
            self.inputUnitType_2 = unitType

        elif purpose == "parameter_3":
            self.inputUnitType_3 = unitType

        elif purpose == "parameter_4":
            self.inputUnitType_4 = unitType

        elif purpose == "parameter_5":
            self.inputUnitType_5 = unitType

        return unitDictionary

    # ==============
    # EVENT HANDLERS
    # ==============
    def statusBar_Hover(self, message):
        self.statusBar.showMessage(message, 5000)

    def cmdClear_Click(self):
        # Clear calculation selector
        self.cmbCalculationSelect.setCurrentIndex(0)

        # Clear lcd value
        self.lcdOutput.display(0)

        # Clear output unit value
        self.lblOutputUnitValue.setText("")

        # Clear output unit selector
        self.cmbChangeOutputUnit.setCurrentIndex(0)
        self.cmbChangeOutputUnit.hide()

        # Clear input unit selectors
        self.cmbUnitOptions_1.setCurrentIndex(0)
        self.cmbUnitOptions_2.setCurrentIndex(0)
        self.cmbUnitOptions_3.setCurrentIndex(0)
        self.cmbUnitOptions_4.setCurrentIndex(0)
        self.cmbUnitOptions_5.setCurrentIndex(0)

        # Clear input parameters
        self.txtParameter_1.setText("")
        self.txtParameter_2.setText("")
        self.txtParameter_3.setText("")
        self.txtParameter_4.setText("")
        self.txtParameter_5.setText("")

        # Clear Calculation Description
        self.lblFormulaDescription.setText("")

        # Clear Error Display
        self.lblErrorDisplay.setText("")
        self.lblErrorDisplay.hide()

    def cmdCalculate_Click(self):
        self.lcdOutput.display(0)
        result = self.calculate()
        self.lcdOutput.display(result)

        return

    def cmbUnitOptions_Change(self, index):
        if index != -1:  # we only care if a unit has been physically selected for change

            # re-calculate if we are changing the scale of a value that has already been calculated
            if self.lcdOutput.value() != 0:
                self.cmdCalculate_Click()

    def cmbChangeOutputUnit_Change(self, index):
        if index != -1:  # we only care if a unit has been physically selected for change
            self.outputUnitScale = self.cmbChangeOutputUnit.currentText()
            unitAbbreviation = self.get_UnitAbbreviation_Combined(self.outputUnitScale)
            self.lblOutputUnitValue.setText(unitAbbreviation)

            # re-calculate if we are changing the scale of a value that has already been calculated
            if self.lcdOutput.value() != 0:
                self.cmdCalculate_Click()

    def cmbCalculationSelect_Change(self, index):
        selectedIndex = int(index - 1)  # subtract one to accommodate for the injected placeholder

        # Reset control values
        self.lblOutput.clear()
        self.lblOutputUnitValue.clear()
        self.lblOutputUnitValue.hide()
        self.lcdOutput.display(0)
        self.txtParameter_1.setText("")
        self.txtParameter_2.setText("")
        self.txtParameter_3.setText("")
        self.txtParameter_4.setText("")
        self.txtParameter_5.setText("")
        self.lblImg.clear()
        self.cmbUnitOptions_1.clear()
        self.cmbUnitOptions_2.clear()
        self.cmbUnitOptions_3.clear()
        self.cmbUnitOptions_4.clear()
        self.cmbUnitOptions_5.clear()
        self.cmbChangeOutputUnit.clear()
        self.cmbChangeOutputUnit.hide()
        self.lblFormulaDescription.clear()
        self.lblErrorDisplay.clear()
        self.lblErrorDisplay.hide()

        # ====================================== #
        # Set control values for new calculation #
        # ====================================== #

        if selectedIndex > -1:
            displayName = self.get_DisplayName(selectedIndex)
            description = str(self.get_Data("description", displayName)).split("\n")
            formulaImageName = str(self.get_Data("formulaImage", displayName))
            self.methodName = str(self.get_Data("methodName", displayName))
            self.outputUnitScale = str(self.get_Data("outputUnitScale", displayName))


            # Change formula image
            imagePath = os.path.join("images", formulaImageName)
            image = QPixmap(imagePath)
            self.lblImg.setPixmap(image)

            self.outputUnitOptions = self.get_UnitDictionary(self.outputUnitScale, "output")
            self.cmbChangeOutputUnit.show()
            self.cmbChangeOutputUnit.addItems(self.outputUnitOptions)

            newDescription = ""

            # lstrip each individual line and ignore the first line if it is a new line only
            if description[0] == '\r' or description[0] == '\n' or description[0] == '\t' or description[0] == '':
                del description[0]

            for line in description:
                newDescription += line.lstrip("\n\r ") + "\n"

            description = newDescription

            self.lblFormulaDescription.setText(description)

        self.set_lblOutput(selectedIndex)
        self.set_Parameters(selectedIndex)
        self.set_lblOutputUnitValue(selectedIndex)

        return

    def menuAbout_Triggered(self):
        msgAbout = QMessageBox()
        msgAbout.setObjectName("msgAbout")
        msgAbout.setIcon(QMessageBox.Information)
        msgAbout.setWindowTitle("About Electrical Engineering Calculator")
        msgAbout.setText("<span style='font-size: 20px;'>Electrical Engineering Calculator</span><br/>"
                         "Copyright ©2022, Mino Girimonti<br/><br/>"
                         "Version 0.1<br/><br/>"
                         "<a style='color: orange;' href='https://github.com/mino827/ElectricalEngineeringCalculator'>"
                         "https://github.com/mino827/ElectricalEngineeringCalculator</a> "
        )
        msgAbout.setStandardButtons(QMessageBox.Ok)
        msgAbout.exec_()

        return

    # ======================
    # INITIALIZATION METHODS
    # ======================
    def __init__(self):
        super().__init__()
        self.fontLabel = None  # Font control for lblCalcOptions, lblFormulaDescriptionTitle, lblFormula,
        # lblParameter_1 to lblParameter_5, txtParameter_1 to txtParameter_5

        self.fontCombo = None  # Font control for cmbUnitOptions_1 through cmbUnitOptions_5
        self.fontCombo2 = None  # Font control for cmbCalculationSelect
        self.fontButton = None  # Font control for cmdCalculate and cmdClear
        self.fontDescription = None  # Font control for lblFormulaDescription
        self.inputUnitType_5 = None  # Used for scaling the input of parameter 5 for calculation
        self.inputUnitType_4 = None  # Used for scaling the input of parameter 4 for calculation
        self.inputUnitType_3 = None  # Used for scaling the input of parameter 3 for calculation
        self.inputUnitType_2 = None  # Used for scaling the input of parameter 2 for calculation
        self.inputUnitType_1 = None  # Used for scaling the input of parameter 1 for calculation
        self.outputUnitType = None  # Used for scaling the output of calculation
        self.listDisplayNames = None  # List of displayNames for all calculations
        self.methodName = None  # Holds the name of the currently selected calculation method
        self.outputUnitScale = None  # Holds the default value of the currently selected output unit
        self.inputUnitOptions_5 = None  # Dictionary of scale items for a given input unit type of parameter 5
        self.inputUnitOptions_4 = None  # Dictionary of scale items for a given input unit type of parameter 4
        self.inputUnitOptions_3 = None  # Dictionary of scale items for a given input unit type of parameter 3
        self.inputUnitOptions_2 = None  # Dictionary of scale items for a given input unit type of parameter 2
        self.inputUnitOptions_1 = None  # Dictionary of scale items for a given input unit type of parameter 1
        self.outputUnitOptions = None  # Dictionary of scale items for a given output unit type
        self.calculations = None  # List of dictionaries for all XML data for all calculations

        self.title = 'Electrical Engineering Calculator'
        self.width = 800
        self.height = 600
        self.left = 15
        self.top = 15
        self.init_UI()

    def init_UI(self):
        """Initialize all application objects"""

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Populate various lists from XML file
        with open("calculations.xml", "r") as f:
            data = f.read()
            doc = BeautifulSoup(data, "xml")

            listMethods = []
            listCalculation = []

        for node in doc.contents[0].contents:
            if node != '\n':
                listCalculation.append(node)

        for calculation in listCalculation:
            methodName = calculation.attrs.get("methodName")
            displayName = calculation.attrs.get("displayName")
            formulaImage = calculation.attrs.get("formulaImage")
            description = calculation.description.get_text()
            outputName = calculation.output.attrs.get("outputName")
            outputUnitScale = calculation.output.attrs.get("outputUnitScale")
            parameters = calculation.input_parameters

            count = 1
            dictParameter = {}

            for parameter in parameters:
                if parameter != '\n':
                    paramName = parameter.attrs.get("paramName")
                    dictParameter["parameter_%d" % count] = paramName
                    inputUnitScale = parameter.attrs.get("inputUnitScale")
                    dictParameter["inputUnitScale_%d" % count] = inputUnitScale
                    count += 1

            dictMethod = {
                "methodName": methodName,
                "displayName": displayName,
                "formulaImage": formulaImage,
                "description": description,
                "parameters": dictParameter,
                "outputName": outputName,
                "outputUnitScale": outputUnitScale
            }

            listMethods.append(dictMethod)

        self.calculations = listMethods

        self.listDisplayNames = []

        for calculation in self.calculations:
            self.listDisplayNames.append(calculation["displayName"])

        self.listDisplayNames.sort()

        self.unitAbbreviations_Combined = self.set_UnitAbbreviations_Combined()

        # Initialize all child controls
        self.init_fonts()
        self.init_menuBar()
        self.init_calculationSelectControls()
        self.init_formulaDisplayControls()
        self.init_lcdOutputControls()
        self.init_outputUnitControls()
        self.init_cmbChangeOutputUnit()
        self.init_inputParameterControls()
        self.init_lblErrorDisplay()
        self.init_formulaDescription()
        self.init_cmdCalculate()
        self.init_cmdClear()
        self.init_statusBar()

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        return

    def init_fonts(self):
        self.fontLabel = QFont()
        self.fontLabel.setPointSize(12)

        self.fontCombo = QFont()
        self.fontCombo.setPointSize(12)

        self.fontCombo2 = QFont()
        self.fontCombo2.setPointSize(10)

        self.fontButton = QFont()
        self.fontButton.setPointSize(20)

        self.fontDescription = QFont()
        self.fontDescription.setPointSize(10)

        return

    def init_menuBar(self):
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')
        fileMenu_Exit = QAction(QIcon('exit.png'), 'E&xit', self)
        fileMenu_Exit.setObjectName("fileMenu_Exit")
        fileMenu_Exit.setShortcut('Alt+F4')
        fileMenu_Exit.setStatusTip('Exit application')
        fileMenu_Exit.triggered.connect(self.close)
        fileMenu.addAction(fileMenu_Exit)

        # calculationsMenu = mainMenu.addMenu('&Calculations')

        helpMenu = mainMenu.addMenu('&Help')

        # helpMenu_CheckUpdates = QAction('Check for &Updates', self)
        # helpMenu_CheckUpdates.setShortcut('Ctrl+U')
        # helpMenu_CheckUpdates.setStatusTip('Check for updates to the Electrical Engineering Calculator')
        # # helpMenu_CheckUpdates.triggered.connect(self.close)
        # helpMenu.addAction(helpMenu_CheckUpdates)

        helpMenu_About = QAction('&About', self)
        helpMenu_About.setShortcut('Ctrl+A')
        helpMenu_About.setStatusTip('About Electrical Engineering Calculator')
        helpMenu_About.triggered.connect(self.menuAbout_Triggered)
        helpMenu.addAction(helpMenu_About)

        return

    def init_calculationSelectControls(self):
        self.lblCalcOptions = QLabel("Solving for:")
        self.lblCalcOptions.setParent(self)
        self.lblCalcOptions.setGeometry(10, 30, 90, 25)
        self.lblCalcOptions.setFont(self.fontLabel)

        functionNames = self.listDisplayNames

        self.calcOptions = ['-- Select Calculation to Perform --'] + functionNames

        self.cmbCalculationSelect = QComboBox()
        self.cmbCalculationSelect.addItems(self.calcOptions)
        self.cmbCalculationSelect.setParent(self)
        self.cmbCalculationSelect.setGeometry(105, 30, 350, 25)
        self.cmbCalculationSelect.setFont(self.fontCombo2)
        self.cmbCalculationSelect.setToolTip("Select a calculation to perform")

        self.cmbCalculationSelect.currentIndexChanged.connect(self.cmbCalculationSelect_Change)

        return

    def init_lcdOutputControls(self):
        self.lcdOutput = QLCDNumber()
        self.lcdOutput.setParent(self)
        self.lcdOutput.setSegmentStyle(QLCDNumber.Filled)
        self.lcdOutput.setGeometry(10, 70, 780, 50)
        self.lcdOutput.setDigitCount(20)
        self.lcdOutput.setToolTip("The results of the current calculation")
        self.lcdOutput.setSmallDecimalPoint(True)
        self.lcdOutput.display(0)

        self.lblOutput = QLabel()
        self.lblOutput.setObjectName("lblOutput")
        self.lblOutput.setParent(self)
        self.lblOutput.setGeometry(15, 105, 121, 10)

        return

    def init_outputUnitControls(self):
        self.lblOutputUnitValue = QLabel()
        self.lblOutputUnitValue.setObjectName("lblOutputUnitValue")
        self.lblOutputUnitValue.setParent(self)
        self.lblOutputUnitValue.setGeometry(762, 90, 25, 15)

        lblOutputUnit = QLabel("UNIT")
        lblOutputUnit.setObjectName("lblOutputUnit")
        lblOutputUnit.setParent(self)
        lblOutputUnit.setGeometry(762, 105, 25, 10)

        return

    def init_cmbChangeOutputUnit(self):
        self.cmbChangeOutputUnit = QComboBox()
        self.cmbChangeOutputUnit.setObjectName("cmbChangeOutputUnit")
        self.cmbChangeOutputUnit.addItems(["-- Change Unit --"])
        self.cmbChangeOutputUnit.setParent(self)
        self.cmbChangeOutputUnit.setGeometry(688, 125, 103, 20)
        self.cmbChangeOutputUnit.currentIndexChanged.connect(self.cmbChangeOutputUnit_Change)

        return

    def init_inputParameterControls(self):
        self.lblParameter_1 = QLabel("Parameter_1:")
        self.lblParameter_1.setParent(self)
        self.lblParameter_1.setGeometry(13, 130, 290, 25)
        self.lblParameter_1.setFont(self.fontLabel)

        self.txtParameter_1 = QLineEdit()
        self.txtParameter_1.setParent(self)
        self.txtParameter_1.setGeometry(10, 155, 290, 25)
        self.txtParameter_1.setFont(self.fontLabel)
        self.txtParameter_1.setAlignment(Qt.AlignRight)
        self.txtParameter_1.setMaxLength(27)
        self.txtParameter_1.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_1 = QComboBox()
        self.cmbUnitOptions_1.setParent(self)
        self.cmbUnitOptions_1.setGeometry(305, 155, 150, 25)
        self.cmbUnitOptions_1.setFont(self.fontCombo)
        self.cmbUnitOptions_1.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_1.setToolTip("Select the applicable unit scale for this input")

        self.lblParameter_2 = QLabel("Parameter_2:")
        self.lblParameter_2.setParent(self)
        self.lblParameter_2.setGeometry(13, 200, 290, 25)
        self.lblParameter_2.setFont(self.fontLabel)

        self.txtParameter_2 = QLineEdit()
        self.txtParameter_2.setParent(self)
        self.txtParameter_2.setGeometry(10, 225, 290, 25)
        self.txtParameter_2.setFont(self.fontLabel)
        self.txtParameter_2.setAlignment(Qt.AlignRight)
        self.txtParameter_2.setMaxLength(27)
        self.txtParameter_2.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_2 = QComboBox()
        self.cmbUnitOptions_2.setParent(self)
        self.cmbUnitOptions_2.setGeometry(305, 225, 150, 25)
        self.cmbUnitOptions_2.setFont(self.fontCombo)
        self.cmbUnitOptions_2.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_2.setToolTip("Select the applicable unit scale for this input")

        self.lblParameter_3 = QLabel("Parameter_3:")
        self.lblParameter_3.setParent(self)
        self.lblParameter_3.setGeometry(13, 270, 290, 25)
        self.lblParameter_3.setFont(self.fontLabel)

        self.txtParameter_3 = QLineEdit()
        self.txtParameter_3.setParent(self)
        self.txtParameter_3.setGeometry(10, 295, 290, 25)
        self.txtParameter_3.setFont(self.fontLabel)
        self.txtParameter_3.setAlignment(Qt.AlignRight)
        self.txtParameter_3.setMaxLength(27)
        self.txtParameter_3.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_3 = QComboBox()
        self.cmbUnitOptions_3.setParent(self)
        self.cmbUnitOptions_3.setGeometry(305, 295, 150, 25)
        self.cmbUnitOptions_3.setFont(self.fontCombo)
        self.cmbUnitOptions_3.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_3.setToolTip("Select the applicable unit scale for this input")

        self.lblParameter_4 = QLabel("Parameter_4:")
        self.lblParameter_4.setParent(self)
        self.lblParameter_4.setGeometry(13, 340, 290, 25)
        self.lblParameter_4.setFont(self.fontLabel)

        self.txtParameter_4 = QLineEdit()
        self.txtParameter_4.setParent(self)
        self.txtParameter_4.setGeometry(10, 365, 290, 25)
        self.txtParameter_4.setFont(self.fontLabel)
        self.txtParameter_4.setAlignment(Qt.AlignRight)
        self.txtParameter_4.setMaxLength(27)
        self.txtParameter_4.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_4 = QComboBox()
        self.cmbUnitOptions_4.setParent(self)
        self.cmbUnitOptions_4.setGeometry(305, 365, 150, 25)
        self.cmbUnitOptions_4.setFont(self.fontCombo)
        self.cmbUnitOptions_4.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_4.setToolTip("Select the applicable unit scale for this input")

        self.lblParameter_5 = QLabel("Parameter_5:")
        self.lblParameter_5.setParent(self)
        self.lblParameter_5.setGeometry(13, 410, 290, 25)
        self.lblParameter_5.setFont(self.fontLabel)

        self.txtParameter_5 = QLineEdit()
        self.txtParameter_5.setParent(self)
        self.txtParameter_5.setGeometry(10, 435, 290, 25)
        self.txtParameter_5.setFont(self.fontLabel)
        self.txtParameter_5.setAlignment(Qt.AlignRight)
        self.txtParameter_5.setMaxLength(27)
        self.txtParameter_5.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_5 = QComboBox()
        self.cmbUnitOptions_5.setParent(self)
        self.cmbUnitOptions_5.setGeometry(305, 435, 150, 25)
        self.cmbUnitOptions_5.setFont(self.fontCombo)
        self.cmbUnitOptions_5.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_5.setToolTip("Select the applicable unit scale for this input")

    def init_lblErrorDisplay(self):
        self.lblErrorDisplay = QLabel()
        self.lblErrorDisplay.setObjectName("lblErrorDisplay")
        self.lblErrorDisplay.setParent(self)
        self.lblErrorDisplay.setGeometry(QRect(10, 488, 445, 40))
        self.lblErrorDisplay.setWordWrap(True)
        self.lblErrorDisplay.setAlignment(Qt.AlignLeft)
        self.lblErrorDisplay.setFont(self.fontDescription)
        self.lblErrorDisplay.setToolTip("Description of the current error, if any")

        return

    def init_formulaDisplayControls(self):
        self.lblImg = QLabel()
        self.lblImg.setObjectName("lblImg")
        self.lblImg.setParent(self)
        self.lblImg.setGeometry(460, 155, 330, 60)
        self.lblImg.setAlignment(Qt.AlignCenter)
        self.lblImg.setToolTip("The relevant formula for ths calculation")

        lblFormula = QLabel("Formula:")
        lblFormula.setObjectName("lblFormula")
        lblFormula.setParent(self)
        lblFormula.setGeometry(470, 155, 120, 25)

        return

    def init_formulaDescription(self):
        self.lblFormulaDescription = QLabel()
        self.lblFormulaDescription.setObjectName("lblFormulaDescription")
        self.lblFormulaDescription.setParent(self)
        self.lblFormulaDescription.setGeometry(QRect(460, 220, 330, 355))
        self.lblFormulaDescription.setWordWrap(True)
        self.lblFormulaDescription.setAlignment(Qt.AlignLeft)
        self.lblFormulaDescription.setFont(self.fontDescription)
        self.lblFormulaDescription.setToolTip("Description of the currently selected calculation")

        lblFormulaDescriptionTitle = QLabel("Calculation Description:")
        lblFormulaDescriptionTitle.setParent(self)
        lblFormulaDescriptionTitle.setGeometry(470, 225, 225, 25)
        lblFormulaDescriptionTitle.setAlignment(Qt.AlignLeft)
        # lblFormulaDescriptionTitle.setFont(self.fontLabel)

    def init_cmdCalculate(self):
        self.cmdCalculate = QPushButton("Calculate")
        self.cmdCalculate.setParent(self)
        self.cmdCalculate.setGeometry(100, 535, 130, 40)
        self.cmdCalculate.setFont(self.fontButton)
        self.cmdCalculate.clicked.connect(self.cmdCalculate_Click)

        return

    def init_cmdClear(self):
        self.cmdClear = QPushButton("Clear")
        self.cmdClear.setParent(self)
        self.cmdClear.setGeometry(240, 535, 130, 40)
        self.cmdClear.setFont(self.fontButton)
        self.cmdClear.clicked.connect(self.cmdClear_Click)

        return

    def init_statusBar(self):
        self.statusBar = QStatusBar()
        self.statusBar_Hover("Start by selecting a calculation type to perform")
        self.setStatusBar(self.statusBar)

        return


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    window = App()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
