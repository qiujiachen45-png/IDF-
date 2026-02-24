import pdfplumber
import os


def simple_extract_parts(pdf_path):
    """
    简化版：直接提取四个部分
    """
    parts = {
        "开端": (1, 9),  # PDF第2-10页
        "发展": (10, 33),  # PDF第11-34页
        "高潮": (34, 35),  # PDF第35-36页
        "结局": (36, 48)  # PDF第37-49页
    }

    with pdfplumber.open(pdf_path) as pdf:
        for part_name, (start, end) in parts.items():
            print(f"提取{part_name}部分...")

            text_parts = []
            for page_num in range(start, end + 1):
                if page_num < len(pdf.pages):
                    text = pdf.pages[page_num].extract_text()
                    if text:
                        text_parts.append(f"【第{page_num + 1}页】\n{text}\n\n")

            # 保存文件
            if text_parts:
                filename = f"老人与海_{part_name}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(''.join(text_parts))
                print(f"✅ 已保存: {filename}")


# 直接运行
simple_extract_parts("oldmansea.pdf")
print("🎉 四个结构部分提取完成！")
