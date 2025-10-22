# -*- coding: utf-8 -*-
"""
markerを使用してカンボジア語PDFから表を抽出してテスト

markerは以下の特徴があります：
- PDF→Markdown変換
- OCR機能内蔵（surya-ocr使用）
- 高速処理
- 表構造の検出

このスクリプトでは、markerで抽出したMarkdownから表データを抽出して、
pdfplumberと比較します。
"""

import os
from pathlib import Path
from marker.convert import convert_single_pdf
from marker.models import load_all_models
import pandas as pd
import re

def extract_markdown_tables_to_csv(markdown_text, output_csv):
    """
    Markdownテキストから表を抽出してCSVに変換

    Args:
        markdown_text (str): Markdown形式のテキスト
        output_csv (str): 出力CSVファイルパス
    """
    # Markdown表のパターンを探す
    # | col1 | col2 | col3 |
    # |------|------|------|
    # | data1| data2| data3|

    tables = []
    lines = markdown_text.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 表の開始を検出（|で始まる行）
        if line.startswith('|') and '|' in line:
            table_lines = []

            # この表の全行を収集
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1

            # 区切り線をスキップ（|---|---|のような行）
            if len(table_lines) >= 2:
                # ヘッダー行
                header_line = table_lines[0]
                headers = [cell.strip() for cell in header_line.split('|')[1:-1]]

                # データ行（区切り線を除く）
                data_rows = []
                for line in table_lines[2:]:  # 0=ヘッダー, 1=区切り線, 2以降=データ
                    if line and not re.match(r'\|[\s\-:]+\|', line):
                        cells = [cell.strip() for cell in line.split('|')[1:-1]]
                        if cells and any(cell for cell in cells):  # 空行をスキップ
                            data_rows.append(cells)

                if data_rows:
                    tables.append({
                        'headers': headers,
                        'data': data_rows
                    })
        else:
            i += 1

    if not tables:
        print("警告: 表が見つかりませんでした")
        return None

    # すべての表を統合
    print(f"\n見つかった表の数: {len(tables)}")

    all_data = []
    for idx, table in enumerate(tables, 1):
        headers = table['headers']
        data = table['data']

        print(f"\n表 {idx}:")
        print(f"  ヘッダー: {headers}")
        print(f"  データ行数: {len(data)}")
        print(f"  列数: {len(headers)}")

        # DataFrameに変換
        df = pd.DataFrame(data, columns=headers if len(headers) == len(data[0]) else None)
        all_data.append(df)

    # 統合
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"\n統合完了:")
        print(f"  総行数: {len(combined_df)}")
        print(f"  総列数: {len(combined_df.columns)}")
        print(f"  出力ファイル: {output_csv}")

        # 列名を表示
        print(f"\n列名:")
        for i, col in enumerate(combined_df.columns):
            try:
                print(f"  {i}: '{col}'")
            except UnicodeEncodeError:
                print(f"  {i}: [カンボジア語列名]")

        # サンプルデータを表示
        print(f"\n最初の5行:")
        for idx in range(min(5, len(combined_df))):
            row = combined_df.iloc[idx]
            print(f"\n  行 {idx}:")
            for col_idx, col in enumerate(combined_df.columns):
                val = row[col]
                if pd.notna(val) and val != '':
                    try:
                        print(f"    列{col_idx} '{col}': {str(val)[:50]}")
                    except:
                        print(f"    列{col_idx}: [カンボジア語データ]")

        return combined_df

    return None

def main():
    """メイン処理"""
    pdf_file = "建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    if not os.path.exists(pdf_file):
        print(f"エラー: PDFファイルが見つかりません - {pdf_file}")
        return

    print("=" * 80)
    print("marker-pdfでカンボジア語PDFを抽出テスト")
    print("=" * 80)

    print(f"\nPDFファイル: {pdf_file}")
    print("\nmarkerモデルを読み込み中...")

    # markerモデルをロード（初回のみダウンロードされる）
    model_lst = load_all_models()

    print("PDFを変換中...")

    # PDFをMarkdownに変換
    full_text, images, out_meta = convert_single_pdf(
        pdf_file,
        model_lst,
        max_pages=None,  # すべてのページを処理
    )

    print(f"\n変換完了!")
    print(f"  抽出テキスト長: {len(full_text)} 文字")
    print(f"  画像数: {len(images)}")

    # Markdownを保存
    md_file = output_dir / "カンボジア語_marker_extracted.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
    print(f"\nMarkdownを保存: {md_file}")

    # 表をCSVに抽出
    csv_file = output_dir / "カンボジア語_marker_extracted.csv"
    print(f"\n表をCSVに抽出中...")
    df = extract_markdown_tables_to_csv(full_text, csv_file)

    if df is not None:
        # pdfplumberの結果と比較
        print("\n" + "=" * 80)
        print("pdfplumberとの比較")
        print("=" * 80)

        pdfplumber_csv = "output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_improved_56cols.csv"
        if os.path.exists(pdfplumber_csv):
            df_pdfplumber = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

            print(f"\npdfplumber結果:")
            print(f"  行数: {len(df_pdfplumber)}")
            print(f"  列数: {len(df_pdfplumber.columns)}")

            print(f"\nmarker結果:")
            print(f"  行数: {len(df)}")
            print(f"  列数: {len(df.columns)}")

            # 翻訳列のデータ数を比較
            print(f"\n翻訳データの比較:")

            # pdfplumberの翻訳列を探す
            pdfplumber_translation_col = None
            for col in df_pdfplumber.columns:
                if 'របក' in str(col):
                    pdfplumber_translation_col = col
                    break

            if pdfplumber_translation_col:
                pdf_trans_count = df_pdfplumber[pdfplumber_translation_col].notna().sum()
                pdf_trans_ratio = pdf_trans_count / len(df_pdfplumber) * 100
                print(f"  pdfplumber: {pdf_trans_count}/{len(df_pdfplumber)} ({pdf_trans_ratio:.1f}%)")

            # markerの翻訳列を探す（列名に'翻訳'または'របក'を含む）
            marker_translation_col = None
            for col in df.columns:
                col_str = str(col)
                if 'របក' in col_str or '翻訳' in col_str or 'translation' in col_str.lower():
                    marker_translation_col = col
                    break

            if marker_translation_col:
                marker_trans_count = df[marker_translation_col].notna().sum()
                marker_trans_ratio = marker_trans_count / len(df) * 100
                print(f"  marker: {marker_trans_count}/{len(df)} ({marker_trans_ratio:.1f}%)")
            else:
                print(f"  marker: 翻訳列が見つかりません")
                print(f"  marker列名: {list(df.columns)}")

    print("\n" + "=" * 80)
    print("完了")
    print("=" * 80)

if __name__ == "__main__":
    main()
