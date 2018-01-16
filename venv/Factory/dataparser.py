
class ParserFactory:
    """Strategy for DataParsers"""
    def __init__(self, parsetype):
        """

        :param parsetype: str
        :type parsetype: AbsParser
        """
        self.parsetype = parsetype

    def process(self, filter_words, count=5):
        """

        :param filter_words: List of keyword
        :param count: limit result filtered per resource
        :return: void
        :rtype: Void
        """
        self.parsetype.process(filter_words, count)