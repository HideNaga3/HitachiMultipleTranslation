"""
pdfplumberで全8言語のPDFからテーブルを抽出してCSVに出力
"""

import pdfplumber
import pandas as pd
from pathlib import Path
import re

# 設定
PDF_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\建設関連PDF")
OUTPUT_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\output")

OUTPUT_DIR.mkdir(exist_ok=True)

# 8言語のPDFファイル
PDF_FILES = [
    "【全課統合版】英語_げんばのことば_建設関連職種.pdf",
    "【全課統合版】タガログ語_げんばのことば_建設関連職種.pdf",
    "【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf",
    "【全課統合版】中国語_げんばのことば_建設関連職種.pdf",
    "【全課統合版】インドネシア語_げんばのことば_建設関連職種.pdf",
    "【全課統合版】ミャンマー語_げんばのことば_建設関連職種.pdf",
    "【全課統合版】タイ語_げんばのことば_建設関連職種.pdf",
    "【全課統合版】ベトナム語_げんばのことば_建設関連職種.pdf",
]


def extract_language_from_filename(filename):
    """ファイル名から言語を抽出"""
    match = re.search(r'【全課統合版】(.+?)_', filename)
    return match.group(1) if match else 'Unknown'


def extract_pdf_to_dataframe(pdf_path, pdf_file):
    """PDFからテーブルを抽出してDataFrameを返す"""

    language = extract_language_from_filename(pdf_file)
    print(f"\n{'='*80}")
    print(f"処理中: {language} - {pdf_file}")
    print(f"{'='*80}")

    all_data = []
    page_info = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"総ページ数: {total_pages}")

            for page_num in range(total_pages):
                page = pdf.pages[page_num]

                # ページからテーブルを抽出
                tables = page.extract_tables()

                if len(tables) == 0:
                    continue

                # 各テーブルを処理
                for table_idx, table in enumerate(tables):
                    if len(table) == 0:
                        continue

                    # ヘッダー行を探す（"No." または "Số" を含む行）
                    header_row_idx = None
                    for i, row in enumerate(table):
                        if any('No.' in str(cell) or 'Số' in str(cell) for cell in row if cell):
                            header_row_idx = i
                            break

                    if header_row_idx is None:
                        continue

                    # ヘッダー行を取得
                    header_row = table[header_row_idx]

                    # データ行を抽出（ヘッダー行の次の行から）
                    data_rows = table[header_row_idx + 1:]

                    if len(data_rows) == 0:
                        continue

                    # ページ情報を記録
                    page_info.append({
                        'page': page_num + 1,
                        'table': table_idx + 1,
                        'header_row': header_row_idx,
                        'data_rows': len(data_rows),
                        'columns': len(header_row)
                    })

                    # 各データ行にページ情報を追加
                    for row in data_rows:
                        # 行の長さをヘッダーと合わせる
                        if len(row) < len(header_row):
                            row.extend([''] * (len(header_row) - len(row)))
                        elif len(row) > len(header_row):
                            row = row[:len(header_row)]

                        # ページ番号とテーブル番号を追加
                        row_with_page = [page_num + 1, table_idx + 1] + row
                        all_data.append(row_with_page)

    except Exception as e:
        print(f"エラー: {language} - {type(e).__name__}: {e}")
        return None

    print(f"処理したページ数: {len(page_info)}")
    print(f"抽出した総行数: {len(all_data)}")

    # DataFrameに変換
    if len(all_data) > 0:
        # 全データ行から最大列数を取得
        max_cols = max(len(row) for row in all_data)

        # 全ての行を最大列数に合わせる
        for row in all_data:
            if len(row) < max_cols:
                row.extend([''] * (max_cols - len(row)))

        # 列名を生成（Page, Table, Data columns）
        columns = ['Page', 'Table']
        for i in range(max_cols - 2):
            columns.append(f'Column_{i}')

        df = pd.DataFrame(all_data, columns=columns)

        # 必要な列のみを選択して並び替え
        # 列の対応: Column_0=番号, Column_1=単語, Column_2=読み方, Column_3=翻訳
        df_final = pd.DataFrame({
            '言語': language,
            'Page': df['Page'],
            '番号': df['Column_0'],
            '単語': df['Column_1'],
            '翻訳': df['Column_3']
        })

        # 全セルにtrimと改行クリーニングを適用
        def clean_cell(value):
            """セルの値をクリーニング（trim + 改行除去）"""
            if pd.isna(value):
                return value
            if isinstance(value, str):
                # 改行を空白に置換
                value = value.replace('\n', ' ').replace('\r', ' ')
                # 複数の空白を1つに
                value = ' '.join(value.split())
                # 前後の空白を削除
                value = value.strip()
            return value

        # 全ての列に適用
        for col in df_final.columns:
            df_final[col] = df_final[col].apply(clean_cell)

        # 翻訳データの充足率
        translation_fill = (df_final['翻訳'].notna() & (df_final['翻訳'].astype(str).str.strip() != '')).sum()
        translation_rate = translation_fill / len(df_final) * 100 if len(df_final) > 0 else 0

        print(f"総行数: {len(df_final)}")
        print(f"翻訳データあり: {translation_fill}/{len(df_final)} ({translation_rate:.1f}%)")

        return df_final

    else:
        print("データが抽出できませんでした")
        return None


