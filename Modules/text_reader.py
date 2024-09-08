
class Text_Reader():
    def __init__(self, file_path : str):
        self.file_path = file_path
        self.ind = 0
        self.final_line = False

        try:
            with open(file_path) as self.file:
                self.lines = [line.strip() for line in self.file.readlines()]
        except FileNotFoundError:
            print('File Not Found')
    
    def read_cur_text(self):
        try:
            return self.lines[self.ind]
        except IndexError:
            self.ind = -1
            self.final_line = True
            return self.lines[self.ind]

    def next_line(self, lines : int = 1):
        if self.lines[self.ind] != self.lines[-1]:
            self.ind += lines
            self.final_line = False
    
    def previous_line(self, lines : int = 1):
        self.ind -= lines
        self.final_line = False
    
    def last_line(self):
        self.ind = -1
        self.final_line = True

    def change_file(self, file_path : str):
        self.file_path = file_path
        self.ind = 0
        self.final_line = False

        try:
            with open(file_path) as self.file:
                self.lines = [line.strip() for line in self.file.readlines()]
        except FileNotFoundError:
            print('File Not Found')

# EXAMPLE

# reader = Text_Reader('storyline.txt')