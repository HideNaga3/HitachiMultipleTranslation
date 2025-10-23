# -*- coding: utf-8 -*-
"""
各CSVファイルの列名を確認するスクリプト
"""

import pandas as pd
from pathlib import Path

def main():
    output_dir = Path("output")
    csv_files = sorted(output_dir.glob("*.csv"))

    for csv_file in csv_files:
        print(f"\n{'='*80}")
        print(f"ファイル: {csv_file.name}")
        print(f"{'='*80}")

        df = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=5)

        print(f"列数: {len(df.columns)}")
        print(f"\n列名一覧:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")

        print(f"\n最初の2行のサンプル:")
        print(df.head(2).to_string())

if __name__ == "__main__":
    main()
