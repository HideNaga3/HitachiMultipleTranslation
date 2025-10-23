# PDFから表を抽出するスクリプト（改善版v2）
# 表の1行目を判定して、単語リストの表のみを抽出する

import pdfplumber
import pandas as pd
import os
from pathlib import Path

def is_valid_word_table(table):
    """
    表が有効な単語リストかどうかを判定する関数

    Args:
        table: pdfplumberで抽出した表データ（2次元リスト）

    Returns:
        bool: 有効な単語リストの表であればTrue
    """
    if not table or len(table) == 0:
        return False

    # 1行目（ヘッダー行）を確認
    first_row = table[0]

    # Noneを除外して文字列に変換
    first_row_str = [str(cell).strip() if cell is not None else '' for cell in first_row]

    # "No." 列が存在するかチェック（ベトナム語の「Số」も含む）
    has_no_column = any('No.' in cell or 'No' == cell or 'Số' in cell for cell in first_row_str)

    # 極端に列数が少ない表は除外（説明文ページなど）
    if len(first_row) < 5:
        return False

    # 1行目がほとんど空の場合は除外
    non_empty_cells = [cell for cell in first_row_str if cell != '' and cell != 'None']
    if len(non_empty_cells) < 3:
        return False

    # "No."列が存在する表のみを有効とする
    return has_no_column


def extract_tables_from_pdf(pdf_path):
    """
    PDFファイルから単語リストの表のみを抽出する関数

    Args:
        pdf_path: PDFファイルのパス

    Returns:
        tuple: (結合されたDataFrame, 総表数, 有効表数)
    """
    all_tables = []
    total_table_count = 0
    valid_table_count = 0

    with pdfplumber.open(pdf_path) as pdf:
        print(f"総ページ数: {len(pdf.pages)}")

        for page_number, page in enumerate(pdf.pages, 1):
            print(f"ページ {page_number}/{len(pdf.pages)} を処理中...")

            # 1ページから複数の表を抽出
            tables = page.extract_tables()

            if tables:
                for table_number, table in enumerate(tables, 1):
                    total_table_count += 1

                    # 空行を除外
                    table = [record for record in table if any(field is not None and str(field).strip() != '' for field in record)]

                    # 有効な単語リストの表かどうかを判定
                    if is_valid_word_table(table):
                        valid_table_count += 1
                        print(f"  表 {table_number} を抽出 (行数: {len(table)}, 列数: {len(table[0]) if table else 0})")

                        # 1行目をヘッダーとしてDataFrame化
                        if len(table) > 1:
                            # ヘッダーのNone値を "Column_X" に置き換え
                            headers = []
                            for i, col in enumerate(table[0]):
                                if col is None or str(col).strip() == '' or str(col).strip() == 'None':
                                    headers.append(f'Column_{i}')
                                else:
                                    headers.append(str(col).strip())

                            # データフレーム作成
                            df = pd.DataFrame(table[1:], columns=headers)

                            # ページ番号と表番号を追加
                            df.insert(0, 'PDFページ番号', page_number)
                            df.insert(1, 'PDF表番号', table_number)

                            all_tables.append(df)
                    else:
                        print(f"  表 {table_number} をスキップ（単語リストではない）")

    # 全ての有効な表を結合
    if all_tables:
        # 全ての列名を収集
        all_columns = set()
        for df in all_tables:
            all_columns.update(df.columns)

        all_columns = sorted(list(all_columns))

        # 各DataFrameを統一された列構成に変換
        normalized_tables = []
        for df in all_tables:
            # 不足している列を空文字列で埋める
            for col in all_columns:
                if col not in df.columns:
                    df[col] = ''

            # 列順を統一
            df = df[all_columns]
            normalized_tables.append(df)

        # 結合
        result_df = pd.concat(normalized_tables, ignore_index=True)

        return result_df, total_table_count, valid_table_count
    else:
        return None, total_table_count, valid_table_count


def main():
    """メイン処理"""
    # PDFファイルが格納されているフォルダ
    pdf_folder = '建設関連PDF'
    output_folder = 'output'

    # 出力フォルダが存在しない場合は作成
    os.makedirs(output_folder, exist_ok=True)

    # PDFファイルを取得
    pdf_files = list(Path(pdf_folder).glob('*.pdf'))

    print(f"処理対象のPDFファイル数: {len(pdf_files)}\n")

    # 各PDFファイルを処理
    for pdf_file in pdf_files:
        print("=" * 60)
        print(f"PDFファイルを読み込み中: {pdf_file}")
        print("=" * 60)

        # 表を抽出
        df, total_count, valid_count = extract_tables_from_pdf(str(pdf_file))

        if df is not None and not df.empty:
            # 出力ファイル名を生成
            base_name = pdf_file.stem  # 拡張子を除いたファイル名
            col_count = len(df.columns)
            output_file = os.path.join(output_folder, f'{base_name}_{col_count}cols.csv')

            # CSVファイルに保存（UTF-8 BOM）
            df.to_csv(output_file, index=False, encoding='utf-8-sig')

            print(f"\n完了!")
            print(f"  総表数: {total_count}")
            print(f"  有効表数: {valid_count}")
            print(f"  除外表数: {total_count - valid_count}")
            print(f"  総行数: {len(df)}")
            print(f"  列数: {col_count}")
            print(f"  出力ファイル: {output_file}")
        else:
            print(f"\n警告: 有効な表が見つかりませんでした")
            print(f"  総表数: {total_count}")
            print(f"  有効表数: {valid_count}")

        print("=" * 60)
        print()


if __name__ == '__main__':
    main()
