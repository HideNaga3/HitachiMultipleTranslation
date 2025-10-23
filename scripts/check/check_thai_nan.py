"""
タイ語CSVの日本語列のNaN（空欄）を確認
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

# タイ語CSV読み込み
thai_csv = os.path.join(output_dir, 'タイ語_pdfplumber_抽出_最終版.csv')
thai_df = pd.read_csv(thai_csv, encoding='utf-8-sig')

output_lines = []

output_lines.append("=" * 80)
output_lines.append("タイ語CSVの日本語列NaN確認")
output_lines.append("=" * 80)
output_lines.append("")

output_lines.append(f"総行数: {len(thai_df)}行")
output_lines.append("")

# 列名確認
output_lines.append("列名:")
for i, col in enumerate(thai_df.columns, 1):
    output_lines.append(f"  {i}. {col}")
output_lines.append("")

# 日本語列の確認（列名が「単語」の可能性）
if '日本語' in thai_df.columns:
    jp_col = '日本語'
elif '単語' in thai_df.columns:
    jp_col = '単語'
else:
    output_lines.append("エラー: 日本語列が見つかりません")
    jp_col = None

if jp_col:
    output_lines.append(f"日本語列: '{jp_col}'")
    output_lines.append("")

    # NaNの確認
    nan_count = thai_df[jp_col].isna().sum()
    empty_count = (thai_df[jp_col].astype(str).str.strip() == '').sum()

    output_lines.append(f"NaN（欠損値）の数: {nan_count}行")
    output_lines.append(f"空文字列の数: {empty_count}行")
    output_lines.append("")

    if nan_count > 0 or empty_count > 0:
        output_lines.append("=" * 80)
        output_lines.append("NaN・空欄の詳細（全件表示）")
        output_lines.append("=" * 80)
        output_lines.append("")

        # NaNまたは空欄の行を抽出
        nan_rows = thai_df[thai_df[jp_col].isna() | (thai_df[jp_col].astype(str).str.strip() == '')]

        for idx, row in nan_rows.iterrows():
            page = row.get('Page', row.get('ページ', 'N/A'))
            number = row.get('番号', row.get('No.', 'N/A'))
            jp = row[jp_col]
            translation = row.get('翻訳', 'N/A')

            # 翻訳があるかチェック
            has_translation = pd.notna(translation) and str(translation).strip() != ''

            output_lines.append(f"行{idx}: Page={page}, No={number}")
            output_lines.append(f"  日本語: {repr(jp)}")
            output_lines.append(f"  翻訳: {'あり' if has_translation else '空欄'}")
            if has_translation:
                output_lines.append(f"  翻訳内容: {str(translation)[:50]}")

            # 前後の行も確認
            if idx > 0:
                prev_jp = thai_df.iloc[idx - 1][jp_col]
                output_lines.append(f"  前行の日本語: {prev_jp}")

            output_lines.append("")

    else:
        output_lines.append("✓ NaN・空欄はありません")

output_lines.append("=" * 80)
output_lines.append("確認完了")
output_lines.append("=" * 80)

# UTF-8でファイルに書き込み
output_file = os.path.join(for_claude_dir, 'thai_nan_check.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"確認結果を保存: {output_file}")
print()

if jp_col:
    print(f"日本語列: '{jp_col}'")
    print(f"NaN数: {nan_count}行")
    print(f"空文字列数: {empty_count}行")
