import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# -------------------------------
# 1️⃣ 加载外部训练集（TSV）
# -------------------------------
def load_training_corpus(file_path='emotion_corpus_300.txt'):
    texts, labels = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '\t' not in line:
                continue
            sentence, label = line.split('\t')
            texts.append(sentence)
            labels.append(label)
    print(f"✅ Loaded {len(texts)} training samples from {file_path}")
    return texts, labels

# -------------------------------
# 2️⃣ 训练朴素贝叶斯分类器
# -------------------------------
def train_emotion_classifier(file_path='emotion_corpus_300.txt'):
    texts, labels = load_training_corpus(file_path)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    clf = MultinomialNB()
    clf.fit(X, labels)
    return vectorizer, clf

# -------------------------------
# 3️⃣ 节点拆句预测累加概率
# -------------------------------
def predict_node_emotions(node_text, vectorizer, clf):
    sentences = [s.strip() for s in node_text.split('.') if s.strip()]
    counts = {c: 0.0 for c in clf.classes_}
    for s in sentences:
        X = vectorizer.transform([s])
        probs = clf.predict_proba(X)[0]
        for i, c in enumerate(clf.classes_):
            counts[c] += probs[i]
    return counts

# -------------------------------
# 4️⃣ 分割文本成节点
# -------------------------------
def split_text_into_nodes(text, part_name):
    node_counts = {'Beginning':4, 'Development':4, 'Climax':3, 'Resolution':3}
    num_nodes = node_counts.get(part_name, 4)
    words = text.split()
    total_words = len(words)
    words_per_node = total_words // num_nodes
    nodes = []
    for i in range(num_nodes):
        start = i*words_per_node
        end = total_words if i==num_nodes-1 else (i+1)*words_per_node
        nodes.append(' '.join(words[start:end]))
    return nodes

# -------------------------------
# 5️⃣ 创建情绪分析
# -------------------------------
def create_detailed_emotion_analysis(text_files_dict, training_file='emotion_corpus_300.txt'):
    parts = ['Beginning', 'Development', 'Climax', 'Resolution']
    vectorizer, clf = train_emotion_classifier(training_file)

    all_emotion_data = []
    node_page_ranges = {
        'Beginning': ["2-3","4-5","6-7","8-9"],
        'Development': ["10-13","14-17","18-21","22-25"],
        'Climax': ["26-29","30-33","34-38"],
        'Resolution': ["39-42","43-46","47-48"]
    }

    for part in parts:
        file_path = text_files_dict.get(part)
        if not file_path or not os.path.exists(file_path):
            print(f"⚠️ Missing file for part: {part}")
            continue
        with open(file_path,'r',encoding='utf-8') as f:
            text = f.read()
        text_nodes = split_text_into_nodes(text, part)
        for idx, node_text in enumerate(text_nodes):
            word_count = len(node_text.split())
            counts = predict_node_emotions(node_text, vectorizer, clf)
            result = counts.copy()
            result.update({
                'part': part,
                'node': f"{part}_Node{idx+1}",
                'node_index': idx+1,
                'word_count': word_count,
                'page_range': node_page_ranges[part][idx]
            })
            all_emotion_data.append(result)
            print(f"{part} Node {idx+1} Pages {node_page_ranges[part][idx]}: "
                  f"Words={word_count}, Positive={counts.get('Positive',0):.2f}, "
                  f"Negative={counts.get('Negative',0):.2f}, Surprise={counts.get('Surprise',0):.2f}")

    df = pd.DataFrame(all_emotion_data)
    create_emotion_visualization(df)
    return df

# -------------------------------
# 6️⃣ 每章折线图
# -------------------------------
def create_emotion_visualization(df):
    emotion_groups = ['Positive','Negative','Surprise']
    colors = ['#2E8B57','#DC143C','#FFD700']
    parts = df['part'].unique()
    fig, axes = plt.subplots(2,2,figsize=(20,12))
    axes = axes.flatten()
    for i, part in enumerate(parts):
        part_data = df[df['part']==part]
        nodes = sorted(part_data['node_index'].unique())
        for j, emotion_group in enumerate(emotion_groups):
            values = [part_data[part_data['node_index']==n][emotion_group].values[0] for n in nodes]
            axes[i].plot(nodes, values, marker='o', linewidth=3, markersize=8, color=colors[j], label=emotion_group, alpha=0.8)
        x_labels = [part_data[part_data['node_index']==n]['page_range'].values[0] for n in nodes]
        axes[i].set_xticks(nodes)
        axes[i].set_xticklabels(x_labels, fontsize=11)
        axes[i].set_title(f'{part} Chapter', fontsize=14, fontweight='bold')
        axes[i].set_ylabel('Emotion Count (probability weighted)', fontsize=12)
        axes[i].grid(True, alpha=0.3, linestyle='--')
        axes[i].legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('ML_Grouped_Emotion_Analysis.png', dpi=300)
    plt.show()
    print("✅ ML Visualization saved: ML_Grouped_Emotion_Analysis.png")

