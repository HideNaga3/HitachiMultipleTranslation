"""
翻訳が必要な全ての日本語単語のユニークリストを作成し、
インポート用CSVに存在するか確認するスクリプト
"""

import pandas as pd

# CSVファイルを読み込み
csv_path = 'output/全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("翻訳が必要な日本語単語のユニークリスト作成")
print("=" * 80)
print()

# 言語リスト（日本語を除く）
languages = {
    'en': '英語',
    'fil-PH': 'タガログ語',
    'zh': '中国語',
    'th': 'タイ語',
    'vi': 'ベトナム語',
    'my': 'ミャンマー語',
    'id': 'インドネシア語',
    'km': 'カンボジア語'
}

# 全ての空欄の日本語単語を収集
all_empty_words = set()
word_language_map = {}  # 単語 -> どの言語で空欄か

for lang_code, lang_name in languages.items():
    # 該当言語が空欄の行を抽出
    empty_rows = df[df[lang_code].isna()]

    # その行の日本語単語を取得
    japanese_words = empty_rows['ja'].tolist()

    for word in japanese_words:
        all_empty_words.add(word)

        if word not in word_language_map:
            word_language_map[word] = []
        word_language_map[word].append(lang_name)

# ソートしてリスト化
unique_words = sorted(list(all_empty_words))

print(f"ユニークな日本語単語数: {len(unique_words)} 語")
print()

# インポート用CSVに存在するか確認
print("-" * 80)
print("インポート用CSVでの存在確認")
print("-" * 80)
print()

all_japanese_words = df['ja'].tolist()
results = []

for i, word in enumerate(unique_words, 1):
    exists = word in all_japanese_words

    if exists:
        # CSVでの行番号を取得
        row_index = df[df['ja'] == word].index[0]
        csv_row = row_index + 2  # ヘッダー行を考慮
    else:
        csv_row = None

    # どの言語で空欄か
    empty_in_languages = word_language_map.get(word, [])
    empty_count = len(empty_in_languages)

    results.append({
        '番号': i,
        '日本語': word,
        'CSV存在': 'あり' if exists else 'なし',
        'CSV行番号': csv_row if exists else '-',
        '空欄言語数': empty_count,
        '空欄の言語': '、'.join(empty_in_languages)
    })

    status = 'OK' if exists else 'NG'
    print(f"{i:2d}. [{status}] {word:<30} (CSV行{csv_row if exists else '-':>4}, {empty_count}言語で空欄)")

print()
print("=" * 80)
print("結果サマリー")
print("=" * 80)
print()

exists_count = sum(1 for r in results if r['CSV存在'] == 'あり')
not_exists_count = sum(1 for r in results if r['CSV存在'] == 'なし')

print(f"総ユニーク単語数: {len(unique_words)} 語")
print(f"CSV内に存在: {exists_count} 語")
print(f"CSV内に不在: {not_exists_count} 語")
print()

if not_exists_count > 0:
    print("警告: CSV内に存在しない単語があります")
    for r in results:
        if r['CSV存在'] == 'なし':
            print(f"  - {r['日本語']}")
    print()
else:
    print("確認完了: 全ての単語がCSV内に存在します")
    print()

# 結果をCSVファイルに保存
output_df = pd.DataFrame(results)
output_path = 'for_claude/unique_words_to_translate.csv'
output_df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"結果を {output_path} に保存しました")

# テキストファイルにも保存（見やすい形式）
txt_path = 'for_claude/unique_words_to_translate.txt'
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("翻訳が必要な日本語単語のユニークリスト\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"総数: {len(unique_words)} 語\n\n")

    for r in results:
        f.write(f"{r['番号']:2d}. {r['日本語']:<30} [CSV行{r['CSV行番号']:>4}] ({r['空欄言語数']}言語)\n")
        f.write(f"    空欄の言語: {r['空欄の言語']}\n\n")

print(f"詳細を {txt_path} に保存しました")
print("=" * 80)
