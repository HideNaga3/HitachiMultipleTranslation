"""
類似度スコア付き比較シートの例を表示
"""
import pandas as pd
import os

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
deliverables_dir = os.path.join(project_root, '成果物_20251023')
for_claude_dir = os.path.join(project_root, 'for_claude')

excel_file = os.path.join(deliverables_dir, '02_逆翻訳_検証結果.xlsx')
df_comparison = pd.read_excel(excel_file, sheet_name='比較', header=0)

# UTF-8で出力
output_file = os.path.join(for_claude_dir, 'similarity_examples.txt')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("類似度スコア付き比較シートの例\n")
    f.write("=" * 80 + "\n\n")

    # 各分類ごとにサンプルを表示
    categories = ['完全一致', '高類似', '中類似', '低類似', '不一致']

    for category in categories:
        df_category = df_comparison[df_comparison['分類'] == category]

        if len(df_category) == 0:
            continue

        f.write("-" * 80 + "\n")
        f.write(f"【{category}】: {len(df_category)}件\n")
        f.write("-" * 80 + "\n\n")

        # 最初の10件を表示
        for idx, row in df_category.head(10).iterrows():
            f.write(f"[{row['アドレス']}] {row['言語']} | 類似度: {row['類似度_difflib']}\n")
            f.write(f"  単語: {row['単語']}\n")
            f.write(f"  再翻訳: {row['再翻訳']}\n")
            f.write(f"  翻訳: {row['翻訳']}\n")
            f.write("\n")

        f.write("\n")

print(f"保存: {output_file}")
print()

# コンソールにも統計を表示
print("=" * 80)
print("分類別統計")
print("=" * 80)
print()

class_counts = df_comparison['分類'].value_counts()
for classification, count in class_counts.items():
    percentage = (count / len(df_comparison)) * 100
    print(f"{classification}: {count}件 ({percentage:.1f}%)")

print()
print(f"総件数: {len(df_comparison)}件")
print()

# 「高類似」と「完全一致」の合計
high_quality = class_counts.get('完全一致', 0) + class_counts.get('高類似', 0)
high_quality_pct = (high_quality / len(df_comparison)) * 100
print(f"高品質翻訳（完全一致+高類似）: {high_quality}件 ({high_quality_pct:.1f}%)")
print()
