import tkinter as tk
from pathlib import Path
from tkinter import ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

import pandas as pd


class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Tools")
        self.attributes("-alpha",1)
        self.attributes('-topmost', 1)
        self.attributes('-toolwindow', 0)
        self.attributes("-fullscreen", False)
        self.overrideredirect(False)
        self.state('normal')
        self.resizable(0,0)
        self.window_width        = 900
        self.window_height       = 600
        self.screen_width        = self.winfo_screenwidth()
        self.screen_height       = self.winfo_screenheight()
        self.position_horizontal = (self.screen_width  - self.window_width )//2
        self.position_vertical   = (self.screen_height - self.window_height)//2
        self.geometry('{}x{}+{}+{}'.format(self.window_width, self.window_height, self.position_horizontal, self.position_vertical))
        self.config(background = 'white',highlightbackground = 'white',highlightcolor = 'white',highlightthickness = 0)

        self.tabControl = ttk.Notebook(self,padding=(2,20,0,0))
        self.CurveFittingTab = tk.Frame(self.tabControl,background='white')
        self.tabControl.add(self.CurveFittingTab, text='Curve Fitting(5PL)',state='normal')
        self.tabControl.pack(expand=True, fill='both')

        self.main_frame = tk.Frame(self.CurveFittingTab)
        self.main_frame.pack(fill="both", expand="true")
        self.search_page = SearchPage(parent=self.main_frame)


class DataTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical"  , command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")
        
        self.stored_dataframe = pd.DataFrame()

    def set_datatable(self, dataframe):
        self.stored_dataframe = dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        self.delete(*self.get_children())
        columns = list(dataframe.columns)
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        for col in columns:
            self.heading(col, text=col)

        df_rows = dataframe.to_numpy().tolist()
        for row in df_rows:
            self.insert("", "end", values=row)
        return None

    def find_value(self, pairs):
        # pairs is a dictionary
        new_df = self.stored_dataframe
        for col, value in pairs.items():
            try:
                query_string = f"`{col}`.str.contains('{value}').fillna(False)"
                new_df = new_df.query(query_string, engine="python")
            except Exception :
                query_string = f"`{col}`=={value}"
                new_df = new_df.query(query_string, engine="python")
        self._draw_table(new_df)

    def reset_table(self):
        self._draw_table(self.stored_dataframe)


class SearchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_names_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background="darkgray",relief='solid',borderwidth = 2)
        self.file_names_listbox.place(relx=0,rely=0,relheight=0.25, relwidth=0.25)
        self.file_names_listbox.drop_target_register(DND_FILES)
        self.file_names_listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)# TO DO Bindin
        self.file_names_listbox.bind("<Double-1>", self._display_file)# TO DO Bindin

        self.search_entrybox = tk.Entry(parent,relief='solid',borderwidth = 2)
        self.search_entrybox.place(relx=0 , rely=0.25, relwidth=0.25)
        self.search_entrybox.bind("<Return>", self.search_table)# TO DO Bindin

        # Treeview
        self.data_table = DataTable(parent)
        self.data_table.place(relx=0 ,rely=0.3,  relwidth=0.25, relheight=0.65)

        self.path_map = {}

    def drop_inside_list_box(self, event):
        file_paths = self._parse_drop_files(event.data)
        current_listbox_items = set(self.file_names_listbox.get(0, "end"))
        for file_path in file_paths:
            if file_path.endswith(".csv"):
                path_object = Path(file_path)
                file_name = path_object.name
                if file_name not in current_listbox_items:
                    self.file_names_listbox.insert("end", file_name)
                    self.path_map[file_name] = file_path

    def _display_file(self, event):
        file_name = self.file_names_listbox.get(self.file_names_listbox.curselection())
        path = self.path_map[file_name]
        df = pd.read_csv(path)
        self.data_table.set_datatable(dataframe=df)

    def _parse_drop_files(self, filename):
        # 'C:/Users/Owner/Downloads/RandomStock Tickers.csv C:/Users/Owner/Downloads/RandomStockTickers.csv'
        size = len(filename)
        res = []  # list of file paths
        name = ""
        idx = 0
        while idx < size:
            if filename[idx] == "{":
                j = idx + 1
                while filename[j] != "}":
                    name += filename[j]
                    j += 1
                res.append(name)
                name = ""
                idx = j
            elif filename[idx] == " " and name != "":
                res.append(name)
                name = ""
            elif filename[idx] != " ":
                name += filename[idx]
            idx += 1
        if name != "":
            res.append(name)
        return res

    def search_table(self, event):
        # column value. [[column,value],column2=value2]....
        entry = self.search_entrybox.get()
        if entry == "":
            self.data_table.reset_table()
        else:
            entry_split = entry.split(",")
            column_value_pairs = {}
            for pair in entry_split:
                pair_split = pair.split("=")
                if len(pair_split) == 2:
                    col = pair_split[0]
                    lookup_value = pair_split[1]
                    column_value_pairs[col] = lookup_value
            self.data_table.find_value(pairs=column_value_pairs)


if __name__ == "__main__":
    root = Application()
    root.mainloop()