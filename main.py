import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from infinite_scroll_parsing import inf_scr_prs
from data_manage import save_results, load_results_txt


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.geometry('350x500')
        self.minsize(350, 400)
        self.title('Welcome to Pikabu parser')

        # configure content
        self.lbl1 = tk.Label(self, text="Let's parse?", font=('Arial', 18))
        self.lbl1.place(anchor='center', relx=0.5, rely=0.1)
        self.lbl2 = tk.Label(self, font=('Arial', 18))
        self.lbl2.place(anchor='center', relx=0.5, rely=0.6)
        self.combo1 = Combobox(self)
        self.combo1.place(anchor='center', relx=0.5, rely=0.18)
        self.combo1['values'] = ('Parse from hot',
                                 'Parse from best',
                                 'Parse from new')
        self.combo1.current(0)
        self.combo2 = Combobox(self)
        self.combo2.place(anchor='center', relx=0.5, rely=0.22)
        self.combo2['values'] = tuple([f'Parse {i} pages' for i in range(1, 101)])
        self.combo2.current(1)
        self.btn_parse = tk.Button(self, text="Let's parse!", command=self.btn_parse_clicked)
        self.btn_parse.place(anchor='center', relx=0.5, rely=0.3)
        self.btn_work_with_data = tk.Button(self, text="Work with the data", command=self.btn_work_with_data_clicked)
        self.btn_work_with_data.place(anchor='n', relx=0.5, rely=0)
        self.btn_work_with_data.configure(height=1, width=350)
        # Todo add a funny image

    def on_closing(self):
        ''' Allows to save the parsed info after closing '''
        if messagebox.askyesno('Save the parsed info', 'Do you want to\nsave all info to .txt?'):
            self.destroy()
        else:
            open("parsed_pikabu.txt", "w").close()
            self.destroy()

    def btn_parse_clicked(self):
        # start parsing
        parse_from = f"https://pikabu.ru/{self.combo1.get().split(' ')[2]}"
        page_num = int(self.combo2.get().split(' ')[1])

        result = inf_scr_prs(parse_from, page_num)

        # show result
        if result[0] == -1:
            self.lbl2.configure(text=f'Oops!\n{result[1]}')
        else:
            self.lbl2.configure(text=f"Done!\nWe have parsed {result[1]} posts\n"
                                     f"from pikabu.ru/{self.combo1.get().split(' ')[2]}")
            save_results(result[0], 'txt')

    def btn_work_with_data_clicked(self):
        # todo окно с вариантами обработки спарсеной инфы
        # найти N постов с наивысшим рейтингом / скачать картинки
        self.lbl2.configure(text='')
        work_with_data_window = WorkWithDataWindow()
        work_with_data_window.mainloop()


class WorkWithDataWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.geometry('300x300')
        self.minsize(300, 300)
        self.title("Let's analyze the data!")

        # load and check the info, configure the window
        self.data = load_results_txt()
        if self.data == -1:
            self.lbl_data_error = tk.Label(self, text="There is a problem\nwith txt file", font=('Arial', 18))
            self.lbl_data_error.place(anchor='center', relx=0.5, rely=0.5)
        elif not self.data:
            self.lbl_no_data = tk.Label(self, text="There is no data", font=('Arial', 18))
            self.lbl_no_data.place(anchor='center', relx=0.5, rely=0.5)
        else:
            self.btn_print_names = tk.Button(self, text="Print the usernames", command=self.btn_print_names_clicked)
            self.btn_print_names.grid(column=1, row=1)
            self.btn_print_names.configure(width=20)
            self.btn_print_top_rating = tk.Button(self, text="Print top rating", command=self.btn_print_top_rating_clicked)
            self.btn_print_top_rating.grid(column=1, row=2)
            self.btn_print_top_rating.configure(width=20)
            self.btn_sort_txt_by_rating = tk.Button(self, text="Sort txt by rating", command=self.btn_sort_txt_by_rating_clicked)
            self.btn_sort_txt_by_rating.grid(column=1, row=3)
            self.btn_sort_txt_by_rating.configure(width=20)

            self.listbox_output = tk.Listbox(self)
            self.listbox_output.grid(column=1, row=4)
            self.listbox_output.configure(width=40)


    def btn_print_names_clicked(self):
        self.listbox_output.delete(0, self.listbox_output.size())
        for i in range(len(self.data)):
            self.listbox_output.insert(i, self.data[i][2])
        # todo we have red the file, ready to analyze

    def btn_print_top_rating_clicked(self):
        self.listbox_output.delete(0, self.listbox_output.size())
        top_rating = 0
        for i in range(len(self.data)):
            if top_rating < int(self.data[i][1]):
                top_rating = int(self.data[i][1])
        self.listbox_output.insert(0, str(top_rating))

    def btn_sort_txt_by_rating_clicked(self):
        self.data.sort(key=lambda x: x[1])
        self.listbox_output.delete(0, self.listbox_output.size())
        for i in range(len(self.data)):
            self.listbox_output.insert(i, self.data[i][1])






if __name__ == '__main__':
    app = App()
    app.protocol('WM_DELETE_WINDOW', app.on_closing)
    app.mainloop()
