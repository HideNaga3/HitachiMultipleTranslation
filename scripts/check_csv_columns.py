# 各言語のCSVファイルの列名を確認するスクリプト
import pandas as pd
import sys
from pathlib import Path

# UTF-8で出力
output_file = 'for_claude/columns_analysis.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

# 出力フォルダ
output_folder = Path('output')

# CSVファイルを取得
csv_files = sorted(list(output_folder.glob('*.csv')))

print(f"CSVファイル数: {len(csv_files)}\n")
print("="*80)

for csv_file in csv_files:
    print(f"\nファイル: {csv_file.name}")
    print("-"*80)

    # CSVを読み込み（最初の5行のみ）
    df = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=5)

    print(f"総列数: {len(df.columns)}")
    print(f"総行数（サンプル）: {len(df)}\n")

    print("列名一覧:")
    for i, col in enumerate(df.columns, 1):
        # 最初の非空値を取得
        sample_value = ''
        for val in df[col]:
            if pd.notna(val) and str(val).strip() != '':
                sample_value = str(val).strip()
                if len(sample_value) > 50:
                    sample_value = sample_value[:50] + "..."
                break

        print(f"  {i:2d}. {col:<40s} サンプル: {sample_value}")

    print("\n" + "="*80)

sys.stdout.close()
print("分析結果を for_claude/columns_analysis.txt に保存しました。")
