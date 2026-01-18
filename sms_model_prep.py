import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

class sms_predictor:
    def __init__(self, classifier, cv) -> None:
        self.classifier = classifier
        self.cv = cv
    
    def predict_spam(self, sample_message):
        sample_message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=sample_message)
        sample_message = sample_message.lower()
        sample_message_words = sample_message.split()
        sample_message_words = [word for word in sample_message_words if not word in set(stopwords.words('english'))]
        ps = PorterStemmer()
        final_message = [ps.stem(word) for word in sample_message_words]
        final_message = ' '.join(final_message)
        temp = self.cv.transform([final_message]).toarray()
        return self.classifier.predict(temp)
