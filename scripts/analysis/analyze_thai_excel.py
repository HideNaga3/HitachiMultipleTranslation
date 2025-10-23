"""タイ語Excelファイルの構造と内容を分析"""
import pandas as pd
import sys

# 出力をファイルにリダイレクト
sys.stdout = open('for_claude/thai_excel_analysis.txt', 'w', encoding='utf-8')

# Excelファイルのパス
excel_file = r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\temp_files\【全課統合版】タイ語_げんばのことば_建設関連職種.xlsx"

print("=" * 80)
print("タイ語Excelファイルの分析")
print("=" * 80)
print()

# Excelファイルのシート名を取得
xls = pd.ExcelFile(excel_file)
print(f"シート数: {len(xls.sheet_names)}")
print(f"シート名: {xls.sheet_names}")
print()

# 各シートを分析
for sheet_name in xls.sheet_names:
    print("=" * 80)
    print(f"シート: {sheet_name}")
    print("=" * 80)

    # シートを読み込み
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    print(f"行数: {len(df)}")
    print(f"列数: {len(df.columns)}")
    print()

    # 列名を表示
    print("列名一覧:")
    for i, col in enumerate(df.columns):
        print(f"  {i}: '{col}'")
    print()

    # 最初の5行を表示
    print("データサンプル（最初の5行）:")
    print(df.head(5).to_string())
    print()

    # 翻訳列と思われる列を検出
    translation_candidates = []
    for col in df.columns:
        if 'แปล' in str(col) or 'translation' in str(col).lower() or '翻訳' in str(col):
            translation_candidates.append(col)

    if translation_candidates:
        print("翻訳列の候補:")
        for col in translation_candidates:
            print(f"  - '{col}'")
            non_empty = df[col].notna().sum()
            total = len(df)
            print(f"    データあり: {non_empty}行 / {total}行 ({non_empty/total*100:.1f}%)")

            # サンプル値を表示
            sample_values = df[col].dropna().head(5).tolist()
            if sample_values:
                print(f"    サンプル値:")
                for j, val in enumerate(sample_values, 1):
                    print(f"      {j}. {val}")
        print()

print("=" * 80)
print("分析完了")
print("=" * 80)
