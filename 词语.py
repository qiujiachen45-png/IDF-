import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np


def find_text_files():
    """
    Find all text files in current directory and subdirectories
    """
    print("Searching for text files...")
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")

    # List all files
    all_files = []
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.txt'):
                all_files.append(os.path.join(root, file))

    print("Found text files:")
    for file in all_files:
        print(f"  - {file}")

    return all_files


def split_text_into_nodes(text, part_name):
    """
    Split text into nodes based on predefined page ranges
    """
    # Define fixed node counts for each part to match page ranges
    node_counts = {
        'Beginning': 4,  # Pages 2-9 -> 4 nodes
        'Development': 4,  # Pages 10-25 -> 4 nodes
        'Climax': 3,  # Pages 26-38 -> 3 nodes
        'Resolution': 3  # Pages 39-48 -> 3 nodes
    }

    num_nodes = node_counts.get(part_name, 4)
    words = text.split()
    total_words = len(words)
    words_per_node = total_words // num_nodes

    nodes = []
    for i in range(num_nodes):
        start_idx = i * words_per_node
        if i == num_nodes - 1:  # Last node gets remaining words
            end_idx = total_words
        else:
            end_idx = (i + 1) * words_per_node
        node_text = ' '.join(words[start_idx:end_idx])
        nodes.append(node_text)

    return nodes


def analyze_emotion_in_text(text):
    """
    Analyze emotion frequency in text using comprehensive English vocabulary
    """
    emotion_dict = {
        'fear': ['fear', 'afraid', 'scared', 'terror', 'dread', 'anxious', 'worry',
                 'frightened', 'horror', 'panic', 'alarm', 'apprehension', 'trepidation',
                 'nervous', 'uneasy', 'threat', 'danger'],
        'anger': ['anger', 'angry', 'mad', 'furious', 'rage', 'hate', 'hostile',
                  'outrage', 'wrath', 'ire', 'resentment', 'fury', 'indignation',
                  'bitter', 'frustrated', 'annoyed', 'irritated'],
        'joy': ['joy', 'happy', 'glad', 'pleased', 'delight', 'smile', 'laugh',
                'cheerful', 'bliss', 'ecstasy', 'elation', 'jubilation', 'euphoria',
                'content', 'pleasure', 'satisfied', 'optimistic'],        'joy': ['joy', 'happy', 'glad', 'pleased', 'delight', 'smile', 'laugh',
                'cheerful', 'bliss', 'ecstasy', 'elation', 'jubilation', 'euphoria',
                'content', 'pleasure', 'satisfied', 'optimistic'],
        'sadness': ['sad', 'sadness', 'unhappy', 'grief', 'sorrow', 'tear', 'cry',
                    'mourn', 'depress', 'melancholy', 'despair', 'misery', 'heartbreak',
                    'lonely', 'hopeless', 'regret', 'disappoint'],
        'trust': ['trust', 'believe', 'faith', 'confidence', 'rely', 'depend',
                  'credence', 'assurance', 'certainty', 'conviction', 'reliance',
                  'secure', 'safe', 'comfort', 'hope'],
        'surprise': ['surprise', 'surprised', 'amazed', 'shock', 'astonish',
                     'wonder', 'astound', 'stun', 'baffle', 'startle', 'bewilder',
                     'unexpected', 'sudden', 'abrupt'],
        'anticip': ['anticipate', 'expect', 'hope', 'look forward', 'await',
                    'foresee', 'predict', 'envision', 'forecast', 'prospect',
                    'prepare', 'plan', 'awaiting', 'eager'],
        'disgust': ['disgust', 'disgusted', 'revulsion', 'nauseated', 'sickening',
                    'repulsion', 'loathing', 'abhorrence', 'distaste', 'aversion',
                    'repulsive', 'offensive', 'horrible']
    }

    emotion_counts = {emotion: 0 for emotion in emotion_dict.keys()}

    text_lower = text.lower()

    for emotion, keywords in emotion_dict.items():
        for keyword in keywords:
            emotion_counts[emotion] += text_lower.count(keyword)

    return emotion_counts


