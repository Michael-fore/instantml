#from repos.Megatron_LM.sentiment_discovery.model import sentiment_classifier
from repos.vaderSentiment.vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentences = ["Karen"]

analyzer = SentimentIntensityAnalyzer()
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence)
    print(vs)
    print("{:-<65} {}".format(sentence, str(vs)))

class TextModels:
    models = {
            'VaderSentiment': SentimentIntensityAnalyzer,
            }       

    def __init__(self, model='VaderSentiment'):
        self.model = self.models.get(model)
        

