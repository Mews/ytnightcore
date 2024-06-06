from io import StringIO

class ConsoleIO(StringIO):
    """
    This is a StringIO that calls the function passed as callback whenever its content changes
    """

    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def write(self, s):
        super().write(s)
        self.callback()

    def writelines(self, lines):
        super().writelines(lines)
        self.callback()

    def truncate(self, pos=None):
        super().truncate(pos)
        self.callback()

    def seek(self, pos, mode=0):
        super().seek(pos, mode)
        self.callback()