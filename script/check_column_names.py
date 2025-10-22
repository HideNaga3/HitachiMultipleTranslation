"""列名を確認するスクリプト"""
import pandas as pd
from pathlib import Path

INPUT_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\output_cleaned")

# 英語CSVの列名を確認
filename = "【全課統合版】英語_げんばのことば_建設関連職種_cleaned.csv"
filepath = INPUT_DIR / filename

print(f"ファイル: {filename}")
print("="*80)

# header=3で読み込み
df = pd.read_csv(filepath, encoding='utf-8-sig', header=3)

print(f"\n行数: {len(df)}")
print(f"列数: {len(df.columns)}")
print(f"\n列名:")
for i, col in enumerate(df.columns):
    print(f"  列{i}: {repr(col)}")

print(f"\nサンプルデータ（最初の5行）:")
print(df.head())

print(f"\n特定の列のデータ:")
for i, col in enumerate(df.columns):
    print(f"\n列{i} ({repr(col)}):")
    print(df[col].head())
