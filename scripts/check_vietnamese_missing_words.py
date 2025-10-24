"""
ベトナム語に無い12語が他の言語ではどうなっているかを確認するスクリプト
"""

import pandas as pd
import sys

# 出力先をファイルに変更
output_file = 'for_claude/vietnamese_missing_words_check.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

# CSVファイルを読み込み
csv_path = 'output/全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("ベトナム語に無い12語の確認")
print("=" * 80)
print()

# ベトナム語のみ空欄の単語を抽出
vi_empty = df[df['vi'].isna()]

print(f"ベトナム語が空欄の単語: {len(vi_empty)} 語")
print()

# 各単語について詳細確認
languages = ['en', 'fil-PH', 'zh', 'th', 'my', 'id', 'km']
lang_names = {
    'en': '英語',
    'fil-PH': 'タガログ語',
    'zh': '中国語',
    'th': 'タイ語',
    'my': 'ミャンマー語',
    'id': 'インドネシア語',
    'km': 'カンボジア語'
}

for idx, row in vi_empty.iterrows():
    csv_row = idx + 2
    ja_word = row['ja']

    print("-" * 80)
    print(f"[CSV行{csv_row}] {ja_word}")
    print("-" * 80)

    # 各言語での状況を確認
    for lang_code in languages:
        lang_name = lang_names[lang_code]
        value = row[lang_code]

        if pd.isna(value):
            status = "✗ 空欄"
        else:
            status = f"✓ あり: {value[:50]}..."  # 最初の50文字

        print(f"  {lang_name:<15}: {status}")

    print()

# サマリー
print("=" * 80)
print("サマリー")
print("=" * 80)
print()

print("ベトナム語に無い12語の分類:")
print()

# 全言語で空欄の単語
all_empty_words = []
# 一部の言語にある単語
some_exist_words = []

for idx, row in vi_empty.iterrows():
    ja_word = row['ja']
    csv_row = idx + 2

    # 他の7言語のいずれかに翻訳があるか確認
    has_translation = False
    for lang_code in languages:
        if pd.notna(row[lang_code]):
            has_translation = True
            break

    if has_translation:
        some_exist_words.append((csv_row, ja_word))
    else:
        all_empty_words.append((csv_row, ja_word))

print(f"1. 他の言語でも全て空欄: {len(all_empty_words)} 語")
if all_empty_words:
    for csv_row, word in all_empty_words:
        print(f"   - [CSV行{csv_row}] {word}")
print()

print(f"2. 他の言語には翻訳がある: {len(some_exist_words)} 語")
if some_exist_words:
    for csv_row, word in some_exist_words:
        print(f"   - [CSV行{csv_row}] {word}")
print()

# ベトナム語特有の表記パターンを確認
print("=" * 80)
print("ベトナム語が空欄の単語の特徴")
print("=" * 80)
print()

# 括弧付きの単語
with_brackets = [row['ja'] for idx, row in vi_empty.iterrows() if '（' in row['ja']]
print(f"括弧付き表記: {len(with_brackets)} 語")
for word in with_brackets:
    csv_row = df[df['ja'] == word].index[0] + 2
    print(f"   - [CSV行{csv_row}] {word}")
print()

# 括弧なしの単語
without_brackets = [row['ja'] for idx, row in vi_empty.iterrows() if '（' not in row['ja']]
print(f"括弧なし表記: {len(without_brackets)} 語")
for word in without_brackets:
    csv_row = df[df['ja'] == word].index[0] + 2
    print(f"   - [CSV行{csv_row}] {word}")
print()

print("=" * 80)

# ファイルを閉じる
sys.stdout.close()
print("結果を for_claude/vietnamese_missing_words_check.txt に保存しました", file=sys.__stdout__)
