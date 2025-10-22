# -*- coding: utf-8 -*-
"""
PDFから表を抽出してCSVに保存するスクリプト

使用方法:
    python extract_tables_from_pdf.py

必要なライブラリ:
    - pdfplumber
    - pandas
    - openpyxl
"""

import pdfplumber
import pandas as pd
from pathlib import Path
import os

def extract_tables_from_pdf(pdf_path, output_dir="output"):
    """
    PDFファイルから表を抽出してCSVに保存

    Args:
        pdf_path (str): PDFファイルのパス
        output_dir (str): 出力ディレクトリ
    """
    # 出力ディレクトリを作成
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # PDFファイル名を取得（拡張子なし）
    pdf_filename = Path(pdf_path).stem

    # 全ページの表データを格納するリスト
    all_tables = []
    max_columns = 0

    print(f"PDFファイルを読み込み中: {pdf_path}")

    # PDFを開いて表を抽出
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"総ページ数: {total_pages}")

        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"ページ {page_num}/{total_pages} を処理中...")

            # ページから表を抽出
            tables = page.extract_tables()

            if tables:
                for table_num, table in enumerate(tables, start=1):
                    if table and len(table) > 0:
                        # ヘッダー行を取得し、Noneを文字列に変換
                        headers = [str(h) if h is not None else f"Column_{i}"
                                   for i, h in enumerate(table[0])]

                        # DataFrameに変換
                        df = pd.DataFrame(table[1:], columns=headers)

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

    # 全ての表を統合（列数の違いを許容）
    print("\n全ての表を統合中...")

    # すべての列名を収集
    all_columns = set()
    for df in all_tables:
        all_columns.update(df.columns)

    # 各DataFrameに不足している列を追加（空文字列で埋める）
    for i, df in enumerate(all_tables):
        for col in all_columns:
            if col not in df.columns:
                df[col] = ""
        # 列の順序を統一
        all_tables[i] = df[sorted(all_columns)]

    # 統合
    combined_df = pd.concat(all_tables, ignore_index=True)

    # CSVファイル名を生成（PDFファイル名_列数cols.csv）
    csv_filename = f"{pdf_filename}_{len(all_columns)}cols.csv"
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
    # PDFファイルのパスを指定
    pdf_files = [
        "建設関連PDF/【全課統合版】英語_げんばのことば_建設関連職種.pdf",
        "建設関連PDF/【全課統合版】タガログ語_げんばのことば_建設関連職種.pdf",
        "建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf",
        "建設関連PDF/【全課統合版】中国語_げんばのことば_建設関連職種.pdf",
        "建設関連PDF/【全課統合版】インドネシア語_げんばのことば_建設関連職種.pdf",
        "建設関連PDF/【全課統合版】ミャンマー語_げんばのことば_建設関連職種.pdf",
        "建設関連PDF/【全課統合版】タイ語_げんばのことば_建設関連職種.pdf",
        "建設関連PDF/【全課統合版】ベトナム語_げんばのことば_建設関連職種.pdf",
    ]

    # 各PDFファイルを処理
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"\n{'='*60}")
            extract_tables_from_pdf(pdf_file)
            print(f"{'='*60}\n")
        else:
            print(f"警告: ファイルが見つかりません - {pdf_file}")

if __name__ == "__main__":
    main()
