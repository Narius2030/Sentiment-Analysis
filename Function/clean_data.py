import pandas as pd
import string
import re
from pyvi import ViTokenizer

class TransformText():
    def __init__(self, path:str, stopword=None) -> None:
        self.data = pd.read_csv(path)
        self.stopwords_path = stopword
    
    def remove_punctuation(self, comment:str) -> str:
        # Create a translation table
        translator = str.maketrans('', '', string.punctuation)
        # Remove punctuation
        new_string = comment.translate(translator)
        # Remove redudant space and break sign
        new_string = re.sub('[\n ]+', ' ', new_string)
        # Remove emoji icon
        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002500-\U00002BEF"  # chinese char
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u"\U00010000-\U0010ffff"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u200d"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\ufe0f"  # dingbats
                u"\u3030"
                                "]+", flags=re.UNICODE)
        new_string = re.sub(emoji_pattern, '', new_string)
        return new_string
    
    def stopwords_vi(self, path) -> list:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            words = [line.split('\n')[0] for line in lines]
        return words
    
    def remove_stopword(self, comment:str) -> str:
        if self.stopwords_path is not None:
            stop_words = self.stopwords_vi(self.stopwords_path)
            filtered = [word for word in comment.split() if word not in stop_words]
            result = ' '.join(filtered)
        else:
            result = comment
        return result
    
    def assign_label(self, row) -> str:
        if row['positive_count'] > row['neutral_count'] and row['positive_count'] > row['negative_count']:
            return 'Positive'
        elif row['negative_count'] > row['neutral_count'] and row['negative_count'] > row['positive_count']:
            return 'Negative'
        elif row['negative_count'] == row['neutral_count'] :
            return 'Negative'
        elif row['neutral_count'] == row ['positive_count']:
            return "Positive"
        else :
            return "Neutral"
        
    def replace_invalid_dates(self, temp):
        try:
            temp['date_time'] = pd.to_datetime(temp['date_time'], errors='coerce')
        except Exception as ex:
            pass

        temp['date_time'].fillna(value=temp['date_time'].mode()[0], inplace=True)
        return temp
        
    def fit_transform(self):
        self.data['comment'] = self.data['comment'].apply(lambda x: x.lower())
        self.data['comment'] = self.data['comment'].apply(self.remove_punctuation)
        self.data['comment'] = self.data['comment'].apply(self.remove_stopword)
        self.data['comment'] = self.data['comment'].apply(lambda x: ViTokenizer.tokenize(x))
        
        self.data['positive_count'] = self.data['label'].apply(lambda x: x.count("Positive"))
        self.data['neutral_count'] = self.data['label'].apply(lambda x: x.count("Neutral"))
        self.data['negative_count'] = self.data['label'].apply(lambda x: x.count("Negative"))
        
        self.data['label'] = self.data.apply(self.assign_label, axis=1)
        self.data = self.replace_invalid_dates(self.data)
        return self.data
        
    def dump(self, path:str):
        self.data.to_csv(path)