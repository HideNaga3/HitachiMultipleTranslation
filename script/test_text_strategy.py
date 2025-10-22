# -*- coding: utf-8 -*-
"""
Text戦略で抽出した内容を詳しく確認
"""

import pdfplumber
import pandas as pd

pdf_path = '建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

print("="*80)
print("Text戦略での抽出内容確認")
print("="*80)

table_settings = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text"
}

with pdfplumber.open(pdf_path) as pdf:
    # 1ページ目
    page = pdf.pages[0]

    tables = page.extract_tables(table_settings=table_settings)

    if tables:
        table = tables[0]

        print(f"\nテーブル構造:")
        print(f"  行数: {len(table)}")
        print(f"  列数: {len(table[0])}")

        # ヘッダー
        print(f"\nヘッダー行:")
        for col_idx, header in enumerate(table[0]):
            header_str = str(header) if header else "[None]"
            try:
                print(f"  列{col_idx}: '{header_str}'")
            except UnicodeEncodeError:
                print(f"  列{col_idx}: [カンボジア語]")

        # 最初の10データ行
        print(f"\nデータ行（No.1-10）:")
        for row_idx in range(1, min(11, len(table))):
            row = table[row_idx]

            print(f"\n  行{row_idx}:")
            for col_idx, val in enumerate(row):
                if val and val.strip():
                    val_str = str(val).strip()
                    try:
                        print(f"    列{col_idx}: '{val_str}'")
                    except UnicodeEncodeError:
                        print(f"    列{col_idx}: [カンボジア語データ]")

# DataFrameに変換して確認
print(f"\n{'='*80}")
print("DataFrame変換後")
print(f"{'='*80}")

with pdfplumber.open(pdf_path) as pdf:
    all_tables = []

    for page_num, page in enumerate(pdf.pages[:3], start=1):  # 最初の3ページ
        tables = page.extract_tables(table_settings=table_settings)

        if tables:
            for table_num, table in enumerate(tables, 1):
                if table and len(table) > 0:
                    # ヘッダー
                    headers = [str(h) if h is not None else f"Column_{i}"
                               for i, h in enumerate(table[0])]

                    # DataFrame作成
                    df = pd.DataFrame(table[1:], columns=headers)
                    df.insert(0, 'Page', page_num)
                    df.insert(1, 'Table', table_num)

                    all_tables.append(df)

    if all_tables:
        # 列名を一意にする
        for i, df in enumerate(all_tables):
            column_counts = {}
            new_columns = []
            for col in df.columns:
                if col in column_counts:
                    column_counts[col] += 1
                    new_col = f"{col}_{column_counts[col]}"
                else:
                    column_counts[col] = 1
                    new_col = col
                new_columns.append(new_col)
            all_tables[i].columns = new_columns

        # 統合
        combined_df = pd.concat(all_tables, ignore_index=True)

        print(f"\n統合結果:")
        print(f"  総行数: {len(combined_df)}")
        print(f"  総列数: {len(combined_df.columns)}")

        print(f"\n列名:")
        for i, col in enumerate(combined_df.columns):
            try:
                print(f"  {i}: '{col}'")
            except UnicodeEncodeError:
                print(f"  {i}: [カンボジア語列名]")

        # No.列を確認
        if 'No.' in combined_df.columns:
            no_valid = combined_df['No.'].notna() & (combined_df['No.'] != '')
            print(f"\nNo.列:")
            print(f"  有効データ: {no_valid.sum()}/{len(combined_df)}")

        # 翻訳らしき列を探す
        print(f"\n各列のデータ数:")
        for col in combined_df.columns:
            if col in ['Page', 'Table']:
                continue

            non_empty = combined_df[col].notna() & (combined_df[col] != '')
            count = non_empty.sum()
            ratio = count / len(combined_df) * 100

            try:
                print(f"  '{col}': {count}/{len(combined_df)} ({ratio:.1f}%)")
            except UnicodeEncodeError:
                print(f"  [カンボジア語列]: {count}/{len(combined_df)} ({ratio:.1f}%)")

print(f"\n{'='*80}")
print("完了")
print(f"{'='*80}")
