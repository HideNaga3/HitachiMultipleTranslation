"""
全言語統合CSVの構造を確認するスクリプト
"""

import pandas as pd
import sys

# 出力先をファイルに変更
output_file = 'for_claude/unified_csv_structure.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

# 統合CSVファイルを読み込み
csv_paths = [
    'output/intermediate/全言語統合_pdfplumber_最終版.csv',
    'output/intermediate/全言語統合_テンプレート形式_ベトナム語順序.csv',
    'output/全言語統合_テンプレート_インポート用.csv'
]

for csv_path in csv_paths:
    print("=" * 80)
    print(f"ファイル: {csv_path}")
    print("=" * 80)
    print()

    try:
        # CSVを読み込み
        df = pd.read_csv(csv_path, encoding='utf-8-sig')

        # 基本情報
        print(f"総行数: {len(df)}")
        print(f"総列数: {len(df.columns)}")
        print()

        # 列名一覧
        print("列名一覧:")
        print("-" * 80)
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        print()

        # Page列と番号列の確認
        has_page = 'Page' in df.columns
        has_bangou = '番号' in df.columns
        has_no = 'No.' in df.columns

        print("重要列の存在確認:")
        print(f"  Page列  : {'✓ あり' if has_page else '✗ なし'}")
        print(f"  番号列  : {'✓ あり' if has_bangou else '✗ なし'}")
        print(f"  No.列   : {'✓ あり' if has_no else '✗ なし'}")
        print()

        # データサンプル（最初の5行）
        if has_page or has_bangou or has_no:
            print("データサンプル（最初の5行）:")
            print("-" * 80)
            display_cols = []
            if has_page:
                display_cols.append('Page')
            if has_bangou:
                display_cols.append('番号')
            if has_no:
                display_cols.append('No.')

            # 単語列を追加
            for col in df.columns:
                if '単語' in col or '日本語' in col or 'ja' in col.lower():
                    display_cols.append(col)
                    break

            if display_cols:
                print(df[display_cols].head(5).to_string(index=False))
            print()

    except Exception as e:
        print(f"エラー: {e}")
        print()

    print()

print("=" * 80)

sys.stdout.close()
print(f"結果を {output_file} に保存しました", file=sys.__stdout__)
