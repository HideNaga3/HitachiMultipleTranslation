# -*- coding: utf-8 -*-
"""
カンボジア語PDF全ページでテスト
"""

import pdfplumber
import pandas as pd
import os

def test_full_extraction(pdf_path, lang, table_settings=None):
    """
    全ページで抽出テスト

    Args:
        pdf_path: PDFファイルのパス
        lang: 言語名
        table_settings: pdfplumberのtable_settings
    """
    print(f"\n全ページテスト: {lang}")

    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"  総ページ数: {total_pages}")

        for page_num, page in enumerate(pdf.pages, start=1):
            if page_num % 10 == 0:
                print(f"  処理中: {page_num}/{total_pages}...")

            # テーブル抽出
            if table_settings:
                tables = page.extract_tables(table_settings=table_settings)
            else:
                tables = page.extract_tables()

            if tables:
                for table_num, table in enumerate(tables, start=1):
                    if table and len(table) > 0:
                        headers = [str(h) if h is not None else f"Column_{i}"
                                   for i, h in enumerate(table[0])]

                        df = pd.DataFrame(table[1:], columns=headers)
                        df.insert(0, 'Page', page_num)
                        df.insert(1, 'Table', table_num)

                        all_tables.append(df)

    if not all_tables:
        print("  エラー: テーブルが見つかりませんでした")
        return

    # 各DataFrameの列名を一意にする
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

    # すべての列名を収集
    all_columns = set()
    for df in all_tables:
        all_columns.update(df.columns)

    # 各DataFrameに不足している列を追加
    for i, df in enumerate(all_tables):
        for col in all_columns:
            if col not in df.columns:
                df[col] = ""
        all_tables[i] = df[sorted(all_columns)]

    # 統合
    combined_df = pd.concat(all_tables, ignore_index=True)

    # 翻訳データをカウント
    translation_keywords = {
        'カンボジア語': ['របក'],
        'タイ語': ['แปล', 'คา']
    }

    keywords = translation_keywords.get(lang, [])
    translation_count = 0

    for col in combined_df.columns:
        col_str = str(col)
        if any(keyword in col_str for keyword in keywords):
            non_empty = combined_df[col].notna() & (combined_df[col] != '')
            count = non_empty.sum()
            try:
                print(f"\n  翻訳候補列: '{col}'")
            except UnicodeEncodeError:
                print(f"\n  翻訳候補列: [表示エラー]")
            print(f"    データ数: {count}")
            if count > 0:
                print(f"    サンプル:")
                sample_indices = combined_df[non_empty].index[:3]
                for idx in sample_indices:
                    val = combined_df[col].iloc[idx]
                    page = combined_df['Page'].iloc[idx]
                    try:
                        print(f"      Page {page}: {str(val)[:40]}")
                    except:
                        print(f"      Page {page}: [表示エラー]")
            translation_count = max(translation_count, count)

    # No.列でフィルタ
    if 'No.' in combined_df.columns:
        valid_rows = combined_df['No.'].notna() & (combined_df['No.'] != '')
        valid_count = valid_rows.sum()
    else:
        valid_count = len(combined_df)

    print(f"\n  結果:")
    print(f"    総テーブル数: {len(all_tables)}")
    print(f"    総行数: {len(combined_df)}")
    print(f"    有効行数: {valid_count}")
    print(f"    総列数: {len(all_columns)}")
    print(f"    翻訳データ: {translation_count}/{valid_count} ({translation_count/valid_count*100:.1f}%)")

    return combined_df

def main():
    """メイン処理"""

    print("="*80)
    print("カンボジア語PDF 全ページ抽出テスト")
    print("="*80)

    pdf_path = '建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

    if not os.path.exists(pdf_path):
        print(f"エラー: ファイルが見つかりません - {pdf_path}")
        return

    # デフォルト設定でテスト
    print("\n【デフォルト設定】")
    df_default = test_full_extraction(pdf_path, 'カンボジア語')

    print(f"\n{'='*80}")
    print("完了")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
