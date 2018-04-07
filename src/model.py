import pickle
from typing import Dict
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import MatrixSimilarity


def save_object(obj, path):
    with open(path + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_object(path):
    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)


class VectorSpaceModel:
    def __init__(self):
        self.dictionary = None
        self.tfidf_similarity = None
        self.tfidf_model = None
        self.profile_index_map = None

    def build(self, profiles: list, profile_index_map: Dict):
        self.dictionary = Dictionary(profiles)
        corpus = list(map(lambda doc: self.dictionary.doc2bow(doc), profiles))
        self.tfidf_model = TfidfModel(corpus)
        tfidf_corpus = list(map(lambda c: self.tfidf_model[c], corpus))
        self.tfidf_similarity = MatrixSimilarity(tfidf_corpus)
        self.profile_index_map = profile_index_map

    def save(self, path: str):
        self.dictionary.save(path + '/dict.mod')
        self.tfidf_model.save(path + '/tfidf_model.mod')
        self.tfidf_similarity.save(path + '/tfidf_sim.mod')
        save_object(self.profile_index_map, path + '/profile_index_map')

    def load(self, path: str):
        self.dictionary = Dictionary.load(path + '/dict.mod')
        self.tfidf_model = TfidfModel.load(path + '/tfidf_model.mod')
        self.tfidf_similarity = MatrixSimilarity.load(path + '/tfidf_sim.mod')
        self.profile_index_map = load_object(path + '/profile_index_map')

    def query(self, query: list, n_results: int):
        query_corpus = self.dictionary.doc2bow(query)
        query_tfidf = self.tfidf_model[query_corpus]
        similarity = enumerate(self.tfidf_similarity[query_tfidf])
        query_result = sorted(similarity, key=lambda kv: -kv[1])[:n_results]
        recommended_articles = list(map(lambda result: self.profile_index_map[result[0]], query_result))
        return recommended_articles