def group_emotions(emotion_counts):
    """
    Group 8 emotions into 3 categories:
    - Positive: joy, trust, anticip (hope/anticipation)
    - Negative: fear, anger, sadness, disgust
    - Neutral/Surprise: surprise
    """
    positive_emotions = ['joy', 'trust', 'anticip']
    negative_emotions = ['fear', 'anger', 'sadness', 'disgust']
    surprise_emotion = ['surprise']

    grouped = {
        'Positive': sum(emotion_counts[emotion] for emotion in positive_emotions),
        'Negative': sum(emotion_counts[emotion] for emotion in negative_emotions),
        'Surprise': sum(emotion_counts[emotion] for emotion in surprise_emotion)
    }

    return grouped


def create_detailed_emotion_analysis():
    """
    Create detailed emotion analysis with fixed nodes per chapter matching page ranges
    """
    # Story parts
    parts = ['Beginning', 'Development', 'Climax', 'Resolution']

    # Find all text files first
    all_text_files = find_text_files()

    if not all_text_files:
        print("❌ No text files found in current directory!")
        print("Please make sure your text files are in the same directory as this script.")
        return None

    # Try to match files with parts
    available_files = []
    used_files = set()

    for part in parts:
        found_file = None

        # Try different naming patterns
        patterns = [
            f'oldmansea_{part.lower()}.txt',
            f'{part.lower()}.txt',
            f'the_old_man_and_the_sea_{part.lower()}.txt',
            f'老人与海_{part.lower()}.txt'
        ]

        # First try exact matches
        for pattern in patterns:
            for file_path in all_text_files:
                file_name = os.path.basename(file_path)
                if file_name.lower() == pattern.lower() and file_path not in used_files:
                    found_file = file_path
                    used_files.add(file_path)
                    break
            if found_file:
                break

        # If no exact match, use any available text file
        if not found_file:
            for file_path in all_text_files:
                if file_path not in used_files:
                    found_file = file_path
                    used_files.add(file_path)
                    break

        if found_file:
            available_files.append(found_file)
            print(f"✅ Using '{os.path.basename(found_file)}' for {part} part")
        else:
            print(f"❌ No file available for: {part}")
            return None

    # Store all emotion data
    all_emotion_data = []

    print("\nAnalyzing text with fixed nodes per chapter...")
    print("=" * 60)

    # Define page ranges for each node to match previous analysis
    node_page_ranges = {
        'Beginning': ["2-3", "4-5", "6-7", "8-9"],
        'Development': ["10-13", "14-17", "18-21", "22-25"],
        'Climax': ["26-29", "30-33", "34-38"],
        'Resolution': ["39-42", "43-46", "47-48"]
    }

    for part, file_path in zip(parts, available_files):
        print(f"\n📖 Processing: {part} ({os.path.basename(file_path)})")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            continue

        # Use fixed node counts based on page ranges
        text_nodes = split_text_into_nodes(text, part)
        num_nodes = len(text_nodes)

        word_count = len(text.split())
        print(f"   Text length: {word_count} words")
        print(f"   Creating {num_nodes} analysis nodes (matching page ranges)")

        # Analyze each node
        for node_idx, node_text in enumerate(text_nodes):
            node_word_count = len(node_text.split())
            emotion_counts = analyze_emotion_in_text(node_text)
            grouped_emotions = group_emotions(emotion_counts)

            # Store results
            result = grouped_emotions.copy()
            result['part'] = part
            result['node'] = f"{part}_Node{node_idx + 1}"
            result['node_index'] = node_idx + 1
            result['word_count'] = node_word_count
            result['page_range'] = node_page_ranges[part][node_idx]

            all_emotion_data.append(result)

            print(f"     Node {node_idx + 1} (Pages {node_page_ranges[part][node_idx]}): {node_word_count} words, " +
                  f"Emotions: Positive={result['Positive']}, Negative={result['Negative']}, Surprise={result['Surprise']}")

    if not all_emotion_data:
        print("❌ No data processed!")
        return None

    # Create DataFrame
    df = pd.DataFrame(all_emotion_data)

    # Create visualization
    create_emotion_visualization(df)

    return df


