import random
import traceback

import sys

import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDockWidget, QApplication, QMessageBox, QMainWindow, QGraphicsOpacityEffect, QAction, \
    QFileDialog
from numpy import *

import Const  # file for keeping const variables
from eeg_data.ImportedData import ImportedData

# from input_interface.Reader import Reader

flag1 = 0

class MainWindow(QMainWindow):      # class MainWindow inherits QMainWindow (class for program's main window purposes, inherits more general QWidget)
    def __init__(self):             # __init__ is a constructor, self as a parameter represents instance of the object which calls the method
                                    # (a reference to an object that is being created)
                                    # 'self' name goes by convention.
        super().__init__()          # super() returns parent object of the MainWindow class (here: QMainWindow) and then it's constructor is called
        self.setObjectName("MainWindowCSS")                       # setting instance (parent) name for CSS styling purposes
        
    def createUI(self):

        settingStyle = " QWidget#MainWindowCSS { background-image:url(./" + Const.BCKG_IMG_STRING + "); " \
                       "                       background-repeat: none;" \
                       "                       background-position: center; } "     # by referencing to only one instance of object(#MyContainer)
                                                                                    # , child widgets (like menubar, statusbar)-
                                                                                    # -wont get inherited attributes (CSS specific syntax)
        self.setStyleSheet(settingStyle)

        ###WINDOW PROPERTIES###

        self.setWindowTitle(Const.APP_NAME_STRING)
        self.setWindowIcon(QIcon(Const.APP_ICON_STRING))           # creating QIcon object and passing cwd path to the icon to be displayed.
        self.setStatusTip("Test flag = " + str(flag1))

        ###STATUSBAR###

        dziwkikoksilasery = QGraphicsOpacityEffect()
        dziwkikoksilasery.setOpacity(0.45)
        self.statusBar().setGraphicsEffect(dziwkikoksilasery)       # ... self explanatory

        ###MENUBAR###

        menubar = self.menuBar()                                    # creates and returns an empty QMenuBar with parent MainWindow object
        filemenu = menubar.addMenu("File")
        viewmenu = menubar.addMenu("View")

        loadFile = QAction(QIcon(Const.LOAD_ICON_STRING), "Load", self)         # QAction class object provides UI action that can be inserted into widgets and then connected to slots
                                                                    # http://doc.qt.io/qt-5/signalsandslots.html
                                                                    # Actions can be performed with bars or keyboard shortcuts
        loadFile.setShortcut("Ctrl+O")
        loadFile.setStatusTip("Load a file")                        # displayed on statusBar object
        loadFile.triggered.connect(self.showDialog)

        quitPlease = QAction("Quit", self)
        quitPlease.setStatusTip("Quit the program")
        quitPlease.triggered.connect(self.close)                    # when action is triggered (by mouse or keyboard) sends QCloseEvent signal (reimplemented below)
                                                                    # to the MainWindow-close slot; see signalsandslots documentation
                                                                    # "close" is written without brackets, because the method is PASSED to connect() method, not CALLED

        changeFlag = QAction("Test flag = " + str(flag1), self)                    ### for test purposes ###
        changeFlag.setShortcut("Ctrl+G")
        changeFlag.triggered.connect(lambda: self.changeFlagMethod(changeFlag, flag1))
                                                                    # lambda passing parameters to function call to function connect() which
                                                                    # requires method name as a slot
                                                                    # interchangeable with functools.partial
        filemenu.addAction(loadFile)
        filemenu.addAction(quitPlease)
        filemenu.addAction(changeFlag)
        filemenu.menuAction().setStatusTip("File menu")            # for QMenu, the text is stored in menuAction action statusTip

        fullScreen = QAction("Full screen", self)                  # switch for fullscreen(presentation)/windowed mode
        fullScreen.setShortcut("Ctrl+Q")
        fullScreen.setStatusTip("Make the main window full screen")
        fullScreen.setCheckable(1)
        fullScreen.triggered.connect(self.fullScreenMethod)

        showPlot = QAction("View plot", self)                      #will run viewPlotMethod() everytime its triggered
        showPlot.setShortcut("Ctrl+B")
        showPlot.setStatusTip("Show the plot made from loaded data")
        showPlot.triggered.connect(lambda: self.viewPlotMethod(data))

        viewmenu.menuAction().setStatusTip("View menu")
        viewmenu.addAction(fullScreen)
        #viewmenu.addAction(showPlot)           temporarily not added, implementation for pyqt5 signal emitting not trivial ;)




    def viewPlotMethod(self, data):
        plotDockWidget = QDockWidget("Plot", self)
        PlotLWidget = pg.GraphicsLayoutWidget()                                #pyqtgraph class for making widget-ready plots
        #PlotLWidget.useOpenGL(True) sucks
        asd = PlotLWidget.addPlot()
        asd.hideAxis("left")
        #PlotLWidget.nextRow = super().newNextRow
        pen_list = ["r", "g", "c", "m", "y", "k", "w"]
        x = 0                                                           #only 10 lines now
        coeff = 0
        for key in sorted(data["signal"].keys()):
            # if key == "info":
            #     continue
            if x >= 10:
                break
            curve1 = pg.PlotCurveItem(data["signal"][key][1]+coeff, pen=[random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), 255])  # (connect = all)
            asd.addItem(curve1)
            x += 1
            coeff += 3000
        #plotObject.plot(values[1])
        #asd.showAxis('bottom')
        plotDockWidget.setWidget(PlotLWidget)                        #making PlotWidget object set as QDockWidget
        plotDockWidget.setFloating(0)                               #in default its docked in MainWindow, 1 = floating around
        self.addDockWidget(Qt.RightDockWidgetArea, plotDockWidget)
                                                                    #   (I will reimplement all this stuff with QLayouts)
        #plotDockWidget.visibilityChanged.connect(self.blankStyle)   #neighbouring dock widgets leave gaps between them
                                                                    #   and it wasn't particularly good looking with the background
    def blankStyle(self):
        self.setStyleSheet(None)

    def fullScreenMethod(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


    ###FOR TEST PURPOSES###
    def changeFlagMethod(self, button, flag):
        global flag1
        if flag == 0:
            button.setText("Make flag = 1")
            flag1 = 1
            self.setStatusTip("1")
        else:
            button.setText("Make flag = 0")
            flag1 = 0
            self.setStatusTip("0")
    #########################

    def showDialog(self):                                           # returns path to the single file selected in dialog
        try:
            fileDialog = QFileDialog(self)
            fileDialog.setNameFilter("*.edf")
            fileDialog.setDirectory("\home")
            if fileDialog.exec():                                             # alternative is QWidget::show(), which doesn't block app flow (user can interact with fileName parent)
                file_path = fileDialog.selectedFiles()                             # right now only one file can be selected
                print(file_path)
            #return(file_path)
                #header, signal = read_edf(file_path[0])
                global data                                                 # i cant reference to connect(slot) when assigning variable.. temporary workaround now
                data = ImportedData(file_path[0]).data
                #^ this should at some point look like this: data = ImportedData(file_path) and data should be referenced with the object methods get_data() and get_info(), temporary workaround for now
                self.viewPlotMethod(data)
                #self.data_loaded.emit()
            #np.set_printoptions(threshold=np.nan)
            #for keys,values in data.items():
            #    if keys == "EEG A1" or keys == "EEG A2":
            #        self.viewPlotMethod(values[1])
        except:
            traceback.print_exc()
            # exec() deletes memory references after the window is closed
                                                                    # show() let Qt preserve pointers and memory for that window (so it can be accessed multiple times or faster)
                                                                    # http://bitesofcode.blogspot.com/2011/10/show-vs-execute.html (PyQt4)

    def closeEvent(self, event):                                    # overriding closeEvent() handler from parent QWidget, gets called when Qt receives a top-level window close() method request
        closeQuestion = QMessageBox()                               # QMessageBox provides dialog box on a screen
        closeQuestion.setWindowTitle(Const.APP_NAME_STRING)
        closeQuestion.setWindowIcon(QIcon(Const.LOAD_ICON_STRING))
        closeQuestion.setText("You sure?")

        closeQuestion.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                                                                    # "Yes" and "Cancel" are taken from predefined set of buttons; combined by OR operator (specific for this API)

        csq = closeQuestion.exec()                                  # when using QMessageBox with StandardButtons set, QMessageBox.exec() returns StandardButton value indicating
                                                                    # which one was clicked

        if csq == QMessageBox.Yes:
            event.accept()                                          # sets the accepted/ignored flag of the event object
        else:
            event.ignore()


mainthread = QApplication(sys.argv)             # mainthread is an application object, sys.argv - list of arguments form command line
mw = MainWindow()
mw.createUI()

screen_width = mainthread.desktop().screenGeometry().width()
screen_height = mainthread.desktop().screenGeometry().height()

mw.setGeometry(screen_width/20, screen_height/20, screen_width/1.1, screen_height/1.1)      #i will rewrite this
mw.show()                                      # show the widget and its children
sys.exit(mainthread.exec())                    # Enters the main event loop and waits until exit() is called, then returns the value that was passed to exit()

#TEST TEST TEST TEST TEST

            # sys.exit([arg]). exit from python interpreter by raising SystemExit exception.
            # integer x as an arg gives specific exit code to the parent process (e.g. shell)
            # ("Process finished with exit code >>x<<""), 0 considered successful
# sys.exit ensures clean exit ie. all cleanup operations are performed within SystemExit exception