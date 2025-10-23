"""
翻訳データ解析スクリプト

全言語統合CSVから以下の情報を抽出：
1. 日本語単語リスト
2. 各言語の単語数（空欄を除く）
3. 各言語の翻訳カバレッジ
"""

import pandas as pd
import json

# CSVファイルを読み込み
csv_path = 'output/全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("翻訳データ解析レポート")
print("=" * 80)
print()

# 基本情報
print(f"総単語数: {len(df)} 語")
print()

# 列名
columns = df.columns.tolist()
print(f"言語列: {', '.join(columns)}")
print()

# 各言語の統計情報
print("-" * 80)
print("言語別統計")
print("-" * 80)

language_stats = {}

for col in columns:
    # 空欄でないセル数をカウント
    non_empty_count = df[col].notna().sum()
    empty_count = df[col].isna().sum()
    coverage = (non_empty_count / len(df)) * 100

    language_stats[col] = {
        'total': len(df),
        'filled': non_empty_count,
        'empty': empty_count,
        'coverage': coverage
    }

    print(f"{col:10s}: {non_empty_count:3d}/{len(df)} ({coverage:5.1f}%) - 空欄: {empty_count}")

print()

# 日本語単語リスト（最初の50語）
print("-" * 80)
print("日本語単語リスト（最初の50語）")
print("-" * 80)

ja_words = df['ja'].tolist()
for i, word in enumerate(ja_words[:50], 1):
    print(f"{i:3d}. {word}")

print()
print(f"... 他 {len(ja_words) - 50} 語")
print()

# 空欄がある行を特定
print("-" * 80)
print("翻訳が空欄の行")
print("-" * 80)

for col in columns:
    if col == 'ja':
        continue

    empty_rows = df[df[col].isna()]
    if len(empty_rows) > 0:
        print(f"\n{col} が空欄の行:")
        for idx, row in empty_rows.iterrows():
            print(f"  行{idx + 2}: {row['ja']}")

print()

# 結果をテキストファイルに保存
txt_path = 'for_claude/translation_data_analysis.txt'
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("翻訳データ解析レポート（詳細版）\n")
    f.write("=" * 80 + "\n\n")

    f.write(f"総単語数: {len(df)} 語\n\n")

    f.write("言語別統計:\n")
    f.write("-" * 80 + "\n")
    for col in columns:
        stats = language_stats[col]
        f.write(f"{col:10s}: {stats['filled']:3d}/{stats['total']} ({stats['coverage']:5.1f}%) - 空欄: {stats['empty']}\n")

    f.write("\n\n日本語単語全リスト:\n")
    f.write("-" * 80 + "\n")
    for i, word in enumerate(ja_words, 1):
        f.write(f"{i:3d}. {word}\n")

print("=" * 80)
print(f"解析結果を {txt_path} に保存しました")
print("=" * 80)
