"""
翻訳データ数の妥当性確認
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

# 各種CSVファイル
unified_csv = os.path.join(output_dir, '全言語統合_比較用.csv')
template_csv = os.path.join(output_dir, '全言語統合_テンプレート形式.csv')
template_count_csv = os.path.join(output_dir, '全言語統合_テンプレート形式_翻訳数付き.csv')

output_file = os.path.join(for_claude_dir, 'translation_count_validation.txt')

output_lines = []

output_lines.append("=" * 80)
output_lines.append("翻訳データ数の妥当性確認")
output_lines.append("=" * 80)
output_lines.append("")

# 1. 個別CSVの行数確認
output_lines.append("【1. 個別CSVファイルの行数】")
output_lines.append("")

individual_files = [
    '英語_pdfplumber_抽出_最終版.csv',
    'タガログ語_pdfplumber_抽出_最終版.csv',
    'カンボジア語_pdfplumber_抽出_最終版.csv',
    '中国語_pdfplumber_抽出_最終版.csv',
    'インドネシア語_pdfplumber_抽出_最終版.csv',
    'ミャンマー語_pdfplumber_抽出_最終版.csv',
    'タイ語_pdfplumber_抽出_最終版.csv',
    'ベトナム語_pdfplumber_抽出_最終版.csv',
]

total_individual_rows = 0
for filename in individual_files:
    filepath = os.path.join(output_dir, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        row_count = len(df)
        total_individual_rows += row_count
        output_lines.append(f"  {filename:45s}: {row_count:4d}行")
    else:
        output_lines.append(f"  {filename:45s}: ファイルなし")

output_lines.append("")
output_lines.append(f"個別CSV合計: {total_individual_rows}行")
output_lines.append("")

# 2. 統合CSVの確認
output_lines.append("【2. 統合CSV（比較用）】")
output_lines.append("")

unified_df = pd.read_csv(unified_csv, encoding='utf-8-sig')
output_lines.append(f"総行数: {len(unified_df)}行")
output_lines.append(f"列数: {len(unified_df.columns)}列")
output_lines.append("")

# 言語別行数
lang_counts = unified_df['言語'].value_counts()
output_lines.append("言語別行数:")
for lang, count in lang_counts.items():
    output_lines.append(f"  {lang:15s}: {count:4d}行")

output_lines.append("")

# 妥当性チェック1: 個別CSV合計 == 統合CSV総行数
is_valid_1 = (total_individual_rows == len(unified_df))
status_1 = "✓ 一致" if is_valid_1 else "✗ 不一致"
output_lines.append(f"【妥当性チェック1】個別CSV合計 vs 統合CSV総行数")
output_lines.append(f"  個別CSV合計: {total_individual_rows}行")
output_lines.append(f"  統合CSV総行数: {len(unified_df)}行")
output_lines.append(f"  結果: {status_1}")
output_lines.append("")

# 3. テンプレート形式CSVの確認
output_lines.append("【3. テンプレート形式CSV】")
output_lines.append("")

template_df = pd.read_csv(template_csv, encoding='utf-8-sig')
output_lines.append(f"総行数: {len(template_df)}行")
output_lines.append(f"列数: {len(template_df.columns)}列")
output_lines.append("")

# 日本語のユニーク数
unique_japanese = unified_df['日本語'].nunique()
output_lines.append(f"統合CSVのユニーク日本語数: {unique_japanese}個")
output_lines.append("")

# 妥当性チェック2: テンプレート行数 == ユニーク日本語数
is_valid_2 = (len(template_df) == unique_japanese)
status_2 = "✓ 一致" if is_valid_2 else "✗ 不一致"
output_lines.append(f"【妥当性チェック2】テンプレート行数 vs ユニーク日本語数")
output_lines.append(f"  テンプレート行数: {len(template_df)}行")
output_lines.append(f"  ユニーク日本語数: {unique_japanese}個")
output_lines.append(f"  結果: {status_2}")
output_lines.append("")

# 4. 翻訳数付きCSVの確認
output_lines.append("【4. 翻訳数付きCSV】")
output_lines.append("")

template_count_df = pd.read_csv(template_count_csv, encoding='utf-8-sig')
output_lines.append(f"総行数: {len(template_count_df)}行")
output_lines.append(f"列数: {len(template_count_df.columns)}列")
output_lines.append("")

# 妥当性チェック3: テンプレートCSV == 翻訳数付きCSV
is_valid_3 = (len(template_df) == len(template_count_df))
status_3 = "✓ 一致" if is_valid_3 else "✗ 不一致"
output_lines.append(f"【妥当性チェック3】テンプレートCSV vs 翻訳数付きCSV")
output_lines.append(f"  テンプレートCSV: {len(template_df)}行")
output_lines.append(f"  翻訳数付きCSV: {len(template_count_df)}行")
output_lines.append(f"  結果: {status_3}")
output_lines.append("")

# 5. 翻訳言語数の分布確認
output_lines.append("【5. 翻訳言語数の分布】")
output_lines.append("")

if '翻訳言語数' in template_count_df.columns:
    count_distribution = template_count_df['翻訳言語数'].value_counts().sort_index(ascending=False)

    for count, num_rows in count_distribution.items():
        percentage = (num_rows / len(template_count_df)) * 100
        output_lines.append(f"  {count}言語: {num_rows:4d}行 ({percentage:5.1f}%)")

    output_lines.append("")

    # 統計
    max_count = template_count_df['翻訳言語数'].max()
    min_count = template_count_df['翻訳言語数'].min()
    avg_count = template_count_df['翻訳言語数'].mean()

    output_lines.append(f"最大: {max_count}言語")
    output_lines.append(f"最小: {min_count}言語")
    output_lines.append(f"平均: {avg_count:.2f}言語")
else:
    output_lines.append("翻訳言語数列が見つかりません")

output_lines.append("")

# 6. 8言語の翻訳データ数確認
output_lines.append("【6. 8言語の翻訳データ総数】")
output_lines.append("")

target_langs = ['en', 'fil-PH', 'zh', 'th', 'vi', 'my', 'id', 'km']

def is_empty_value(value):
    if pd.isna(value):
        return True
    if isinstance(value, str):
        cleaned = str(value).strip()
        return cleaned == '' or cleaned.lower() == 'nan'
    return False

lang_translation_counts = {}
for lang in target_langs:
    if lang in template_count_df.columns:
        non_empty = sum(~template_count_df[lang].apply(is_empty_value))
        lang_translation_counts[lang] = non_empty
        output_lines.append(f"  {lang:10s}: {non_empty:4d}件")

output_lines.append("")

total_translations = sum(lang_translation_counts.values())
expected_translations = len(template_count_df) * len(target_langs)

output_lines.append(f"翻訳データ総数: {total_translations}件")
output_lines.append(f"期待値（524 x 8）: {expected_translations}件")
output_lines.append(f"充足率: {(total_translations / expected_translations * 100):.2f}%")
output_lines.append("")

# 妥当性チェック4: 翻訳データ総数
shortage = expected_translations - total_translations
output_lines.append(f"【妥当性チェック4】翻訳データ総数")
output_lines.append(f"  翻訳データ総数: {total_translations}件")
output_lines.append(f"  期待値: {expected_translations}件")
output_lines.append(f"  不足: {shortage}件")
output_lines.append("")

# 7. 総合評価
output_lines.append("=" * 80)
output_lines.append("総合評価")
output_lines.append("=" * 80)
output_lines.append("")

all_checks = [is_valid_1, is_valid_2, is_valid_3]
passed_checks = sum(all_checks)

output_lines.append(f"チェック項目: {len(all_checks)}件")
output_lines.append(f"合格: {passed_checks}件")
output_lines.append(f"不合格: {len(all_checks) - passed_checks}件")
output_lines.append("")

if all(all_checks):
    output_lines.append("✓ すべての妥当性チェックに合格しました")
else:
    output_lines.append("✗ 一部の妥当性チェックに不合格がありました")
    output_lines.append("")
    output_lines.append("不合格の項目:")
    if not is_valid_1:
        output_lines.append("  - チェック1: 個別CSV合計 vs 統合CSV総行数")
    if not is_valid_2:
        output_lines.append("  - チェック2: テンプレート行数 vs ユニーク日本語数")
    if not is_valid_3:
        output_lines.append("  - チェック3: テンプレートCSV vs 翻訳数付きCSV")

output_lines.append("")
output_lines.append("=" * 80)
output_lines.append("確認完了")
output_lines.append("=" * 80)

# UTF-8でファイルに書き込み
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"検証結果を保存: {output_file}")
print()
print("=" * 80)
print("簡易サマリー")
print("=" * 80)
print(f"個別CSV合計: {total_individual_rows}行")
print(f"統合CSV総行数: {len(unified_df)}行")
print(f"テンプレート行数: {len(template_df)}行")
print(f"ユニーク日本語数: {unique_japanese}個")
print(f"翻訳データ総数: {total_translations}件 / {expected_translations}件 ({(total_translations / expected_translations * 100):.2f}%)")
print(f"妥当性チェック: {passed_checks}/{len(all_checks)} 合格")
print("=" * 80)
