"""
逆翻訳結果の確認
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

# Excelファイル読み込み
excel_file = os.path.join(output_dir, '逆翻訳_検証結果.xlsx')

# inputシート
df_input = pd.read_excel(excel_file, sheet_name='input')
# outputシート
df_output = pd.read_excel(excel_file, sheet_name='output')

output_lines = []

output_lines.append("=" * 80)
output_lines.append("逆翻訳結果の確認")
output_lines.append("=" * 80)
output_lines.append("")

output_lines.append(f"inputシート: {len(df_input)}行 x {len(df_input.columns)}列")
output_lines.append(f"outputシート: {len(df_output)}行 x {len(df_output.columns)}列")
output_lines.append("")

# タイ語のサンプル（3-10行目）
output_lines.append("=" * 80)
output_lines.append("タイ語の逆翻訳サンプル（3-10行目）")
output_lines.append("=" * 80)
output_lines.append("")

for i in range(2, min(10, len(df_output))):
    ja = df_input.iloc[i]['ja']
    th_original = df_input.iloc[i]['th']
    th_back = df_output.iloc[i]['th']

    output_lines.append(f"行{i+1}:")
    output_lines.append(f"  日本語: {ja}")
    output_lines.append(f"  タイ語（元）: {repr(th_original)[:100]}")
    output_lines.append(f"  逆翻訳結果: {repr(th_back)[:100]}")
    output_lines.append("")

# CIDコードが含まれているか確認
output_lines.append("=" * 80)
output_lines.append("CIDコードの確認")
output_lines.append("=" * 80)
output_lines.append("")

cid_count = 0
for col in ['en', 'fil-PH', 'zh', 'th', 'vi', 'my', 'id', 'km']:
    col_cid_count = df_output[col].astype(str).str.contains(r'\(cid:', na=False).sum()
    if col_cid_count > 0:
        output_lines.append(f"{col:10s}: {col_cid_count}件のCIDコード検出")
        cid_count += col_cid_count

if cid_count == 0:
    output_lines.append("CIDコードは検出されませんでした")
else:
    output_lines.append("")
    output_lines.append(f"合計: {cid_count}件のCIDコード検出")
    output_lines.append("")
    output_lines.append("問題:")
    output_lines.append("Google Translate APIのレスポンスがHTMLエスケープされている可能性があります。")

output_lines.append("")
output_lines.append("=" * 80)

# UTF-8でファイルに書き込み
output_file = os.path.join(for_claude_dir, 'reverse_translation_check.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"確認結果を保存: {output_file}")
print()
print(f"CIDコード検出数: {cid_count}件")
