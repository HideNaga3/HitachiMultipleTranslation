"""
比較シートの内容を確認
"""
import pandas as pd
import os

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
deliverables_dir = os.path.join(project_root, '成果物_20251023')

excel_file = os.path.join(deliverables_dir, '02_逆翻訳_検証結果.xlsx')

print("=" * 80)
print("比較シートの確認")
print("=" * 80)
print()

# 比較シート読み込み
df_comparison = pd.read_excel(excel_file, sheet_name='比較', header=0)

print(f"比較シート: {len(df_comparison)}行")
print()

print("最初の20件:")
print("-" * 80)

# UTF-8で出力ファイルに書き込む
output_file = os.path.join(project_root, 'for_claude', 'comparison_preview.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("比較シートの内容（最初の20件）\n")
    f.write("=" * 80 + "\n\n")

    for idx, row in df_comparison.head(20).iterrows():
        line = f"【{idx+1}】{row['アドレス']} | {row['言語']} | 一致: {row['一致']}\n"
        line += f"  単語: {row['単語']}\n"
        line += f"  再翻訳: {row['再翻訳']}\n"
        line += f"  翻訳: {row['翻訳']}\n"
        line += "\n"
        f.write(line)

print(f"保存: {output_file}")
print()

# 統計情報
print("=" * 80)
print("統計情報")
print("=" * 80)
print()

# 一致/不一致の集計
match_counts = df_comparison['一致'].value_counts()
print("一致/不一致の集計:")
for match_val, count in match_counts.items():
    print(f"  {match_val}: {count}件")

print()

# 言語別の差異数
lang_counts = df_comparison['言語'].value_counts()
print("言語別の差異数:")
for lang, count in lang_counts.items():
    print(f"  {lang}: {count}件")

print()
print(f"総差異数: {len(df_comparison)}件")
print()
