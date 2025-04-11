from tkinter import *
from tkinter.messagebox import *

# класс Paint
class Paint(Frame):
    def draw(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                              event.y - self.brush_size,
                              event.x + self.brush_size,
                              event.y + self.brush_size,
                              fill=self.color, outline=self.color)
    def set_color(self, new_color):
        self.color = new_color

        # Изменение размера кисти

    def set_brush_size(self, new_size):
        self.brush_size = new_size
    def save_canvas(self):
        self.canv.postscript(file="tmp_canvas.eps")
        pass
    def setUI(self):
        # Устанавливаем название окна
        self.parent.title("Demo Paint")
        # Размещаем активные элементы на родительском окне
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(6, weight=1)
        self.rowconfigure(2, weight=1)

        # Создаем холст с белым фоном
        self.canv = Canvas(self, bg="white")

        # Приклепляем канвас методом grid. Он будет находится в 3м ряду, первой колонке,
        # и будет занимать 7 колонок, задаем отступы по X и Y в 5 пикселей, и
        # заставляем растягиваться при растягивании всего окна

        self.canv.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky=E + W + S + N)

        # задаем реакцию холста на нажатие левой кнопки мыши
        self.canv.bind("<B1-Motion>", self.draw)

        # создаем метку для кнопок изменения цвета кисти
        color_lab = Label(self, text="Цвет: ")

        # Устанавливаем созданную метку в первый ряд и первую колонку,
        # задаем горизонтальный отступ в 6 пикселей
        color_lab.grid(row=0, column=0, padx=6)

        # создание кнопки: установка текста кнопки, задание ширины кнопки (10 символов)
        black_btn = Button(self, text="черный", width=10, command=lambda: self.set_color("black"))

        # устанавливаем кнопку в первый ряд, вторая колонка
        black_btn.grid(row=0, column=1)

        # Создаем метку для кнопок изменения размера кисти
        size_lab = Label(self, text="Размер кисти: ")
        size_lab.grid(row=1, column=0, padx=5)
        one_btn = Button(self, text="2x", width=10, command=lambda: self.set_brush_size(2))
        one_btn.grid(row=1, column=1)

        clear_btn = Button(self, text="Очистить", width=10, command=lambda: self.canv.delete("all"))
        clear_btn.grid(row=0, column=3, sticky=W)
        save_btn = Button(self, text="Сохранить", width=10, command=lambda: self.save_canvas())
        save_btn.grid(row=0, column=4, sticky=W)
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.brush_size = 2
        self.brush_color = "black"
        self.color = "black"
        self.parent = parent
        self.setUI()
        self.canv.bind("<B1-Motion>", self.draw)


# выход из программы  
def close_win():
    if askyesno("Выход", "Вы уверены?"):
        root.destroy()

# вывод справки    
def about():
  showinfo("Demo Paint", "Простейшая рисовалка от сайта: https://it-black.ru")


# функция для создания главного окна
def main():
    global root
    root = Tk()
    root.geometry("800x600+300+300")
    app = Paint(root)
    m = Menu(root)
    root.config(menu=m)

    fm = Menu(m)
    m.add_cascade(label="Файл", menu=fm)
    fm.add_command(label="Выход", command=close_win)

    hm = Menu(m)
    m.add_cascade(label="Справка", menu=hm)
    hm.add_command(label="О программе", command=about)
    
    root.mainloop()
if __name__ == "__main__":
    main()