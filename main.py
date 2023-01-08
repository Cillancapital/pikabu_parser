import tkinter as tk
from tkinter.ttk import Combobox
from infinite_scroll_parsing import inf_scr_prs
from data_manage import save_results


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #configure the root window
        self.geometry('350x600')
        self.minsize(350, 600)
        self.title('Welcome to Pikabu parser')

        #configure content
        self.lbl1 = tk.Label(self, text="Chose your destiny", font=('Arial', 18))
        self.lbl1.place(anchor='center', relx=0.5, rely=0.1)

        self.combo1 = Combobox(self)
        self.combo1.place(anchor='center', relx=0.5, rely=0.18)
        self.combo1['values'] = ('Parse from hot', 'Parse from best')
        self.combo1.current(0)

        self.combo2 = Combobox(self)
        self.combo2.place(anchor='center', relx=0.5, rely=0.22)
        self.combo2['values'] = tuple([f'Parse {i} pages' for i in range(1,100)])
        self.combo2.current(0)

        self.btn1 = tk.Button(self, text ="Let's parse!", command=self.btn1_clicked)
        self.btn1.place(anchor='center', relx=0.5, rely=0.3)

        #Todo add a funny image

    def btn1_clicked(self):
        self.lbl2 = tk.Label(self, font=('Arial', 18))
        self.lbl2.place(anchor='center', relx=0.5, rely=0.6)
        #start parsing
        parse_from = f"https://pikabu.ru/{self.combo1.get().split(' ')[2]}"
        page_num = int(self.combo2.get().split(' ')[1])

        result = inf_scr_prs(parse_from, page_num)

        #show result
        if result[0] == -1:
            self.lbl2.configure(text=f'Oops!\n{result[1]}')
        else:
            self.lbl2.configure(text=f'Done!\n We have parsed {result[1]} posts')
            save_results(result[0], 'txt')



if __name__ == '__main__':
    app = App()
    app.mainloop()


