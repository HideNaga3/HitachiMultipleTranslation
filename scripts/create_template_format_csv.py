"""
統合CSVをテンプレート形式（横持ち）に変換
列: ja, en, fil-PH, pt, es, pt-BR, zh, ko, fr, hi, th, vi, my, ne, bn, id, ta, si, mn, ar, fa, tr, ru, ur, km, lo, ms, de, hu, cs, pl, nl, da, fi, sv, lb, af, fr-CA
"""
import pandas as pd
import json
import os
from datetime import datetime

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
core_files_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\core_files'

unified_csv = os.path.join(output_dir, '全言語統合_比較用.csv')
template_csv = os.path.join(core_files_dir, 'ourput_csv_template_utf8bom.csv')

print("=" * 80)
print("テンプレート形式CSVへの変換")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# テンプレートの列順を取得
template_df = pd.read_csv(template_csv, encoding='utf-8-sig', nrows=0)
template_columns = template_df.columns.tolist()
print(f"テンプレート列数: {len(template_columns)}列")
print(f"列: {', '.join(template_columns)}")
print()

# 統合CSVを読み込み
unified_df = pd.read_csv(unified_csv, encoding='utf-8-sig')
print(f"統合CSV: {len(unified_df)}行")
print()

# 言語名 → 言語コードのマッピング
lang_name_to_code = {
    '英語': 'en',
    'タガログ語': 'fil-PH',
    'カンボジア語': 'km',
    '中国語': 'zh',
    'インドネシア語': 'id',
    'ミャンマー語': 'my',
    'タイ語': 'th',
    'ベトナム語': 'vi',
}

print("言語コードマッピング:")
for name, code in lang_name_to_code.items():
    print(f"  {name} → {code}")
print()

# 日本語をキーにしてピボット
print("=" * 80)
print("ピボット処理中...")
print("=" * 80)
print()

# 日本語列でグループ化して、各言語の翻訳を横持ちにする
result_data = []

# 日本語のユニークな値を取得（順序を保持）
unique_japanese = unified_df['日本語'].drop_duplicates().tolist()

for jp_word in unique_japanese:
    row_data = {'ja': jp_word}

    # 各言語の翻訳を取得
    for lang_name, lang_code in lang_name_to_code.items():
        lang_rows = unified_df[(unified_df['日本語'] == jp_word) & (unified_df['言語'] == lang_name)]

        if len(lang_rows) > 0:
            # 複数行ある場合は最初の行を使用
            translation = lang_rows.iloc[0]['翻訳']
            row_data[lang_code] = translation if pd.notna(translation) else ''
        else:
            row_data[lang_code] = ''

    result_data.append(row_data)

# DataFrameを作成
result_df = pd.DataFrame(result_data)

# テンプレートの列順に並べ替え（存在する列のみ）
available_columns = [col for col in template_columns if col in result_df.columns]
result_df = result_df[available_columns]

# 不足している列を空列として追加
for col in template_columns:
    if col not in result_df.columns:
        result_df[col] = ''

# 列順を完全にテンプレートに合わせる
result_df = result_df[template_columns]

print(f"変換後のデータ: {len(result_df)}行 x {len(result_df.columns)}列")
print()

# 統計情報
print("言語別データ状況:")
for lang_code in template_columns:
    if lang_code == 'ja':
        continue
    non_empty = result_df[lang_code].notna().sum()
    has_value = (result_df[lang_code] != '').sum()
    print(f"  {lang_code:10s}: {has_value:4d}行に翻訳あり")

print()

# 保存
output_file = os.path.join(output_dir, '全言語統合_テンプレート形式.csv')
result_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print("=" * 80)
print("変換完了")
print("=" * 80)
print(f"出力ファイル: {output_file}")
print()
