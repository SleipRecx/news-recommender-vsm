import os
from surprise import KNNBasic
from surprise import Dataset
from surprise import Reader

input_fname = '../data/dataset1.txt'
rootPath = os.path.abspath('.')
input_file = rootPath + os.sep + input_fname

reader = Reader(line_format='user item rating', sep='\t')
data = Dataset.load_from_file('dataset1.txt', reader=reader)

sim_options = {'name': 'cosine',
               'user_based': True}

algo = KNNBasic(sim_options=sim_options)