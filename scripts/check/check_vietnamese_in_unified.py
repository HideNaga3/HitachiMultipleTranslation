"""
ベトナム語のみに存在する24語が統合CSVにあるか確認
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
output_lines.append("ベトナム語のみに存在する24語が統合CSVに存在するか確認")
output_lines.append("=" * 80)
output_lines.append("")

vietnamese_only_terms = [
    'けれん', '不安定', '不安定な', '丸セパレーター（丸セパ）',
    '予防', '予防する', '嘔吐', '嘔吐する',
    '基礎型枠（メタルフォー ム）', '墜落', '墜落する', '感電',
    '感電する', '準備', '確認', '確認する',
    '落下', '落下する', '転倒', '転倒する'
]

found_count = 0
not_found_count = 0

for i, term in enumerate(vietnamese_only_terms, 1):
    term_rows = unified_df[unified_df['日本語'] == term]

    if len(term_rows) > 0:
        found_count += 1
        output_lines.append(f"{i:2d}. {term} - 統合CSVに存在 ({len(term_rows)}行)")

        # どの言語にあるか確認
        languages = term_rows['言語'].unique()
        output_lines.append(f"    言語: {', '.join(languages)}")

        # ベトナム語の翻訳確認
        vi_row = term_rows[term_rows['言語'] == 'ベトナム語']
        if len(vi_row) > 0:
            vi_trans = vi_row.iloc[0]['翻訳']
            page = vi_row.iloc[0]['ページ']
            output_lines.append(f"    ベトナム語翻訳: {str(vi_trans)[:50]}")
            output_lines.append(f"    ページ: {page}")

        output_lines.append("")
    else:
        not_found_count += 1
        output_lines.append(f"{i:2d}. {term} - 統合CSVに見つかりません")
        output_lines.append("")

output_lines.append("=" * 80)
output_lines.append("サマリー")
output_lines.append("=" * 80)
output_lines.append("")
output_lines.append(f"統合CSVに存在: {found_count}語")
output_lines.append(f"統合CSVに不在: {not_found_count}語")
output_lines.append("")

if found_count > 0 and not_found_count == 0:
    output_lines.append("結論:")
    output_lines.append("ベトナム語のみの24語は統合CSVには存在します。")
    output_lines.append("しかし、テンプレートCSVには含まれていません。")
    output_lines.append("")
    output_lines.append("推測される原因:")
    output_lines.append("- テンプレート作成時に、タイ語基準で並び替えた際に除外された")
    output_lines.append("- タイ語順序リストに含まれていない日本語は、Categoricalでソート時に削除された")

# UTF-8でファイルに書き込み
output_file = os.path.join(for_claude_dir, 'vietnamese_in_unified_check.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"確認結果を保存: {output_file}")
print()
print(f"統合CSVに存在: {found_count}/{len(vietnamese_only_terms)}語")
print(f"統合CSVに不在: {not_found_count}/{len(vietnamese_only_terms)}語")
