from nltk import IBMModel1, IBMModel2, IBMModel3
from nltk.translate import AlignedSent


class Model:
    def __init__(self):
        self._typeModel = ''
        self._corpus = []
        self._iterator = 0
        self._model = None

    def getTypeModel(self):
        return self._typeModel

    def setTypeModel(self, typeModel):
        self._typeModel = typeModel

    def _preProcessing(self, corpus):
        for i in range(0, len(corpus)):
            sentences = []
            for j in corpus[i].values():
                sentences.append(j.split(' '))
            self._corpus.append(AlignedSent(sentences[1], sentences[0]))

    def _ibm1(self):
        self._model = IBMModel1(self._corpus, self._iterator)

    def _ibm2(self):
        self._model = IBMModel2(self._corpus, self._iterator)

    def _ibm3(self):
        self._model = IBMModel3(self._corpus, self._iterator)

    def run_model(self, typeModel, corpus, iterator):
        self._preProcessing(corpus)
        self._iterator = int(iterator)
        self._typeModel = typeModel
        if self._typeModel == '1':
            self._ibm1()
        if self._typeModel == '2':
            self._ibm2()
        else:
            self._ibm3()
        return self._corpus, self._model
