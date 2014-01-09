import sys
from PyQt4 import QtGui, QtCore, QtSvg
from PyQt4.QtWebKit import QGraphicsWebView
from kartograph import Kartograph
from kartograph import options

class MapInput(QtGui.QWidget):
    
    def __init__(self):
        super(MapInput, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        self.countries = []
        self.existingChecks = []
        
        self.K = Kartograph()
        
        self.CountryInput = QtGui.QLineEdit(self)
        
        #self.CountryList = QtGui.QTextEdit(self)
        #self.CountryList.setReadOnly(True)
        
        self.AddButton = QtGui.QPushButton("Add", self)
        self.AddButton.clicked.connect(self.buttonClicked)
        
        self.GenButton = QtGui.QPushButton('Generate', self)
        self.GenButton.clicked.connect(self.generateClicked)
        
        self.DispButton = QtGui.QPushButton('Display', self)
        self.DispButton.clicked.connect(self.displayClicked)
        
        self.statusBar = QtGui.QStatusBar(self)
        
        self.br = QtSvg.QGraphicsSvgItem("world.svg").boundingRect()
        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self.scene)
        self.SvgItem = QtSvg.QGraphicsSvgItem("world.svg").boundingRect()
        self.webview = QGraphicsWebView()
        self.webview.load(QtCore.QUrl("world.svg"))
        self.webview.setFlags(QtGui.QGraphicsItem.ItemClipsToShape)
        self.webview.setCacheMode(QtGui.QGraphicsItem.NoCache)
        self.webview.resize(self.br.width(), self.br.height())
        self.scene.addItem(self.webview)
        self.view.resize(self.br.width()+10, self.br.height()+10)
        
        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        
        self.bottomCheck = 4
        
        self.grid.addWidget(self.AddButton, 1, 1)
        self.grid.addWidget(self.GenButton, 2, 1)
        self.grid.addWidget(self.DispButton, 3, 1)
        #grid.addWidget(self.CountryList, 4, 1)
        self.grid.addWidget(self.CountryInput, 1, 2)
        self.grid.addWidget(self.statusBar, 36, 0, 1, 3, QtCore.Qt.AlignBottom)
        self.grid.addWidget(self.view, 2, 2, 34, 50)
        
        self.setLayout(self.grid)
        
        #self.center()
        self.setWindowTitle('Map Display - Width ' + str(self.br.width()) + ', Height ' + str(self.br.height()))
        
        self.generateClicked()
        self.displayClicked()
        
        self.show()
        
        
    def buttonClicked(self):
        
        country = self.CountryInput.text()
        
        #add a check for if countries contains country
        #if not (self.countries.contains(country)):
        
        self.countries.append(country)
        
        self.generateClicked()
        
        self.displayClicked()
        
        self.CountryInput.setText('')
        
        self.countries = [c for c in self.countries if not c == '']
        
    def generateClicked(self):
    
        self.generateMap(self.countries)
        #self.updateSB("Map generated.")
        self.statusBar.showMessage("Map generated.")
        
    def displayClicked(self):
        
        #add an SVG object to the main window, make this re-render that
        
        self.statusBar.showMessage("Displaying, please wait...")
        
        css = open('world2.css').read()
        cfg = options.read_map_config(open('world.json'))
        
        self.K.generate(cfg, outfile='world.svg', stylesheet=css, preview = False)
        
        self.webview.load(QtCore.QUrl("world.svg"))
        
        self.statusBar.showMessage("Map Displayed.")
        
        
        if self.CountryInput.text() and not self.CountryInput.text() in self.existingChecks:
            tempWidget = QtGui.QCheckBox(self.CountryInput.text(), self)
            tempWidget.toggle()
            tempWidget.stateChanged.connect(self.toggleDisplay)
            self.grid.addWidget(tempWidget, self.bottomCheck, 1)
            self.bottomCheck += 1
            self.existingChecks.append(self.CountryInput.text())
        
        self.updateCountryText()
        
    def generateMap(self, countrylist):
        
        self.generateCSS(countrylist)
    
    def generateCSS(self, countrylist):
    
        x = 0
        css = open('world2.css', 'w')
        #print "css opened"    
        css.write('#world {\n    fill: #f5f3f2;\n},\n')
        css.write('#countries {\n    fill: #f5f3f2;\n    stroke: #882222;\n    stroke-width: 0.5px;\n    stroke-opacity: 0.4;\n}')

        for c in countrylist:
            countryString = ',\n#countries[name=%s]{\n    fill: #ff0000;\n}' % c
            css.write(countryString)
            #print c
            #print x
            x+=x
    
        css.close()
        
    def toggleDisplay(self):
        senderText = self.sender().text()
        print self.sender().isChecked()
        if not self.sender().isChecked():
            print self.sender().text()
            self.countries = [c for c in self.countries if not c == self.sender().text()]
            print self.countries
        if self.sender().isChecked():
            self.countries.append(self.sender().text())
            print self.countries
            
        self.buttonClicked()
        
    def updateCountryText(self):
    
        CountryList = self.countries
        displayString = QtCore.QString('')
        
        for country in CountryList:
        
            displayString.append(country)
            displayString.append('\n')
        #self.CountryList.setText(displayString)
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    #mw = MainWindow()
    mp = MapInput()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
