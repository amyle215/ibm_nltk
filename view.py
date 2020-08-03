from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QGridLayout, QWidget, QFileDialog, QPushButton, \
    QTableWidget, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QColor
from model import Model
import json


class View(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.model = Model()
        self._model = None
        self._corpus = None
        self.layout = QGridLayout()
        self.title = 'Machine Translation - IBM1'
        self.left = 500
        self.top = 200
        self.width = 700
        self.height = 400

        self.sourceQLabel = QLabel(self)
        self.sourceQLineEdit = QLineEdit(self)

        self.targetQLabel = QLabel(self)
        self.targetQLineEdit = QLineEdit(self)
        self.enter_btn = QPushButton("Enter")
        self.enter_btn.clicked.connect(self._runModelSentences)

        self.openFileQLabel = QLabel(self)
        self.openFileQLineEdit = QLineEdit(self)
        self.openFile_btn = QPushButton("Browser..")

        self.typeModelQLabel = QLabel(self)
        self.typeModelQComboBox = QComboBox()
        self.iteratorQLabel = QLabel(self)
        self.iteratorQLineEdit = QLineEdit(self)

        self.tableWidget = QTableWidget()
        self.excuse_btn = QPushButton("Excuse")

        self.widget = QWidget()
        self.excuse_btn.clicked.connect(self._runModel)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileQLabel.setText('Load File:')
        self.sourceQLabel.setText('Source:')
        self.targetQLabel.setText('Target:')
        self.typeModelQLabel.setText('Model:')
        self.iteratorQLabel.setText('The number of iterator:')

        self.iteratorQLineEdit.setText('1')
        self.typeModelQComboBox.addItems(['1', '2', '3'])

        self.setCentralWidget(self.widget)

        self.createGridLayout()
        self.widget.setLayout(self.layout)

    def createGridLayout(self):

        self.layout.addWidget(self.sourceQLabel, 0, 0)
        self.layout.addWidget(self.sourceQLineEdit, 0, 1, 1, 3)

        self.layout.addWidget(self.targetQLabel, 1, 0)
        self.layout.addWidget(self.targetQLineEdit, 1, 1, 1, 3)
        self.layout.addWidget(self.enter_btn, 1, 4)

        self.layout.addWidget(self.openFileQLabel, 2, 0)
        self.layout.addWidget(self.openFileQLineEdit, 2, 1, 1, 3)
        self.layout.addWidget(self.openFile_btn, 2, 4)

        self.layout.addWidget(self.typeModelQLabel, 3, 0)
        self.layout.addWidget(self.typeModelQComboBox, 3, 1)
        self.layout.addWidget(self.iteratorQLabel, 3, 2)
        self.layout.addWidget(self.iteratorQLineEdit, 3, 3)

        self.layout.addWidget(self.excuse_btn, 4, 0)
        self.layout.addWidget(self.tableWidget, 5, 0, 5, 5)

    def setOpenFileQLineEdit(self, text):
        """Set OpenFileQLineEdit's text."""
        self.openFileQLineEdit.setText(text)

    def getOpenFileQLineEdit(self):
        """Get OpenFileQLineEdit's text."""
        return self.openFileQLineEdit.text()

    def setIteratorQLineEdit(self, text):
        """Set OpenFileQLineEdit's text."""
        self.iteratorQLineEdit.setText(text)

    def getIteratorQLineEdit(self):
        """Get OpenFileQLineEdit's text."""
        return self.iteratorQLineEdit.text()

    def openDialog(self):
        fileName, _ = QFileDialog.getOpenFileName()
        self.openFileQLineEdit.setText(fileName)

    def getTypeModel(self):
        return str(self.typeModelQComboBox.currentText())

    def createTable(self, src_vocab, trg_vocab, model):
        translation_table = model.translation_table
        self.tableWidget.setRowCount(len(trg_vocab) + 1)
        self.tableWidget.setColumnCount(len(src_vocab) + 1)
        for i in range(0, len(trg_vocab)):
            self.tableWidget.setItem(i + 1, 0, QTableWidgetItem(trg_vocab[i]))
        for j in range(0, len(src_vocab)):
            self.tableWidget.setItem(0, j + 1, QTableWidgetItem(src_vocab[j]))
        for i in range(0, len(trg_vocab)):
            maxValue, row, column = round(translation_table[trg_vocab[0]][src_vocab[0]], 2), 0, 0
            for j in range(0, len(src_vocab)):
                value = round(translation_table[trg_vocab[i]][src_vocab[j]], 2)
                self.tableWidget.setItem(i + 1, j + 1, QTableWidgetItem(str(value)))
                if value > maxValue:
                    maxValue, row, column = value, i, j
            self.tableWidget.item(row + 1, column + 1).setBackground(QColor(0, 255, 0))
        self.layout.addWidget(self.tableWidget, 5, 0, len(trg_vocab) + 1, len(src_vocab) + 1)

    def _runModelSentences(self):
        self.createTable(self.sourceQLineEdit.text().split(' '), self.targetQLineEdit.text().split(' ')
                         , self._model)

    def _runModel(self):
        self._corpus, self._model = self.model.run_model(self.getTypeModel(), self._getCorpus(),
                                                         self.getIteratorQLineEdit())
        src_vocab = [i for i in self._model.src_vocab if i]
        trg_vocab = [i for i in self._model.trg_vocab if i]
        self.createTable(src_vocab, trg_vocab, self._model)

    def _getCorpus(self):
        """Load corpus file located at `filename` into a list of dicts"""
        fileName = self.getOpenFileQLineEdit()
        if fileName is not '':
            with open(fileName, 'r') as f:
                corpus = json.load(f)
            return corpus
