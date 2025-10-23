"""Excelファイルの列名を確認するスクリプト"""
import pandas as pd
from pathlib import Path

EXCEL_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\建設関係Excel")

# 英語Excelの列名を確認
filename = "【全課統合版】英語_げんばのことば_建設関連職種.xlsx"
filepath = EXCEL_DIR / filename

print(f"ファイル: {filename}")
print("="*80)

# Excelを読み込み（header=1で2行目を列名として）
df = pd.read_excel(filepath, sheet_name=0, header=1)

print(f"\n行数: {len(df)}")
print(f"列数: {len(df.columns)}")
print(f"\n列名:")
for i, col in enumerate(df.columns):
    print(f"  列{i}: {repr(col)}")

print(f"\nデータ（最初の5行）:")
print(df.head())

print(f"\n各列の最初の5つの値:")
for i, col in enumerate(df.columns):
    print(f"\n列{i} ({repr(col)}):")
    print(df[col].head())
