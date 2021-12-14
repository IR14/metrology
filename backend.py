from math import sqrt, fabs

import pandas as pd


def get_file_data(filename):
    result = []

    with open(filename, 'r') as openReadFile:
        for line in openReadFile:
            result = line.split()

            for i, j in enumerate(result):
                result[i] = float(result[i].replace(',', '.'))

            print(result)

            return result


def get_excel_table1(filename):
    return pd.read_excel(filename, names=['n', '1p', '5p', '99p', '95p'], skiprows=1)


def get_excel_table2(filename):
    return pd.read_excel(filename, names=['n', 'm', '1p', '2p', '5p'], skiprows=1)


def avg_data(mas):
    s = 0
    for i in range(0, len(mas)):
        s += mas[i];
    avg = s / len(mas)

    print(avg)

    return avg


def deviation_offset(mas, avg):
    n = len(mas)

    temp = 0
    for i in mas:
        temp += (i - avg) ** 2

    return sqrt(temp / n)


def quantile(mas, deviation, avg):
    n = len(mas)

    temp = 0
    for i in mas:
        temp += fabs(i - avg)

    return temp / n / deviation


if __name__ == '__main__':
    # FILENAME = input()
    FILENAME = 'G_v22_a.txt'

    fileData = get_file_data(FILENAME)

    # Среднее значение по выборке
    avg_curr = avg_data(fileData)
    print('Среднее значение по выборке: %s' % avg_curr)

    # Смещенное среднее квадратическое отклонение
    deviation_curr = deviation_offset(fileData, avg_curr)
    print('Смещенное среднее квадратическое отклонение: %s' % deviation_curr)

    # Отношение квантиля d~
    quantile_curr = quantile(fileData, deviation_curr, avg_curr)
    print('Отношение квантиля d~: %s' % quantile_curr)

    k = get_excel_table2('Table_B_2.xlsx')
    print(k)

    k2 = get_excel_table1('Table_B_1.xlsx')
    print(k2)
