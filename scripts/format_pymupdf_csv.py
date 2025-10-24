"""
PyMuPDF抽出CSVを整形
形式: 言語, Page, No, 日本語, 翻訳
"""

import pandas as pd
from pathlib import Path
import sys
import io

# UTF-8出力を強制
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("PyMuPDF抽出CSVの整形")
print("="*80)

# 入力ファイル
input_csv = Path('output') / 'test_カンボジア語_pymupdf抽出.csv'
output_csv = Path('output') / 'カンボジア語_pymupdf_整形版.csv'

print(f"\n入力: {input_csv.name}")

# CSV読み込み
df = pd.read_csv(input_csv, encoding='utf-8-sig')

print(f"元データ: {len(df)}行 x {len(df.columns)}列")

# 必要な列を抽出
formatted_df = pd.DataFrame({
    '言語': 'カンボジア語',
    'Page': df['Page'],
    'No': df['Column_0'],
    '日本語': df['Column_1'],
    '翻訳': df['Column_3']
})

# 日本語が空の行を除外
formatted_df = formatted_df[formatted_df['日本語'].notna()].copy()

# 空白をトリム
formatted_df['日本語'] = formatted_df['日本語'].str.strip()
formatted_df['翻訳'] = formatted_df['翻訳'].fillna('').str.strip()

print(f"整形後: {len(formatted_df)}行 x {len(formatted_df.columns)}列")

# データサンプル表示
print(f"\n【整形後データのサンプル（最初の10行）】")
print("="*80)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 40)
print(formatted_df.head(10).to_string(index=False))

# CSV保存
formatted_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

print(f"\n" + "="*80)
print(f"整形完了")
print(f"出力: {output_csv}")
print(f"サイズ: {output_csv.stat().st_size / 1024:.1f} KB")
print("="*80)

# 統計情報
print(f"\n【統計情報】")
print(f"総行数: {len(formatted_df)}")
print(f"ユニークな日本語単語: {formatted_df['日本語'].nunique()}")
print(f"翻訳が空の行: {(formatted_df['翻訳'] == '').sum()}")
print(f"ページ数: {formatted_df['Page'].nunique()}")

# ページごとの行数
print(f"\nページごとの行数（最初の10ページ）:")
page_counts = formatted_df.groupby('Page').size()
for page, count in page_counts.head(10).items():
    print(f"  ページ {page}: {count}行")

print("\n整形完了！")
