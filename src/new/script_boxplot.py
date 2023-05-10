import statistics
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression
import numpy as np
import scipy.stats as stats
import matplotlib.dates as mdates
from datetime import datetime


def boxPlotGenerator(values, label):
    fig, ax = plt.subplots()

    ax.boxplot(values)
    ax.set_title(label)
    ax.set_xlabel('All repos')
    ax.set_ylabel(label)

    plt.show()


def ageBoxPlotGenerator(ages):
    datascriacao = [datetime.strptime(
        valor, '%Y-%m-%dT%H:%M:%SZ') for valor in ages]

    valores_convertidos = [
        round((datetime.utcnow() - valor).days / 365.25, 2) for valor in datascriacao]

    # Criação da figura e eixos
    fig, ax = plt.subplots()

    # Criação do boxplot com os valores de data/hora convertidos
    ax.boxplot([valores_convertidos])

    # Configuração dos rótulos e títulos dos eixos
    ax.set_title('Idade dos repositórios')
    ax.set_xlabel('All repos')
    ax.set_ylabel('Idade em anos')

    # Exibição do boxplot
    plt.show()


def main():
    df = pd.read_csv('num_builds_temp.csv')

    num_builds = df["num_total_builds"]
    label_builds = "Número total de builds"

    df2 = pd.read_csv('repos_new_list.csv')

    starCount = df2["stars"]
    label_stars = "Número total de estrelas"

    ages = df2["createdAt"]

    print("builds")
    boxPlotGenerator(num_builds, label_builds)
    print("stars")
    boxPlotGenerator(starCount, label_stars)
    print("idade")
    ageBoxPlotGenerator(ages)


main()
