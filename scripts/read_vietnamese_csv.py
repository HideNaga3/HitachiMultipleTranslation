"""
ベトナム語のPDF抽出CSVを読み込んでヘッダーを確認
"""

import pandas as pd
import os

output_dir = 'output'

# ベトナム語のCSVファイルを探す
files = os.listdir(output_dir)
vietnamese_files = [f for f in files if 'ベトナム' in f and 'pdfplumber' in f and '最終' in f]

print("=" * 80)
print("ベトナム語のPDF抽出CSVファイル")
print("=" * 80)
print()

if not vietnamese_files:
    print("ベトナム語のPDF抽出CSVが見つかりませんでした")
    print()
    print("ベトナムを含むファイル:")
    vietnamese_all = [f for f in files if 'ベトナム' in f and f.endswith('.csv')]
    for f in vietnamese_all:
        print(f"  - {f}")
else:
    target_file = vietnamese_files[0]
    print(f"対象ファイル: {target_file}")
    print()

    csv_path = os.path.join(output_dir, target_file)

    # CSVを読み込み
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    print("=" * 80)
    print("CSVヘッダー（列名）")
    print("=" * 80)
    print()

    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")

    print()
    print(f"総列数: {len(df.columns)}")
    print(f"総行数: {len(df)}")
    print()

    # Page列とNo.列の確認
    has_page = 'Page' in df.columns
    has_no = 'No.' in df.columns
    has_table = 'Table' in df.columns

    print("=" * 80)
    print("重要列の確認")
    print("=" * 80)
    print()
    print(f"Page列: {'✓ あり' if has_page else '✗ なし'}")
    print(f"No.列: {'✓ あり' if has_no else '✗ なし'}")
    print(f"Table列: {'✓ あり' if has_table else '✗ なし'}")
    print()

    # 最初の10行を表示
    print("=" * 80)
    print("データサンプル（最初の10行）")
    print("=" * 80)
    print()

    # 主要列のみ表示
    display_cols = []
    if has_page:
        display_cols.append('Page')
    if has_table:
        display_cols.append('Table')
    if has_no:
        display_cols.append('No.')

    # 日本語列とベトナム語列を追加
    for col in df.columns:
        if '日本語' in col or 'ベトナム' in col:
            display_cols.append(col)

    if display_cols:
        print(df[display_cols].head(10).to_string(index=False))
    else:
        print("主要列が見つかりません。全列を表示:")
        print(df.head(3))

print()
print("=" * 80)
