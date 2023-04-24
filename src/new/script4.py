import csv
from datetime import datetime
import pandas as pd
import requests
import json
from datetime import timedelta
import re

# imprimindo a soma dos tempos em formato de horas e minutos
# horas, minutos = divmod(soma_tempos.seconds // 60, 60)
# print(f"Tempo total: {horas}h{minutos:02d}m")


def calculate_metrics(csv2, csv3):
    with open(csv3, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            num_build_failure = int(row[2])
            num_fixed_instantly = int(row[3])
            num_not_fixed_instantly = int(row[4])

            m5 = (num_fixed_instantly/num_build_failure)*100
            m6 = (num_not_fixed_instantly/num_build_failure)*100
            print("M5: ", m5, "%")
            print("M6: ", m6, "%")

    with open(csv2, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        soma = timedelta()
        count = 0
        for row in reader:
            intervalo = row[5]

            horas, minutos = map(int, re.findall(r'\d+', intervalo))
            delta_tempo = timedelta(hours=horas, minutes=minutos)
            soma += delta_tempo
            count = count + 1

        m8 = soma/count
        print("M8: ", m8, "horas")

    return


def main():
    calculate_metrics('csv2_intervalos.csv', 'csv3_build_efficiency.csv')


main()
