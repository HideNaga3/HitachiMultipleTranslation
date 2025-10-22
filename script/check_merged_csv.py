# -*- coding: utf-8 -*-
"""
統合CSVの内容を確認するスクリプト
"""

import pandas as pd

# 統合CSVを読み込み
df = pd.read_csv("output_cleaned/全言語統合.csv", encoding='utf-8-sig')

print("="*80)
print("統合CSV 統計情報")
print("="*80)

print(f"\n総行数: {len(df):,}行")
print(f"総列数: {len(df.columns)}列")

print(f"\n列名一覧:")
for i, col in enumerate(df.columns, 1):
    try:
        print(f"  {i:2d}. {col}")
    except UnicodeEncodeError:
        print(f"  {i:2d}. [エンコーディングエラー]")

print(f"\n言語別の行数:")
language_counts = df['言語'].value_counts()
for language, count in language_counts.items():
    print(f"  {language}: {count}行")

print(f"\n番号の範囲:")
print(f"  最小: {df['番号'].min()}")
print(f"  最大: {df['番号'].max()}")

print(f"\nサンプルデータ（最初の10行）:")
sample = df[['言語', '番号', '単語', '翻訳']].head(10)
try:
    print(sample.to_string(index=False))
except UnicodeEncodeError:
    print("[エンコーディングエラーのため表示できません]")

print(f"\n各言語のサンプル（各1行）:")
for language in df['言語'].unique():
    lang_data = df[df['言語'] == language][['言語', '番号', '単語', '翻訳']].head(1)
    try:
        print(lang_data.to_string(index=False, header=False))
    except UnicodeEncodeError:
        print(f"{language}: [エンコーディングエラー]")

print("\n"*2)
print("="*80)
print("統合完了 - ファイルは Excel や他のアプリケーションで開けます")
print("="*80)
