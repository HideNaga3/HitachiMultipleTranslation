# -*- coding: utf-8 -*-
"""
元のoutputフォルダのCSVで翻訳データを確認
"""

import pandas as pd
from pathlib import Path
import glob

print("="*80)
print("元の抽出CSV - 翻訳列確認")
print("="*80)

# outputフォルダの全CSVファイルを取得
csv_files = glob.glob("output/*.csv")

for csv_file in sorted(csv_files):
    filename = Path(csv_file).name

    # 言語名を抽出
    if 'カンボジア語' in filename:
        lang = 'カンボジア語'
    elif 'タイ語' in filename:
        lang = 'タイ語'
    else:
        continue  # カンボジア語とタイ語のみチェック

    print(f"\n{'='*80}")
    print(f"ファイル: {filename}")
    print(f"言語: {lang}")
    print(f"{'='*80}")

    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig')

        print(f"\n列名 ({len(df.columns)}列):")
        for i, col in enumerate(df.columns, 1):
            # 各列のデータ数を確認
            non_empty = df[col].notna() & (df[col] != '')
            count = non_empty.sum()
            print(f"  {i:2d}. データあり {count:4d}/{len(df):4d} 行")

        # 翻訳らしき列を探す
        print(f"\n列名の詳細:")
        for i, col in enumerate(df.columns, 1):
            col_lower = str(col).lower()
            is_translation = any(keyword in col_lower for keyword in [
                'translation', 'terjemahan', 'pagsasalin', 'dịch',
                'ဘာသာ', '词意', '中文', 'របក', 'แปล', '译'
            ]) or 'ြန' in col

            non_empty = df[col].notna() & (df[col] != '')
            count = non_empty.sum()

            mark = " ← 翻訳候補!" if is_translation else ""

            try:
                print(f"  {i:2d}. '{col}' (データ: {count}/{len(df)}){mark}")
            except UnicodeEncodeError:
                print(f"  {i:2d}. [表示エラー] (データ: {count}/{len(df)}){mark}")

            # サンプルデータ
            if is_translation and count > 0:
                print(f"       サンプル:")
                for idx in df[non_empty].index[:3]:
                    val = df[col].iloc[idx]
                    try:
                        print(f"         [{idx}] {str(val)[:40]}")
                    except:
                        print(f"         [{idx}] [表示エラー]")

    except Exception as e:
        print(f"エラー: {e}")

print(f"\n{'='*80}")
print("確認完了")
print(f"{'='*80}")
