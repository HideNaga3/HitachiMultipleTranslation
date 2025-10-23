# -*- coding: utf-8 -*-
"""
複数のPDF抽出設定を試して最適な設定を見つけるスクリプト
"""

import pdfplumber
import pandas as pd
from pathlib import Path
import os

def count_translation_data(df, lang):
    """
    DataFrameから翻訳データの行数をカウント

    Args:
        df: DataFrame
        lang: 言語名 ('カンボジア語' or 'タイ語')

    Returns:
        int: 翻訳データがある行数
    """
    # 翻訳列を探す
    translation_keywords = {
        'カンボジア語': ['របក'],
        'タイ語': ['แปล', 'คา แปล']
    }

    keywords = translation_keywords.get(lang, [])

    for col in df.columns:
        col_str = str(col)
        if any(keyword in col_str for keyword in keywords):
            # この列で空でないデータをカウント
            non_empty = df[col].notna() & (df[col] != '')
            return non_empty.sum()

    return 0

def test_extraction_settings(pdf_path, lang, test_name, table_settings):
    """
    指定された設定でPDFからテーブルを抽出してテスト

    Args:
        pdf_path: PDFファイルのパス
        lang: 言語名
        test_name: テスト名
        table_settings: pdfplumberのtable_settings

    Returns:
        dict: テスト結果
    """
    print(f"\n  テスト: {test_name}")

    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        # 最初の5ページだけテスト（高速化のため）
        test_pages = min(5, len(pdf.pages))

        for page_num, page in enumerate(pdf.pages[:test_pages], start=1):
            # 設定を使ってテーブル抽出
            tables = page.extract_tables(table_settings=table_settings)

            if tables:
                for table_num, table in enumerate(tables, start=1):
                    if table and len(table) > 0:
                        # ヘッダー行を取得
                        headers = [str(h) if h is not None else f"Column_{i}"
                                   for i, h in enumerate(table[0])]

                        # DataFrameに変換
                        df = pd.DataFrame(table[1:], columns=headers)
                        df.insert(0, 'Page', page_num)
                        df.insert(1, 'Table', table_num)

                        all_tables.append(df)

    if not all_tables:
        return {
            'test_name': test_name,
            'total_tables': 0,
            'total_rows': 0,
            'translation_rows': 0,
            'translation_ratio': 0.0
        }

    # すべての列名を収集（重複を許容）
    all_columns_list = []
    for df in all_tables:
        all_columns_list.extend(df.columns.tolist())

    # 一意な列名のセットを作成
    all_columns_unique = list(set(all_columns_list))

    # 各DataFrameの列名を一意にする
    for i, df in enumerate(all_tables):
        # 列名の重複をチェックして修正
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

        df.columns = new_columns

        # 不足している列を追加
        for col in all_columns_unique:
            if col not in df.columns:
                df[col] = ""

        all_tables[i] = df

    # 統合
    combined_df = pd.concat(all_tables, ignore_index=True)

    # 翻訳データをカウント
    translation_count = count_translation_data(combined_df, lang)

    # No.列でフィルタ（有効な行数）
    if 'No.' in combined_df.columns:
        valid_rows = combined_df['No.'].notna() & (combined_df['No.'] != '')
        valid_count = valid_rows.sum()
    else:
        valid_count = len(combined_df)

    result = {
        'test_name': test_name,
        'total_tables': len(all_tables),
        'total_rows': len(combined_df),
        'valid_rows': valid_count,
        'total_columns': len(all_columns_unique),
        'translation_rows': translation_count,
        'translation_ratio': translation_count / valid_count if valid_count > 0 else 0.0
    }

    print(f"    テーブル数: {result['total_tables']}")
    print(f"    総行数: {result['total_rows']}")
    print(f"    有効行数: {result['valid_rows']}")
    print(f"    列数: {result['total_columns']}")
    print(f"    翻訳データ: {result['translation_rows']}/{result['valid_rows']} ({result['translation_ratio']*100:.1f}%)")

    return result

def main():
    """メイン処理"""

    # テスト対象のPDFファイル
    test_pdfs = [
        {
            'path': '建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf',
            'lang': 'カンボジア語'
        },
        {
            'path': '建設関連PDF/【全課統合版】タイ語_げんばのことば_建設関連職種.pdf',
            'lang': 'タイ語'
        }
    ]

    # テストする設定パターン
    test_settings = [
        {
            'name': 'デフォルト設定',
            'settings': {}
        },
        {
            'name': 'Text戦略',
            'settings': {
                "vertical_strategy": "text",
                "horizontal_strategy": "text"
            }
        },
        {
            'name': 'Lines戦略 + 高い許容値',
            'settings': {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance": 5,
                "join_tolerance": 5
            }
        },
        {
            'name': 'Text戦略 + 高い許容値',
            'settings': {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "snap_tolerance": 5,
                "join_tolerance": 5
            }
        },
        {
            'name': 'Lines Strict戦略',
            'settings': {
                "vertical_strategy": "lines_strict",
                "horizontal_strategy": "lines_strict"
            }
        },
        {
            'name': 'Text + 広い単語間隔',
            'settings': {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "text_tolerance": 5,
                "text_x_tolerance": 5,
                "text_y_tolerance": 5
            }
        }
    ]

    print("="*80)
    print("PDF抽出設定テスト")
    print("="*80)

    all_results = []

    for pdf_info in test_pdfs:
        pdf_path = pdf_info['path']
        lang = pdf_info['lang']

        if not os.path.exists(pdf_path):
            print(f"\n警告: ファイルが見つかりません - {pdf_path}")
            continue

        print(f"\n{'='*80}")
        print(f"PDF: {lang}")
        print(f"{'='*80}")

        for test_config in test_settings:
            result = test_extraction_settings(
                pdf_path,
                lang,
                test_config['name'],
                test_config['settings']
            )
            result['lang'] = lang
            all_results.append(result)

    # 結果のサマリー
    print(f"\n{'='*80}")
    print("テスト結果サマリー")
    print(f"{'='*80}")

    for lang in ['カンボジア語', 'タイ語']:
        lang_results = [r for r in all_results if r['lang'] == lang]
        if not lang_results:
            continue

        print(f"\n{lang}:")
        print(f"  {'設定名':<30} {'翻訳データ':<20} {'比率':<10}")
        print(f"  {'-'*30} {'-'*20} {'-'*10}")

        # 翻訳比率でソート
        lang_results.sort(key=lambda x: x['translation_ratio'], reverse=True)

        for result in lang_results:
            ratio_str = f"{result['translation_ratio']*100:.1f}%"
            trans_str = f"{result['translation_rows']}/{result['valid_rows']}"
            print(f"  {result['test_name']:<30} {trans_str:<20} {ratio_str:<10}")

    # 最適設定を提案
    print(f"\n{'='*80}")
    print("推奨設定")
    print(f"{'='*80}")

    for lang in ['カンボジア語', 'タイ語']:
        lang_results = [r for r in all_results if r['lang'] == lang]
        if lang_results:
            best = max(lang_results, key=lambda x: x['translation_ratio'])
            print(f"\n{lang}: 「{best['test_name']}」")
            print(f"  翻訳データ取得率: {best['translation_ratio']*100:.1f}%")

if __name__ == "__main__":
    main()
