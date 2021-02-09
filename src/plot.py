import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

import numpy as np

import datetime
import database as db


years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')


def create_graph(period=1):
    sql = "SELECT * FROM prices ORDER BY date DESC"
    rows = db.exec(sql)

    dates = [datetime.datetime.strptime(
        row[db.PRICES_DATE], "%Y-%m-%d %H:%M:%S.%f") for row in rows]

    dates = []
    values = []
    for row in rows:
        row_date = datetime.datetime.strptime(
            row[db.PRICES_DATE], "%Y-%m-%d %H:%M:%S.%f")
        if datetime.datetime.now() - datetime.timedelta(days=period) <= row_date:
            dates += [row_date]
            values += [row[db.PRICES_VAL]]

    fig, ax = plt.subplots()

    ax.plot(dates, values)

    ymax = max(values)
    xpos = values.index(ymax)
    xmax = dates[xpos]

    ymin = min(values)
    xpos = values.index(ymin)
    xmin = dates[xpos]

    ax.annotate(f"max: {ymax}", xy=(xmax, ymax), xytext=(xmax, ymax + 0.1))
    ax.annotate(f"min: {ymin}", xy=(xmin, ymin), xytext=(xmin, ymin - 0.1))

    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()

    plt.plot()
    plt.savefig(f'graph_{period}.png')
