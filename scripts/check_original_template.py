"""
元のテンプレートCSV（タイ語順序ソート前）にベトナム語のみの24語があるか確認
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

output_lines = []

output_lines.append("=" * 80)
output_lines.append("元のテンプレートCSVにベトナム語のみの24語があるか確認")
output_lines.append("=" * 80)
output_lines.append("")

# 元のテンプレートCSV（タイ語順序ソート前）
original_template = os.path.join(output_dir, '全言語統合_テンプレート形式.csv')

if os.path.exists(original_template):
    df = pd.read_csv(original_template, encoding='utf-8-sig')

    output_lines.append(f"ファイル: 全言語統合_テンプレート形式.csv")
    output_lines.append(f"行数: {len(df)}行")
    output_lines.append("")

    vietnamese_only_terms = [
        'けれん', '不安定', '不安定な', '丸セパレーター（丸セパ）',
        '予防', '予防する', '嘔吐', '嘔吐する',
        '基礎型枠（メタルフォー ム）', '墜落', '墜落する', '感電',
        '感電する', '準備', '確認', '確認する',
        '落下', '落下する', '転倒', '転倒する'
    ]

    found = 0
    not_found = 0

    for term in vietnamese_only_terms[:5]:  # 先頭5個だけ確認
        term_row = df[df['ja'] == term]
        if len(term_row) > 0:
            found += 1
            output_lines.append(f"{term}: 存在")
        else:
            not_found += 1
            output_lines.append(f"{term}: 不在")

    output_lines.append("")
    output_lines.append(f"確認結果（先頭5語）: 存在={found}, 不在={not_found}")

else:
    output_lines.append("元のテンプレートCSVが見つかりません")

output_lines.append("")
output_lines.append("=" * 80)

# タイ語順序ソート後のテンプレートCSV
sorted_template = os.path.join(output_dir, '全言語統合_テンプレート形式_タイ語順序.csv')

if os.path.exists(sorted_template):
    df_sorted = pd.read_csv(sorted_template, encoding='utf-8-sig')

    output_lines.append(f"ファイル: 全言語統合_テンプレート形式_タイ語順序.csv")
    output_lines.append(f"行数: {len(df_sorted)}行")
    output_lines.append("")

    found = 0
    not_found = 0

    for term in vietnamese_only_terms[:5]:
        term_row = df_sorted[df_sorted['ja'] == term]
        if len(term_row) > 0:
            found += 1
            output_lines.append(f"{term}: 存在")
        else:
            not_found += 1
            output_lines.append(f"{term}: 不在")

    output_lines.append("")
    output_lines.append(f"確認結果（先頭5語）: 存在={found}, 不在={not_found}")

else:
    output_lines.append("タイ語順序ソート後のテンプレートCSVが見つかりません")

output_lines.append("")
output_lines.append("=" * 80)
output_lines.append("結論")
output_lines.append("=" * 80)
output_lines.append("")

if os.path.exists(original_template) and os.path.exists(sorted_template):
    original_len = len(pd.read_csv(original_template, encoding='utf-8-sig'))
    sorted_len = len(pd.read_csv(sorted_template, encoding='utf-8-sig'))

    output_lines.append(f"元のテンプレート: {original_len}行")
    output_lines.append(f"タイ語順序ソート後: {sorted_len}行")
    output_lines.append(f"差分: {original_len - sorted_len}行")
    output_lines.append("")

    if original_len > sorted_len:
        output_lines.append("タイ語順序ソート時に行が失われています！")
        output_lines.append("")
        output_lines.append("原因:")
        output_lines.append("pandas Categoricalでソートする際、")
        output_lines.append("categoriesに含まれていない値（タイ語データにない日本語）は削除されます。")

# UTF-8でファイルに書き込み
output_file = os.path.join(for_claude_dir, 'original_template_check.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"確認結果を保存: {output_file}")
