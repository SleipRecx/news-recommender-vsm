import kf as kf
from surprise import Dataset
from surprise import Reader
from surprise import SVD

reader = Reader(line_format='user item rating', sep='  ')
data = Dataset.load_from_file('dataset_file', reader=reader)

algo = SVD()

for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)