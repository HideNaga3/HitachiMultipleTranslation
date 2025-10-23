"""
「雇用保険」のテンプレート変換処理をデバッグ
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'
unified_csv = os.path.join(output_dir, '全言語統合_比較用.csv')
debug_output = os.path.join(for_claude_dir, 'employment_debug.txt')

# ファイルに書き込み
output_lines = []

output_lines.append("=" * 80)
output_lines.append("「雇用保険」変換デバッグ")
output_lines.append("=" * 80)
output_lines.append("")

# 統合CSVを読み込み
unified_df = pd.read_csv(unified_csv, encoding='utf-8-sig')

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

output_lines.append("統合CSVから「雇用保険」の全データを抽出:")
output_lines.append("")

employment_rows = unified_df[unified_df['日本語'] == '雇用保険']
output_lines.append(f"雇用保険の行数: {len(employment_rows)}")
output_lines.append("")

for idx, row in employment_rows.iterrows():
    lang = row['言語']
    translated = row['翻訳']
    output_lines.append(f"  言語={lang}, 翻訳あり={pd.notna(translated)}, 翻訳値={repr(translated)[:50]}")

output_lines.append("")
output_lines.append("=" * 80)
output_lines.append("テンプレート変換ロジックをシミュレート:")
output_lines.append("=" * 80)
output_lines.append("")

jp_word = '雇用保険'
row_data = {'ja': jp_word}

for lang_name, lang_code in lang_name_to_code.items():
    # 元のロジックと同じ
    lang_rows = unified_df[(unified_df['日本語'] == jp_word) & (unified_df['言語'] == lang_name)]

    output_lines.append(f"[{lang_name}] → [{lang_code}]")
    output_lines.append(f"  検索条件: 日本語={jp_word} AND 言語={lang_name}")
    output_lines.append(f"  該当行数: {len(lang_rows)}")

    if len(lang_rows) > 0:
        translation = lang_rows.iloc[0]['翻訳']
        output_lines.append(f"  翻訳値: {repr(translation)[:60]}")
        output_lines.append(f"  pd.notna(translation): {pd.notna(translation)}")

        final_value = translation if pd.notna(translation) else ''
        row_data[lang_code] = final_value
        output_lines.append(f"  最終値: {repr(final_value)[:60]}")
    else:
        row_data[lang_code] = ''
        output_lines.append(f"  最終値: '' (行が見つからない)")

    output_lines.append("")

output_lines.append("=" * 80)
output_lines.append("最終的な row_data:")
output_lines.append("=" * 80)
output_lines.append("")

for key, value in row_data.items():
    value_repr = repr(value)[:60] if value else '(空文字列)'
    output_lines.append(f"  {key:10s}: {value_repr}")

output_lines.append("")
output_lines.append("=" * 80)
output_lines.append("デバッグ完了")
output_lines.append("=" * 80)

# UTF-8でファイルに書き込み
with open(debug_output, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"デバッグ結果を保存: {debug_output}")
