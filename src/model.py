from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import MatrixSimilarity


class VectorSpaceModel:
    def __init__(self):
        self.dictionary = None
        self.tfidf_similarity = None
        self.tfidf_model = None
        self.profile_index_map = None

    def build(self, profiles: list):
        self.dictionary = Dictionary(profiles)
        corpus = list(map(lambda doc: self.dictionary.doc2bow(doc), profiles))
        self.tfidf_model = TfidfModel(corpus)
        tfidf_corpus = list(map(lambda c: self.tfidf_model[c], corpus))
        self.tfidf_similarity = MatrixSimilarity(tfidf_corpus)

    def save(self, path: str):
        self.dictionary.save(path + '/dict.mod')
        self.tfidf_model.save(path + '/tfidf_model.mod')
        self.tfidf_similarity.save(path + '/tfidf_sim.mod')

    def load(self, path: str):
        self.dictionary = Dictionary.load(path + '/dict.mod')
        self.tfidf_model = TfidfModel.load(path + '/tfidf_model.mod')
        self.tfidf_similarity = MatrixSimilarity.load(path + '/tfidf_sim.mod')

    def query(self, query: list, threshold: float):
        query_corpus = self.dictionary.doc2bow(query)
        query_tfidf = self.tfidf_model[query_corpus]
        similarity = enumerate(self.tfidf_similarity[query_tfidf])
        query_result = sorted(similarity, key=lambda kv: -kv[1])
        result = []
        for res in query_result:
            if res[1] > threshold:
                result.append(res)
            else:
                break
        return result
