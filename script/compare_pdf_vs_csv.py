# -*- coding: utf-8 -*-
"""
PDFの実際の内容と抽出CSVを比較
"""

import pandas as pd

# 抽出されたCSV
csv_file = "output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_50cols.csv"
df = pd.read_csv(csv_file, encoding='utf-8-sig')

print("="*80)
print("カンボジア語PDF vs 抽出CSV 比較")
print("="*80)

# Page 1のデータを確認
page_1 = df[df['Page'] == 1].copy()

print(f"\nPage 1の抽出データ:")
print(f"  総行数: {len(page_1)}")

# No. 1-6を確認
target_rows = page_1[page_1['No.'].isin([1, 2, 3, 4, 5, 6])]

print(f"\nNo.1-6のデータ:")
for idx, row in target_rows.iterrows():
    no = row['No.']
    print(f"\n--- No.{int(no)} (行{idx}) ---")

    # 空でない列を全て表示
    col_with_data = []
    for col_idx, col in enumerate(df.columns):
        if col in ['Page', 'Table']:
            continue

        val = row[col]
        if pd.notna(val) and val != '':
            col_with_data.append({
                'index': col_idx,
                'name': col,
                'value': val
            })

    print(f"  データがある列数: {len(col_with_data)}")
    for item in col_with_data:
        try:
            val_str = str(item['value'])[:50]
            print(f"    列[{item['index']:2d}] '{item['name']}': {val_str}")
        except UnicodeEncodeError:
            print(f"    列[{item['index']:2d}] [表示エラー]: [データあり]")

# 期待される構造（画像から）
print(f"\n{'='*80}")
print("期待されるデータ（画像から）")
print(f"{'='*80}")

expected_data = [
    {"No": 1, "単語": "技能実習", "読み方": "ぎのうじっしゅう", "翻訳": "ការប្រយិត្តិក្បណ្យជះប្រយុ（カンボジア語）"},
    {"No": 2, "単語": "技能実習生", "読み方": "ぎのうじっしゅうせい", "翻訳": "កម្សិក្បការប្រយិត្តិប្រវែនជះប្រយុ（カンボジア語）"},
    {"No": 3, "単語": "工場", "読み方": "こうじょう", "翻訳": "រោងចក（カンボジア語）"},
    {"No": 4, "単語": "製造", "読み方": "せいぞう", "翻訳": "ការផលិត（カンボジア語）"},
    {"No": 5, "単語": "機械", "読み方": "きかい", "翻訳": "ម៉ាស៊ីន（カンボジア語）"},
    {"No": 6, "単語": "安全", "読み方": "あんぜん", "翻訳": "សុវត្ថិភាព（カンボジア語）"},
]

for item in expected_data:
    print(f"\n  No.{item['No']}:")
    print(f"    単語: {item['単語']}")
    print(f"    読み方: {item['読み方']}")
    print(f"    翻訳: {item['翻訳']}")

print(f"\n{'='*80}")
print("問題: 翻訳列（4列目）のデータが抽出されていない")
print(f"{'='*80}")
