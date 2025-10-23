# -*- coding: utf-8 -*-
"""
全言語のクリーンCSVのヘッダーを確認するスクリプト
"""

import pandas as pd
from pathlib import Path
import json

def main():
    output_dir = Path("output_cleaned")
    csv_files = sorted(output_dir.glob("*_cleaned.csv"))

    headers_info = {}

    for csv_file in csv_files:
        # 言語名を抽出
        language = csv_file.stem.replace('_cleaned', '')

        # CSVを読み込み
        df = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=2)

        headers_info[language] = {
            'columns': list(df.columns),
            'count': len(df.columns)
        }

        try:
            print(f"\n{language}:")
            print(f"  列数: {len(df.columns)}")
            print(f"  列名: {list(df.columns)}")
        except UnicodeEncodeError:
            print(f"\n{language}:")
            print(f"  列数: {len(df.columns)}")
            print(f"  列名: [エンコーディングエラー]")

    # JSON形式でも保存
    with open("headers_mapping.json", "w", encoding="utf-8") as f:
        json.dump(headers_info, f, ensure_ascii=False, indent=2)

    print("\n\nheaders_mapping.json に保存しました")

if __name__ == "__main__":
    main()
