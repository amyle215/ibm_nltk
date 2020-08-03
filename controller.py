import json


class Controller:
    def __init__(self, model, view):
        """Controller initializer."""
        self._view = view
        self._model = model
        self._connectAction()

    def _getCorpus(self):
        """Load corpus file located at `filename` into a list of dicts"""
        fileName = self._view.getOpenFileQLineEdit()
        if fileName is not '':
            with open(fileName, 'r') as f:
                corpus = json.load(f)
            return corpus

    def _connectAction(self):
        self._view.openFile_btn.clicked.connect(self._view.openDialog)
