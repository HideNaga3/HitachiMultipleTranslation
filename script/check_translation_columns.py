# -*- coding: utf-8 -*-
"""
各言語のクリーンCSVで翻訳列の状態を確認するスクリプト
"""

import pandas as pd
from pathlib import Path

# 確認する言語
languages = [
    'カンボジア語',
    'タイ語',
    'ベトナム語',
    'ミャンマー語',
    '中国語',
    '英語',
    'インドネシア語',
    'タガログ語'
]

print("="*80)
print("各言語のクリーンCSV - 翻訳列確認")
print("="*80)

for lang in languages:
    filename = f"output_cleaned/{lang}_cleaned.csv"

    if not Path(filename).exists():
        print(f"\n❌ {lang}: ファイルが見つかりません")
        continue

    df = pd.read_csv(filename, encoding='utf-8-sig')

    print(f"\n{'='*80}")
    print(f"言語: {lang}")
    print(f"{'='*80}")

    print(f"\n列名一覧 ({len(df.columns)}列):")
    for i, col in enumerate(df.columns, 1):
        try:
            print(f"  {i:2d}. {col}")
        except UnicodeEncodeError:
            print(f"  {i:2d}. [表示エラー]")

    # 翻訳らしき列を探す
    translation_candidates = []
    for col in df.columns:
        col_lower = str(col).lower()
        if any(keyword in col_lower for keyword in [
            'translation', 'terjemahan', 'pagsasalin', 'dịch',
            'ဘာသာ', '词意', '中文', 'របក', 'แปล', '译'
        ]) or 'ြန' in col:
            translation_candidates.append(col)

    if translation_candidates:
        try:
            print(f"\n翻訳候補列: {translation_candidates}")
        except UnicodeEncodeError:
            print(f"\n翻訳候補列: {len(translation_candidates)}個")

        for col in translation_candidates:
            non_empty = df[col].notna() & (df[col] != '')
            count = non_empty.sum()
            try:
                print(f"\n  列「{col}」:")
            except UnicodeEncodeError:
                print(f"\n  列 [表示エラー]:")
            print(f"    データあり: {count}/{len(df)} 行")

            if count > 0:
                print(f"    サンプル（最初の3件）:")
                sample_data = df[non_empty][col].head(3)
                for idx, val in sample_data.items():
                    try:
                        print(f"      [{idx+1}] {str(val)[:50]}")
                    except:
                        print(f"      [{idx+1}] [表示エラー]")
    else:
        print(f"\n⚠️ 翻訳候補列が見つかりません")
        print(f"\n全列のサンプル（1行目）:")
        if len(df) > 0:
            for col in df.columns:
                val = df[col].iloc[0]
                if pd.notna(val) and val != '':
                    try:
                        print(f"  {col}: {str(val)[:30]}")
                    except UnicodeEncodeError:
                        print(f"  [表示エラー]: [表示エラー]")

print(f"\n{'='*80}")
print("確認完了")
print(f"{'='*80}")
