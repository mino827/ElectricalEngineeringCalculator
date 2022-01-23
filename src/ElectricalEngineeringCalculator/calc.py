import sys
from bs4 import BeautifulSoup
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QTextLine, QPixmap
from PyQt5.QtWidgets import (QDesktopWidget, QMainWindow, QLabel, QStatusBar, QApplication, QLCDNumber, QComboBox,
                             QPushButton, QLineEdit)
import ElectronicsCalculator.electronics_calculator as ec
import ElectronicsCalculator.scale_factors as sf


class App(QMainWindow):
    """GUI class that interacts with the ElectronicsCalculator package"""

    def center(self):
        """Center the object on screen"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def calculate(self):
        retval = 0.0

        if self.methodName == "wavelength":
            retval = ec.wavelength(float(self.txtParameter_1.text()))

        elif self.methodName == "frequency_wl":
            retval = ec.frequency_wl(float(self.txtParameter_1.text()))

        elif self.methodName == "frequency_lxl":
            retval = ec.frequency_lxl(float(self.txtParameter_1.text()),
                                      float(self.txtParameter_2.text()))

        elif self.methodName == "frequency_cxc":
            retval = ec.frequency_cxc(float(self.txtParameter_1.text()),
                                      float(self.txtParameter_2.text()))

        elif self.methodName == "antenna_length_qw":
            retval = ec.antenna_length_qw(float(self.txtParameter_1.text()))

        elif self.methodName == "capacitance_fxc":
            retval = ec.capacitance_fxc(float(self.txtParameter_1.text()),
                                        float(self.txtParameter_2.text()))

        elif self.methodName == "inductance_fxl":
            retval = ec.inductance_fxl(float(self.txtParameter_1.text()),
                                       float(self.txtParameter_2.text()))

        elif self.methodName == "back_emf":
            retval = ec.back_emf(float(self.txtParameter_1.text()),
                                 float(self.txtParameter_2.text()),
                                 float(self.txtParameter_3.text()),
                                 float(self.txtParameter_4.text()))

        elif self.methodName == "reactance_inductive_fl":
            retval = ec.reactance_inductive_fl(float(self.txtParameter_1.text()),
                                               float(self.txtParameter_2.text()))

        elif self.methodName == "reactance_capacitive_fc":
            retval = ec.reactance_capacitive_fc(float(self.txtParameter_1.text()),
                                                float(self.txtParameter_2.text()))

        elif self.methodName == "reactance_capacitive_zr":
            retval = ec.reactance_capacitive_zr(float(self.txtParameter_1.text()),
                                                float(self.txtParameter_2.text()))

        return retval

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
        """Reads calculations.xml file and provides the various bits of data to the GUI"""

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
            outputUnitScope = calculation.output.attrs.get("outputUnitScope")
            parameters = calculation.input_parameters

            count = 1
            dictParameter = {}

            for parameter in parameters:
                if parameter != '\n':
                    paramName = parameter.attrs.get("paramName")
                    dictParameter["parameter_%d" % count] = paramName
                    count += 1

            dictMethod = {
                "methodName": methodName,
                "displayName": displayName,
                "formulaImage": formulaImage,
                "description": description,
                "parameters": dictParameter,
                "outputName": outputName,
                "outputUnitScope": outputUnitScope
            }

            listMethods.append(dictMethod)

        return listMethods

    def get_Data(self, dataItem, displayName):
        retval = object

        for calculation in self.calculations:
            if calculation["displayName"] == displayName:
                retval = calculation[dataItem]
                break

        return retval

    def get_DisplayName(self, selectedIndex):
        return self.listDisplayNames[selectedIndex]

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
        displayName = self.get_DisplayName(selectedIndex)
        outputName = "Output: %s" % str(self.get_Data("outputName", displayName))

        self.lblOutput.setText(outputName)

        return

    def set_lblOutputUnitValue(self, selectedIndex):
        displayName = self.get_DisplayName(selectedIndex)
        outputUnitScope = str(self.get_Data("outputUnitScope", displayName))
        unitAbbreviation = self.get_UnitAbbreviation(outputUnitScope)
        self.lblOutputUnitValue.setText(unitAbbreviation)

        return

    def get_UnitAbbreviation(self, unit):
        retval = ""

        if unit == "HERTZ":
            retval = "Hz"
        elif unit == "OHMS":
            retval = "Ω"
        elif unit == "SECONDS":
            retval = "s"
        elif unit == "HENRIES":
            retval = "H"
        elif unit == "FARADS":
            retval = "F"
        elif unit == "METERS":
            retval = "m"
        elif unit == "VOLTS":
            retval = "V"
        else:
            retval = ""

        return retval

    def set_Parameters(self, selectedIndex):
        if selectedIndex != -1:
            displayName = self.get_DisplayName(selectedIndex)
            parameters = self.get_Data("parameters", displayName)
            parameterCount = len(parameters)

            if parameterCount == 5:
                self.lblParameter_5.show()
                self.txtParameter_5.show()
                self.cmbUnitOptions_5.show()
                self.lblParameter_5.setText(parameters["parameter_5"] + ":")

                self.lblParameter_4.show()
                self.txtParameter_4.show()
                self.cmbUnitOptions_4.show()
                self.lblParameter_4.setText(parameters["parameter_4"] + ":")

                self.lblParameter_3.show()
                self.txtParameter_3.show()
                self.cmbUnitOptions_3.show()
                self.lblParameter_3.setText(parameters["parameter_3"] + ":")

                self.lblParameter_2.show()
                self.txtParameter_2.show()
                self.cmbUnitOptions_2.show()
                self.lblParameter_2.setText(parameters["parameter_2"] + ":")

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
                self.lblParameter_1.setText(parameters["parameter_1"] + ":")

            elif parameterCount == 4:
                self.lblParameter_5.hide()
                self.txtParameter_5.hide()
                self.cmbUnitOptions_5.hide()

                self.lblParameter_4.show()
                self.txtParameter_4.show()
                self.cmbUnitOptions_4.show()
                self.lblParameter_4.setText(parameters["parameter_4"] + ":")

                self.lblParameter_3.show()
                self.txtParameter_3.show()
                self.cmbUnitOptions_3.show()
                self.lblParameter_3.setText(parameters["parameter_3"] + ":")

                self.lblParameter_2.show()
                self.txtParameter_2.show()
                self.cmbUnitOptions_2.show()
                self.lblParameter_2.setText(parameters["parameter_2"] + ":")

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
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
                self.lblParameter_3.setText(parameters["parameter_3"] + ":")

                self.lblParameter_2.show()
                self.txtParameter_2.show()
                self.cmbUnitOptions_2.show()
                self.lblParameter_2.setText(parameters["parameter_2"] + ":")

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
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
                self.lblParameter_2.setText(parameters["parameter_2"] + ":")

                self.lblParameter_1.show()
                self.txtParameter_1.show()
                self.cmbUnitOptions_1.show()
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
        displayName = self.get_DisplayName(selectedIndex)
        self.methodName = str(self.get_Data("methodName", displayName))

        return

    # ==============
    # EVENT HANDLERS
    # ==============
    def statusBar_Hover(self, message):
        self.statusBar.showMessage(message, 5000)

    def cmdClear_Click(self):
        self.resetAll()

    def cmdCalculate_Click(self):
        result = self.calculate()
        self.lcdOutput.display(result)

        return

    def cmdChangeOutputUnit_Click(self):
        pass

    def cmbCalculationSelect_Change(self, index):
        selectedIndex = int(index - 1)  # subtract one to accommodate for the injected placeholder

        self.set_lblFormulaDescription(selectedIndex)
        self.set_lblOutput(selectedIndex)
        self.set_Parameters(selectedIndex)
        self.set_Method(selectedIndex)
        self.set_lblOutputUnitValue(selectedIndex)

        return

    # ======================
    # INITIALIZATION METHODS
    # ======================
    def __init__(self):
        super().__init__()
        self.fontCombo2 = None
        self.helpAboutSubMenu = None
        self.helpMenu = None
        self.editMenu = None
        self.fileExitSubMenu = None
        self.fileMenu = None
        self.mainMenu = None
        self.lblCalcOptions = None
        self.lblFormula = None
        self.lblOutput = None
        self.lblInputs = None
        self.lblFormulaDescriptionTitle = None
        self.cmdCalculate = None
        self.fontDescription = None
        self.fontButton = None
        self.fontCombo = None
        self.fontLabel = None
        self.cmdClear = None
        self.cmbCalculationSelect = None
        self.calcOptions = None
        self.lblParameter_2 = None
        self.lblParameter_4 = None
        self.lblParameter_5 = None
        self.lblParameter_3 = None
        self.lblFormulaDescription = None
        self.unitOptions_5 = None
        self.txtParameter_3 = None
        self.unitOptions_3 = None
        self.cmbUnitOptions_4 = None
        self.txtParameter_4 = None
        self.txtParameter_5 = None
        self.cmbUnitOptions_3 = None
        self.unitOptions_4 = None
        self.cmbUnitOptions_5 = None
        self.cmbUnitOptions_2 = None
        self.unitOptions_2 = None
        self.txtParameter_2 = None
        self.unitOptions_1 = None
        self.cmbUnitOptions_1 = None
        self.cmdChangeOutputUnit = None
        self.lblOutputUnit = None
        self.lblOutputUnitValue = None
        self.txtParameter_1 = None
        self.lblParameter_1 = None
        self.statusBar = None
        self.lcdOutput = None
        self.lblImg = None
        self.imagePath = None
        self.calculations = None
        self.methodName = None
        self.listDisplayNames = []
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

        for calculation in self.calculations:
            self.listDisplayNames.append(calculation["displayName"])

        self.listDisplayNames.sort()

        # Initialize all child controls
        self.init_fonts()
        self.init_menuBar()
        self.init_calculationSelectControls()
        self.init_formulaDisplayControls()
        self.init_lcdOutputControls()
        self.init_outputUnitControls()
        self.init_cmdChangeOutputUnit()
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

        self.unitOptions_1 = ['-- Select Unit --', 'Unit1', 'Unit2', 'Unit3', 'Unit4']
        self.cmbUnitOptions_1 = QComboBox()
        self.cmbUnitOptions_1.addItems(self.unitOptions_1)
        self.cmbUnitOptions_1.setParent(self)
        self.cmbUnitOptions_1.setGeometry(305, 200, 150, 25)
        self.cmbUnitOptions_1.setFont(self.fontCombo)
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

        self.unitOptions_2 = ['-- Select Unit --', 'Unit1', 'Unit2', 'Unit3', 'Unit4']
        self.cmbUnitOptions_2 = QComboBox()
        self.cmbUnitOptions_2.addItems(self.unitOptions_2)
        self.cmbUnitOptions_2.setParent(self)
        self.cmbUnitOptions_2.setGeometry(305, 250, 150, 25)
        self.cmbUnitOptions_2.setFont(self.fontCombo)
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

        self.unitOptions_3 = ['-- Select Unit --', 'Unit1', 'Unit2', 'Unit3', 'Unit4']
        self.cmbUnitOptions_3 = QComboBox()
        self.cmbUnitOptions_3.addItems(self.unitOptions_3)
        self.cmbUnitOptions_3.setParent(self)
        self.cmbUnitOptions_3.setGeometry(305, 300, 150, 25)
        self.cmbUnitOptions_3.setFont(self.fontCombo)
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

        self.unitOptions_4 = ['-- Select Unit --', 'Unit1', 'Unit2', 'Unit3', 'Unit4']
        self.cmbUnitOptions_4 = QComboBox()
        self.cmbUnitOptions_4.addItems(self.unitOptions_4)
        self.cmbUnitOptions_4.setParent(self)
        self.cmbUnitOptions_4.setGeometry(305, 350, 150, 25)
        self.cmbUnitOptions_4.setFont(self.fontCombo)
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

        self.unitOptions_5 = ['-- Select Unit --', 'Unit1', 'Unit2', 'Unit3', 'Unit4']
        self.cmbUnitOptions_5 = QComboBox()
        self.cmbUnitOptions_5.addItems(self.unitOptions_5)
        self.cmbUnitOptions_5.setParent(self)
        self.cmbUnitOptions_5.setGeometry(305, 400, 150, 25)
        self.cmbUnitOptions_5.setFont(self.fontCombo)
        self.cmbUnitOptions_5.setStyleSheet("background-color: #555555; color: white; padding: 0px 5px 0px 5px; "
                                            "border: 1px solid; border-color: #212121;")
        self.cmbUnitOptions_5.setToolTip("Select the applicable unit scale for this input")

    def init_cmdChangeOutputUnit(self):
        self.cmdChangeOutputUnit = QPushButton("Change Unit")
        self.cmdChangeOutputUnit.setParent(self)
        self.cmdChangeOutputUnit.setGeometry(717, 155, 75, 20)
        self.cmdChangeOutputUnit.setStyleSheet("background-color: #555555; border-color: #212121; color: white; "
                                               "padding-bottom: 3px;")

    def init_outputUnitControls(self):
        self.lblOutputUnitValue = QLabel()
        self.lblOutputUnitValue.setParent(self)
        self.lblOutputUnitValue.setGeometry(762, 120, 25, 10)
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
        self.fontLabel.setPointSize(16)

        self.fontCombo = QFont()
        self.fontCombo.setPointSize(14)

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
