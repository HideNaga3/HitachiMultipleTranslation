"""
PyMuPDFで抽出したCSVの構造を詳しく確認
最終インポート用CSV形式に整形可能かチェック
"""

import pandas as pd
from pathlib import Path

# CSVファイルを読み込む
csv_path = Path('output') / 'test_カンボジア語_pymupdf抽出.csv'

print("="*80)
print("PyMuPDF抽出データの詳細確認")
print("="*80)

# CSV読み込み
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print(f"\nCSVファイル: {csv_path.name}")
print(f"総行数: {len(df)}")
print(f"総列数: {len(df.columns)}")
print(f"\n全列名:")
for i, col in enumerate(df.columns):
    print(f"  {i}: {col}")

# ページごとの行数を確認
print(f"\n" + "="*80)
print("ページごとの統計")
print("="*80)
page_stats = df.groupby('Page').size()
print(f"総ページ数: {len(page_stats)}")
print(f"各ページの行数（最初の10ページ）:")
for page, count in page_stats.head(10).items():
    print(f"  ページ {page}: {count}行")

# 最初の10行の詳細データ
print(f"\n" + "="*80)
print("データサンプル（最初の10行、全列表示）")
print("="*80)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

for idx, row in df.head(10).iterrows():
    print(f"\n--- 行 {idx} (Page={row['Page']}, Table={row['Table']}) ---")
    for col in df.columns:
        value = row[col]
        if pd.notna(value) and value != '':
            print(f"  {col}: {value}")

# 特定のページ（19ページ）を詳しく確認
print(f"\n" + "="*80)
print("ページ19のデータ（CIDコードがあった問題ページ）")
print("="*80)
page19_df = df[df['Page'] == 19]
print(f"ページ19の行数: {len(page19_df)}")
print(f"\n最初の5行:")
for idx, row in page19_df.head(5).iterrows():
    print(f"\n--- 行 {idx} ---")
    for col in df.columns:
        value = row[col]
        if pd.notna(value) and value != '':
            print(f"  {col}: {value}")

# 列の内容から推測される構造
print(f"\n" + "="*80)
print("データ構造の推定")
print("="*80)
print("\nColumn_0に含まれるユニークな値の例（最初の20件）:")
col0_unique = df['Column_0'].dropna().unique()[:20]
for val in col0_unique:
    print(f"  {val}")

print("\nColumn_1に含まれる値の例（最初の10件）:")
col1_samples = df['Column_1'].dropna().head(10)
for idx, val in col1_samples.items():
    print(f"  行{idx}: {val}")

# 最終インポート用形式との比較
print(f"\n" + "="*80)
print("最終インポート用CSV形式との比較")
print("="*80)
target_path = Path('output') / '全言語統合_テンプレート_インポート用.csv'
if target_path.exists():
    target_df = pd.read_csv(target_path, encoding='utf-8-sig')
    print(f"\n目標形式:")
    print(f"  行数: {len(target_df)}")
    print(f"  列数: {len(target_df.columns)}")
    print(f"  列名: {list(target_df.columns)}")
    print(f"\n目標形式のサンプル（最初の3行）:")
    print(target_df.head(3))

    # カンボジア語列の確認
    if 'km' in target_df.columns:
        print(f"\n目標形式のカンボジア語サンプル:")
        km_samples = target_df['km'].dropna().head(5)
        for idx, val in km_samples.items():
            ja_word = target_df.loc[idx, 'ja'] if 'ja' in target_df.columns else '?'
            print(f"  {ja_word} -> {val}")
else:
    print("\n目標CSVファイルが見つかりません")

print(f"\n" + "="*80)
print("確認完了")
print("="*80)
