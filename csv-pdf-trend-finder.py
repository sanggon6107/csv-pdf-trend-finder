from tkinter import *
from tkinter import filedialog
import pandas as pd
from tika import parser
import re
class UI :
    def __init__(self, master) :
        pass

    def SelectCsvFile(self) :
        pass

    def SelectPdfFile(self) :
        pass

    def Start(self) :
        pass


def main() :
    root = Tk()
    root.title("CSV-PDF TREND NAME FINDER")
    UI(root)
    root.mainloop()


if __name__ == "__main__" :
    main()