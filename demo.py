from function.clean_data import TransformText

tft = TransformText("./data/mobile_feedback/Train.csv", stopword="./data/vietnamese-stopwords.txt")
data = tft.fit_transform()
print(data)