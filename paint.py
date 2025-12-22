from tkinter import *
from tkinter.messagebox import *
from PIL import Image
import cv2
import numpy as np


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
    def rec_digit(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        gray = 255-img
        # применяем пороговую обработку
        (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # удаляем нулевые строки и столбцы
        while np.sum(gray[0]) == 0:
            gray = gray[1:]
        while np.sum(gray[:,0]) == 0:
            gray = np.delete(gray,0,1)
        while np.sum(gray[-1]) == 0:
            gray = gray[:-1]
        while np.sum(gray[:,-1]) == 0:
            gray = np.delete(gray,-1,1)
        rows, сols = gray.shape

        # изменяем размер, чтобы помещалось в box 20x20 пикселей
        if rows > cols:
            factor = 20.0/rows
            rows = 20
            cols = int(round(cols*factor))
            gray = cv2.resize(gray, (cols,rows))
        else:
            factor = 20.0/cols
            cols = 20
            rows = int(round(rows*factor))
            gray = cv2.resize(gray, (cols, rows))

        cv2.imwrite('gray'+ img_path, gray)
        gray = cv2.resize(gray, (28, 28))
        img = gray / 255.0
        img = np.array(img).reshape(-1, 28, 28, 1)
        print("img", img)
        # out = str(np.argmax(model.predict(img)))
        return img
    # Изменение размера кисти
    def set_brush_size(self, new_size):
        self.brush_size = new_size
    def save_canvas(self):
        self.canv.postscript(file='tmp_canvas.ps', colormode='color')
        # self.rec_digit('tmp_canvas.ps')
        img = Image.open('tmp_canvas.ps')
        img.save('./canvas.png')
        # pixel_array = np.array(image)
        # print("pixel_array", pixel_array)
        pass
    def image_to_number(self):

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
        clear_btn.grid(row=0, column=2, sticky=W)
        clear_btn = Button(self, text="Вычислить", width=10, command=lambda: self.image_to_number())
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

# функция для создания главного окна
def main():
    global root
    root = Tk()
    root.geometry("800x600+300+300")
    app = Paint(root)
    m = Menu(root)
    root.config(menu=m)
    root.mainloop()

if __name__ == "__main__":
    main()