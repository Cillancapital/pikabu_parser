import tkinter as tk
from tkinter.ttk import Combobox
from infinite_scroll_parsing import inf_scr_prs
from data_manage import save_results, load_results_txt


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.geometry('350x600')
        self.minsize(350, 600)
        self.title('Welcome to Pikabu parser')

        # configure content
        self.lbl1 = tk.Label(self, text="Chose your destiny", font=('Arial', 18))
        self.lbl1.place(anchor='center', relx=0.5, rely=0.1)

        self.combo1 = Combobox(self)
        self.combo1.place(anchor='center', relx=0.5, rely=0.18)
        self.combo1['values'] = ('Parse from hot',
                                 'Parse from best',
                                 'Parse from new')
        self.combo1.current(0)

        self.combo2 = Combobox(self)
        self.combo2.place(anchor='center', relx=0.5, rely=0.22)
        self.combo2['values'] = tuple([f'Parse {i} pages' for i in range(1, 100)])
        self.combo2.current(0)

        self.btn1 = tk.Button(self, text="Let's parse!", command=self.btn1_clicked)
        self.btn1.place(anchor='center', relx=0.5, rely=0.3)

        self.btn_work_with_data = tk.Button(self, text="Work with the data", command=self.btn_work_with_data_clicked)
        self.btn_work_with_data.place(anchor='n', relx=0.5, rely=0)
        self.btn_work_with_data.configure(height=1, width=350)

        # Todo add a funny image

    def btn1_clicked(self):
        self.lbl2 = tk.Label(self, font=('Arial', 18))
        self.lbl2.place(anchor='center', relx=0.5, rely=0.6)
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

        # create a btn to work with the data
        '''self.btn_settings = tk.Button(self, text="Settings", command=self.btn_settings_clicked)
        self.btn_settings.place(anchor='n', relx=0.5, rely=0)
        self.btn_settings.configure(height=1, width=350)'''
    @staticmethod
    def btn_work_with_data_clicked():
        # todo окно с вариантами обработки спарсеной инфы
        # найти N постов с наивысшим рейтингом / скачать картинки
        work_with_data_window = WorkWithDataWindow()
        work_with_data_window.mainloop()


class WorkWithDataWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.geometry('300x300')
        self.minsize(300, 300)
        self.title("Let's analyze the data!")

        # configure content
        self.btn1 = tk.Button(self, text="Print me the usernames", command=self.btn1_clicked)
        self.btn1.place(anchor='center', relx=0.5, rely=0.3)

    @staticmethod
    def btn1_clicked():
        data = load_results_txt()
        if data == -1:
            print("There is a problem with txt file")
        elif not data:
            print("There is no data")
        else:
            print(data)
        # todo we have red the file, ready to analyze


if __name__ == '__main__':
    app = App()
    app.mainloop()
