from tkinter import Text, Button, Label, Radiobutton, StringVar, Tk, INSERT
from tkinter import filedialog as fd

from backend import *


def get_result():
    global filename
    upsign = var1.get()
    downsign = var2.get()
    upper_laplace_quantile = var3.get()
    normal_distribution1 = False
    normal_distribution2 = False

    fileData = get_file_data(filename)

    # Среднее значение по выборке
    avg_curr = avg_data(fileData)
    # print('Среднее значение по выборке: %s' % avg_curr)

    # Смещенное среднее квадратическое отклонение
    deviation_curr = mean_square_deviation(fileData, avg_curr, len(fileData))
    # print('Смещенное среднее квадратическое отклонение: %s' % deviation_curr)

    # Отношение квантиля d~
    quantile_curr = quantile(fileData, deviation_curr, avg_curr)
    # print('Отношение квантиля d~: %s' % quantile_curr)

    table1 = get_excel_table1('Table_B_1.xlsx')
    downsign_curr = interp(len(fileData), table1['n'].values, table1[downsign].values)
    upsign_curr = interp(len(fileData), table1['n'].values, table1[upsign].values)

    table2 = get_excel_table2('Table_B_2_n.xlsx')
    upper_laplace_quantile_curr = interp(len(fileData), table2['n'].values, table2[upper_laplace_quantile].values)
    m_exception = interp(len(fileData), table2['n'].values, table2['m'].values)

    exceed_curr = upper_laplace_quantile_curr * mean_square_deviation(fileData, avg_curr, len(fileData) - 1)
    for i in fileData:
        if i - avg_curr > exceed_curr:
            # print(i-avg_curr, ' k ', exceed_curr, ' m ', m_exception)
            m_exception -= 1

    # print("%s < %s <= %s" % (upsign_curr, quantile_curr, downsign_curr))
    if upsign_curr < quantile_curr <= downsign_curr:
        normal_distribution1 = True

    if m_exception >= 0:
        normal_distribution2 = True

    message = '''Среднее арифметическое значение: %f\nСреднее квадратическое отклонение: %f\nПринадлежит нормальному распределению: %s'''
    normal_distribution_message = 'НЕТ'

    if normal_distribution1 and normal_distribution2:
        normal_distribution_message = 'ДА'
    # if normal_distribution1 and normal_distribution2:
    #     lbl11.configure(text="ДА")
    # else:
    #     lbl11.configure(text="НЕТ")

    txt1.config(state='normal')
    txt1.delete("1.0", "end")
    txt1.insert(INSERT, message % (avg_curr, deviation_curr, normal_distribution_message))
    txt1.config(state='disabled')

    # lbl7.configure(text=str(avg_curr))
    # lbl9.configure(text=str(deviation_curr))


def read_file_2():
    global filename
    filename = fd.askopenfilename(filetypes=(("text files", "*.txt"),))

    txt.config(state='normal')
    txt.delete("1.0", "end")
    txt.insert('end', filename)
    txt.config(state='disabled')


if __name__ == '__main__':
    PERCENT1 = '1p'
    PERCENT2 = '2p'
    PERCENT5 = '5p'
    PERCENT95 = '95p'
    PERCENT99 = '99p'
    global filename

    window = Tk()
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    window.title("ГОСТ Р 8.736-2011")
    window.geometry('600x300')

    txt = Text(window, height=1, width=60)
    txt.grid(row=0, column=0, sticky='w')
    txt.config(state='disabled')
    btn1 = Button(window, text="Выбрать файл", command=read_file_2).grid(row=0, column=1, sticky='w', padx=10)

    lbl1 = Label(window, text="Выберите уровень значимости:").grid(column=0, row=2, columnspan=1, sticky='w')

    lbl2 = Label(window, text="Верхний уровень:").grid(column=0, row=3, sticky='w')
    var1 = StringVar()
    var1.set(PERCENT1)
    rb1 = Radiobutton(text="1%", variable=var1, value=PERCENT1).grid(columnspan=1, row=3)
    rb2 = Radiobutton(text="5%", variable=var1, value=PERCENT5).grid(columnspan=2, row=3)

    lbl3 = Label(window, text="Нижний уровень:").grid(column=0, row=4, sticky='w')
    var2 = StringVar()
    var2.set(PERCENT99)
    rb1 = Radiobutton(text="95%", variable=var2, value=PERCENT95).grid(columnspan=1, row=4)
    rb2 = Radiobutton(text="99%", variable=var2, value=PERCENT99).grid(columnspan=2, row=4)

    lbl4 = Label(window, text="Выберите верхний квантиль Лапласа:").grid(column=0, row=5, sticky='w')
    var3 = StringVar()
    var3.set(PERCENT1)
    rb1 = Radiobutton(text="1%", variable=var3, value=PERCENT1).grid(column=0, row=6, columnspan=2)
    rb2 = Radiobutton(text="2%", variable=var3, value=PERCENT2).grid(column=0, row=7, columnspan=2)
    rb3 = Radiobutton(text="5%", variable=var3, value=PERCENT5).grid(column=0, row=8, columnspan=2)

    btn3 = Button(window, text="Получить результаты", command=get_result).grid(column=0, row=9, columnspan=2)

    lbl5 = Label(window, text="Результаты измерений:").grid(column=0, row=10, columnspan=2, sticky='w')

    message = '''Среднее арифметическое значение:\nСреднее квадратическое отклонение:\nПринадлежит нормальному распределению:'''
    txt1 = Text(window, height=3, width=60)
    txt1.insert('end', message)
    txt1.grid(row=11, column=0, sticky='w')
    txt1.config(state='disabled')

    window.mainloop()
