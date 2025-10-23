# -*- coding: utf-8 -*-
"""
列2にデータがある行を探す
"""

import pandas as pd

csv_file = "output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_improved_56cols.csv"

df = pd.read_csv(csv_file, encoding='utf-8-sig')

print("="*80)
print("列2にデータがある行を探す")
print("="*80)

# 列2（インデックス1、0始まり）を確認
col_idx = 1
col_name = df.columns[col_idx]

try:
    print(f"\n列{col_idx}の列名: '{col_name}'")
except UnicodeEncodeError:
    print(f"\n列{col_idx}の列名: [カンボジア語]")

# この列にデータがある行を探す
non_empty = df.iloc[:, col_idx].notna() & (df.iloc[:, col_idx] != '')

print(f"データがある行数: {non_empty.sum()}/{len(df)}")

if non_empty.sum() > 0:
    print(f"\nデータがある最初の5行:")

    for idx in df[non_empty].head(5).index:
        page = df.loc[idx, 'Page'] if 'Page' in df.columns else '?'
        no = df.loc[idx, 'No.'] if 'No.' in df.columns else '?'
        val = df.iloc[idx, col_idx]

        print(f"\n  行{idx}: Page {page}, No.{no}")
        try:
            print(f"    列{col_idx}の値: {str(val)}")
        except:
            print(f"    列{col_idx}の値: [カンボジア語データ]")

        # この行の他の列も確認（最初の10列）
        print(f"    他の列（最初の10列）:")
        for col_i in range(min(10, len(df.columns))):
            other_val = df.iloc[idx, col_i]
            if pd.notna(other_val) and other_val != '':
                try:
                    print(f"      列{col_i}: {str(other_val)[:30]}")
                except:
                    print(f"      列{col_i}: [データあり]")

print(f"\n{'='*80}")
print("完了")
print(f"{'='*80}")
