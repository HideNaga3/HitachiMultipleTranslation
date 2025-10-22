# -*- coding: utf-8 -*-
"""
ベトナム語版CSVの列名を確認するスクリプト
"""

import pandas as pd

# ベトナム語版を読み込み
df = pd.read_csv("output/【全課統合版】ベトナム語_げんばのことば_建設関連職種_27cols.csv",
                 encoding='utf-8-sig', nrows=5)

print(f"列数: {len(df.columns)}")
print(f"\n列名リスト:")

# 列名をファイルに保存（print ではエンコーディングエラーになるため）
with open("vietnamese_columns.txt", "w", encoding="utf-8") as f:
    for i, col in enumerate(df.columns, 1):
        f.write(f"{i}. {col}\n")

print("列名を vietnamese_columns.txt に保存しました")

# No. 列があるか確認
if 'No.' in df.columns:
    print("\n[OK] No. 列が存在します")
else:
    print("\n[NG] No. 列が存在しません")
    print("\n'No' を含む列名を検索:")
    for col in df.columns:
        if 'no' in str(col).lower() or '番号' in str(col) or 'số' in str(col).lower():
            print(f"  候補: {repr(col)}")
