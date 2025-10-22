# -*- coding: utf-8 -*-
"""
改善版：Text戦略を使用してPDFから表を抽出

特徴:
- Text戦略で列を正しく検出
- ヘッダー行を自動検出（"No."を含む行）
- カンボジア語・タイ語の翻訳データも正しく抽出
"""

import pdfplumber
import pandas as pd
from pathlib import Path
import os

def find_header_row(table):
    """
    テーブルからヘッダー行を探す

    Args:
        table: pdfplumberで抽出したテーブル

    Returns:
        int: ヘッダー行のインデックス（見つからない場合は0）
    """
    for row_idx, row in enumerate(table):
        # "No."を含む行を探す
        for cell in row:
            if cell and 'No.' in str(cell):
                return row_idx

    return 0

def extract_tables_from_pdf_improved(pdf_path, output_dir="output"):
    """
    改善版：PDFファイルから表を抽出してCSVに保存

    Args:
        pdf_path (str): PDFファイルのパス
        output_dir (str): 出力ディレクトリ
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    pdf_filename = Path(pdf_path).stem

    # Text戦略を使用
    table_settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "text"
    }

    all_tables = []
    max_columns = 0

    print(f"PDFファイルを読み込み中: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"総ページ数: {total_pages}")

        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"ページ {page_num}/{total_pages} を処理中...")

            # Text戦略でテーブル抽出
            tables = page.extract_tables(table_settings=table_settings)

            if tables:
                for table_num, table in enumerate(tables, start=1):
                    if table and len(table) > 0:
                        # ヘッダー行を探す
                        header_row_idx = find_header_row(table)

                        if header_row_idx >= len(table) - 1:
                            # ヘッダー行しかない、またはデータ行がない
                            continue

                        # ヘッダー行を取得
                        headers = table[header_row_idx]
                        headers = [str(h) if h is not None and h != '' else f"Column_{i}"
                                   for i, h in enumerate(headers)]

                        # データ行を取得（ヘッダー行の次の行から）
                        data_rows = table[header_row_idx + 1:]

                        # 空行をスキップ
                        data_rows = [row for row in data_rows if any(cell and str(cell).strip() for cell in row)]

                        if not data_rows:
                            continue

                        # DataFrameに変換
                        df = pd.DataFrame(data_rows, columns=headers)

                        # 列数を記録
                        current_cols = len(df.columns)
                        if current_cols > max_columns:
                            max_columns = current_cols

                        # ページ番号と表番号を追加
                        df.insert(0, 'Page', page_num)
                        df.insert(1, 'Table', table_num)

                        all_tables.append(df)
                        print(f"  表 {table_num} を抽出 (行数: {len(df)}, 列数: {current_cols})")

    if not all_tables:
        print("警告: 表が見つかりませんでした")
        return

    # 全ての表を統合
    print("\n全ての表を統合中...")

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

    # CSVファイル名を生成
    csv_filename = f"{pdf_filename}_improved_{len(all_columns)}cols.csv"
    csv_path = output_path / csv_filename

    # CSVに保存（UTF-8 BOM付き）
    print(f"\nCSVファイルに保存中: {csv_path}")
    combined_df.to_csv(csv_path, index=False, encoding='utf-8-sig')

    print(f"\n完了!")
    print(f"  総表数: {len(all_tables)}")
    print(f"  総行数: {len(combined_df)}")
    print(f"  総列数: {len(all_columns)}")
    print(f"  出力ファイル: {csv_path}")

    return csv_path

def main():
    """メイン処理"""
    # テスト：カンボジア語とタイ語のみ
    pdf_files = [
        "建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf",
        "建設関連PDF/【全課統合版】タイ語_げんばのことば_建設関連職種.pdf",
    ]

    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"\n{'='*80}")
            extract_tables_from_pdf_improved(pdf_file)
            print(f"{'='*80}\n")
        else:
            print(f"警告: ファイルが見つかりません - {pdf_file}")

if __name__ == "__main__":
    main()
