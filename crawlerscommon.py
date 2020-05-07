#! python3

class SimpleFormatter:
    def __init__(self, uppercase=False, sort=True):
        self._resultset = None
        self._uppercase = uppercase
        self._sort = sort

    def setResultSet(self, resultset):
        self._resultset = resultset

    def printResult(self):
        result = None
        if self._sort:
            result = sorted(self._resultset)
        else:
            result = list(self._resultset)
        for value in result:
            if self._uppercase:
                print(value.upper())
            else:
                print(value)    

class TemplateFormatter(SimpleFormatter):
    _template = str()

    def __init__(self, prefix, postfix):
        super().__init__(uppercase=False, sort=False)
        self._template = prefix + '{0}' + postfix

    def printResult(self):
        for value in self._resultset:
            print(self._template.format(value))

class MECFormatter(SimpleFormatter):
    prefix = str()

    def __init__(self, prefix):
        super().__init__(uppercase=False, sort=False)
        self.prefix = prefix

    def printResult(self):
        i = 0
        for value in self._resultset:
            print('{0}{1}={2}'.format(self.prefix, i, value.upper()))
            i = i + 1

class Crawler:
    resultset = set()
    of = None

    def __init__(self, outputformatter=SimpleFormatter(uppercase=True)):
        self.setOutputFormatter(outputformatter)

    def setOutputFormatter(self, value):
        self.of = value
        if self.of:
            self.of.setResultSet(self.resultset)

    def clearResult(self):
        self.resultset.clear()
        
    def printResult(self):
        if self.of:
            self.of.printResult()
        else:
            print("Output Formatter not set! Call Crawler.setOutputFormatter()")    
