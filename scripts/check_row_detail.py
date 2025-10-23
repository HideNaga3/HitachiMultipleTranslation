# -*- coding: utf-8 -*-
"""
Page 1のNo.1の行を詳しく確認
"""

import pandas as pd

csv_file = "output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_improved_56cols.csv"

df = pd.read_csv(csv_file, encoding='utf-8-sig')

print("="*80)
print("Page 1 No.1の行 - 詳細確認")
print("="*80)

# Page 1 No.1を探す
target = df[(df['Page'] == 1) & (df['No.'] == 1.0)]

if len(target) > 0:
    row = target.iloc[0]

    print(f"\nPage 1, No.1の全列データ:")
    print(f"（期待値: No.=1, 単語=技能実習, 読み方=ぎのうじっしゅう, 翻訳=カンボジア語）")
    print()

    # 最初の30列を全て表示（空でも）
    for col_idx in range(min(30, len(df.columns))):
        col = df.columns[col_idx]
        val = row[col]

        if pd.notna(val) and val != '':
            try:
                val_str = str(val)
                print(f"  列{col_idx:2d} '{col}': {val_str}")
            except UnicodeEncodeError:
                print(f"  列{col_idx:2d} [カンボジア語列名]: [データあり]")
        else:
            try:
                print(f"  列{col_idx:2d} '{col}': [空]")
            except UnicodeEncodeError:
                print(f"  列{col_idx:2d} [カンボジア語列名]: [空]")

else:
    print("Page 1 No.1が見つかりません")

print(f"\n{'='*80}")
print("完了")
print(f"{'='*80}")