def create_emotion_visualization(df):
    """
    Create visualization for grouped emotion analysis (3 lines only)
    """
    emotion_groups = ['Positive', 'Negative', 'Surprise']
    colors = ['#2E8B57', '#DC143C', '#FFD700']  # Green, Red, Gold
    parts = df['part'].unique()

    # Create subplots for each part
    fig, axes = plt.subplots(2, 2, figsize=(20, 12))
    axes = axes.flatten()

    for i, part in enumerate(parts):
        part_data = df[df['part'] == part]
        nodes = sorted(part_data['node_index'].unique())

        # Plot each emotion group
        for group_idx, emotion_group in enumerate(emotion_groups):
            emotion_values = []
            for node in nodes:
                node_data = part_data[part_data['node_index'] == node]
                if len(node_data) > 0:
                    emotion_values.append(node_data[emotion_group].values[0])
                else:
                    emotion_values.append(0)

            axes[i].plot(nodes, emotion_values,
                         marker='o',
                         linewidth=3,
                         markersize=8,
                         color=colors[group_idx],
                         label=emotion_group,
                         alpha=0.8)

        # Set simplified x-axis with only page numbers
        x_labels = []
        for node in nodes:
            node_data = part_data[part_data['node_index'] == node]
            if len(node_data) > 0:
                page_range = node_data['page_range'].values[0]
                x_labels.append(f"P{page_range}")
            else:
                x_labels.append(f"Node{node}")

        axes[i].set_xticks(nodes)
        axes[i].set_xticklabels(x_labels, fontsize=11)

        axes[i].set_title(f'{part} Chapter', fontsize=14, fontweight='bold')
        axes[i].set_xlabel('', fontsize=12)
        axes[i].set_ylabel('Emotion Frequency', fontsize=12)
        axes[i].grid(True, alpha=0.3, linestyle='--')
        axes[i].legend(fontsize=10)

        # Add word count and node info
        total_words = part_data['word_count'].sum()
        node_count = len(part_data)
        axes[i].text(0.02, 0.98, f'Words: {total_words}\nSections: {node_count}',
                     transform=axes[i].transAxes, fontsize=10,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('Grouped_Emotion_Analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Create combined overview chart
    create_combined_overview(df)

    print("✅ All visualizations saved successfully!")


def create_combined_overview(df):
    """
    Create a combined overview chart showing all parts with 3 lines
    """
    emotion_groups = ['Positive', 'Negative', 'Surprise']
    colors = ['#2E8B57', '#DC143C', '#FFD700']

    plt.figure(figsize=(18, 8))

    parts = df['part'].unique()

    # Create x-axis labels with page ranges only
    x_labels = []
    x_positions = []
    current_pos = 0

    for part in parts:
        part_data = df[df['part'] == part]
        nodes = sorted(part_data['node_index'].unique())
        for node in nodes:
            node_data = part_data[part_data['node_index'] == node]
            if len(node_data) > 0:
                page_range = node_data['page_range'].values[0]
                x_labels.append(f"P{page_range}")
            else:
                x_labels.append("")
            x_positions.append(current_pos)
            current_pos += 1

    # Plot each emotion group across all nodes
    for group_idx, emotion_group in enumerate(emotion_groups):
        emotion_values = []
        for part in parts:
            part_data = df[df['part'] == part]
            nodes = sorted(part_data['node_index'].unique())
            for node in nodes:
                node_data = part_data[part_data['node_index'] == node]
                if len(node_data) > 0:
                    emotion_values.append(node_data[emotion_group].values[0])
                else:
                    emotion_values.append(0)

        plt.plot(x_positions, emotion_values,
                 marker='o',
                 linewidth=3,
                 markersize=6,
                 color=colors[group_idx],
                 label=emotion_group,
                 alpha=0.8)

    plt.title('The Old Man and The Sea - Emotion Analysis by Page Ranges',
              fontsize=16, fontweight='bold', pad=20)

    # Set x-axis with page ranges only
    plt.xlabel('PDF Page Ranges', fontsize=12)
    plt.xticks(x_positions, x_labels, rotation=45, fontsize=10)

    plt.ylabel('Emotion Frequency', fontsize=12)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    # Add chapter separators and labels
    chapter_boundaries = []
    current_boundary = 0
    for part in parts:
        part_data = df[df['part'] == part]
        chapter_boundaries.append(current_boundary)
        current_boundary += len(part_data)

    for i, (boundary, part) in enumerate(zip(chapter_boundaries, parts)):
        if i < len(chapter_boundaries) - 1:
            plt.axvline(x=chapter_boundaries[i + 1] - 0.5, color='gray', linestyle='--', alpha=0.7)
        plt.text((boundary + chapter_boundaries[i + 1] - 0.5) / 2 if i < len(chapter_boundaries) - 1 else (
                                                                                                                      boundary + current_boundary - 1) / 2,
                 plt.ylim()[1] * 0.95, part,
                 ha='center', va='top', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))

    plt.tight_layout()
    plt.savefig('Combined_Grouped_Emotion_Analysis.png', dpi=300, bbox_inches='tight')
    plt.show()


def generate_detailed_report(df):
    """
    Generate detailed analysis report for grouped emotions
    """
    emotion_groups = ['Positive', 'Negative', 'Surprise']

    report = []
    report.append("GROUPED EMOTION ANALYSIS REPORT - THE OLD MAN AND THE SEA")
    report.append("=" * 70)
    report.append("Analysis with fixed nodes per chapter matching page ranges")
    report.append("")
    report.append("Emotion Groups:")
    report.append("- Positive: joy, trust, anticipation")
    report.append("- Negative: fear, anger, sadness, disgust")
    report.append("- Surprise: surprise")
    report.append("")

    parts = df['part'].unique()

    for part in parts:
        part_data = df[df['part'] == part]
        nodes = sorted(part_data['node_index'].unique())

        report.append(f"\n{part.upper()} ANALYSIS")
        report.append("-" * 50)

        total_words = part_data['word_count'].sum()
        report.append(f"Total words: {total_words}")
        report.append(f"Number of nodes: {len(nodes)}")
        report.append("")

        # Node-by-node analysis with page ranges
        for node in nodes:
            node_data = part_data[part_data['node_index'] == node]
            if len(node_data) > 0:
                node_row = node_data.iloc[0]
                report.append(f"Pages {node_row['page_range']}:")
                report.append(f"  Words: {node_row['word_count']}")

                # All emotion groups
                for emotion_group in emotion_groups:
                    count = node_row[emotion_group]
                    if count > 0:
                        report.append(f"  {emotion_group}: {count}")
                report.append("")

    # Overall statistics
    report.append("\nOVERALL STATISTICS")
    report.append("-" * 50)

    total_emotions = {emotion: df[emotion].sum() for emotion in emotion_groups}
    dominant_emotion = max(total_emotions.items(), key=lambda x: x[1])

    report.append(f"Most frequent emotion group: {dominant_emotion[0]} ({dominant_emotion[1]} occurrences)")
    report.append("")
    report.append("Emotion group distribution:")
    for emotion_group in emotion_groups:
        report.append(f"  {emotion_group}: {total_emotions[emotion_group]}")

    # Save report
    with open('Grouped_Emotion_Analysis_Report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print("✅ Detailed report saved: Grouped_Emotion_Analysis_Report.txt")

    # Print summary to console
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    for part in parts:
        part_data = df[df['part'] == part]
        print(f"\n{part}:")
        print(f"  Sections: {len(part_data)}")
        print(f"  Total words: {part_data['word_count'].sum()}")

        part_emotions = {emotion: part_data[emotion].sum() for emotion in emotion_groups}
        top_emotion = max(part_emotions.items(), key=lambda x: x[1])
        print(f"  Dominant emotion group: {top_emotion[0]} ({top_emotion[1]})")


# Main execution
if __name__ == "__main__":
    print("Starting Grouped Emotion Analysis with Fixed Nodes...")
    print("=" * 70)

    try:
        df = create_detailed_emotion_analysis()
        if df is not None:
            generate_detailed_report(df)
            print("\n🎉 Analysis completed successfully!")
            print("\n📁 Generated files:")
            print("   - Grouped_Emotion_Analysis.png")
            print("   - Combined_Grouped_Emotion_Analysis.png")
            print("   - Grouped_Emotion_Analysis_Report.txt")
        else:
            print("❌ Analysis failed - no data processed")
    except Exception as e:
        print(f"❌ Analysis failed with error: {e}")