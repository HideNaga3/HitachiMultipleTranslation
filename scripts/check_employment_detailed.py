"""
雇用保険のth, km列の詳細確認（バイトレベル）
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'
template_csv = os.path.join(output_dir, '全言語統合_テンプレート形式_翻訳数付き.csv')
detail_output = os.path.join(for_claude_dir, 'employment_detail.txt')

def is_empty_value(value):
    """check_missing_languages.pyと同じロジック"""
    if pd.isna(value):
        return True
    if isinstance(value, str):
        cleaned = str(value).strip()
        return cleaned == '' or cleaned.lower() == 'nan'
    return False

output_lines = []

output_lines.append("=" * 80)
output_lines.append("雇用保険のth, km列の詳細確認")
output_lines.append("=" * 80)
output_lines.append("")

# CSVを読み込み
df = pd.read_csv(template_csv, encoding='utf-8-sig')

# 雇用保険の行を抽出
employment_row = df[df['ja'] == '雇用保険']

if len(employment_row) > 0:
    row = employment_row.iloc[0]

    output_lines.append("【タイ語 (th) 列の詳細】")
    output_lines.append("")

    th_value = row['th']
    output_lines.append(f"  型: {type(th_value)}")
    output_lines.append(f"  pd.isna(): {pd.isna(th_value)}")
    output_lines.append(f"  repr(): {repr(th_value)}")
    output_lines.append(f"  長さ: {len(str(th_value)) if not pd.isna(th_value) else 'N/A'}")

    if not pd.isna(th_value):
        th_str = str(th_value)
        output_lines.append(f"  strip後: {repr(th_str.strip())}")
        output_lines.append(f"  strip後長さ: {len(th_str.strip())}")
        output_lines.append(f"  lower(): {repr(th_str.lower())}")
        output_lines.append(f"  バイト: {th_str.encode('utf-8')[:100]}")

    output_lines.append(f"  is_empty_value(): {is_empty_value(th_value)}")
    output_lines.append("")

    output_lines.append("【カンボジア語 (km) 列の詳細】")
    output_lines.append("")

    km_value = row['km']
    output_lines.append(f"  型: {type(km_value)}")
    output_lines.append(f"  pd.isna(): {pd.isna(km_value)}")
    output_lines.append(f"  repr(): {repr(km_value)}")
    output_lines.append(f"  長さ: {len(str(km_value)) if not pd.isna(km_value) else 'N/A'}")

    if not pd.isna(km_value):
        km_str = str(km_value)
        output_lines.append(f"  strip後: {repr(km_str.strip())}")
        output_lines.append(f"  strip後長さ: {len(km_str.strip())}")
        output_lines.append(f"  lower(): {repr(km_str.lower())}")
        output_lines.append(f"  バイト: {km_str.encode('utf-8')[:100]}")

    output_lines.append(f"  is_empty_value(): {is_empty_value(km_value)}")
    output_lines.append("")

    output_lines.append("【翻訳言語数列の値】")
    output_lines.append("")
    count_value = row['翻訳言語数']
    output_lines.append(f"  値: {count_value}")
    output_lines.append(f"  型: {type(count_value)}")
    output_lines.append("")

    # 全8言語の値確認
    output_lines.append("【全8言語の is_empty_value() 結果】")
    output_lines.append("")
    target_langs = ['en', 'fil-PH', 'zh', 'th', 'vi', 'my', 'id', 'km']

    empty_count = 0
    for lang in target_langs:
        if lang in df.columns:
            value = row[lang]
            is_empty = is_empty_value(value)
            if is_empty:
                empty_count += 1
            status = "[空]" if is_empty else "[有]"
            output_lines.append(f"  {status} {lang:10s}: is_empty={is_empty}")
        else:
            output_lines.append(f"  [?] {lang:10s}: 列が存在しない")

    output_lines.append("")
    output_lines.append(f"空欄判定された言語数: {empty_count}")
    output_lines.append(f"翻訳ありと判定された言語数: {8 - empty_count}")

else:
    output_lines.append("[エラー] 雇用保険の行が見つかりませんでした")

output_lines.append("")
output_lines.append("=" * 80)
output_lines.append("確認完了")
output_lines.append("=" * 80)

# UTF-8でファイルに書き込み
with open(detail_output, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"詳細確認結果を保存: {detail_output}")
