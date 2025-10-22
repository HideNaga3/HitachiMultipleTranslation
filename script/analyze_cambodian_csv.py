# -*- coding: utf-8 -*-
"""
カンボジア語の元CSVを詳しく分析
"""

import pandas as pd

# 元のカンボジア語CSV
csv_file = "output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_50cols.csv"

df = pd.read_csv(csv_file, encoding='utf-8-sig')

print("="*80)
print("カンボジア語 元CSV分析")
print("="*80)

print(f"\n総行数: {len(df)}")
print(f"総列数: {len(df.columns)}")

# 各列のデータ数を確認
print(f"\n各列のデータ数:")
col_data = []
for i, col in enumerate(df.columns):
    non_empty = df[col].notna() & (df[col] != '')
    count = non_empty.sum()
    col_data.append({
        'index': i,
        'column': col,
        'count': count,
        'ratio': count / len(df) * 100
    })

# データ数が多い順にソート
col_data_sorted = sorted(col_data, key=lambda x: x['count'], reverse=True)

print(f"\nデータ数TOP 20列:")
for item in col_data_sorted[:20]:
    try:
        print(f"  [{item['index']:2d}] データ {item['count']:3d}/{len(df)} ({item['ratio']:5.1f}%) - '{item['column']}'")
    except UnicodeEncodeError:
        print(f"  [{item['index']:2d}] データ {item['count']:3d}/{len(df)} ({item['ratio']:5.1f}%) - [表示エラー]")

# No.列とPage列を確認
print(f"\nNo.列の確認:")
if 'No.' in df.columns:
    no_col = df['No.']
    valid = no_col.notna() & (no_col != '')
    print(f"  有効データ: {valid.sum()}/{len(df)}")
    print(f"  ユニーク値: {no_col[valid].nunique()}")

if 'Page' in df.columns:
    page_col = df['Page']
    print(f"\nPage列の範囲: {page_col.min()} - {page_col.max()}")
    print(f"  ページ別行数:")
    page_counts = page_col.value_counts().sort_index()
    for page, count in page_counts.head(10).items():
        print(f"    Page {page}: {count}行")

# 翻訳らしき列を探す
print(f"\n翻訳候補列の詳細:")
translation_keywords = ['របក']

for col in df.columns:
    col_str = str(col)
    if any(keyword in col_str for keyword in translation_keywords):
        non_empty = df[col].notna() & (df[col] != '')
        count = non_empty.sum()

        try:
            print(f"\n列名: '{col}'")
        except UnicodeEncodeError:
            print(f"\n列名: [表示エラー]")

        print(f"  データ数: {count}/{len(df)} ({count/len(df)*100:.1f}%)")
        print(f"  データがあるページ:")

        if count > 0:
            pages_with_data = df[non_empty]['Page'].unique()
            print(f"    {sorted(pages_with_data)}")

            print(f"\n  サンプルデータ（最初の5件）:")
            sample_df = df[non_empty].head(5)
            for idx, row in sample_df.iterrows():
                page = row['Page']
                no = row['No.'] if 'No.' in df.columns else ''
                val = row[col]
                try:
                    print(f"    [{idx}] Page {page}, No.{no}: {str(val)[:50]}")
                except:
                    print(f"    [{idx}] Page {page}, No.{no}: [表示エラー]")

# 特定のページ（19ページ）を詳しく見る
print(f"\n{'='*80}")
print("Page 19の詳細分析")
print(f"{'='*80}")

page_19 = df[df['Page'] == 19]
print(f"\nPage 19の行数: {len(page_19)}")

if len(page_19) > 0:
    print(f"\nPage 19で空でない列:")
    for col in df.columns:
        if col in ['Page', 'Table']:
            continue
        non_empty = page_19[col].notna() & (page_19[col] != '')
        if non_empty.sum() > 0:
            try:
                print(f"  '{col}': {non_empty.sum()}件")
            except UnicodeEncodeError:
                print(f"  [表示エラー]: {non_empty.sum()}件")

print(f"\n{'='*80}")
print("分析完了")
print(f"{'='*80}")
