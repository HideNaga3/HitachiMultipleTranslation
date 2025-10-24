"""
ベトナム語のPDF抽出CSVを確認し、Page列とNo.列があるか確認するスクリプト
"""

import pandas as pd
import os
import sys

# 出力先をファイルに変更
output_file = 'for_claude/vietnamese_pdf_structure.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

# ベトナム語のPDF抽出CSVファイルを探す
output_dir = 'output'
csv_files = [f for f in os.listdir(output_dir) if 'ベトナム' in f and f.endswith('.csv')]

print("=" * 80)
print("ベトナム語のPDF抽出CSVファイル")
print("=" * 80)
print()

if not csv_files:
    print("ベトナム語のCSVファイルが見つかりませんでした")
    sys.stdout.close()
    sys.exit(1)

print(f"見つかったファイル数: {len(csv_files)}")
print()

for csv_file in csv_files:
    print(f"- {csv_file}")

print()

# 最終版のファイルを選択
target_file = None
for f in csv_files:
    if '最終' in f or 'pdfplumber' in f:
        target_file = f
        break

if not target_file:
    target_file = csv_files[0]

csv_path = os.path.join(output_dir, target_file)

print("=" * 80)
print(f"確認するファイル: {target_file}")
print("=" * 80)
print()

# CSVを読み込み
df = pd.read_csv(csv_path, encoding='utf-8-sig')

# 列名を表示
print("列名:")
print("-" * 80)
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print()
print(f"総列数: {len(df.columns)}")
print(f"総行数: {len(df)}")
print()

# Page列とNo.列があるか確認
has_page = 'Page' in df.columns or 'ページ' in df.columns
has_no = 'No.' in df.columns or '番号' in df.columns or 'No' in df.columns

print("=" * 80)
print("重要列の確認")
print("=" * 80)
print()
print(f"Page列: {'✓ あり' if has_page else '✗ なし'}")
print(f"No.列: {'✓ あり' if has_no else '✗ なし'}")
print()

# 最初の10行を表示（列が多い場合は主要列のみ）
print("=" * 80)
print("データサンプル（最初の10行）")
print("=" * 80)
print()

# 表示する列を選択
display_cols = []
if has_page:
    page_col = 'Page' if 'Page' in df.columns else 'ページ'
    display_cols.append(page_col)
if has_no:
    no_col = [c for c in df.columns if 'No' in c or '番号' in c][0]
    display_cols.append(no_col)

# 日本語列を探す
ja_cols = [c for c in df.columns if '日本語' in c or 'ja' in c.lower()]
if ja_cols:
    display_cols.append(ja_cols[0])

# ベトナム語列を探す
vi_cols = [c for c in df.columns if 'ベトナム' in c or 'vi' in c.lower() or 'Việt' in c]
if vi_cols:
    display_cols.append(vi_cols[0])

if display_cols:
    print(df[display_cols].head(10).to_string(index=False))
else:
    print("主要列が見つからないため、全列を表示:")
    print(df.head(10))

print()

# PageとNo.でソートした場合のサンプル
if has_page and has_no:
    print("=" * 80)
    print("PageとNo.でソート後のサンプル")
    print("=" * 80)
    print()

    page_col = 'Page' if 'Page' in df.columns else 'ページ'
    no_col = [c for c in df.columns if 'No' in c or '番号' in c][0]

    df_sorted = df.sort_values([page_col, no_col])
    print(df_sorted[display_cols].head(10).to_string(index=False))
    print()

print("=" * 80)

# ファイルを閉じる
sys.stdout.close()
print("結果を for_claude/vietnamese_pdf_structure.txt に保存しました", file=sys.__stdout__)
