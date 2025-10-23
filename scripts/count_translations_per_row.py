"""
テンプレート形式CSVの各行について、翻訳が入っている言語数をカウント
"""
import pandas as pd
import os
from datetime import datetime

def is_empty_value(value):
    """値が空かどうか判定"""
    if pd.isna(value):
        return True
    if isinstance(value, str):
        cleaned = str(value).strip()
        return cleaned == '' or cleaned.lower() == 'nan'
    return False

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
template_csv = os.path.join(output_dir, '全言語統合_テンプレート形式.csv')

print("=" * 80)
print("各行の翻訳言語数カウント")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# CSVを読み込み
df = pd.read_csv(template_csv, encoding='utf-8-sig')
print(f"データ: {len(df)}行 x {len(df.columns)}列")
print()

# 翻訳列（ja以外）を取得
translation_columns = [col for col in df.columns if col != 'ja']
print(f"翻訳列数: {len(translation_columns)}列")
print(f"列: {', '.join(translation_columns)}")
print()

# 各行について翻訳数をカウント
translation_counts = []

for idx, row in df.iterrows():
    count = 0
    for col in translation_columns:
        if not is_empty_value(row[col]):
            count += 1
    translation_counts.append(count)

# カウント結果を新しい列として追加
df['翻訳言語数'] = translation_counts

print("=" * 80)
print("統計情報")
print("=" * 80)
print()

# 統計情報
max_count = max(translation_counts)
min_count = min(translation_counts)
avg_count = sum(translation_counts) / len(translation_counts)

print(f"最大翻訳言語数: {max_count}言語")
print(f"最小翻訳言語数: {min_count}言語")
print(f"平均翻訳言語数: {avg_count:.2f}言語")
print()

# 翻訳言語数ごとの分布
from collections import Counter
count_distribution = Counter(translation_counts)

print("翻訳言語数の分布:")
for count in sorted(count_distribution.keys(), reverse=True):
    num_rows = count_distribution[count]
    percentage = (num_rows / len(df)) * 100
    print(f"  {count:2d}言語: {num_rows:4d}行 ({percentage:5.1f}%)")

print()

# サンプル表示（翻訳数が多い順）
print("=" * 80)
print("翻訳数が多い順（上位10件）")
print("=" * 80)
print()

df_sorted = df.sort_values('翻訳言語数', ascending=False)

for i, (idx, row) in enumerate(df_sorted.head(10).iterrows(), 1):
    japanese = row['ja']
    count = row['翻訳言語数']

    # 翻訳がある言語をリストアップ
    translated_langs = [col for col in translation_columns if not is_empty_value(row[col])]

    print(f"{i}. {japanese} ({count}言語)")
    print(f"   翻訳言語: {', '.join(translated_langs[:10])}{' ...' if len(translated_langs) > 10 else ''}")
    print()

# 翻訳数が少ない順
print("=" * 80)
print("翻訳数が少ない順（下位10件）")
print("=" * 80)
print()

for i, (idx, row) in enumerate(df_sorted.tail(10).iterrows(), 1):
    japanese = row['ja']
    count = row['翻訳言語数']

    # 翻訳がある言語をリストアップ
    translated_langs = [col for col in translation_columns if not is_empty_value(row[col])]

    print(f"{i}. {japanese} ({count}言語)")
    if len(translated_langs) > 0:
        print(f"   翻訳言語: {', '.join(translated_langs)}")
    else:
        print(f"   翻訳なし")
    print()

# 保存（翻訳言語数列を追加）
output_file = os.path.join(output_dir, '全言語統合_テンプレート形式_翻訳数付き.csv')
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print("=" * 80)
print("保存完了")
print("=" * 80)
print(f"出力ファイル: {output_file}")
print()
