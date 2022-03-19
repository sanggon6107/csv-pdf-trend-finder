from tkinter import *
from tkinter import filedialog
import pandas as pd
from tika import parser
import re
class UI :
    def __init__(self, master) :
        self.master = master
        master.geometry("640x480+200+200")
        master.resizable(False, False)

        self.frame_csv = LabelFrame(master, text = "csv 파일")
        self.frame_csv.pack(fill = "x", padx = 10, pady = 10, ipadx = 10)

        self.entry_csv_path = Entry(self.frame_csv)
        self.entry_csv_path.pack(side = "left", expand = True, fill = "x", padx = 10, pady = 5, ipady = 5)

        self.select_csv = Button(self.frame_csv, text = "찾아보기", command = self.SelectCsvFile)
        self.select_csv.pack(side = "left", padx = 5)

        self.frame_pdf = LabelFrame(master, text = "pdf 파일")
        self.frame_pdf.pack(fill = "x", padx = 10, pady = 10, ipadx = 10)

        self.entry_pdf_path = Entry(self.frame_pdf)
        self.entry_pdf_path.pack(side = "left", expand = True, fill = "x", padx = 10, pady = 5, ipady = 5)

        self.select_pdf = Button(self.frame_pdf, text = "찾아보기", command = self.SelectPdfFile)
        self.select_pdf.pack(side = "left", padx = 5)

        self.frame_status_list = Frame(master)
        self.frame_status_list.pack(fill = "both", padx = 10, pady = 10)

        self.scroll_bar = Scrollbar(self.frame_status_list)
        self.scroll_bar.pack(side = "right", fill = "y")

        self.status_list = Listbox(self.frame_status_list, selectmode = "extended", height = 15, yscrollcommand=self.scroll_bar.set)
        self.status_list.pack(side = "left", fill = "both", expand = True)
        self.scroll_bar.config(command = self.status_list.yview)

        self.frame_start_exit = Frame(master)
        self.frame_start_exit.pack(fill = "x", padx = 10, pady = 10, ipadx = 10)

        self.btn_exit = Button(self.frame_start_exit, text = "종료", command = self.master.quit)
        self.btn_exit.pack(side = "right", padx = 5, pady = 5, ipadx = 10)
        self.btn_start = Button(self.frame_start_exit, text = "시작", command = self.Start)
        self.btn_start.pack(side = "right", padx = 5, pady = 5, ipadx = 10)
        

    def SelectCsvFile(self) :
        file = filedialog.askopenfilenames(title = "파일을 선택하세요,", \
            filetypes = (("csv파일", "*.csv"), ("모든 파일", "*.*")), \
            initialdir = "./")

        self.entry_csv_path.delete(0, END)
        if file != "" :
            self.entry_csv_path.insert(1, file[-1])

    def SelectPdfFile(self) :
        file = filedialog.askopenfilenames(title = "파일을 선택하세요,", \
            filetypes = (("pdf파일", "*.pdf"), ("모든 파일", "*.*")), \
            initialdir = "./")

        self.entry_pdf_path.delete(0, END)
        if file != "" :
            self.entry_pdf_path.insert(1, file[-1])

    def Start(self) :
        
        self.data = parser.from_file(self.entry_pdf_path.get())
        self.content = self.data["content"].replace("\n", "").replace(" ", "").replace("\t", "")

        self.csv_data = pd.read_csv(self.entry_csv_path.get())

        self.count_invalid = 0
        self.count_valid = 0

        for row in self.csv_data["trend"] :
            self.row_pre = row.replace(" ", "")

            if self.content.find(self.row_pre) != 1 :
                self.count_valid += 1
                continue
            else :
                itr = re.findall("-?".join(list(self.row_pre)), self.content)
                if len(itr) == 0 :
                    self.count_invalid += 1
                    self.status_list.insert(END, "There's no [{}] in the pdf file.".format(self.row_pre))
                    continue
                
                self.status_list.insert(END, "I found these for [{}] : ".format(self.row_pre))
                for m in itr :
                    self.status_list.insert(END, m)
                self.status_list.insert(END, " ")
                self.count_valid += 1
        self.status_list.insert(END, "count_valid : {0} / {1}".format(self.count_valid, len(self.csv_data)))
        self.status_list.insert(END, "count_invalid : {}".format(self.count_invalid))


def main() :
    root = Tk()
    root.title("CSV-PDF TREND NAME FINDER")
    UI(root)
    root.mainloop()


if __name__ == "__main__" :
    main()