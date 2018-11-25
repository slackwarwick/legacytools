#! python3

class OutputFormatter:
    result = set()

    def __init__(self):
        pass

    def setResultSet(self, resultset):
        self.result = resultset

    def printResult(self):
        pass

class UppercaseFormatter(OutputFormatter):

    def __init__(self):
        super().__init__()

    def printResult(self):
        for value in self.result:
            print(value.upper())


class TemplateFormatter(OutputFormatter):
    template = str()

    def __init__(self, prefix, postfix):
        super().__init__()
        self.template = prefix + '{0}' + postfix

    def printResult(self):
        for value in self.result:
            print(self.template.format(value))

class MECFormatter(OutputFormatter):
    prefix = str()

    def __init__(self, prefix):
        super().__init__()
        self.prefix = prefix

    def printResult(self):
        i = 0
        for value in self.result:
            print('{0}{1}={2}'.format(self.prefix, i, value.upper()))
            i = i + 1

class Crawler:
    resultset = set()
    of = None

    def __init__(self, outputformatter=UppercaseFormatter()):
        self.setOutputFormatter(outputformatter)

    def setOutputFormatter(self, value):
        self.of = value
        if self.of:
            self.of.setResultSet(self.resultset)

    def printResult(self):
        if self.of:
            self.of.printResult()
        else:
            print("Output Formatter not set! Call Crawler.setOutputFormatter()")    
