from tkinter import *
from tkinter.messagebox import *
from PIL import Image
import shutil
import math
import cv2
import numpy as np
from network import NeuralNetwork, load_network, max_index
from scipy.ndimage.measurements import center_of_mass

def revers(arr):
    for item in range(len(arr)):
        if arr[item] > 0:
            arr[item] = 0.0
        else:
            arr[item] = 1.0
    return arr
def getBestShift(img):
    cy,cx = center_of_mass(img)
    
    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty

def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted
def rec_digit(img_path):
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
    rows,cols = gray.shape
    
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

    # расширяем до размера 28x28
    colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
    rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
    gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')

    # сдвигаем центр масс
    shiftx,shifty = getBestShift(gray)
    shifted = shift(gray,shiftx,shifty)
    gray = shifted
    
    cv2.imwrite('gray'+ img_path, gray)
    img = gray / 255.0
    img = np.array(img).reshape(-1,28, 28, 1)
    X = img.reshape(28 * 28)
    return X
# класс Paint
class Paint(Frame):
    def draw(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                              event.y - self.brush_size,
                              event.x + self.brush_size,
                              event.y + self.brush_size,
                              fill=self.color, outline=self.color)
    def neiron_check(self):
        self.canv.postscript(file="my_dram.eps", colormode="mono")
        eps_image = Image.open("./my_dram.eps")
        eps_image.save("./temp.png", "png")
        X = rec_digit("./temp.png")
        # Переводим изображение в числовой вариант
        output = self.network.feedforward(X)
        print("output", max_index(output))
        
    def save_canvas(self):
        self.canv.postscript(file="my_dram.eps", colormode="mono")
    def setUI(self):
        # Устанавливаем название окна
        self.parent.title("Demo Paint")
        # Размещаем активные элементы на родительском окне
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(10, weight=1)
        self.rowconfigure(3, weight=1)

        # Создаем холст с белым фоном
        # self.canv = Canvas(self, bg="white", width=28, height=28)
        self.canv = Canvas(bg="white", borderwidth=0, bd=0)
        self.canv.pack(anchor=CENTER, expand=1)
        # Приклепляем канвас методом grid. Он будет находится в 3м ряду, первой колонке,
        # и будет занимать 7 колонок, задаем отступы по X и Y в 5 пикселей, и
        # заставляем растягиваться при растягивании всего окна
        # self.canv.grid(row=2, column=1, padx=7, pady=7, sticky=E + W + S + N)

        # задаем реакцию холста на нажатие левой кнопки мыши
        self.canv.bind("<B1-Motion>", self.draw)

        # создаем метку для кнопок изменения цвета кисти
        color_lab = Label(self, text="Действия: ")

        # Устанавливаем созданную метку в первый ряд и первую колонку,
        # задаем горизонтальный отступ в 6 пикселей
        color_lab.grid(row=0, column=0, padx=6)


        clear_btn = Button(self, text="Очистить", width=7, command=lambda: self.canv.delete("all"))
        clear_btn.grid(row=0, column=1, columnspan=1, sticky=NS)
        save_btn = Button(self, text="Сохранить", width=7, command=lambda: self.save_canvas())
        save_btn.grid(row=0, column=2, columnspan=1, sticky=W)
        save_btn = Button(self, text="Вычислить ", width=7, command=lambda: self.neiron_check())
        save_btn.grid(row=0, column=3, columnspan=1, sticky=W)
        
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.network = load_network("neuron.json")
        self.brush_size = 3
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
    root.geometry("450x300")
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