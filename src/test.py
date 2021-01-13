import pandas as pd
from parser import parse

parse(pd.read_json('thread.json'))
# print(parse(pd.read_json('thread.json')))
