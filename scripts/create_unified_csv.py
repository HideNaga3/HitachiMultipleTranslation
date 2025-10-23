"""
全言語CSVを統合した比較用CSVを作成
列: 行ID, ファイル名, 言語, ページ, 番号, 日本語, 翻訳
"""
import pandas as pd
import os
from datetime import datetime

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'

# 対象ファイル（8言語）
language_files = {
    '英語': '英語_pdfplumber_抽出_最終版.csv',
    'タガログ語': 'タガログ語_pdfplumber_抽出_最終版.csv',
    'カンボジア語': 'カンボジア語_pdfplumber_抽出_最終版.csv',
    '中国語': '中国語_pdfplumber_抽出_最終版.csv',
    'インドネシア語': 'インドネシア語_pdfplumber_抽出_最終版.csv',
    'ミャンマー語': 'ミャンマー語_pdfplumber_抽出_最終版.csv',
    'タイ語': 'タイ語_pdfplumber_抽出_最終版.csv',
    'ベトナム語': 'ベトナム語_pdfplumber_抽出_最終版.csv',
}

print("=" * 80)
print("全言語統合CSV作成")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 統合データを格納
all_data = []
row_id = 1

for lang_name, filename in language_files.items():
    csv_path = os.path.join(output_dir, filename)

    print(f"読み込み中: {lang_name} ({filename})")

    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    for idx, row in df.iterrows():
        all_data.append({
            '行ID': row_id,
            'ファイル名': filename,
            '言語': lang_name,
            'ページ': row.iloc[1],
            '番号': row.iloc[2],
            '日本語': row.iloc[3],
            '翻訳': row.iloc[4]
        })
        row_id += 1

    print(f"  → {len(df)}行を追加")

# DataFrameを作成
unified_df = pd.DataFrame(all_data)

print()
print(f"総行数: {len(unified_df)}行")
print()

# 保存
output_file = os.path.join(output_dir, '全言語統合_比較用.csv')
unified_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print("=" * 80)
print("作成完了")
print("=" * 80)
print(f"出力ファイル: {output_file}")
print()

# 統計情報
print("言語別行数:")
for lang_name in language_files.keys():
    count = len(unified_df[unified_df['言語'] == lang_name])
    print(f"  {lang_name:15s}: {count:4d}行")

print()
