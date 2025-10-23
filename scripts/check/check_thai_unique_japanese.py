"""
タイ語固有の日本語（他の言語にない日本語）を確認
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

# 統合CSV読み込み
unified_csv = os.path.join(output_dir, '全言語統合_比較用.csv')
unified_df = pd.read_csv(unified_csv, encoding='utf-8-sig')

output_lines = []

output_lines.append("=" * 80)
output_lines.append("タイ語固有の日本語確認")
output_lines.append("=" * 80)
output_lines.append("")

# 各言語の日本語セット
lang_japanese = {}
for lang in unified_df['言語'].unique():
    lang_df = unified_df[unified_df['言語'] == lang]
    lang_japanese[lang] = set(lang_df['日本語'].dropna().unique())

output_lines.append("言語別ユニーク日本語数:")
for lang in sorted(lang_japanese.keys()):
    output_lines.append(f"  {lang:15s}: {len(lang_japanese[lang]):4d}個")
output_lines.append("")

# タイ語固有の日本語
thai_only = lang_japanese['タイ語']
for lang, jp_set in lang_japanese.items():
    if lang != 'タイ語':
        thai_only = thai_only - jp_set

output_lines.append("=" * 80)
output_lines.append("タイ語のみに存在する日本語")
output_lines.append("=" * 80)
output_lines.append("")
output_lines.append(f"タイ語固有の日本語数: {len(thai_only)}個")
output_lines.append("")

if len(thai_only) > 0:
    output_lines.append("タイ語固有の日本語一覧:")
    for i, jp in enumerate(sorted(thai_only), 1):
        # タイ語データを取得
        thai_row = unified_df[(unified_df['言語'] == 'タイ語') & (unified_df['日本語'] == jp)]
        if len(thai_row) > 0:
            page = thai_row.iloc[0]['ページ']
            number = thai_row.iloc[0]['番号']
            translation = thai_row.iloc[0]['翻訳']
            output_lines.append(f"  {i:2d}. {jp}")
            output_lines.append(f"      Page={page}, No={number}")
            output_lines.append(f"      翻訳: {str(translation)[:50]}")
            output_lines.append("")
else:
    output_lines.append("タイ語固有の日本語はありません（全て他言語にも存在）")

# 逆に、他言語にあってタイ語にない日本語
output_lines.append("=" * 80)
output_lines.append("他言語にあってタイ語にない日本語")
output_lines.append("=" * 80)
output_lines.append("")

all_japanese = set()
for jp_set in lang_japanese.values():
    all_japanese = all_japanese.union(jp_set)

missing_in_thai = all_japanese - lang_japanese['タイ語']

output_lines.append(f"タイ語に欠けている日本語数: {len(missing_in_thai)}個")
output_lines.append("")

if len(missing_in_thai) > 0:
    output_lines.append("タイ語に欠けている日本語一覧（先頭20件）:")
    for i, jp in enumerate(sorted(missing_in_thai)[:20], 1):
        # どの言語にあるか確認
        exists_in = []
        for lang, jp_set in lang_japanese.items():
            if jp in jp_set:
                exists_in.append(lang)
        output_lines.append(f"  {i:2d}. {jp}")
        output_lines.append(f"      存在言語: {', '.join(exists_in)}")
        output_lines.append("")
else:
    output_lines.append("タイ語に欠けている日本語はありません")

output_lines.append("=" * 80)
output_lines.append("確認完了")
output_lines.append("=" * 80)

# UTF-8でファイルに書き込み
output_file = os.path.join(for_claude_dir, 'thai_unique_japanese.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"確認結果を保存: {output_file}")
print()
print(f"タイ語固有の日本語: {len(thai_only)}個")
print(f"タイ語に欠けている日本語: {len(missing_in_thai)}個")
