"""
テンプレートCSVで雇用保険のkm列を確認
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'
template_csv = os.path.join(output_dir, '全言語統合_テンプレート形式.csv')
check_output = os.path.join(for_claude_dir, 'template_km_check.txt')

output_lines = []

output_lines.append("=" * 80)
output_lines.append("テンプレートCSVで雇用保険のkm列を確認")
output_lines.append("=" * 80)
output_lines.append("")

# CSVを読み込み
df = pd.read_csv(template_csv, encoding='utf-8-sig')

output_lines.append(f"総行数: {len(df)}")
output_lines.append(f"列数: {len(df.columns)}")
output_lines.append("")
output_lines.append("列名一覧:")
output_lines.append(str(df.columns.tolist()))
output_lines.append("")

# 雇用保険の行を抽出
employment_row = df[df['ja'] == '雇用保険']

output_lines.append(f"雇用保険の行数: {len(employment_row)}")
output_lines.append("")

if len(employment_row) > 0:
    row = employment_row.iloc[0]

    output_lines.append("全列の値:")
    output_lines.append("")

    for col in df.columns:
        value = row[col]
        is_empty = pd.isna(value) or str(value).strip() == ''
        status = "[空]" if is_empty else "[有]"
        value_repr = repr(value)[:60] if not is_empty else "(空欄)"

        output_lines.append(f"{status} {col:10s}: {value_repr}")

    output_lines.append("")
    output_lines.append("=" * 80)
    output_lines.append("重要な列の詳細:")
    output_lines.append("=" * 80)
    output_lines.append("")

    target_langs = ['ja', 'en', 'fil-PH', 'zh', 'th', 'vi', 'my', 'id', 'km']

    for lang in target_langs:
        if lang in df.columns:
            value = row[lang]
            is_empty = pd.isna(value) or str(value).strip() == ''
            status = "[空]" if is_empty else "[有]"
            value_repr = repr(value)[:60] if not is_empty else "(空欄)"

            output_lines.append(f"{status} {lang:10s}: {value_repr}")
        else:
            output_lines.append(f"[×] {lang:10s}: 列が存在しない")

else:
    output_lines.append("[情報] 雇用保険の行が見つかりませんでした")

output_lines.append("")
output_lines.append("=" * 80)
output_lines.append("確認完了")
output_lines.append("=" * 80)

# UTF-8でファイルに書き込み
with open(check_output, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"確認結果を保存: {check_output}")
