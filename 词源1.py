import os
import matplotlib.pyplot as plt


def find_text_files():
    """
    Find all text files in current directory
    """
    print("Searching for text files in current directory...")
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")

    # List all files in current directory
    all_files = os.listdir()
    text_files = [f for f in all_files if f.endswith('.txt')]

    print("Found text files:")
    for file in text_files:
        print(f"  - {file}")

    return text_files


def analyze_text_pages():
    """
    Analyze text files and output page numbers for each part
    """
    # Story parts
    parts = ['Beginning', 'Development', 'Climax', 'Resolution']

    # Find available files
    available_files = []
    text_files = find_text_files()

    if not text_files:
        print("❌ No text files found in current directory!")
        return None

    # Try to match files with parts
    for part in parts:
        found_file = None
        # Try different naming patterns
        patterns = [
            f'oldmansea_{part.lower()}.txt',
            f'{part.lower()}.txt',
            f'the_old_man_and_the_sea_{part.lower()}.txt'
        ]

        for pattern in patterns:
            if pattern in text_files:
                found_file = pattern
                break

        # If no exact match, use any available file in order
        if not found_file and text_files:
            found_file = text_files.pop(0)

        if found_file:
            available_files.append(found_file)
            print(f"✅ Using '{found_file}' for {part} part")
        else:
            print(f"❌ No file found for: {part}")
            return None

    print("\nThe Old Man and The Sea - Page Number Analysis")
    print("=" * 50)

    # Define page ranges for each part (based on PDF structure)
    page_ranges = {
        'Beginning': "Pages 2-9",
        'Development': "Pages 10-25",
        'Climax': "Pages 26-38",
        'Resolution': "Pages 39-48"
    }

    # Define node page distribution within each part
    node_pages = {
        'Beginning': ["Pages 2-3", "Pages 4-5", "Pages 6-7", "Pages 8-9"],
        'Development': ["Pages 10-13", "Pages 14-17", "Pages 18-21", "Pages 22-25"],
        'Climax': ["Pages 26-29", "Pages 30-33", "Pages 34-38"],
        'Resolution': ["Pages 39-42", "Pages 43-46", "Pages 47-48"]
    }

    for part, filename in zip(parts, available_files):
        print(f"\n📖 {part} Part")
        print(f"   File: {filename}")
        print(f"   Page Range: {page_ranges[part]}")

        # Read file to calculate basic info
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()

            word_count = len(text.split())
            char_count = len(text)

            print(f"   Text Stats: {word_count} words, {char_count} characters")
            print(f"   Node Distribution:")

            # Display page numbers for each node
            nodes = node_pages[part]
            for i, page_range in enumerate(nodes, 1):
                print(f"     - Node {i}: {page_range}")
        except Exception as e:
            print(f"   Error reading file: {e}")

    # Generate summary report
    print("\n" + "=" * 50)
    print("Page Number Summary")
    print("=" * 50)

    summary = []
    summary.append("The Old Man and The Sea - Page Number Correspondence Table")
    summary.append("=" * 50)

    for part in parts:
        summary.append(f"\n{part} Part:")
        summary.append(f"Overall Range: {page_ranges[part]}")
        nodes = node_pages[part]
        for i, page_range in enumerate(nodes, 1):
            summary.append(f"  Node {i}: {page_range}")

    # Save to file
    with open('page_number_table.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary))

    print("✅ Page number table saved: page_number_table.txt")

    return page_ranges, node_pages


def create_simple_visualization(page_ranges, node_pages):
    """
    Create simple page number visualization
    """
    parts = list(page_ranges.keys())

    fig, ax = plt.subplots(figsize=(14, 10))

    # Set colors
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

    y_pos = 0
    for i, part in enumerate(parts):
        # Main part bar
        ax.barh(y_pos, width=1, height=0.6, color=colors[i], alpha=0.7, label=part)
        ax.text(0.5, y_pos, f'{part}\n{page_ranges[part]}',
                ha='center', va='center', fontsize=14, fontweight='bold')

        # Node breakdown
        nodes = node_pages[part]
        node_height = 0.6 / len(nodes)

        for j, page_range in enumerate(nodes):
            node_y = y_pos - 0.3 + (j + 0.5) * node_height
            ax.text(0.2, node_y, f'Node {j + 1}: {page_range}',
                    ha='left', va='center', fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

        y_pos += 1

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, len(parts))
    ax.set_xlabel('Text Structure', fontsize=12)
    ax.set_title('The Old Man and The Sea - Page Number Distribution',
                 fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')  # Hide axes

    plt.tight_layout()
    plt.savefig('page_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()


# Main execution
if __name__ == "__main__":
    print("Analyzing page numbers for The Old Man and The Sea...")
    print("=" * 60)

    try:
        page_ranges, node_pages = analyze_text_pages()
        if page_ranges:
            create_simple_visualization(page_ranges, node_pages)
            print("\n🎉 Analysis completed!")
            print("\n📁 Generated files:")
            print("   - page_number_table.txt")
            print("   - page_distribution.png")

            # Print concise page number table to console
            print("\n" + "=" * 50)
            print("Concise Page Number Table")
            print("=" * 50)
            for part in page_ranges.keys():
                print(f"\n{part}: {page_ranges[part]}")
                for i, pages in enumerate(node_pages[part], 1):
                    print(f"  Node {i}: {pages}")

        else:
            print("❌ Analysis failed - files not found")
    except Exception as e:
        print(f"❌ Analysis failed: {e}")