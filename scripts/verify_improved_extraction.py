# -*- coding: utf-8 -*-
"""
改善版抽出CSVの翻訳データを確認
"""

import pandas as pd

languages = [
    {'name': 'カンボジア語', 'file': 'output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_improved_56cols.csv', 'keywords': ['របក']},
    {'name': 'タイ語', 'file': 'output/【全課統合版】タイ語_げんばのことば_建設関連職種_improved_49cols.csv', 'keywords': ['แปล', 'คา']},
]

print("="*80)
print("改善版抽出CSV - 翻訳データ確認")
print("="*80)

for lang_info in languages:
    lang = lang_info['name']
    csv_file = lang_info['file']
    keywords = lang_info['keywords']

    print(f"\n{'='*80}")
    print(f"{lang}")
    print(f"{'='*80}")

    df = pd.read_csv(csv_file, encoding='utf-8-sig')

    print(f"\n総行数: {len(df)}")
    print(f"総列数: {len(df.columns)}")

    # No.列を確認
    if 'No.' in df.columns:
        no_valid = df['No.'].notna() & (df['No.'] != '')
        print(f"\nNo.列の有効データ: {no_valid.sum()}/{len(df)}")

    # 翻訳列を探す
    translation_cols = []
    for col in df.columns:
        col_str = str(col)
        if any(keyword in col_str for keyword in keywords):
            translation_cols.append(col)

    print(f"\n翻訳候補列: {len(translation_cols)}個")

    for col in translation_cols:
        non_empty = df[col].notna() & (df[col] != '')
        count = non_empty.sum()
        ratio = count / len(df) * 100

        try:
            print(f"\n列: '{col}'")
        except UnicodeEncodeError:
            print(f"\n列: [カンボジア語/タイ語]")

        print(f"  データ数: {count}/{len(df)} ({ratio:.1f}%)")

        if count > 0:
            print(f"  サンプル（最初の5件）:")
            sample_indices = df[non_empty].head(5).index
            for idx in sample_indices:
                page = df.loc[idx, 'Page'] if 'Page' in df.columns else '?'
                no = df.loc[idx, 'No.'] if 'No.' in df.columns else '?'
                val = df.loc[idx, col]
                try:
                    print(f"    Page {page}, No.{no}: {str(val)[:50]}")
                except:
                    print(f"    Page {page}, No.{no}: [カンボジア語/タイ語データ]")

print(f"\n{'='*80}")
print("確認完了")
print(f"{'='*80}")
