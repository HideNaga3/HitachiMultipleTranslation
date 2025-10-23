"""タイ語とカンボジア語のCSVファイルの列名と翻訳列データを調査"""
import pandas as pd
import glob
import os
import sys

# 出力をUTF-8ファイルにリダイレクト
sys.stdout = open('for_claude/thai_khmer_investigation.txt', 'w', encoding='utf-8')

def investigate_csv(filepath):
    """CSVファイルの列名と翻訳列データを調査"""
    print(f"\n{'='*80}")
    print(f"ファイル: {os.path.basename(filepath)}")
    print(f"{'='*80}")

    # CSVを読み込み
    df = pd.read_csv(filepath, encoding='utf-8-sig')

    # 基本情報
    print(f"\n総行数: {len(df)}")
    print(f"総列数: {len(df.columns)}")

    # 列名をすべて表示（Unicodeコードポイントも表示）
    print(f"\n【列名一覧】")
    for i, col in enumerate(df.columns):
        unicode_repr = ''.join([f'U+{ord(c):04X}' for c in col])
        print(f"  {i}: '{col}'")
        print(f"      Unicode: {unicode_repr}")

    # 翻訳列と思われる列を検出
    print(f"\n【翻訳列の候補検出】")
    translation_candidates = []
    for col in df.columns:
        # タイ語の翻訳列: คา แปล, คำแปล, など
        # カンボジア語の翻訳列: កា បក្ប្រប, カーバクプローブ など
        if 'แปล' in col or 'បក្' in col or 'translation' in col.lower() or '翻訳' in col:
            translation_candidates.append(col)
            print(f"  候補: '{col}'")

    # 各翻訳候補列のデータ状況を確認
    print(f"\n【翻訳列のデータ状況】")
    for col in translation_candidates:
        non_empty = df[col].notna().sum()
        empty = df[col].isna().sum()
        total = len(df)
        print(f"\n  列名: '{col}'")
        print(f"    データあり: {non_empty}行 ({non_empty/total*100:.1f}%)")
        print(f"    空欄: {empty}行 ({empty/total*100:.1f}%)")
        print(f"    サンプル（最初の5つの非空値）:")
        sample_values = df[col].dropna().head(5).tolist()
        for j, val in enumerate(sample_values, 1):
            print(f"      {j}. {val}")

# タイ語CSVを調査
print("\n" + "="*80)
print("タイ語CSVの調査")
print("="*80)

thai_files = glob.glob("output/*タイ語*.csv")
if thai_files:
    for f in thai_files:
        investigate_csv(f)
else:
    print("タイ語CSVファイルが見つかりません")

# カンボジア語CSVを調査
print("\n" + "="*80)
print("カンボジア語CSVの調査")
print("="*80)

khmer_files = glob.glob("output/*カンボジア*.csv")
if khmer_files:
    for f in khmer_files:
        investigate_csv(f)
else:
    print("カンボジア語CSVファイルが見つかりません")
