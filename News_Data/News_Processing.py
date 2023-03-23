import pandas as pd
import datetime

with open("news.txt") as f:
    information = f.read()
list_news=information.split('\n')
print(list_news)