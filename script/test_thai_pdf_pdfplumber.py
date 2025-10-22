"""
pdfplumberでタイ語PDFから1ページずつテーブルを抽出するテストスクリプト
"""

import pdfplumber
import pandas as pd
from pathlib import Path

# 設定
PDF_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\建設関連PDF")
PDF_FILE = "【全課統合版】タイ語_げんばのことば_建設関連職種.pdf"

pdf_path = PDF_DIR / PDF_FILE

print(f"PDFファイル: {PDF_FILE}")
print(f"パス: {pdf_path}")
print("="*80)

# PDFを開く
with pdfplumber.open(pdf_path) as pdf:
    print(f"\n総ページ数: {len(pdf.pages)}")

    # 最初の10ページをテスト
    max_pages = min(10, len(pdf.pages))

    for page_num in range(max_pages):
        page = pdf.pages[page_num]
        print(f"\n{'='*80}")
        print(f"ページ {page_num + 1} / {len(pdf.pages)}")
        print(f"{'='*80}")

        # ページからテーブルを抽出
        tables = page.extract_tables()

        print(f"抽出されたテーブル数: {len(tables)}")

        if len(tables) == 0:
            print("  → テーブルなし")
            continue

        # 各テーブルを処理
        for table_idx, table in enumerate(tables):
            print(f"\n  テーブル {table_idx + 1}:")
            print(f"    行数: {len(table)}")

            if len(table) == 0:
                print("    → 空のテーブル")
                continue

            print(f"    列数: {len(table[0])}")

            # DataFrameに変換
            df = pd.DataFrame(table)

            # 最初の5行を表示
            print(f"\n    最初の5行:")
            for i in range(min(5, len(df))):
                try:
                    # Unicodeエラーを回避するため、repr()を使用
                    row_data = [str(cell)[:20] if cell else '' for cell in df.iloc[i, :5]]
                    print(f"      行{i}: 列数={len(row_data)}, データあり={sum(1 for x in row_data if x)}")
                except Exception as e:
                    print(f"      行{i}: 表示エラー - {type(e).__name__}")

            # ヘッダー行を探す（"No." を含む行）
            header_row = None
            for i, row in enumerate(table):
                if any('No.' in str(cell) for cell in row if cell):
                    header_row = i
                    print(f"\n    ヘッダー行を発見: 行{i}")
                    # セル数のみ表示
                    non_empty = sum(1 for cell in row[:10] if cell and str(cell).strip())
                    print(f"      最初の10列中、データあり: {non_empty}列")
                    break

            # データ行の例を表示
            if header_row is not None and header_row + 1 < len(table):
                data_row_idx = header_row + 1
                print(f"\n    最初のデータ行（行{data_row_idx}）:")
                data_row = table[data_row_idx]
                non_empty_count = 0
                for j, cell in enumerate(data_row[:10]):  # 最初の10列のみ
                    if cell and str(cell).strip():
                        non_empty_count += 1
                print(f"      最初の10列中、データあり: {non_empty_count}列")

            print(f"\n    DataFrameサイズ: {df.shape}")
            print(f"    列名: {df.columns.tolist()[:10]}")  # 最初の10列のみ

print(f"\n{'='*80}")
print("テスト完了")