# -------------------------------
# 7️⃣ 生成报告
# -------------------------------
def generate_detailed_report(df):
    emotion_groups = ['Positive','Negative','Surprise']
    report = ["ML GROUPED EMOTION ANALYSIS REPORT - THE OLD MAN AND THE SEA", "="*70]
    parts = df['part'].unique()
    for part in parts:
        part_data = df[df['part']==part]
        nodes = sorted(part_data['node_index'].unique())
        report.append(f"\n{part.upper()} ANALYSIS")
        report.append("-"*50)
        total_words = part_data['word_count'].sum()
        report.append(f"Total words: {total_words}")
        report.append(f"Number of nodes: {len(nodes)}")
        for node in nodes:
            node_row = part_data[part_data['node_index']==node].iloc[0]
            report.append(f"Pages {node_row['page_range']}: Words={node_row['word_count']}")
            for e in emotion_groups:
                count = node_row[e]
                if count>0:
                    report.append(f"  {e}: {count:.2f}")
    with open('ML_Grouped_Emotion_Analysis_Report.txt','w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    print("✅ ML Detailed report saved: ML_Grouped_Emotion_Analysis_Report.txt")

# -------------------------------
# 8️⃣ 合并四章 + 总览折线图
# -------------------------------
def create_combined_emotion_plot(df):
    emotion_groups = ['Positive', 'Negative', 'Surprise']
    colors = ['#2E8B57','#DC143C','#FFD700']
    parts = ['Beginning','Development','Climax','Resolution']

    fig = plt.figure(figsize=(20,16))

    # 每章折线图
    for i, part in enumerate(parts):
        ax = plt.subplot2grid((3,2),(i//2,i%2))
        part_data = df[df['part']==part]
        nodes = sorted(part_data['node_index'].unique())
        for j, emotion in enumerate(emotion_groups):
            values = [part_data[part_data['node_index']==n][emotion].values[0] for n in nodes]
            ax.plot(nodes, values, marker='o', linewidth=3, markersize=8,
                    color=colors[j], alpha=0.8, label=emotion)
        x_labels = [part_data[part_data['node_index']==n]['page_range'].values[0] for n in nodes]
        ax.set_xticks(nodes)
        ax.set_xticklabels(x_labels, fontsize=11)
        ax.set_title(f'{part} Chapter', fontsize=14, fontweight='bold')
        ax.set_ylabel('Emotion Count', fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)

    # 总览折线图
    ax_overall = plt.subplot2grid((3,1),(2,0))
    all_nodes = []
    all_page_ranges = []
    all_counts = {e: [] for e in emotion_groups}
    for part in parts:
        part_data = df[df['part']==part].sort_values('node_index')
        for idx, row in part_data.iterrows():
            all_nodes.append(f"{part}_Node{row['node_index']}")
            all_page_ranges.append(row['page_range'])
            for e in emotion_groups:
                all_counts[e].append(row[e])
    for e, c in zip(emotion_groups, colors):
        ax_overall.plot(range(len(all_nodes)), all_counts[e], marker='o', linewidth=3, markersize=8,
                        color=c, alpha=0.8, label=e)
    ax_overall.set_xticks(range(len(all_nodes)))
    ax_overall.set_xticklabels(all_page_ranges, rotation=45, fontsize=11)
    ax_overall.set_xlabel("PDF Page Ranges", fontsize=12)
    ax_overall.set_ylabel("Emotion Count", fontsize=12)
    ax_overall.set_title("Overall Emotion Analysis (Combined Plot)", fontsize=16, fontweight='bold')
    ax_overall.grid(True, alpha=0.3, linestyle='--')
    ax_overall.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig('ML_Combined_Emotion_Analysis.png', dpi=300)
    plt.show()
    print("✅ Combined Emotion Visualization saved: ML_Combined_Emotion_Analysis.png")

# -------------------------------
# 9️⃣ 单独整本书总览折线图
# -------------------------------
def create_overall_emotion_plot(df):
    emotion_groups = ['Positive', 'Negative', 'Surprise']
    colors = ['#2E8B57','#DC143C','#FFD700']

    all_nodes = []
    all_page_ranges = []
    all_counts = {e: [] for e in emotion_groups}

    for part in ['Beginning','Development','Climax','Resolution']:
        part_data = df[df['part']==part].sort_values('node_index')
        for idx, row in part_data.iterrows():
            all_nodes.append(f"{part}_Node{row['node_index']}")
            all_page_ranges.append(row['page_range'])
            for e in emotion_groups:
                all_counts[e].append(row[e])

    plt.figure(figsize=(20,6))
    for e, c in zip(emotion_groups, colors):
        plt.plot(range(len(all_nodes)), all_counts[e], marker='o', linewidth=3, markersize=8,
                 color=c, alpha=0.8, label=e)
    plt.xticks(range(len(all_nodes)), all_page_ranges, rotation=45)
    plt.xlabel("PDF Page Ranges", fontsize=12)
    plt.ylabel("Emotion Count (probability weighted)", fontsize=12)
    plt.title("The Old Man and The Sea - Overall Emotion Analysis", fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig('ML_Overall_Emotion_Analysis.png', dpi=300)
    plt.show()
    print("✅ Overall Emotion Visualization saved: ML_Overall_Emotion_Analysis.png")

# -------------------------------
# 10️⃣ 主程序
# -------------------------------
if __name__ == "__main__":
    # 指定四部分文本文件路径（请根据实际文件名修改）
    text_files_dict = {
        "Beginning": "老人与海_开端.txt",
        "Development": "老人与海_发展.txt",
        "Climax": "老人与海_高潮.txt",
        "Resolution": "老人与海_结局.txt"
    }

    print("Starting Machine Learning Grouped Emotion Analysis...")
    df = create_detailed_emotion_analysis(text_files_dict, training_file='emotion_corpus_300.txt')
    if df is not None:
        generate_detailed_report(df)
        # 单独总览图
        create_overall_emotion_plot(df)
        # 合并图（四章 + 总览）
        create_combined_emotion_plot(df)
        print("\n🎉 ML Analysis completed successfully!")
