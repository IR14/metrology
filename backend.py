from math import sqrt, fabs

from pandas import read_excel
# import pandas as pd
from numpy import interp
# import numpy as np
#
# def normal_dist(x , mean , sd):
#     prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
#     return prob_density

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
    return read_excel(filename, names=['n', '1p', '5p', '99p', '95p'], skiprows=1)


def get_excel_table2(filename):
    return read_excel(filename, names=['n', 'm', '1p', '2p', '5p'], skiprows=1)


def get_excel_gibs(filename):
    return read_excel(filename, names=['n', '1p', '5p'], skiprows=1)


def get_excel_student(filename):
    return read_excel(filename, names=['n', '95p', '99p'], skiprows=1)


def avg_data(mas):
    s = 0
    for i in range(0, len(mas)):
        s += mas[i];
    avg = s / len(mas)

    return avg


def mean_square_deviation(mas, avg, n):
    """
    n-1 - common
    n - star option
    """

    temp = 0
    for i in mas:
        temp += (i - avg) ** 2

    return sqrt(temp / n)


def mean_square_deviation_avg(n, deviation):
    return deviation / sqrt(n)


def quantile(mas, deviation, avg):
    n = len(mas)

    temp = 0
    for i in mas:
        temp += fabs(i - avg)

    return temp / n / deviation


def gross_exclusion(mas, avg, deviation, gt):
    g1 = fabs(max(mas) - avg) / deviation
    g2 = abs(avg - min(mas)) / deviation

    while g1 > gt or g2 > gt:
        if g1 > gt:
            mas.remove(max(mas))

        if g2 > gt:
            mas.remove(min(mas))

        avg = avg_data(mas)
        deviation = mean_square_deviation(mas, avg, n=len(mas))

        g1 = fabs(max(mas) - avg) / deviation
        g2 = abs(avg - min(mas)) / deviation

    print(len(mas))
    return mas


def nonexclusive_system_error(mas_len, confidence_probability, mean_square_deviation_avg):
    n = int(input("Enter count of errors: "))
    errors = []
    k = None
    # q1, q2 = None, None

    for i in range(n):
        print("Enter error n.", i + 1)
        errors.append(float(input()))

    n = len(errors)
    errors_sum = sum(map(fabs, errors))

    if confidence_probability == 0.95:
        k = 1.1
    else:
        k = 1.4
        # if n > 4:
        #     k = 1.4
        # else:
        #     q1 = errors[0]
        #     q2 = errors[1]
        #
        #     for i in range(2, n):
        #         if errors[i]

    errors_with_confidence_probability = k * sqrt(sum(list(map(lambda x: x ** 2, errors))))

    mean_square_deviation_of_nonexclusive_system_error = errors_with_confidence_probability / sqrt(3) / k

    mean_square_deviation_sigma = sqrt(
        sum(list(map((lambda x: x ** 2, [mean_square_deviation_of_nonexclusive_system_error,
                                         mean_square_deviation_avg])))))

    student_ratio = get_excel_student('Table_D_1.xlsx')

    curr_student_ratio = interp(mas_len - 1,
                                student_ratio['n'].values,
                                student_ratio[confidence_probability].values)

    confidence_border = curr_student_ratio * mean_square_deviation_avg

    k_ratio = (confidence_border + errors_sum) / (
            mean_square_deviation_avg + mean_square_deviation_of_nonexclusive_system_error)

    delta = k_ratio * mean_square_deviation_sigma

    return delta


# if __name__ == '__main__':
#     # FILENAME = input()
#     FILENAME = 'G_v22_a.txt'
#     normal_distribution1 = False
#     normal_distribution2 = False
#
#     fileData = get_file_data(FILENAME)
#     # x = np.linspace(1, 50, 40)
#     # print(len(x))
#     # mean = np.mean(x)
#     # sd = np.std(x)
#     # pdf = normal_dist(x, mean, sd)
#     # print(pdf)
#     # fileData = pdf
#
#     # Среднее значение по выборке
#     avg_curr = avg_data(fileData)
#     print('Среднее значение по выборке: %s' % avg_curr)
#
#     # Смещенное среднее квадратическое отклонение
#     deviation_curr = mean_square_deviation(fileData, avg_curr, len(fileData))
#     print('Смещенное среднее квадратическое отклонение: %s' % deviation_curr)
#
#     tableA = get_excel_gibs('Table_A_1.xlsx')
#     # print(tableA.iloc[len(fileData)-3][1])
#     # interp(len(fileData), tableA['n'].values, tableA['1p'].values)
#     print(len(fileData))
#     # gross_exclusion(mas=fileData, avg=avg_curr, deviation=deviation_curr,
#     #                 gt=interp(len(fileData), tableA['n'].values, tableA['1p'].values))
#     # Отношение квантиля d~
#     quantile_curr = quantile(fileData, deviation_curr, avg_curr)
#     print('Отношение квантиля d~: %s' % quantile_curr)
#
#     downsign = '1p'
#     upsign = '99p'
#     upper_laplace_quantile = '2p'
#
#     table1 = get_excel_table1('Table_B_1.xlsx')
#     downsign_curr = interp(len(fileData), table1['n'].values, table1[downsign].values)
#     upsign_curr = interp(len(fileData), table1['n'].values, table1[upsign].values)
#
#     table2 = get_excel_table2('Table_B_2_n.xlsx')
#     upper_laplace_quantile_curr = interp(len(fileData), table2['n'].values, table2[upper_laplace_quantile].values)
#     m_exception = interp(len(fileData), table2['n'].values, table2['m'].values)
#
#     exceed_curr = upper_laplace_quantile_curr * mean_square_deviation(fileData, avg_curr, len(fileData) - 1)
#     for i in fileData:
#         if i - avg_curr > exceed_curr:
#             print(i-avg_curr, ' k ', exceed_curr, ' m ', m_exception)
#             m_exception -= 1
#
#     print("%s < %s <= %s" % (upsign_curr, quantile_curr, downsign_curr))
#     if upsign_curr < quantile_curr <= downsign_curr:
#         normal_distribution1 = True
#
#     if m_exception >= 0:
#         normal_distribution2 = True
#
#     if normal_distribution1 and normal_distribution2:
#         print("Текущая выборка ПРИНАДЛЕЖИТ нормальному распределению по составному критерию!")
#     else:
#         print("Текущая выборка НЕ ПРИНАДЛЕЖИТ нормальному распределению по составному критерию!")
#
#     # gross_exclusion(mas=fileData, avg=avg_curr, deviation=deviation_curr,
#     #                 gt=get_excel_gibs('Table_A_1.xlsx').iloc[len(fileData)-3][1])
