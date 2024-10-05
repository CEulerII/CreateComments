import tkinter as tk 
from pathlib import Path
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk



class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style("cosmo")  # 设置 ttkbootstrap 的主题
        self.title("Curve Fitting Tools")
        self.attributes("-alpha", 1)
        self.attributes('-topmost', 1)
        self.attributes('-toolwindow', 0)
        self.attributes("-fullscreen", False)
        self.overrideredirect(False)
        self.state('normal')
        self.resizable(0, 0)
        self.window_width = 900
        self.window_height = 600
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.position_horizontal = (self.screen_width - self.window_width) // 2
        self.position_vertical = (self.screen_height - self.window_height) // 2
        self.geometry('{}x{}+{}+{}'.format(self.window_width, self.window_height, self.position_horizontal, self.position_vertical))
        self.config(background='white')

        self.tabControl = ttk.Notebook(self, padding=(2, 20, 0, 0))
        self.CurveFittingTab = ttk.Frame(self.tabControl)  # 使用 ttk.Frame 替代 tk.Frame
        self.tabControl.add(self.CurveFittingTab, text='Curve Fitting(5PL)', state='normal')
        self.tabControl.pack(expand=True, fill='both')

        self.main_frame = ttk.Frame(self.CurveFittingTab)
        self.main_frame.pack(fill="both", expand="true")
        self.search_page = SearchPage(parent=self.main_frame)



class DataTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = ttk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = ttk.Scrollbar(self, orient="horizontal", command=self.xview)
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
            self.column(col, width=int(self.winfo_width() * 0.5), anchor="center")

        df_rows = dataframe.to_numpy().tolist()
        for row in df_rows:
            self.insert("", "end", values=row)
        return None


    def clear_table(self):
        self.delete(*self.get_children())
        self["columns"] = []


    def find_value(self, pairs):
        new_df = self.stored_dataframe
        for col, value in pairs.items():
            try:
                query_string = f"`{col}`.str.contains('{value}').fillna(False)"
                new_df = new_df.query(query_string, engine="python")
            except Exception:
                query_string = f"`{col}`=={value}"
                new_df = new_df.query(query_string, engine="python")

        if new_df.empty:
            self.delete(*self.get_children())
            return None

        self._draw_table(new_df)

    def reset_table(self):
        self._draw_table(self.stored_dataframe)



class SearchPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        
        self.min_label = ttk.Label(parent, text="a.Min:\nb.Min:\nc.Min:\nd.Min:\nm.Min:\n")
        self.min_label.place(relx=0.3, rely=0.7, relwidth=0.05, relheight=0.2)

        self.max_label = ttk.Label(parent, text="a.Max:\nb.Max:\nc.Max:\nd.Max:\nm.Max:\n")
        self.max_label.place(relx=0.45, rely=0.7, relwidth=0.05, relheight=0.2)
        
        
        self.a_min_entrybox = ttk.Entry(parent)
        self.a_min_entrybox.insert(0, -1)
        self.a_min_entrybox.place(relx=0.35, rely=0.71, relwidth=0.075, relheight=0.025)

        self.b_min_entrybox = ttk.Entry(parent)
        self.b_min_entrybox.insert(0, -np.inf)
        self.b_min_entrybox.place(relx=0.35, rely=0.75, relwidth=0.075, relheight=0.025)

        self.c_min_entrybox = ttk.Entry(parent)
        self.c_min_entrybox.insert(0, 0)
        self.c_min_entrybox.place(relx=0.35, rely=0.79, relwidth=0.075, relheight=0.025)

        self.d_min_entrybox = ttk.Entry(parent)
        self.d_min_entrybox.insert(0, -np.inf)
        self.d_min_entrybox.place(relx=0.35, rely=0.83, relwidth=0.075, relheight=0.025)

        self.m_min_entrybox = ttk.Entry(parent)
        self.m_min_entrybox.insert(0, -np.inf)
        self.m_min_entrybox.place(relx=0.35, rely=0.87, relwidth=0.075, relheight=0.025)

        self.a_max_entrybox = ttk.Entry(parent)
        self.a_max_entrybox.insert(0, 1)
        self.a_max_entrybox.place(relx=0.50, rely=0.71, relwidth=0.075, relheight=0.025)

        self.b_max_entrybox = ttk.Entry(parent)
        self.b_max_entrybox.insert(0, np.inf)
        self.b_max_entrybox.place(relx=0.50, rely=0.75, relwidth=0.075, relheight=0.025)

        self.c_max_entrybox = ttk.Entry(parent)
        self.c_max_entrybox.insert(0, np.inf)
        self.c_max_entrybox.place(relx=0.50, rely=0.79, relwidth=0.075, relheight=0.025)

        self.d_max_entrybox = ttk.Entry(parent)
        self.d_max_entrybox.insert(0, np.inf)
        self.d_max_entrybox.place(relx=0.50, rely=0.83, relwidth=0.075, relheight=0.025)

        self.m_max_entrybox = ttk.Entry(parent)
        self.m_max_entrybox.insert(0, np.inf)
        self.m_max_entrybox.place(relx=0.50, rely=0.87, relwidth=0.075, relheight=0.025)

        
        
        self.xdata_label = ttk.Label(parent, text="XData:")
        self.xdata_label.place(relx=0, rely=0.2, relwidth=0.05, relheight=0.05)

        self.xdata_entrybox = ttk.Entry(parent)
        self.xdata_entrybox.place(relx=0.05, rely=0.2, relwidth=0.075, relheight=0.05)

        self.ydata_label = ttk.Label(parent, text="YData:")
        self.ydata_label.place(relx=0.125, rely=0.2, relwidth=0.05, relheight=0.05)

        self.ydata_entrybox = ttk.Entry(parent)
        self.ydata_entrybox.place(relx=0.175, rely=0.2, relwidth=0.075, relheight=0.05)

        self.data_table = DataTable(parent)
        self.data_table.place(relx=0, rely=0.3, relwidth=0.25, relheight=0.65)


        self.path_map = {}
        self.current_df = None
        self.plot_frame = None

        # Bind the Enter key to the search function
        self.xdata_entrybox.bind("<Return>", self.search_table)
        self.ydata_entrybox.bind("<Return>", self.search_table)

        # Listbox for dropped files
        self.file_names_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background="lightgray", relief='sunken', borderwidth=0)
        self.file_names_listbox.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
        self.file_names_listbox.drop_target_register(DND_FILES)
        self.file_names_listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)
        self.file_names_listbox.bind("<Double-1>", self._display_file)

        self.clear_button = ttk.Button(parent, text=' File List Clear ', command=self.clear_file_list)
        self.clear_button.place(relx=0.05, rely=0.95, relwidth=0.15, relheight=0.05)

        self.start_button = ttk.Button(parent, text=' Start ', command=self.plot_5pl_curve)
        self.start_button.place(relx=0.35, rely=0.95, relwidth=0.25, relheight=0.05)


        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.f_plot = self.fig.add_subplot(111)
        self.canvs = FigureCanvasTkAgg(self.fig, parent)
        self.canvs.get_tk_widget().place(relx=0.3, rely=0, relwidth=0.65, relheight=0.65)

        self.result_label = ttk.Label(parent, text="a=\nb=\nc=\nd=\nm=\nR2=")
        self.result_label.place(relx=0.75, rely=0.7, relwidth=0.05, relheight=0.2)

        self.result_value_label = ttk.Label(parent, text="0.0000000000\n0.0000000000\n0.0000000000\n0.0000000000\n0.0000000000\n0.0000000000", justify="left", anchor="w")
        self.result_value_label.place(relx=0.8, rely=0.7, relwidth=0.15, relheight=0.2)

        self.copy_button = ttk.Button(parent, text=' Copy Result Parameter ', command=self.copy_result_to_clipboard)
        self.copy_button.place(relx=0.65, rely=0.95, relwidth=0.25, relheight=0.05)


    def drop_inside_list_box(self, event):
        file_paths = self._parse_drop_files(event.data)
        current_listbox_items = set(self.file_names_listbox.get(0, "end"))
        for file_path in file_paths:
            if not file_path.endswith(".csv"):
                messagebox.showerror(title='Warning', message='Please Input csv Files !')
                continue
            path_object = Path(file_path)
            file_name = path_object.name
            if file_name not in current_listbox_items:
                self.file_names_listbox.insert("end", file_name)
                self.path_map[file_name] = file_path


    def _display_file(self, event):
        file_name = self.file_names_listbox.get(self.file_names_listbox.curselection())
        path = self.path_map[file_name]
        df = pd.read_csv(path)

        if df.shape[1] != 2:
            messagebox.showerror(title='Warning', message='The Data File Should Only Have XData And YData !')
            return

        if list(df.columns) != ['XData', 'YData']:
            messagebox.showerror(title='Warning', message='The Data Column Name Should Be "XData" And "YData" !')
            return

        if df['XData'].count() != df['YData'].count():
            messagebox.showerror(title='Warning', message='The Number Of "XData" And "YData" Should Be The Same !')
            return

        if not pd.to_numeric(df['XData'], errors='coerce').notnull().all() or not pd.to_numeric(df['YData'], errors='coerce').notnull().all():
            messagebox.showerror(title='Warning', message='XData And YData Should Be Value !')
            return

        self.current_df = df
        self.data_table.set_datatable(dataframe=df)


    def search_table(self, event):
        if not self.path_map:  # 检查是否有文件拖入
            messagebox.showerror(title='Warning', message='Please Input a csv Files !')
            return

        if self.current_df is None:  # 检查是否有文件加载到DataTable
            messagebox.showerror(title='Warning', message='Please Double Click File Name To Input Data Into DataTable !')
            return

        # 获取XData和YData的输入值
        xdata_value = self.xdata_entrybox.get()
        ydata_value = self.ydata_entrybox.get()

        column_value_pairs = {}
        if xdata_value != "":
            column_value_pairs['XData'] = xdata_value
        if ydata_value != "":
            column_value_pairs['YData'] = ydata_value

        if column_value_pairs:
            self.data_table.find_value(pairs=column_value_pairs)
        else:
            self.data_table.reset_table()

    def clear_file_list(self):
        # 清空文件列表框中的文件名
        self.file_names_listbox.delete(0, 'end')
        self.path_map.clear()  # 清除路径映射
        self.data_table.clear_table()  # 清空DataTable并移除列标题
        self.current_df = None  # 重置current_df
        self.f_plot.clear()  # 清空绘图
        self.canvs.draw()  # 更新图表
        self.result_value_label.config(text="0.0000000000\n0.0000000000\n0.0000000000\n0.0000000000\n0.0000000000\n0.0000000000")  # 清空结果显示
    
        # 重置输入框的参数最小值和最大值为默认值
        self.a_min_entrybox.delete(0, tk.END)
        self.a_min_entrybox.insert(0, -1)
        
        self.b_min_entrybox.delete(0, tk.END)
        self.b_min_entrybox.insert(0, -np.inf)
        
        self.c_min_entrybox.delete(0, tk.END)
        self.c_min_entrybox.insert(0, 0)
        
        self.d_min_entrybox.delete(0, tk.END)
        self.d_min_entrybox.insert(0, -np.inf)
        
        self.m_min_entrybox.delete(0, tk.END)
        self.m_min_entrybox.insert(0, -np.inf)
        
        self.a_max_entrybox.delete(0, tk.END)
        self.a_max_entrybox.insert(0, 1)
        
        self.b_max_entrybox.delete(0, tk.END)
        self.b_max_entrybox.insert(0, np.inf)
        
        self.c_max_entrybox.delete(0, tk.END)
        self.c_max_entrybox.insert(0, np.inf)
        
        self.d_max_entrybox.delete(0, tk.END)
        self.d_max_entrybox.insert(0, np.inf)
        
        self.m_max_entrybox.delete(0, tk.END)
        self.m_max_entrybox.insert(0, np.inf)
        
        # 清空XData和YData输入框的值
        self.xdata_entrybox.delete(0, tk.END)
        self.ydata_entrybox.delete(0, tk.END)

        

    def _parse_drop_files(self, filename):
        size = len(filename)
        res = []
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


    def _parse_entry_values(self, entrybox):
        value = entrybox.get()
        if value.lower() == "-inf":
            return -np.inf
        elif value.lower() == "inf":
            return np.inf
        else:
            try:
                return float(value)
            except ValueError:
                messagebox.showerror(title='Warning', message='Please Enter Values As Parameter Boundary !')
                return None

    def plot_5pl_curve(self):
        if self.current_df is None:
            messagebox.showerror(title='Error', message='Please Load A File First !')
            return


        xdata = self.current_df['XData'].values
        ydata = self.current_df['YData'].values

        # 从Entry中获取最小和最大值
        a_min = self._parse_entry_values(self.a_min_entrybox)
        b_min = self._parse_entry_values(self.b_min_entrybox)
        c_min = self._parse_entry_values(self.c_min_entrybox)
        d_min = self._parse_entry_values(self.d_min_entrybox)
        m_min = self._parse_entry_values(self.m_min_entrybox)

        a_max = self._parse_entry_values(self.a_max_entrybox)
        b_max = self._parse_entry_values(self.b_max_entrybox)
        c_max = self._parse_entry_values(self.c_max_entrybox)
        d_max = self._parse_entry_values(self.d_max_entrybox)
        m_max = self._parse_entry_values(self.m_max_entrybox)

        # 检查是否有无效输入
        if None in [a_min, b_min, c_min, d_min, m_min, a_max, b_max, c_max, d_max, m_max]:
            return
        
        if a_min == np.inf or b_min == np.inf or c_min == np.inf or d_min == np.inf or m_min == np.inf:
            messagebox.showerror(title='Warning', message='Minimum Value Can Not Be Positive Infinity !')
            return
        
        if a_max == -np.inf or b_max == -np.inf or c_max == -np.inf or d_max == -np.inf or m_max == -np.inf:
            messagebox.showerror(title='Warning', message='Maximum Value Can Not Be Negative Infinity !')
            return

        # 定义5PL拟合函数
        def func_5PL(x, a, b, c, d, m):
            try:
                return abs(d + (a - d) * (1 + (x / c) ** b) ** (-m))
            except Exception:
                pass

        x = list(np.arange(0, max(xdata), 0.01))  # 设定x的范围

        # 进行5PL拟合
        param_bounds = ([a_min, b_min, c_min, d_min, m_min], [a_max, b_max, c_max, d_max, m_max])
        try:
            popt, _ = curve_fit(func_5PL, xdata, ydata, maxfev=10000, bounds=param_bounds)
        except RuntimeError as e:
            messagebox.showerror(title='Error', message=f'Curve fitting failed: {str(e)}')
            return

        # 计算R^2值
        mean = np.mean(ydata)
        ss_tot = np.sum((ydata - mean) ** 2)
        ss_res = np.sum((ydata - func_5PL(xdata, *popt)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        # 清空之前的绘图
        self.f_plot.clear()

        # 绘制拟合曲线和数据点
        self.f_plot.scatter(xdata, ydata, color='red', label='Data')
        y_fit = [func_5PL(i, *popt) for i in x]
        self.f_plot.plot(x, y_fit, color='black', label='Fitted Curve')
        self.f_plot.set_xlabel('XData')
        self.f_plot.set_ylabel('YData')

        # 显示参数和R^2值
        self.f_plot.legend([f'a={popt[0]:.5f}\n'
                            f'b={popt[1]:.5f}\n'
                            f'c={popt[2]:.5f}\n'
                            f'd={popt[3]:.5f}\n'
                            f'm={popt[4]:.5f}\n'
                            f'R2={r_squared:.10f}'],
                            loc='lower right', prop={'size': 8})

        # 更新绘图
        self.canvs.draw()

        # 更新Label显示参数
        result_text = "\n".join([f'{popt[0]:.10f}', f'{popt[1]:.10f}', f'{popt[2]:.10f}', 
                                 f'{popt[3]:.10f}', f'{popt[4]:.10f}', f'{r_squared:.10f}'])
        self.result_value_label.config(text=result_text)

    def copy_result_to_clipboard(self):
        result_values = self.result_value_label.cget("text")
        self.clipboard_clear()
        self.clipboard_append(result_values)
        self.update()  # 更新剪贴板


if __name__ == "__main__":
    root = Application()
    root.mainloop()