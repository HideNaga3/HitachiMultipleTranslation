"""
成果物ファイルの実際の内容を確認
"""
import pandas as pd
import os

deliverables_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\成果物_20251023'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

output_lines = []

output_lines.append("=" * 80)
output_lines.append("成果物ファイルの実際の内容確認")
output_lines.append("=" * 80)
output_lines.append("")

# CSVファイルの確認
output_lines.append("[1] CSVファイル - 01_全言語統合_テンプレート_インポート用.csv")
output_lines.append("-" * 80)

csv_file = os.path.join(deliverables_dir, '01_全言語統合_テンプレート_インポート用.csv')
df_csv = pd.read_csv(csv_file, encoding='utf-8-sig')

output_lines.append(f"総行数: {len(df_csv) + 1}行（ヘッダー1行 + データ{len(df_csv)}行）")
output_lines.append(f"列数: {len(df_csv.columns)}列")
output_lines.append("")

output_lines.append("ヘッダー:")
output_lines.append("  " + ", ".join(df_csv.columns.tolist()))
output_lines.append("")

output_lines.append("最初の5行（データ）:")
for idx in range(min(5, len(df_csv))):
    row = df_csv.iloc[idx]
    output_lines.append(f"  行{idx+2}（データ{idx+1}）: {row['ja']}")

output_lines.append("")
output_lines.append("最後の3行（データ）:")
for idx in range(max(0, len(df_csv) - 3), len(df_csv)):
    row = df_csv.iloc[idx]
    output_lines.append(f"  行{idx+2}（データ{idx+1}）: {row['ja']}")

output_lines.append("")
output_lines.append("")

# Excelファイルの確認
output_lines.append("[2] Excelファイル - 02_逆翻訳_検証結果.xlsx")
output_lines.append("-" * 80)

excel_file = os.path.join(deliverables_dir, '02_逆翻訳_検証結果.xlsx')
df_input = pd.read_excel(excel_file, sheet_name='input', header=None)
df_output = pd.read_excel(excel_file, sheet_name='output', header=None)

output_lines.append(f"inputシート: {len(df_input)}行（ヘッダーなし、データのみ）")
output_lines.append(f"outputシート: {len(df_output)}行（ヘッダーなし、データのみ）")
output_lines.append("")

output_lines.append("inputシートの最初の5行:")
for idx in range(min(5, len(df_input))):
    row = df_input.iloc[idx]
    output_lines.append(f"  行{idx+1}: {row[0]}")  # 0列目は日本語

output_lines.append("")

output_lines.append("outputシートの最初の5行:")
for idx in range(min(5, len(df_output))):
    row = df_output.iloc[idx]
    output_lines.append(f"  行{idx+1}: {row[0]}")  # 0列目は日本語

output_lines.append("")

output_lines.append("座標一致確認（最初の3行の日本語列を比較）:")
for idx in range(min(3, len(df_input))):
    input_val = df_input.iloc[idx, 0]
    output_val = df_output.iloc[idx, 0]
    match = "✓" if input_val == output_val else "✗"
    output_lines.append(f"  行{idx+1}: input='{input_val}' vs output='{output_val}' [{match}]")

output_lines.append("")
output_lines.append("")

# サンプルデータの詳細
output_lines.append("[3] サンプルデータ詳細（CSVとExcelの比較）")
output_lines.append("-" * 80)

output_lines.append("CSV 1行目（ヘッダー）:")
output_lines.append("  " + ", ".join(df_csv.columns.tolist()))
output_lines.append("")

output_lines.append("CSV 2行目（データ1行目）:")
row1_csv = df_csv.iloc[0]
for col in df_csv.columns:
    output_lines.append(f"  {col}: {row1_csv[col]}")
output_lines.append("")

output_lines.append("Excel inputシート 1行目（データ、ヘッダーなし）:")
row1_excel_input = df_input.iloc[0]
for idx, val in enumerate(row1_excel_input):
    col_name = df_csv.columns[idx] if idx < len(df_csv.columns) else f"列{idx}"
    output_lines.append(f"  {col_name}: {val}")
output_lines.append("")

output_lines.append("Excel outputシート 1行目（逆翻訳結果、ヘッダーなし）:")
row1_excel_output = df_output.iloc[0]
for idx, val in enumerate(row1_excel_output):
    col_name = df_csv.columns[idx] if idx < len(df_csv.columns) else f"列{idx}"
    output_lines.append(f"  {col_name}: {val}")

output_lines.append("")
output_lines.append("=" * 80)
output_lines.append("確認完了")
output_lines.append("=" * 80)

# ファイルに保存
output_file = os.path.join(for_claude_dir, 'file_content_verification.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

# コンソールにも出力
for line in output_lines:
    print(line)

print()
print(f"確認結果を保存: {output_file}")
