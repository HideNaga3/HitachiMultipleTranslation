# -*- coding: utf-8 -*-
"""
CSVファイルから表のヘッダーパターンを分析するスクリプト
"""

import pandas as pd
from pathlib import Path
import sys

def analyze_table_headers(csv_path):
    """
    CSVファイルの表ヘッダーパターンを分析

    Args:
        csv_path (str): CSVファイルのパス
    """
    print(f"\n{'='*80}")
    print(f"ファイル分析: {Path(csv_path).name}")
    print(f"{'='*80}\n")

    # CSVを読み込み
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    # 基本情報
    print(f"総行数: {len(df)}")
    print(f"総列数: {len(df.columns)}")
    print(f"\n列名一覧:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")

    # Page と Table でグループ化して、各表の構造を確認
    print(f"\n{'='*80}")
    print("各表の構造分析:")
    print(f"{'='*80}\n")

    if 'Page' in df.columns and 'Table' in df.columns:
        grouped = df.groupby(['Page', 'Table'])

        # 各グループで、どの列に値が入っているかを確認
        table_patterns = {}

        for (page, table), group in grouped:
            # 空でない列を特定（NaNや空文字列でない）
            non_empty_cols = []
            for col in df.columns:
                if col in ['Page', 'Table']:
                    continue
                # 少なくとも1つの非空値があるか確認
                if group[col].notna().any() and (group[col] != '').any():
                    non_empty_cols.append(col)

            # パターンをタプルに変換（ソート済み）
            pattern = tuple(sorted(non_empty_cols))

            if pattern not in table_patterns:
                table_patterns[pattern] = []
            table_patterns[pattern].append((page, table, len(group)))

        # パターンごとに表示
        print(f"検出されたヘッダーパターン数: {len(table_patterns)}\n")

        for i, (pattern, tables) in enumerate(sorted(table_patterns.items(), key=lambda x: len(x[1]), reverse=True), 1):
            print(f"パターン #{i}: 該当表数 = {len(tables)}")
            print(f"  列数: {len(pattern)}")
            print(f"  列名: {', '.join(pattern[:10])}{' ...' if len(pattern) > 10 else ''}")
            print(f"  該当する表（最初の5個）:")
            for page, table, rows in tables[:5]:
                print(f"    - Page {page}, Table {table} ({rows}行)")
            if len(tables) > 5:
                print(f"    ... 他{len(tables)-5}個の表")
            print()

            # 最初の表のサンプルデータを表示
            page, table, _ = tables[0]
            sample = df[(df['Page'] == page) & (df['Table'] == table)].head(3)
            print(f"  サンプルデータ (Page {page}, Table {table} の最初の3行):")

            # パターンの列のみ表示
            display_cols = ['Page', 'Table'] + list(pattern)[:8]
            print(sample[display_cols].to_string(index=False))
            print(f"\n{'-'*80}\n")

    else:
        print("警告: Page または Table 列が見つかりません")

def main():
    """メイン処理"""
    # 英語版のみ分析（代表として）
    csv_file = "output/【全課統合版】英語_げんばのことば_建設関連職種_27cols.csv"

    if not Path(csv_file).exists():
        print(f"エラー: ファイルが見つかりません - {csv_file}")
        sys.exit(1)

    analyze_table_headers(csv_file)

if __name__ == "__main__":
    main()
