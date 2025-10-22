# -*- coding: utf-8 -*-
"""
座標ベースでPDFから表データを抽出

pdfplumberで文字の座標を取得し、
X座標を基準に列を検出して正しく表データを抽出します。
"""

import pdfplumber
import pandas as pd
from pathlib import Path
from collections import defaultdict

def extract_table_by_coordinates(page, page_num):
    """
    座標ベースで表データを抽出

    Args:
        page: pdfplumberのPageオブジェクト
        page_num: ページ番号

    Returns:
        list: 抽出した表データ（行のリスト）
    """
    chars = page.chars

    if not chars:
        return []

    # y座標でグループ化（行を検出）
    chars_sorted = sorted(chars, key=lambda c: (c.get('top', 0), c.get('x0', 0)))

    lines = []
    current_line = []
    current_y = None
    tolerance = 5  # y座標の許容差

    for char in chars_sorted:
        y = char.get('top', 0)

        if current_y is None or abs(y - current_y) <= tolerance:
            current_line.append(char)
            current_y = y
        else:
            if current_line:
                lines.append(current_line)
            current_line = [char]
            current_y = y

    if current_line:
        lines.append(current_line)

    # 列の境界を検出（X座標の分布から）
    # すべての文字のX座標を収集
    all_x = [c.get('x0', 0) for c in chars]
    all_x_sorted = sorted(set(all_x))

    # 列の境界を決定（X座標の大きなギャップを探す）
    column_boundaries = []
    prev_x = None

    for x in all_x_sorted:
        if prev_x is not None and x - prev_x > 30:  # 30ポイント以上のギャップ
            column_boundaries.append((prev_x + x) / 2)
        prev_x = x

    # 列の境界が見つからない場合、固定値を使用
    if not column_boundaries:
        # 一般的な表の列境界（PDF単位、左から）
        column_boundaries = [250, 400, 550, 700, 850, 1000]

    print(f"\nページ {page_num}:")
    print(f"  検出された行数: {len(lines)}")
    print(f"  列の境界 (X座標): {[f'{x:.1f}' for x in column_boundaries]}")

    # 各行を列に分割
    table_data = []

    for line_idx, line in enumerate(lines):
        # 行のテキストを列ごとに分割
        row_data = [''] * (len(column_boundaries) + 1)

        # 文字をx座標でソート
        line_sorted = sorted(line, key=lambda c: c.get('x0', 0))

        # 各文字をどの列に属するかを決定
        for char in line_sorted:
            x = char.get('x0', 0)
            text = char.get('text', '')

            # この文字がどの列に属するかを決定
            col_idx = 0
            for boundary in column_boundaries:
                if x < boundary:
                    break
                col_idx += 1

            # 列に文字を追加
            if col_idx < len(row_data):
                row_data[col_idx] += text

        # 空でない行のみ追加
        if any(cell.strip() for cell in row_data):
            table_data.append(row_data)

    return table_data

def main():
    """メイン処理"""
    pdf_file = "建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print("=" * 80)
    print("座標ベースPDF抽出")
    print("=" * 80)
    print(f"\nPDFファイル: {pdf_file}")

    all_data = []

    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        print(f"総ページ数: {total_pages}")

        for page_num in range(1, min(total_pages + 1, 6)):  # 最初の5ページをテスト
            page = pdf.pages[page_num - 1]
            table_data = extract_table_by_coordinates(page, page_num)

            if table_data:
                print(f"  抽出行数: {len(table_data)}")

                # ページ番号を追加
                for row in table_data:
                    all_data.append([page_num] + row)

                # サンプルを表示（最初の3行）
                print(f"  サンプル（最初の3行）:")
                for i, row in enumerate(table_data[:3]):
                    print(f"\n    行{i}:")
                    for col_idx, cell in enumerate(row):
                        if cell.strip():
                            try:
                                print(f"      列{col_idx}: {cell.strip()[:50]}")
                            except:
                                print(f"      列{col_idx}: [カンボジア語・{len(cell)}文字]")

    if all_data:
        # DataFrameに変換
        max_cols = max(len(row) for row in all_data)
        headers = ['Page'] + [f'Column_{i}' for i in range(max_cols - 1)]

        # 列数を揃える
        for row in all_data:
            while len(row) < max_cols:
                row.append('')

        df = pd.DataFrame(all_data, columns=headers)

        # CSVに保存
        csv_file = output_dir / "カンボジア語_coordinate_extracted.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')

        print(f"\n統合完了:")
        print(f"  総行数: {len(df)}")
        print(f"  総列数: {len(df.columns)}")
        print(f"  出力ファイル: {csv_file}")

        # 各列のデータ数を確認
        print(f"\n各列のデータ数:")
        for col in df.columns:
            non_empty = df[col].notna() & (df[col] != '') & (df[col].str.strip() != '')
            count = non_empty.sum()
            ratio = count / len(df) * 100 if len(df) > 0 else 0
            print(f"  {col}: {count}/{len(df)} ({ratio:.1f}%)")

            # カンボジア語文字を含むデータをカウント
            if count > 0:
                khmer_count = df[col].apply(lambda x: bool(x and any('\u1780' <= c <= '\u17FF' for c in str(x)))).sum()
                if khmer_count > 0:
                    print(f"    カンボジア語データ: {khmer_count}行")

    print(f"\n{'=' * 80}")
    print("完了")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    main()
