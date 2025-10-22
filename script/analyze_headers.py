# カンボジア語とタイ語のCSVヘッダーと実データを分析するスクリプト
import pandas as pd
import sys

# 出力をファイルに保存
output_file = 'for_claude/header_analysis.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

def analyze_csv(file_path, lang_name):
    print(f"\n{'='*80}")
    print(f"{lang_name} の分析")
    print(f"{'='*80}")

    # CSVを読み込み
    df = pd.read_csv(file_path, encoding='utf-8-sig')

    print(f"\n総行数: {len(df)}")
    print(f"総列数: {len(df.columns)}")

    print(f"\n列名一覧:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")

    # No.列が数値の行を抽出（実際の単語データ）
    if 'No.' in df.columns:
        # No.列が数値の行のみを抽出
        valid_data = df[pd.to_numeric(df['No.'], errors='coerce').notna()]

        print(f"\n有効なデータ行数（No.が数値）: {len(valid_data)}")

        if len(valid_data) > 0:
            print(f"\n最初の5行のデータ:")
            print("-"*80)

            # 最初の5行を表示
            for idx, row in valid_data.head(5).iterrows():
                print(f"\n行 {idx + 2}:")
                for col in df.columns:
                    value = row[col]
                    if pd.notna(value) and str(value).strip() != '':
                        # 長すぎる値は省略
                        value_str = str(value)
                        if len(value_str) > 50:
                            value_str = value_str[:50] + "..."
                        print(f"  {col}: {value_str}")

# カンボジア語を分析
analyze_csv(
    'output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_50cols.csv',
    'カンボジア語'
)

# タイ語を分析
analyze_csv(
    'output/【全課統合版】タイ語_げんばのことば_建設関連職種_42cols.csv',
    'タイ語'
)

# 出力を閉じる
sys.stdout.close()

print("分析結果を for_claude/header_analysis.txt に保存しました。")
