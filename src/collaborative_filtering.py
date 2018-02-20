from surprise import KNNBasic
from surprise import Dataset
from surprise import Reader

reader = Reader(line_format='user item rating', sep='  ')
data = Dataset.load_from_file('data/dataset1.txt', reader=reader)

sim_options = {'name': 'cosine',
               'user_based': True}

algo = KNNBasic(sim_options=sim_options)