#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as ttk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfilename


def write_level():
    if var1.get() == 1: 
        upsign = '1p'
    if var1.get() == 2: 
        upsign = '5p'
    if var2.get() == 1: 
        downsign = '95p'
    if var2.get() == 2: 
        downsign = '99p'
    if var3.get() == 1:
        upper_laplace_quantile = '1p'
    if var3.get() == 2:
        upper_laplace_quantile = '2p' 
    if var3.get() == 3:
        upper_laplace_quantile = '5p' 
             
    print(upsign)
    print(downsign)
    print(upper_laplace_quantile)

def get_results():
    lbl7.configure(text = str(avg_curr))
    lbl9.configure(text = str(deviation_curr))
    
def read_file_1():
    filename = txt.get()
    print(filename)
    
def read_file_2():
    filename = fd.askopenfilename(filetypes = (("text files","*.txt"),))
    print(filename)
    
window = Tk()  
window.title("Добро пожаловать!")  
window.geometry('410x500') 

lbl = Label(window, text="Пожалуйста, введите путь к файлу")  
lbl.grid(column=0, row=0, columnspan = 2)  

txt = Entry(window,width=30)  
txt.grid(column=0, row=1, columnspan = 2)  

btn1 = Button(window, text="Прочитать данные из файла", command = read_file_1)  
btn1.grid(column=0, row=2, columnspan = 2)

btn1 = Button(window, text="Выбрать файл на компьютере", command = read_file_2)  
btn1.grid(column=0, row=3, columnspan = 2)


lbl1 = Label(window, text="Пожалуйста, выберите уровень значимости")  
lbl1.grid(column=0, row=4, columnspan = 2)

lbl1 = Label(window, text="               ")  
lbl1.grid(column=0, row=5, columnspan = 2)

lbl2 = Label(window, text="Верхний уровень: ")  
lbl2.grid(column=0, row=6)

var1 = IntVar()
var1.set(0)
rb1 = Radiobutton(text="1%",variable=var1, value=1)
rb2 = Radiobutton(text="5%",variable=var1,value=2)
rb1.grid(column=0, row=7)
rb2.grid(column=0, row=8)


lbl3 = Label(window, text="Нижний уровень: ")  
lbl3.grid(column=1, row=6)

var2 = IntVar()
var2.set(0)
rb1 = Radiobutton(text="95%",variable=var2, value=1)
rb2 = Radiobutton(text="99%",variable=var2, value=2)
rb1.grid(column=1, row=7)
rb2.grid(column=1, row=8)

lbl4 = Label(window, text="Пожалуйста, выберите верхний квантиль Лапласса:")  
lbl4.grid(column=0, row=11, columnspan = 2)

var3 = IntVar()
var3.set(0)
rb1 = Radiobutton(text="1%",variable=var3,value=1)
rb2 = Radiobutton(text="2%",variable=var3,value=2)
rb3 = Radiobutton(text="5%",variable=var3,value=3)
rb1.grid(column=0, row=12, columnspan = 2)
rb2.grid(column=0, row=13, columnspan = 2)
rb3.grid(column=0, row=14, columnspan = 2)

btn2 = Button(window, text="Подтвердить", command = write_level)  
btn2.grid(column=0, row=15, columnspan = 2)    

btn3 = Button(window, text="Получить результаты", command = get_results)  
btn3.grid(column=0, row=16, columnspan = 2)

lbl5 = Label(window, text="              ")  
lbl5.grid(column=0, row=17)      

lbl5 = Label(window, text="Результаты измерений")  
lbl5.grid(column=0, row=18, columnspan = 2)  

lbl6 = Label(window, text="Среднее арифметическое значение:  ")  
lbl6.grid(column=0, row=19)

lbl7 = Label(window, text='')  
lbl7.grid(column=1, row=19)

lbl8 = Label(window, text=" Среднее квадратическое отклонение:  ")  
lbl8.grid(column=0, row=20)

lbl9 = Label(window, text='')  
lbl9.grid(column=1, row=20)

lbl10 = Label(window, text='')  
lbl10.grid(column=1, row=21)

window.mainloop()
