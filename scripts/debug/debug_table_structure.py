# -*- coding: utf-8 -*-
"""
PDFのテーブル構造を詳しくデバッグ
"""

import pdfplumber
import pandas as pd

pdf_path = '建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

print("="*80)
print("カンボジア語PDF テーブル構造デバッグ")
print("="*80)

with pdfplumber.open(pdf_path) as pdf:
    # 1ページ目を確認
    page = pdf.pages[0]

    print(f"\nPage 1:")
    print(f"  ページサイズ: {page.width} x {page.height}")

    # デフォルト設定でテーブル抽出
    print(f"\n【デフォルト設定】")
    tables = page.extract_tables()

    print(f"  検出されたテーブル数: {len(tables)}")

    for table_num, table in enumerate(tables, 1):
        print(f"\n  テーブル {table_num}:")
        print(f"    行数: {len(table)}")
        if table:
            print(f"    列数: {len(table[0])}")

            # ヘッダー
            print(f"\n    ヘッダー行:")
            headers = table[0]
            for col_idx, header in enumerate(headers):
                header_str = str(header) if header else "[None]"
                try:
                    print(f"      列{col_idx}: '{header_str}'")
                except UnicodeEncodeError:
                    print(f"      列{col_idx}: [表示エラー]")

            # 最初のデータ行（No.1）
            if len(table) > 1:
                print(f"\n    データ行1（No.1）:")
                row1 = table[1]
                for col_idx, val in enumerate(row1):
                    val_str = str(val) if val else "[None]"
                    try:
                        print(f"      列{col_idx}: '{val_str}'")
                    except UnicodeEncodeError:
                        print(f"      列{col_idx}: [表示エラー]")

    # 異なる設定でテスト
    print(f"\n{'='*80}")
    print("【異なる設定でテスト】")
    print(f"{'='*80}")

    test_settings = [
        {
            "name": "Text戦略",
            "settings": {
                "vertical_strategy": "text",
                "horizontal_strategy": "text"
            }
        },
        {
            "name": "Lines戦略",
            "settings": {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            }
        },
        {
            "name": "Text戦略 + 高許容値",
            "settings": {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "snap_tolerance": 10,
                "join_tolerance": 10,
                "text_tolerance": 10
            }
        },
        {
            "name": "明示的な線検出",
            "settings": {
                "vertical_strategy": "explicit",
                "horizontal_strategy": "explicit",
                "explicit_vertical_lines": page.curves + page.edges,
                "explicit_horizontal_lines": page.curves + page.edges
            }
        }
    ]

    for test_config in test_settings:
        print(f"\n{test_config['name']}:")

        try:
            tables = page.extract_tables(table_settings=test_config['settings'])

            if tables:
                for table_num, table in enumerate(tables, 1):
                    if table:
                        print(f"  テーブル{table_num}: {len(table)}行 x {len(table[0])}列")

                        # ヘッダーの列数を確認
                        if len(table) > 0:
                            print(f"    ヘッダー列数: {len(table[0])}")

                        # データ行の列数を確認
                        if len(table) > 1:
                            print(f"    データ行1の列数: {len(table[1])}")

                            # データ行1の内容（空でない列）
                            non_empty_cols = []
                            for col_idx, val in enumerate(table[1]):
                                if val and val.strip():
                                    non_empty_cols.append(col_idx)
                            print(f"    空でない列: {non_empty_cols} ({len(non_empty_cols)}個)")
            else:
                print(f"  テーブルなし")

        except Exception as e:
            print(f"  エラー: {e}")

print(f"\n{'='*80}")
print("デバッグ完了")
print(f"{'='*80}")
