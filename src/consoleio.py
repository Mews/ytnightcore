from io import StringIO

class ConsoleIO(StringIO):
    """
    This is a StringIO that calls the function passed as callback whenever its content changes

    It also has a method to read a line and remove it which is popline
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
    
    def popline(self):
        #Disable the callback while running the function to avoid infinite recursion
        og_callback = self.callback
        self.callback = lambda: None

        self.seek(0) # Set the position to the beggining of the IO to read the first line
        line = self.readline()

        remaining_content = self.getvalue()[len(line):]

        self.truncate(0) # Clear the StringIO
        self.seek(0) # Set the position to the beggining of the IO
        self.write(remaining_content) # Write the content without the line

        self.callback = og_callback

        return line