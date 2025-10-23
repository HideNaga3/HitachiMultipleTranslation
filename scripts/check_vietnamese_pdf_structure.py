"""
ベトナム語のPDF抽出CSV（最終版）の構造を確認するスクリプト
"""

import pandas as pd
import sys

# 出力先をファイルに変更
output_file = 'for_claude/vietnamese_pdf_structure.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

# ベトナム語のPDF抽出CSVを読み込み
csv_path = 'output/intermediate/ベトナム語_pdfplumber_抽出_最終版.csv'

print("=" * 80)
print("ベトナム語 PDF抽出CSV（最終版）の構造")
print("=" * 80)
print()
print(f"ファイル: {csv_path}")
print()

# CSVを読み込み
df = pd.read_csv(csv_path, encoding='utf-8-sig')

# 基本情報
print("=" * 80)
print("基本情報")
print("=" * 80)
print()
print(f"総行数: {len(df)}")
print(f"総列数: {len(df.columns)}")
print()

# 列名一覧
print("=" * 80)
print("列名一覧")
print("=" * 80)
print()
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")
print()

# Page列とNo.列の確認
has_page = 'Page' in df.columns
has_no = 'No.' in df.columns
has_bangou = '番号' in df.columns
has_table = 'Table' in df.columns

print("=" * 80)
print("重要列の存在確認")
print("=" * 80)
print()
print(f"  Page列  : {'✓ あり' if has_page else '✗ なし'}")
print(f"  No.列   : {'✓ あり' if has_no else '✗ なし'}")
print(f"  番号列  : {'✓ あり' if has_bangou else '✗ なし'}")
print(f"  Table列 : {'✓ あり' if has_table else '✗ なし'}")
print()

# データサンプル（最初の10行）
print("=" * 80)
print("データサンプル（最初の10行）")
print("=" * 80)
print()

# 主要列を選択して表示
display_cols = []
if has_page:
    display_cols.append('Page')
if has_table:
    display_cols.append('Table')
if has_no:
    display_cols.append('No.')
elif has_bangou:
    display_cols.append('番号')

# 単語列と翻訳列を追加
if '単語' in df.columns:
    display_cols.append('単語')
if '翻訳' in df.columns:
    display_cols.append('翻訳')

if display_cols:
    print(df[display_cols].head(10).to_string(index=False))
else:
    print("主要列が見つかりません。全列の最初の3行:")
    print(df.head(3))

print()

# Pageと番号の統計情報
if has_page and (has_no or has_bangou):
    print("=" * 80)
    print("Page列と番号列の統計情報")
    print("=" * 80)
    print()
    print(f"  Page範囲: {df['Page'].min()} ～ {df['Page'].max()}")
    print(f"  Page数  : {df['Page'].nunique()} ページ")

    no_col = 'No.' if has_no else '番号'
    print(f"  {no_col}範囲 : {df[no_col].min()} ～ {df[no_col].max()}")
    print()

    # Page別の番号の分布（最初の5ページ）
    print(f"  Page別の{no_col}範囲（最初の5ページ）:")
    for page in sorted(df['Page'].unique())[:5]:
        page_data = df[df['Page'] == page]
        print(f"    Page {page}: {no_col} {page_data[no_col].min()} ～ {page_data[no_col].max()} ({len(page_data)} 行)")
    print()

print("=" * 80)

sys.stdout.close()
print(f"結果を {output_file} に保存しました", file=sys.__stdout__)
