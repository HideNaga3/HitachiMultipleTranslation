# -*- coding: utf-8 -*-
"""
改善版CSVの全列のデータ数を確認
"""

import pandas as pd

csv_file = "output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_improved_56cols.csv"

print("="*80)
print("カンボジア語 改善版CSV - 全列データ数確認")
print("="*80)

df = pd.read_csv(csv_file, encoding='utf-8-sig')

print(f"\n総行数: {len(df)}")
print(f"総列数: {len(df.columns)}")

# No.列の有効データ
if 'No.' in df.columns:
    no_valid = df['No.'].notna() & (df['No.'] != '')
    valid_count = no_valid.sum()
    print(f"\nNo.列の有効データ: {valid_count}行")
else:
    valid_count = len(df)
    print(f"\nNo.列なし、全行を基準とします")

# 各列のデータ数を確認
print(f"\n各列のデータ数（データ数が多い順）:")

col_data = []
for col in df.columns:
    if col in ['Page', 'Table']:
        continue

    non_empty = df[col].notna() & (df[col] != '')
    count = non_empty.sum()
    ratio = count / valid_count * 100 if valid_count > 0 else 0

    col_data.append({
        'column': col,
        'count': count,
        'ratio': ratio
    })

# データ数が多い順にソート
col_data_sorted = sorted(col_data, key=lambda x: x['count'], reverse=True)

# TOP 20を表示
print(f"\nTOP 20列:")
for i, item in enumerate(col_data_sorted[:20], 1):
    col = item['column']
    count = item['count']
    ratio = item['ratio']

    try:
        print(f"  {i:2d}. '{col}': {count}/{valid_count} ({ratio:.1f}%)")
    except UnicodeEncodeError:
        print(f"  {i:2d}. [カンボジア語列]: {count}/{valid_count} ({ratio:.1f}%)")

# データが80%以上ある列を確認
print(f"\nデータが80%以上ある列:")
for item in col_data_sorted:
    if item['ratio'] >= 80:
        try:
            print(f"  '{item['column']}': {item['count']}/{valid_count} ({item['ratio']:.1f}%)")
        except UnicodeEncodeError:
            print(f"  [カンボジア語列]: {item['count']}/{valid_count} ({item['ratio']:.1f}%)")

        # サンプルデータを表示
        col = item['column']
        non_empty = df[col].notna() & (df[col] != '')
        if non_empty.sum() > 0:
            print(f"    サンプル（最初の3件）:")
            for idx in df[non_empty].head(3).index:
                val = df.loc[idx, col]
                try:
                    print(f"      {str(val)[:50]}")
                except:
                    print(f"      [カンボジア語データ]")

print(f"\n{'='*80}")
print("完了")
print(f"{'='*80}")
