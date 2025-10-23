"""
outputフォルダ内のCSVファイルを調査するスクリプト

1. 全CSVファイルの一覧
2. 各CSVのヘッダー（列名）
3. Page列、No.列の有無
4. データのサンプル
"""

import pandas as pd
import os

print("=" * 80)
print("outputフォルダ内のCSVファイル調査")
print("=" * 80)
print()

output_dir = 'output'

# CSVファイルの一覧を取得
csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
csv_files.sort()

print(f"CSVファイル数: {len(csv_files)}")
print()

# 各ファイルを調査
for i, csv_file in enumerate(csv_files, 1):
    print("-" * 80)
    print(f"[{i}/{len(csv_files)}] {csv_file}")
    print("-" * 80)

    csv_path = os.path.join(output_dir, csv_file)

    try:
        # CSVを読み込み（最初の5行のみ）
        df = pd.read_csv(csv_path, encoding='utf-8-sig', nrows=5)

        # 列名を表示
        print(f"列数: {len(df.columns)}")
        print(f"行数（サンプル）: {len(df)}")
        print()
        print("列名:")
        for j, col in enumerate(df.columns, 1):
            print(f"  {j:2d}. {col}")
        print()

        # Page列とNo.列の確認
        has_page = any('page' in col.lower() for col in df.columns)
        has_no = any('no' in col.lower() or '番号' in col for col in df.columns)
        has_table = any('table' in col.lower() for col in df.columns)

        print("重要列:")
        print(f"  Page列: {'✓ あり' if has_page else '✗ なし'}")
        print(f"  No.列: {'✓ あり' if has_no else '✗ なし'}")
        print(f"  Table列: {'✓ あり' if has_table else '✗ なし'}")
        print()

        # ベトナム語関連のファイルは詳細表示
        if 'ベトナム' in csv_file:
            print("【ベトナム語ファイル - 詳細表示】")
            print()
            print("最初の3行:")
            print(df.head(3))
            print()

    except Exception as e:
        print(f"エラー: {e}")
        print()

    # 処理を区切る
    if i < len(csv_files):
        print()

print("=" * 80)
print("調査完了")
print("=" * 80)
