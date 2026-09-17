#
# parser.py
#

class AbstractParser():

    @property
    def format(self) -> str:
        raise NotImplementedError


class DrumAscii_v1_3(AbstractParser):

    @property
    def format(self) -> str:
        return 'DRUM-ASCII'


class ParserFactory:
    def __init__(self, parsers: list[AbstractParser]):
        self._parsers = parsers


    def getParser(self, input: str) -> AbstractParser:
        """
        Return the right parser depending on the first line of input
        :param input:
        :return:
        """
        key, value = input.split(':', 1)
        if key.upper() == 'FORMAT':
            for p in self._parsers:
                if value.upper() == p.format:
                    return p
            raise LookupError('Format not found')
        else:
            raise LookupError("'FORMAT' line not found")

