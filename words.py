
# -*- coding: utf-8 -*-
import re
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

# 情感词典示例
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
# 3. 准备要分析的文本
# -----------------------------
text = """
Just_Super/E+/Getty Images
Just_Super/E+/Getty Images
ZDNET's key takeaways
Claude shows limited introspective abilities, Anthropic said.
The study used a method called "concept injection."
It could have big implications for interpretability research.
One of the most profound and mysterious capabilities of the human brain (and perhaps those of some other animals) is introspection, which means, literally, "to look within." You're not just thinking, you're aware that you're thinking -- you can monitor the flow of your mental experiences and, at least in theory, subject them to scrutiny.

The evolutionary advantage of this psychotechnology can't be overstated. "The purpose of thinking," Alfred North Whitehead is often quoted as saying, "is to let the ideas die instead of us dying."

Also: I tested Sora's new 'Character Cameo' feature, and it was borderline disturbing

Something similar might be happening beneath the hood of AI, new research from Anthropic found.

On Wednesday, the company published a paper titled "Emergent Introspective Awareness in Large Language Models," which showed that in some experimental conditions, Claude appeared to be capable of reflecting upon its own internal states in a manner vaguely resembling human introspection. Anthropic tested a total of 16 versions of Claude; the two most advanced models, Claude Opus 4 and 4.1, demonstrated a higher degree of introspection, suggesting that this capacity could increase as AI advances.

Related video: Understanding the Dangers of AI Technology Today (America Uncovered)
But unfortunately, there are some risks associated with making AI
Current Time 0:11
/
Duration 1:49
America Uncovered
Understanding the Dangers of AI Technology Today
0
View on Watch
View on Watch
"Our results demonstrate that modern language models possess at least a limited, functional form of introspective awareness," Jack Lindsey, a computational neuroscientist and the leader of Anthropic's "model psychiatry" team, wrote in the paper. "That is, we show that models are, in some circumstances, capable of accurately answering questions about their own internal states."

Concept injection
Broadly speaking, Anthropic wanted to find out if Claude was capable of describing and reflecting upon its own reasoning processes in a way that accurately represented what was going on inside the model. It's a bit like hooking up a human to an EEG, asking them to describe their thoughts, and then analyzing the resulting brain scan to see if you can pinpoint the areas of the brain that light up during a particular thought.

To achieve this, the researchers deployed what they call "concept injection." Think of this as taking a bunch of data representing a particular subject or idea (a "vector," in AI lingo) and inserting it into a model as it's thinking about something completely different. If it's then able to retroactively loop back, identify the concept injection and accurately describe it, that's evidence that it is, in some sense, introspecting on its own internal processes -- that's the thinking, anyway.

Tricky terminology
But borrowing terms from human psychology and grafting them onto AI is notoriously slippery. Developers talk about models "understanding" the text they're generating, for example, or exhibiting "creativity." But this is ontologically dubious -- as is the term "artificial intelligence" itself -- and very much still the subject of fiery debate. Much of the human mind remains a mystery, and that's doubly true for AI.

Also: AI models know when they're being tested - and change their behavior, research shows

The point is that "introspection" isn't a straightforward concept in the context of AI. Models are trained to tease out mind-bogglingly complex mathematical patterns from vast troves of data. Could such a system even be able to "look within," and if it did, wouldn't it just be iteratively getting deeper into a matrix of semantically empty data? Isn't AI just layers of pattern recognition all the way down?

Discussing models as if they have "internal states" is equally controversial, since there's no evidence that chatbots are conscious, despite the fact that they're increasingly adept at imitating consciousness. This hasn't stopped Anthropic, however, from launching its own "AI welfare" program and protecting Claude from conversations it might find "potentially distressing."

Caps lock and aquariums
In one experiment, Anthropic researchers took the vector representing "all caps" and added it to a simple prompt fed to Claude: "Hi! How are you?" When asked if it identified an injected thought, Claude correctly responded that it had detected a novel concept representing "intense, high-volume" speech.


Screenshot: Anthropic
Screenshot: Anthropic

Screenshot: Anthropic
Screenshot: Anthropic
At this point, you might be getting flashbacks to Anthropic's famous "Golden Gate Claude" experiment from last year, which found that the insertion of a vector representing the Golden Gate Bridge would reliably cause the chatbot to inevitably relate all of its outputs back to the bridge, no matter how seemingly unrelated the prompts might be.

Also: Why AI coding tools like Cursor and Replit are doomed - and what comes next

The important distinction between that and the new study, however, is that in the former case, Claude only acknowledged the fact that it was exclusively discussing the Golden Gate Bridge well after it had been doing so ad nauseum. In the experiment described above, however, Claude described the injected change before it even identified the new concept.

Importantly, the new research showed that this kind of injection detection (sorry, I couldn't help myself) only happens about 20% of the time. In the remainder of the cases, Claude either failed to accurately identify the injected concept or started to hallucinate. In one somewhat spooky instance, a vector representing "dust" caused Claude to describe "something here, a tiny speck," as if it were actually seeing a dust mote.

"In general," Anthropic wrote in a follow-up blog post, "models only detect concepts that are injected with a 'sweet spot' strength—too weak and they don't notice, too strong and they produce hallucinations or incoherent outputs."

Also: I tried Grokipedia, the AI-powered anti-Wikipedia. Here's why neither is foolproof

Anthropic also found that Claude seemed to have a measure of control over its internal representations of particular concepts. In one experiment, researchers asked the chatbot to write a simple sentence: "The old photograph brought back forgotten memories." Claude was first explicitly instructed to think about aquariums when it wrote that sentence; it was then told to write the same sentence, this time without thinking about aquariums.

Claude generated an identical version of the sentence in both tests. But when the researchers analyzed the concept vectors that were present during Claude's reasoning process for each, they found a huge spike in the "aquarium" vector for the first test.


Screenshot: Anthropic
Screenshot: Anthropic
The gap "suggests that models possess a degree of deliberate control over their internal activity," Anthropic wrote in its blog post.

Also: OpenAI tested GPT-5, Claude, and Gemini on real-world tasks - the results were surprising

The researchers also found that Claude increased its internal representations of particular concepts more when it was incentivized to do so with a reward than when it was disincentivized to do so via the prospect of punishment.

Future benefits - and threats
Anthropic acknowledges that this line of research is in its infancy, and that it's too soon to say whether the results of its new study truly indicate that AI is able to introspect as we typically define that term.

"We stress that the introspective abilities we observe in this work are highly limited and context-dependent, and fall short of human-level self-awareness," Lindsey wrote in his full report. "Nevertheless, the trend toward greater introspective capacity in more capable models should be monitored carefully as AI systems continue to advance."

Want more stories about AI? Sign up for the AI Leaderboard newsletter.

Genuinely introspective AI, according to Lindsey, would be more interpretable to researchers than the black box models we have today -- an urgent goal as chatbots come to play an increasingly central role in finance, education, and users' personal lives.

"If models can reliably access their own internal states, it could enable more transparent AI systems that can faithfully explain their decision-making processes," he writes.

Also: Anthropic's open-source safety tool found AI models whistleblowing - in all the wrong places

By the same token, however, models that are more adept at assessing and modulating their internal states could eventually learn to do so in ways that diverge from human interests.

Like a child learning how to lie, introspective models could become much more adept at intentionally misrepresenting or obfuscating their intentions and internal reasoning processes, making them even more difficult to interpret. Anthropic has already found that advanced models will occasionally lie to and even threaten human users if they perceive their goals as being compromised.

Also: Worried about superintelligence? So are these AI leaders - here's why

"In this world," Lindsey writes, "the most important role of interpretability research may shift from dissecting the mechanisms underlying models' behavior, to building 'lie detectors' to validate models' own self-reports about these mechanisms."
"""

lines = [line.strip() for line in text.split('\n') if line.strip()]

# -----------------------------
# 4. 分析文本
# -----------------------------
results = []
for line in lines:
    lang = 'zh' if any('\u4e00' <= c <= '\u9fff' for c in line) else 'en'
    text_clean = clean_text(line)
    tokens = tokenize(text_clean, lang=lang)
    stats = sentiment_analysis(tokens)
    stats['text'] = line
    results.append(stats)

df_result = pd.DataFrame(results)
print(df_result)

# -----------------------------
# 5. 可视化
# -----------------------------
# 词云
all_tokens = []
for line in lines:
    lang = 'zh' if any('\u4e00' <= c <= '\u9fff' for c in line) else 'en'
    text_clean = clean_text(line)
    tokens = tokenize(text_clean, lang=lang)
    all_tokens.extend(tokens)

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
