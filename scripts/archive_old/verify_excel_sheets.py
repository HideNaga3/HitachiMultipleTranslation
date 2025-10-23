"""
Excelファイルの両シートを詳しく確認
"""
import pandas as pd
import os

deliverables_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\成果物_20251023'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

excel_file = os.path.join(deliverables_dir, '02_逆翻訳_検証結果.xlsx')

output_lines = []
output_lines.append("=" * 80)
output_lines.append("逆翻訳Excelファイルの詳細確認")
output_lines.append("=" * 80)
output_lines.append("")

# inputシート
df_input = pd.read_excel(excel_file, sheet_name='input', header=None)
output_lines.append("[inputシート]")
output_lines.append(f"行数: {len(df_input)}行")
output_lines.append(f"列数: {len(df_input.columns)}列")
output_lines.append("")

output_lines.append("1行目（元データの1行目、ヘッダーなし）:")
row1 = df_input.iloc[0]
for i in range(min(10, len(row1))):
    output_lines.append(f"  列{i+1}: {row1[i]}")
output_lines.append(f"  ... (残り{len(row1)-10}列)")

output_lines.append("")
output_lines.append("2行目（元データの2行目）:")
row2 = df_input.iloc[1]
for i in range(min(10, len(row2))):
    output_lines.append(f"  列{i+1}: {row2[i]}")

output_lines.append("")
output_lines.append("")

# outputシート
df_output = pd.read_excel(excel_file, sheet_name='output', header=None)
output_lines.append("[outputシート]")
output_lines.append(f"行数: {len(df_output)}行")
output_lines.append(f"列数: {len(df_output.columns)}列")
output_lines.append("")

output_lines.append("1行目（逆翻訳結果の1行目、ヘッダーなし）:")
row1_out = df_output.iloc[0]
for i in range(min(10, len(row1_out))):
    output_lines.append(f"  列{i+1}: {row1_out[i]}")
output_lines.append(f"  ... (残り{len(row1_out)-10}列)")

output_lines.append("")
output_lines.append("2行目（逆翻訳結果の2行目）:")
row2_out = df_output.iloc[1]
for i in range(min(10, len(row2_out))):
    output_lines.append(f"  列{i+1}: {row2_out[i]}")

output_lines.append("")
output_lines.append("")

# 説明
output_lines.append("=" * 80)
output_lines.append("説明")
output_lines.append("=" * 80)
output_lines.append("")
output_lines.append("【inputシート】")
output_lines.append("  - 各列は元の言語のまま")
output_lines.append("  - 列1: 日本語")
output_lines.append("  - 列2: 英語")
output_lines.append("  - 列3: タガログ語")
output_lines.append("  - 列4以降: 各言語の翻訳")
output_lines.append("")
output_lines.append("【outputシート】")
output_lines.append("  - 各列を日本語に逆翻訳した結果")
output_lines.append("  - 列1: 日本語（そのまま）")
output_lines.append("  - 列2: 英語→日本語")
output_lines.append("  - 列3: タガログ語→日本語")
output_lines.append("  - 列4以降: 各言語→日本語")
output_lines.append("")
output_lines.append("※outputシートは全列が日本語になるのが正しい動作です")
output_lines.append("　これにより、元の翻訳が正確かどうかを比較できます")

output_lines.append("")
output_lines.append("=" * 80)

# ファイルに保存
output_file = os.path.join(for_claude_dir, 'excel_sheets_verification.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"確認結果を保存: {output_file}")
