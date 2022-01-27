import inspect
import sys
from bs4 import BeautifulSoup
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (QDesktopWidget, QMainWindow, QLabel, QStatusBar, QApplication, QLCDNumber, QComboBox,
                             QPushButton, QLineEdit)
import ElectronicsCalculator.electronics_calculator as ec
import ElectronicsCalculator.scale_factors as sf

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


class App(QMainWindow):
    """GUI class that interacts with the ElectronicsCalculator package"""

    def center(self):
        """Center the object on screen"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def scaleParameter(self, parameterValue, inputUnitType, inputUnitScale):
        retval = 0.0

        if parameterValue != "":
            parameterValue = float(parameterValue)
            scaleInput = self.mapUnitToEnum(inputUnitType)
            factorInput = scaleInput[inputUnitScale]
            retval = sf.scale_in(parameterValue, factorInput)

        return retval

    def calculate(self):
        """Directly interfaces with the ElectronicsCalculator module to perform the calculations"""

        retval = 0.0
        value_1 = self.txtParameter_1.text()
        value_2 = self.txtParameter_2.text()
        value_3 = self.txtParameter_3.text()
        value_4 = self.txtParameter_4.text()
        value_5 = self.txtParameter_5.text()

        parameter_1 = self.scaleParameter(value_1, self.inputUnitType_1, self.cmbUnitOptions_1.currentText())
        parameter_2 = self.scaleParameter(value_2, self.inputUnitType_2, self.cmbUnitOptions_2.currentText())
        parameter_3 = self.scaleParameter(value_3, self.inputUnitType_3, self.cmbUnitOptions_3.currentText())
        parameter_4 = self.scaleParameter(value_4, self.inputUnitType_4, self.cmbUnitOptions_4.currentText())
        parameter_5 = self.scaleParameter(value_5, self.inputUnitType_5, self.cmbUnitOptions_5.currentText())

        if self.methodName == "wavelength":
            retval = ec.wavelength(parameter_1)

        elif self.methodName == "frequency_wl":
            retval = ec.frequency_wl(parameter_1)

        elif self.methodName == "frequency_lxl":
            retval = ec.frequency_lxl(parameter_1, parameter_2)

        elif self.methodName == "frequency_cxc":
            retval = ec.frequency_cxc(parameter_1, parameter_2)

        elif self.methodName == "antenna_length_qw":
            retval = ec.antenna_length_qw(parameter_1)

        elif self.methodName == "capacitance_fxc":
            retval = ec.capacitance_fxc(parameter_1, parameter_2)

        elif self.methodName == "inductance_fxl":
            retval = ec.inductance_fxl(parameter_1, parameter_2)

        elif self.methodName == "back_emf":
            retval = ec.back_emf(parameter_1, parameter_2, parameter_3, parameter_4)

        elif self.methodName == "reactance_inductive_fl":
            retval = ec.reactance_inductive_fl(parameter_1, parameter_2)

        elif self.methodName == "reactance_capacitive_fc":
            retval = ec.reactance_capacitive_fc(parameter_1, parameter_2)

        elif self.methodName == "reactance_capacitive_zr":
            retval = ec.reactance_capacitive_zr(parameter_1, parameter_2)

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

    def resetAll(self):
        """Resets all GUI elements to their initial state"""

        # Clear calculation selector
        self.cmbCalculationSelect.setCurrentIndex(0)

        # Set lcd value
        self.lcdOutput.display(0)

        # Clear unit value
        self.lblOutputUnitValue.setText("")

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

    def readXML(self):
        """Reads calculations.xml file and provides the various bits of data to the GUI via a list of dictionaries.
        Stored in self.Calculations
        """

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

        return listMethods

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
            **time
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

    def set_Method(self, selectedIndex):
        """Does a lookup of the self.calculations dictionary for the name of the method associated with the selected
         calculation """

        displayName = self.get_DisplayName(selectedIndex)
        self.methodName = str(self.get_Data("methodName", displayName))

        return

    def set_lblFormulaDescription(self, selectedIndex):
        if selectedIndex == -1:
            description = ""
        else:
            displayName = self.get_DisplayName(selectedIndex)
            description = str(self.get_Data("description", displayName)).split("\n")
            newDescription = ""

            # lstrip each individual line and ignore the first line if it is a new line only
            if description[0] == '\r' or description[0] == '\n' or description[0] == '\t' or description[0] == '':
                del description[0]

            for line in description:
                newDescription += line.lstrip("\n\r ") + "\n"

            description = newDescription

        self.lblFormulaDescription.setText(description)

        return

    def set_lblOutput(self, selectedIndex):
        """Sets the text displayed in the 'Output:' label above the lcd"""
        displayName = self.get_DisplayName(selectedIndex)
        outputName = "Output: %s" % str(self.get_Data("outputName", displayName))

        self.lblOutput.setText(outputName)

        return

    def set_lblOutputUnitValue(self, selectedIndex):
        """Sets the lblOutputUnitValue control with the abbreviation of the currently selected output unit"""

        displayName = self.get_DisplayName(selectedIndex)
        self.outputUnitScale = str(self.get_Data("outputUnitScale", displayName))
        unitAbbreviation = self.get_UnitAbbreviation_Combined(self.outputUnitScale)
        self.lblOutputUnitValue.setText(unitAbbreviation)

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
        Does a lookup for a given unit and returns its appropriate abbreviation value

        Input: unit [str] - The unit whose abbreviation we are seeking
        Output: unitAbbreviations[unit] [str] - The abbreviation
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
        # self.outputUnitType = ""
        # self.inputUnitType_1 = ""
        # self.inputUnitType_2 = ""
        # self.inputUnitType_3 = ""
        # self.inputUnitType_4 = ""
        # self.inputUnitType_5 = ""
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
        self.resetAll()

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
        self.lcdOutput.display(0)
        self.txtParameter_1.setText("")
        self.txtParameter_2.setText("")
        self.txtParameter_3.setText("")
        self.txtParameter_4.setText("")
        self.txtParameter_5.setText("")
        self.cmbUnitOptions_1.clear()
        self.cmbUnitOptions_2.clear()
        self.cmbUnitOptions_3.clear()
        self.cmbUnitOptions_4.clear()
        self.cmbUnitOptions_5.clear()
        self.cmbChangeOutputUnit.clear()

        # Set control values for new calculation
        self.set_lblFormulaDescription(selectedIndex)
        self.set_lblOutput(selectedIndex)
        self.set_Parameters(selectedIndex)
        self.set_Method(selectedIndex)
        self.set_lblOutputUnitValue(selectedIndex)

        self.outputUnitOptions = self.get_UnitDictionary(self.outputUnitScale, "output")
        self.cmbChangeOutputUnit.addItems(self.outputUnitOptions)

        return

    # ======================
    # INITIALIZATION METHODS
    # ======================
    def __init__(self):
        super().__init__()
        self.inputUnitType_5 = None     # Used for scaling the input of parameter 5 for calculation
        self.inputUnitType_4 = None     # Used for scaling the input of parameter 4 for calculation
        self.inputUnitType_3 = None     # Used for scaling the input of parameter 3 for calculation
        self.inputUnitType_2 = None     # Used for scaling the input of parameter 2 for calculation
        self.inputUnitType_1 = None     # Used for scaling the input of parameter 1 for calculation
        self.outputUnitType = None      # Used for scaling the output of calculation
        self.listDisplayNames = None    # List of displayNames for all calculations
        self.methodName = None          # Holds the name of the currently selected calculation method
        self.outputUnitScale = None     # Holds the default value of the currently selected output unit
        self.inputUnitOptions_5 = None  # Dictionary of scale items for a given input unit type of parameter 5
        self.inputUnitOptions_4 = None  # Dictionary of scale items for a given input unit type of parameter 4
        self.inputUnitOptions_3 = None  # Dictionary of scale items for a given input unit type of parameter 3
        self.inputUnitOptions_2 = None  # Dictionary of scale items for a given input unit type of parameter 2
        self.inputUnitOptions_1 = None  # Dictionary of scale items for a given input unit type of parameter 1
        self.outputUnitOptions = None   # Dictionary of scale items for a given output unit type
        self.calculations = None        # List of dictionaries for all XML data for all calculations

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
        self.setStyleSheet("background-color: #303030; color: white;")

        # Populate various lists from XML file
        self.calculations = self.readXML()

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
        self.init_formulaDescription()
        self.init_cmdCalculate()
        self.init_cmdClear()
        self.init_statusBar()

        self.center()

    def init_statusBar(self):
        self.statusBar = QStatusBar()
        self.statusBar_Hover("Start by selecting a calculation type to perform")
        self.statusBar.setStyleSheet("background-color: #3D3D3D; color: white; border-color: #212121;")
        self.setStatusBar(self.statusBar)

    def init_cmdClear(self):
        self.cmdClear = QPushButton("Clear")
        self.cmdClear.setParent(self)
        self.cmdClear.setGeometry(590, 520, 200, 50)
        self.cmdClear.setStyleSheet("background-color: #555555; color: white; padding-bottom: 5px; border-color: "
                                    "#212121;")
        self.cmdClear.setFont(self.fontButton)
        self.cmdClear.clicked.connect(self.cmdClear_Click)

    def init_cmdCalculate(self):
        self.cmdCalculate = QPushButton("Calculate")
        self.cmdCalculate.setParent(self)
        self.cmdCalculate.setGeometry(300, 520, 200, 50)
        self.cmdCalculate.setStyleSheet("background-color: #555555; color: white; padding-bottom: 5px; border-color: "
                                        "#212121;")
        self.cmdCalculate.setFont(self.fontButton)
        self.cmdCalculate.clicked.connect(self.cmdCalculate_Click)

        return

    def init_formulaDescription(self):
        self.lblFormulaDescriptionTitle = QLabel("Calculation Description:")
        self.lblFormulaDescriptionTitle.setParent(self)
        self.lblFormulaDescriptionTitle.setGeometry(QRect(460, 170, 225, 50))
        self.lblFormulaDescriptionTitle.setAlignment(Qt.AlignLeft)
        self.lblFormulaDescriptionTitle.setFont(self.fontLabel)

        self.lblFormulaDescription = QLabel()
        self.lblFormulaDescription.setParent(self)
        self.lblFormulaDescription.setGeometry(QRect(460, 200, 330, 310))
        self.lblFormulaDescription.setWordWrap(True)
        self.lblFormulaDescription.setAlignment(Qt.AlignLeft)
        self.lblFormulaDescription.setStyleSheet("align: top; padding: 10px; border: 1px solid; border-color: #212121; "
                                                 "background-color: #3D3D3D;")
        self.lblFormulaDescription.setFont(self.fontDescription)
        self.lblFormulaDescription.setToolTip("Description of the currently selected calculation")

    def init_inputParameterControls(self):
        self.lblInputs = QLabel("Inputs:")
        self.lblInputs.setParent(self)
        self.lblInputs.setGeometry(10, 175, 250, 25)

        self.lblParameter_1 = QLabel("Parameter_1:")
        self.lblParameter_1.setParent(self)
        self.lblParameter_1.setGeometry(10, 200, 140, 25)
        self.lblParameter_1.setFont(self.fontLabel)

        self.txtParameter_1 = QLineEdit()
        self.txtParameter_1.setParent(self)
        self.txtParameter_1.setGeometry(150, 200, 150, 25)
        self.txtParameter_1.setFont(self.fontLabel)
        self.txtParameter_1.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 2px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.txtParameter_1.setAlignment(Qt.AlignRight)
        self.txtParameter_1.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_1 = QComboBox()
        self.cmbUnitOptions_1.setParent(self)
        self.cmbUnitOptions_1.setGeometry(305, 200, 150, 25)
        self.cmbUnitOptions_1.setFont(self.fontCombo)
        self.cmbUnitOptions_1.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_1.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 0px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.cmbUnitOptions_1.setToolTip("Select the applicable unit scale for this input")

        self.lblParameter_2 = QLabel("Parameter_2:")
        self.lblParameter_2.setParent(self)
        self.lblParameter_2.setGeometry(10, 250, 150, 25)
        self.lblParameter_2.setFont(self.fontLabel)

        self.txtParameter_2 = QLineEdit()
        self.txtParameter_2.setParent(self)
        self.txtParameter_2.setGeometry(150, 250, 150, 25)
        self.txtParameter_2.setFont(self.fontLabel)
        self.txtParameter_2.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 2px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.txtParameter_2.setAlignment(Qt.AlignRight)
        self.txtParameter_2.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_2 = QComboBox()
        self.cmbUnitOptions_2.setParent(self)
        self.cmbUnitOptions_2.setGeometry(305, 250, 150, 25)
        self.cmbUnitOptions_2.setFont(self.fontCombo)
        self.cmbUnitOptions_2.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_2.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 0px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.cmbUnitOptions_2.setToolTip("Select the applicable unit scale for this input")

        self.lblParameter_3 = QLabel("Parameter_3:")
        self.lblParameter_3.setParent(self)
        self.lblParameter_3.setGeometry(10, 300, 150, 25)
        self.lblParameter_3.setFont(self.fontLabel)

        self.txtParameter_3 = QLineEdit()
        self.txtParameter_3.setParent(self)
        self.txtParameter_3.setGeometry(150, 300, 150, 25)
        self.txtParameter_3.setFont(self.fontLabel)
        self.txtParameter_3.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 2px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.txtParameter_3.setAlignment(Qt.AlignRight)
        self.txtParameter_3.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_3 = QComboBox()
        self.cmbUnitOptions_3.setParent(self)
        self.cmbUnitOptions_3.setGeometry(305, 300, 150, 25)
        self.cmbUnitOptions_3.setFont(self.fontCombo)
        self.cmbUnitOptions_3.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_3.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 0px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.cmbUnitOptions_3.setToolTip("Select the applicable unit scale for this input")

        self.lblParameter_4 = QLabel("Parameter_4:")
        self.lblParameter_4.setParent(self)
        self.lblParameter_4.setGeometry(10, 350, 150, 25)
        self.lblParameter_4.setFont(self.fontLabel)

        self.txtParameter_4 = QLineEdit()
        self.txtParameter_4.setParent(self)
        self.txtParameter_4.setGeometry(150, 350, 150, 25)
        self.txtParameter_4.setFont(self.fontLabel)
        self.txtParameter_4.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 2px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.txtParameter_4.setAlignment(Qt.AlignRight)
        self.txtParameter_4.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_4 = QComboBox()
        self.cmbUnitOptions_4.setParent(self)
        self.cmbUnitOptions_4.setGeometry(305, 350, 150, 25)
        self.cmbUnitOptions_4.setFont(self.fontCombo)
        self.cmbUnitOptions_4.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_4.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 0px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.cmbUnitOptions_4.setToolTip("Select the applicable unit scale for this input")

        self.lblParameter_5 = QLabel("Parameter_5:")
        self.lblParameter_5.setParent(self)
        self.lblParameter_5.setGeometry(10, 400, 150, 25)
        self.lblParameter_5.setFont(self.fontLabel)

        self.txtParameter_5 = QLineEdit()
        self.txtParameter_5.setParent(self)
        self.txtParameter_5.setGeometry(150, 400, 150, 25)
        self.txtParameter_5.setFont(self.fontLabel)
        self.txtParameter_5.setStyleSheet(
            "background-color: #555555; color: white; padding: 0px 5px 2px 5px; border: 1px "
            "solid; border-color: #212121;")
        self.txtParameter_5.setAlignment(Qt.AlignRight)
        self.txtParameter_5.setToolTip("Enter a number for to this parameter")

        self.cmbUnitOptions_5 = QComboBox()
        self.cmbUnitOptions_5.setParent(self)
        self.cmbUnitOptions_5.setGeometry(305, 400, 150, 25)
        self.cmbUnitOptions_5.setFont(self.fontCombo)
        self.cmbUnitOptions_5.currentIndexChanged.connect(self.cmbUnitOptions_Change)
        self.cmbUnitOptions_5.setStyleSheet("background-color: #555555; color: white; padding: 0px 5px 0px 5px; "
                                            "border: 1px solid; border-color: #212121;")
        self.cmbUnitOptions_5.setToolTip("Select the applicable unit scale for this input")

    def init_cmbChangeOutputUnit(self):
        self.cmbChangeOutputUnit = QComboBox()
        self.cmbChangeOutputUnit.addItems(["-- Change Unit --"])
        self.cmbChangeOutputUnit.setParent(self)
        self.cmbChangeOutputUnit.setGeometry(688, 155, 103, 20)
        self.cmbChangeOutputUnit.currentIndexChanged.connect(self.cmbChangeOutputUnit_Change)
        self.cmbChangeOutputUnit.setStyleSheet("background-color: #555555; border-color: #212121; color: white; "
                                               "padding: 2px 0px 2px 3px;")

    def init_outputUnitControls(self):
        self.lblOutputUnitValue = QLabel()
        self.lblOutputUnitValue.setParent(self)
        self.lblOutputUnitValue.setGeometry(762, 120, 25, 15)
        self.lblOutputUnitValue.setStyleSheet("background-color: #C0D5C0; color: #000000;")

        self.lblOutputUnit = QLabel("UNIT")
        self.lblOutputUnit.setParent(self)
        self.lblOutputUnit.setGeometry(762, 135, 25, 10)
        self.lblOutputUnit.setStyleSheet("background-color: #C0D5C0; color: #000000;")

    def init_lcdOutputControls(self):
        self.lblOutput = QLabel("Output:")
        self.lblOutput.setParent(self)
        self.lblOutput.setGeometry(10, 75, 250, 25)

        self.lcdOutput = QLCDNumber()
        self.lcdOutput.setParent(self)
        self.lcdOutput.setSegmentStyle(QLCDNumber.Filled)
        self.lcdOutput.setGeometry(10, 100, 780, 50)
        self.lcdOutput.setStyleSheet("background-color: #C0D5C0; color: #000000;")
        self.lcdOutput.setDigitCount(25)
        self.lcdOutput.setToolTip("The results of the current calculation")
        self.lcdOutput.setSmallDecimalPoint(True)
        self.lcdOutput.display(0)

    def init_formulaDisplayControls(self):
        self.lblFormula = QLabel("Formula:")
        self.lblFormula.setParent(self)
        self.lblFormula.setGeometry(360, 60, 120, 25)
        self.lblFormula.setFont(self.fontLabel)

        self.imagePath = "c:\\test.jpg"
        self.lblImg = QLabel()
        self.lblImg.setPixmap(QPixmap(self.imagePath))
        self.lblImg.setParent(self)
        self.lblImg.setGeometry(460, 30, 330, 60)
        self.lblImg.setStyleSheet("border: 1px solid; border-color: #212121; background-color: #3D3D3D;")
        self.lblImg.setToolTip("The relevant formula for ths calculation")

    def init_calculationSelectControls(self):
        self.lblCalcOptions = QLabel("Solving for:")
        self.lblCalcOptions.setParent(self)
        self.lblCalcOptions.setGeometry(10, 30, 120, 25)
        self.lblCalcOptions.setFont(self.fontLabel)

        functionNames = self.listDisplayNames

        self.calcOptions = ['-- Select --'] + functionNames

        self.cmbCalculationSelect = QComboBox()
        self.cmbCalculationSelect.addItems(self.calcOptions)
        self.cmbCalculationSelect.setParent(self)
        self.cmbCalculationSelect.setGeometry(130, 30, 300, 25)
        self.cmbCalculationSelect.setFont(self.fontCombo2)
        self.cmbCalculationSelect.setToolTip("Select a calculation to perform")
        self.cmbCalculationSelect.setStyleSheet("padding-left: 5px; border: 1px solid; border-color: #212121; "
                                                "background-color: #555555;")

        self.cmbCalculationSelect.currentIndexChanged.connect(self.cmbCalculationSelect_Change)

    def init_menuBar(self):
        self.mainMenu = self.menuBar()
        self.mainMenu.setStyleSheet("menuBar {background-color: #3D3D3D; color: white; border-color: #212121;}"
                                    "menuBar:hover {background-color: #555555;}")

        self.fileMenu = self.mainMenu.addMenu('File')
        self.fileExitSubMenu = self.fileMenu.addMenu('Exit')

        self.editMenu = self.mainMenu.addMenu('Calculations')

        self.helpMenu = self.mainMenu.addMenu('Help')
        self.helpAboutSubMenu = self.helpMenu.addMenu('About')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
