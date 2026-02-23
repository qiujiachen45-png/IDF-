# -*- coding: utf-8 -*-
import re
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import chardet

# -----------------------------
# 情感词典示例
# -----------------------------
positive_words = {"good", "happy", "support", "excellent", "love", "喜欢", "支持", "高兴"}
negative_words = {"bad", "sad", "against", "terrible", "hate", "讨厌", "反对", "伤心"}
negation_words = {"not", "never", "没有", "不"}
emphasis_words = {"very", "extremely", "非常", "极其"}

# -----------------------------
# 1. 文本预处理函数
# -----------------------------
def clean_text(text):
    """去除网址、特殊符号、标点"""
    text = re.sub(r"http\S+|www.\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip().lower()

def tokenize(text, lang='en'):
    if lang == 'zh':
        return list(jieba.cut(text))
    else:
        return text.split()

# -----------------------------
# 2. 情感/态度词统计函数
# -----------------------------
def sentiment_analysis(tokens):
    counts = Counter(tokens)
    pos_count = sum(counts[w] for w in positive_words if w in counts)
    neg_count = sum(counts[w] for w in negative_words if w in counts)
    negation_count = sum(counts[w] for w in negation_words if w in counts)
    emphasis_count = sum(counts[w] for w in emphasis_words if w in counts)
    total_words = len(tokens) if len(tokens) > 0 else 1
    sentiment_score = (pos_count - neg_count) / total_words
    return {
        'pos_count': pos_count,
        'neg_count': neg_count,
        'negation_count': negation_count,
        'emphasis_count': emphasis_count,
        'sentiment_score': sentiment_score
    }

# -----------------------------
# 3. 自动检测文件编码并读取 txt
# -----------------------------
txt_file = "ll.txt"

# 读取二进制，检测编码
with open(txt_file, "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print("Detected encoding:", encoding)

# 按检测到的编码读取文本
with open(txt_file, 'r', encoding=encoding) as f:
    lines = [line.strip() for line in f if line.strip()]

# -----------------------------
# 4. 分析文本
# -----------------------------
results = []
all_tokens = []

for line in lines:
    # 简单语言判断：含中文就用 zh，否则用 en
    lang = 'zh' if any('\u4e00' <= c <= '\u9fff' for c in line) else 'en'
    text_clean = clean_text(line)
    tokens = tokenize(text_clean, lang=lang)
    stats = sentiment_analysis(tokens)
    stats['text'] = line
    results.append(stats)
    all_tokens.extend(tokens)

# -----------------------------
# 5. 统计分析
# -----------------------------
df_result = pd.DataFrame(results)
print(df_result.describe())
print(df_result[['text','sentiment_score']])

# -----------------------------
# 6. 可视化
# -----------------------------
# 词云
wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='simhei.ttf').generate(" ".join(all_tokens))
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 情感折线图
plt.figure(figsize=(10,4))
plt.plot(df_result['sentiment_score'], marker='o')
plt.title('Sentiment Score Trend')
plt.xlabel('Text Index')
plt.ylabel('Sentiment Score')
plt.show()

