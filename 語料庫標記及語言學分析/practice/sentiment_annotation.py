import csv
import pandas as pd

# --- 讀入要標記的檔案 --- #
sample_file = list(csv.reader(open('new_sample.txt', "r"), delimiter = '\t'))

# --- 命名header --- #
df = pd.DataFrame(sample_file, columns=["sample", "sample_segmented", "polarity"]) 
df = df.drop(['sample', 'polarity'], axis=1) #把參考用的column拿掉
# df

# --- 讀入情緒詞辭典 (NTUSD wordlist) --- #
positive_words = open("positive_words.txt","r").read().split("\n")
negative_words = open("negative_words.txt","r").read().split("\n")

# --- 計算文本中的正向詞彙 --- #
positive_score = []
for text in list(df.sample_segmented):
    result = 0
    for words in positive_words:
        if words in text:
            result += 1
    positive_score.append(result)
# positive_score

# --- 計算文本中的負向詞彙 --- #
negative_score = []
for text in list(df.sample_segmented):
    result = 0
    for words in negative_words:
        if words in text:
            result -= 1
    negative_score.append(result)
# negative_score
# df['positive_score'] = positive_score
# df['negative_score'] = negative_score

# --- 加總文本中正負向詞彙的數量，判斷文本情緒極度 --- #
df['polarity_score'] = [positive_score[i] + negative_score[i] for i in range(len(positive_score))]

# --- 以數值標記情緒極度 (正向：1 / 中性：0 / 負向：-1) --- #
df.loc[df.polarity_score > 0, 'sentiment'] = '1' 
df.loc[df.polarity_score < 0, 'sentiment'] = '-1' 
df.loc[df.polarity_score == 0, 'sentiment'] = '0' 
# df = df.drop(['polarity_score'], axis=1)

# --- 將標記後的檔案輸出為csv格式 --- #
df.to_csv('sentiment_annotation_sample.csv', index=False, header=True)



##### install pandas for python3.X 
# $sudo python3 -m pip install pandas