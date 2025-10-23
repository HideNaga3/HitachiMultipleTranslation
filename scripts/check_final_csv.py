# -*- coding: utf-8 -*-
"""
最終的な統合CSVの内容を確認するスクリプト
"""

import pandas as pd

# 統合CSVを読み込み
df = pd.read_csv("output_cleaned/全言語統合.csv", encoding='utf-8-sig')

print("="*80)
print("最終統合CSV - 確認")
print("="*80)

print(f"\n総行数: {len(df):,}行")
print(f"総列数: {len(df.columns)}列")

print(f"\n列名:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print(f"\n言語別の行数:")
language_counts = df['言語'].value_counts()
for language, count in language_counts.items():
    print(f"  {language}: {count}行")

print(f"\nPDFページ番号の範囲:")
print(f"  最小: {df['PDFページ番号'].min()}")
print(f"  最大: {df['PDFページ番号'].max()}")

print(f"\n番号の範囲:")
print(f"  最小: {df['番号'].min()}")
print(f"  最大: {df['番号'].max()}")

print(f"\n各言語のサンプル（最初の3行ずつ）:")
for language in sorted(df['言語'].unique()):
    print(f"\n--- {language} ---")
    lang_data = df[df['言語'] == language].head(3)
    for idx, row in lang_data.iterrows():
        try:
            print(f"  {row['番号']:2d} | Page {row['PDFページ番号']:2d} | {row['単語'][:20]:20s} | {str(row['翻訳'])[:30]:30s}")
        except:
            print(f"  {row['番号']:2d} | Page {row['PDFページ番号']:2d} | [表示エラー]")

print("\n" + "="*80)
print("ファイルパス: output_cleaned/全言語統合.csv")
print("このファイルは Excel、Google Sheets、pandas などで利用できます")
print("="*80)
