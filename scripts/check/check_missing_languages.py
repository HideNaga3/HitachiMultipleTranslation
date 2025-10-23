"""
翻訳が8言語未満の単語について、欠けている言語を確認
"""
import pandas as pd
import os

def is_empty_value(value):
    """値が空かどうか判定"""
    if pd.isna(value):
        return True
    if isinstance(value, str):
        cleaned = str(value).strip()
        return cleaned == '' or cleaned.lower() == 'nan'
    return False

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
template_csv = os.path.join(output_dir, '全言語統合_テンプレート形式_翻訳数付き.csv')

print("=" * 80)
print("翻訳が不完全な単語の欠損言語確認")
print("=" * 80)
print()

# CSVを読み込み
df = pd.read_csv(template_csv, encoding='utf-8-sig')

# 翻訳列（ja以外、翻訳言語数列を除く）
translation_columns = [col for col in df.columns if col not in ['ja', '翻訳言語数']]

# 8言語の翻訳列（実際にデータがある言語）
target_langs = ['en', 'fil-PH', 'zh', 'th', 'vi', 'my', 'id', 'km']

print(f"対象言語（8言語）: {', '.join(target_langs)}")
print()

# 翻訳数が6または7の行を抽出
incomplete_rows = df[(df['翻訳言語数'] >= 6) & (df['翻訳言語数'] < 8)]

print(f"翻訳が不完全な単語: {len(incomplete_rows)}個")
print()

if len(incomplete_rows) > 0:
    print("=" * 80)
    print("詳細情報")
    print("=" * 80)
    print()

    for idx, row in incomplete_rows.iterrows():
        japanese = row['ja']
        count = int(row['翻訳言語数'])

        # 翻訳がある言語とない言語を分類
        has_translation = []
        missing_translation = []

        for lang in target_langs:
            if not is_empty_value(row[lang]):
                has_translation.append(lang)
            else:
                missing_translation.append(lang)

        print(f"【{japanese}】 ({count}言語)")
        print(f"  [O] 翻訳あり: {', '.join(has_translation)}")
        print(f"  [X] 翻訳なし: {', '.join(missing_translation)}")
        print()

    # 欠損言語の統計
    print("=" * 80)
    print("欠損言語の統計")
    print("=" * 80)
    print()

    missing_count = {}
    for lang in target_langs:
        missing_count[lang] = 0

    for idx, row in incomplete_rows.iterrows():
        for lang in target_langs:
            if is_empty_value(row[lang]):
                missing_count[lang] += 1

    print("言語別の欠損回数:")
    for lang in sorted(missing_count.items(), key=lambda x: x[1], reverse=True):
        lang_code, count = lang
        if count > 0:
            print(f"  {lang_code:10s}: {count}回")

else:
    print("[情報] 全ての単語が8言語に翻訳されています")

print()
print("=" * 80)
print("確認完了")
print("=" * 80)
