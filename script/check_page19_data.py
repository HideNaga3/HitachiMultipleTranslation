# -*- coding: utf-8 -*-
"""
Page 19のデータ内容を確認
"""

import pandas as pd

csv_file = "output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_50cols.csv"
df = pd.read_csv(csv_file, encoding='utf-8-sig')

print("="*80)
print("Page 19 データ内容確認")
print("="*80)

# Page 19のデータを抽出
page_19 = df[df['Page'] == 19].copy()

print(f"\nPage 19の行数: {len(page_19)}")

if len(page_19) > 0:
    # 最初の数行を確認
    print(f"\nPage 19の最初の3行:")

    for idx, row in page_19.head(3).iterrows():
        print(f"\n--- 行{idx} ---")
        print(f"Page: {row['Page']}, Table: {row['Table']}, No.: {row['No.']}")

        # 空でない列とその値を表示
        for col in df.columns:
            if col in ['Page', 'Table', 'No.']:
                continue

            val = row[col]
            if pd.notna(val) and val != '':
                try:
                    val_str = str(val)[:60]
                    print(f"  列{df.columns.get_loc(col):2d} '{col}': {val_str}")
                except UnicodeEncodeError:
                    print(f"  列{df.columns.get_loc(col):2d} [表示エラー]: [データあり]")

# 全ページでデータが多い列（列31）の内容を確認
print(f"\n{'='*80}")
print("データ数が多い列の内容確認")
print(f"{'='*80}")

# 列31を確認（424/534データ）
col_31_name = df.columns[31]
try:
    print(f"\n列31: '{col_31_name}'")
except UnicodeEncodeError:
    print(f"\n列31: [表示エラー]")

col_31_data = df[col_31_name]
non_empty = col_31_data.notna() & (col_31_data != '')

print(f"データ数: {non_empty.sum()}/{len(df)}")
print(f"\nサンプルデータ（最初の5件）:")
for idx in df[non_empty].head(5).index:
    page = df.loc[idx, 'Page']
    no = df.loc[idx, 'No.']
    val = df.loc[idx, col_31_name]
    try:
        print(f"  Page {page}, No.{no}: {str(val)[:60]}")
    except:
        print(f"  Page {page}, No.{no}: [表示エラー]")

print(f"\n{'='*80}")
print("完了")
print(f"{'='*80}")
