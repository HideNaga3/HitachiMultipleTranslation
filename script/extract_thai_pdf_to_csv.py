"""
pdfplumberでタイ語PDFからテーブルを抽出してCSVに出力
"""

import pdfplumber
import pandas as pd
from pathlib import Path

# 設定
PDF_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\建設関連PDF")
OUTPUT_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\output")
PDF_FILE = "【全課統合版】タイ語_げんばのことば_建設関連職種.pdf"

pdf_path = PDF_DIR / PDF_FILE
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"PDFファイル: {PDF_FILE}")
print(f"パス: {pdf_path}")
print("="*80)

# 全ページのデータを格納するリスト
all_data = []
page_info = []

# PDFを開く
with pdfplumber.open(pdf_path) as pdf:
    print(f"\n総ページ数: {len(pdf.pages)}")

    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]

        # ページからテーブルを抽出
        tables = page.extract_tables()

        if len(tables) == 0:
            continue

        # 各テーブルを処理
        for table_idx, table in enumerate(tables):
            if len(table) == 0:
                continue

            # ヘッダー行を探す（"No." を含む行）
            header_row_idx = None
            for i, row in enumerate(table):
                if any('No.' in str(cell) for cell in row if cell):
                    header_row_idx = i
                    break

            if header_row_idx is None:
                print(f"  警告: ページ{page_num+1} テーブル{table_idx+1} - ヘッダー行が見つかりません")
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

print(f"\n{'='*80}")
print(f"抽出結果")
print(f"{'='*80}")
print(f"処理したページ数: {len(page_info)}")
print(f"抽出した総行数: {len(all_data)}")

# DataFrameに変換
if len(all_data) > 0:
    # 全データ行から最大列数を取得
    max_cols = max(len(row) for row in all_data)
    print(f"最大列数: {max_cols}")

    # 全ての行を最大列数に合わせる
    for row in all_data:
        if len(row) < max_cols:
            row.extend([''] * (max_cols - len(row)))

    # 列名を生成（Page, Table, Data columns）
    columns = ['Page', 'Table']
    for i in range(max_cols - 2):
        columns.append(f'Column_{i}')

    df = pd.DataFrame(all_data, columns=columns)

    # ファイル名から言語を抽出
    # 例: 【全課統合版】タイ語_げんばのことば_建設関連職種.pdf → タイ語
    import re
    match = re.search(r'【全課統合版】(.+?)_', PDF_FILE)
    language = match.group(1) if match else 'Unknown'
    print(f"\n抽出された言語: {language}")

    # 必要な列のみを選択して並び替え
    # 列の対応: Column_0=番号, Column_1=単語, Column_2=読み方, Column_3=翻訳
    df_final = pd.DataFrame({
        '言語': language,
        'Page': df['Page'],
        '番号': df['Column_0'],
        '単語': df['Column_1'],
        '翻訳': df['Column_3']
    })

    # CSV出力
    output_file = OUTPUT_DIR / f"{language}_pdfplumber_抽出_最終版.csv"
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"\n出力ファイル: {output_file}")
    print(f"総行数: {len(df_final)}")
    print(f"総列数: {len(df_final.columns)}")
    print(f"\n列名: {df_final.columns.tolist()}")

    # 統計情報
    print(f"\n統計情報:")
    print(f"  ページ別行数:")
    page_counts = df_final['Page'].value_counts().sort_index()
    for page, count in list(page_counts.items())[:10]:  # 最初の10ページのみ表示
        print(f"    ページ{page}: {count}行")
    if len(page_counts) > 10:
        print(f"    ... (他 {len(page_counts) - 10} ページ)")

    # 翻訳データの充足率
    translation_fill = (df_final['翻訳'].notna() & (df_final['翻訳'].astype(str).str.strip() != '')).sum()
    translation_rate = translation_fill / len(df_final) * 100 if len(df_final) > 0 else 0
    print(f"\n  翻訳データあり: {translation_fill}/{len(df_final)} ({translation_rate:.1f}%)")

    # サンプルデータを表示（最初の5行、文字数制限）
    print(f"\nサンプルデータ（最初の5行）:")
    for i in range(min(5, len(df_final))):
        row = df_final.iloc[i]
        print(f"  行{i+1}: 言語={row['言語']}, Page={row['Page']}, 番号={row['番号']}, 単語={str(row['単語'])[:15]}..., 翻訳={str(row['翻訳'])[:20]}...")

else:
    print("\nエラー: データが抽出できませんでした")

print(f"\n{'='*80}")
print("処理完了")
