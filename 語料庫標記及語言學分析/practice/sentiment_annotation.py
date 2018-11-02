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


### >>>>>>>>>>> 試試也將新聞語料庫做情緒標記 <<<<<<<<<< ###
# --- 你會需要的套件
# import pandas as pd
# import json

# # --- 讀入新聞語料庫的檔案 (json file)
# with open('your json file') as json_data:
#     d = json.load(json_data)

# # --- 將讀入的json file 轉換為 df 格式
# news_data = pd.DataFrame.from_records(d)
# # news_data

# # --- 只截取斷詞好的新聞文本column
# news_content = pd.DataFrame(news_data['cln_content'])

# # --- 計算positive word 在每一個sample出現的count
# positive_word_score = []
# for text in list(news_content.cln_content):
#     result = 0
#     for words in positive_words:
#         if words in text:
#             result += 1 
#     positive_word_score.append(result)
# # positive_word_score

# # --- 計算positive pattern 在每一個sample出現的count 
# positive_pattern = '還好.+(會|不會)?'
# positive_pattern_score = []
# for text in list(news_content.cln_content):
#     positive_pattern_score.append(len(re.findall(positive_pattern,text)))
# # positive_pattern_score

# # --- 將 positive word和positive pattern計算後的結果合併
# positive_score = [positive_word_score[i] + positive_pattern_score[i] for i in range(len(positive_word_score))]
# #positive_score

# # --- 計算negative word 在每一個sample出現的count 
# negative_word_score = []
# for text in list(news_content.cln_content):
#     result = 0
#     for words in negative_words:
#         if words in text:
#             result -= 1 
#     negative_word_score.append(result)
# # negative_word_score

# # --- 計算negative pattern 在每一個sample出現的count 
# negative_pattern = r'都.*了.*還.*|連.+都.+|結果.+都'
# negative_pattern_score = []
# for text in list(news_content.cln_content):
#     negative_pattern_score.append(len(re.findall(negative_pattern,text))*-1)
# # negative_pattern_score

# # --- 將 negative word和 negative pattern計算後的結果合併
# negative_score = [negative_word_score[i] + negative_pattern_score[i] for i in range(len(negative_word_score))]
# # negative_score

# news_content['polarity_score'] = [positive_score[i] + negative_score[i] for i in range(len(positive_score))]

# news_content.to_csv('news_annotation.csv', index=False, header=True)