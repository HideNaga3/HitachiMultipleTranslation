"""
PyMuPDFで抽出したCSVファイルを検証する
CIDコードの有無を確認
"""

import pandas as pd
import re
from pathlib import Path

# CSVファイルを読み込む
csv_path = Path('output') / 'test_カンボジア語_pymupdf抽出.csv'

print("="*80)
print("PyMuPDF抽出結果の検証")
print("="*80)

# CSV読み込み
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print(f"\nCSVファイル: {csv_path}")
print(f"行数: {len(df)}")
print(f"列数: {len(df.columns)}")
print(f"\n列名: {list(df.columns)[:10]}")  # 最初の10列

# CIDコード検索
cid_pattern = r'\(cid:\d+\)'
cid_found = False
cid_count = 0
cid_examples = []

for col in df.columns:
    if df[col].dtype == 'object':
        # 各セルをチェック
        for idx, value in enumerate(df[col]):
            if pd.notna(value):
                value_str = str(value)
                if re.search(cid_pattern, value_str):
                    cid_found = True
                    cid_matches = re.findall(cid_pattern, value_str)
                    cid_count += len(cid_matches)

                    if len(cid_examples) < 5:
                        cid_examples.append({
                            'row': idx,
                            'col': col,
                            'value': value_str[:100],  # 最初の100文字
                            'cid_codes': cid_matches
                        })

# 結果表示
print("\n" + "="*80)
print("CIDコード検証結果")
print("="*80)

if cid_found:
    print(f"[!] CIDコードが見つかりました: {cid_count}件")
    print(f"\n例:")
    for i, example in enumerate(cid_examples, 1):
        print(f"\n  {i}. 行{example['row']}, 列'{example['col']}'")
        print(f"     CIDコード: {example['cid_codes']}")
        print(f"     値: {example['value']}")
else:
    print("[OK] CIDコードなし!")

# データサンプル表示
print("\n" + "="*80)
print("データサンプル（最初の5行）")
print("="*80)
print(df.head())

print("\n" + "="*80)
print("検証完了")
print("="*80)