def main():
    """メイン処理"""
    print(f"{'='*80}")
    print("全8言語PDF抽出処理開始")
    print(f"{'='*80}")

    all_results = []
    all_dataframes = []

    # 各言語のPDFを処理
    for pdf_file in PDF_FILES:
        pdf_path = PDF_DIR / pdf_file

        if not pdf_path.exists():
            print(f"\n警告: ファイルが見つかりません - {pdf_file}")
            continue

        df = extract_pdf_to_dataframe(pdf_path, pdf_file)

        if df is not None:
            language = extract_language_from_filename(pdf_file)

            # 個別CSV出力
            output_file = OUTPUT_DIR / f"{language}_pdfplumber_抽出_最終版.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"出力: {output_file}")

            # 統合用にDataFrameを保存
            all_dataframes.append(df)

            # 結果を記録
            translation_fill = (df['翻訳'].notna() & (df['翻訳'].astype(str).str.strip() != '')).sum()
            translation_rate = translation_fill / len(df) * 100 if len(df) > 0 else 0

            all_results.append({
                '言語': language,
                '行数': len(df),
                '翻訳あり': translation_fill,
                '翻訳充足率': f"{translation_rate:.1f}%"
            })

    # 全言語統合CSV作成
    if len(all_dataframes) > 0:
        print(f"\n{'='*80}")
        print("全言語統合中")
        print(f"{'='*80}")

        df_combined = pd.concat(all_dataframes, ignore_index=True)

        combined_output = OUTPUT_DIR / "全言語統合_pdfplumber_最終版.csv"
        df_combined.to_csv(combined_output, index=False, encoding='utf-8-sig')

        print(f"\n統合ファイル出力: {combined_output}")
        print(f"総行数: {len(df_combined)}")
        print(f"総列数: {len(df_combined.columns)}")

        # 言語別統計
        print(f"\n言語別行数:")
        lang_counts = df_combined['言語'].value_counts()
        for lang, count in lang_counts.items():
            print(f"  {lang}: {count}行")

        # 全体の翻訳充足率
        total_translation = (df_combined['翻訳'].notna() & (df_combined['翻訳'].astype(str).str.strip() != '')).sum()
        total_rate = total_translation / len(df_combined) * 100 if len(df_combined) > 0 else 0
        print(f"\n全体の翻訳充足率: {total_translation}/{len(df_combined)} ({total_rate:.1f}%)")

    # サマリーテーブル表示
    if len(all_results) > 0:
        print(f"\n{'='*80}")
        print("処理サマリー")
        print(f"{'='*80}")
        df_summary = pd.DataFrame(all_results)
        print(df_summary.to_string(index=False))

    print(f"\n{'='*80}")
    print("全処理完了!")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
