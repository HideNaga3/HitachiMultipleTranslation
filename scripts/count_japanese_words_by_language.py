"""
各言語で翻訳が必要な「日本語単語」の数を集計するスクリプト

つまり、各言語で空欄になっている行の日本語単語を数えます。
"""

import pandas as pd

# CSVファイルを読み込み
csv_path = 'output/全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("各言語で翻訳が必要な日本語単語の数")
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

# 結果を格納するリスト
results = []

print(f"{'言語名':<15} {'コード':<10} {'翻訳が必要な日本語単語数':>25}")
print("-" * 80)

for lang_code, lang_name in languages.items():
    # 該当言語が空欄の行を抽出
    empty_rows = df[df[lang_code].isna()]

    # その行の日本語単語を取得
    japanese_words = empty_rows['ja'].tolist()

    # 単語数
    word_count = len(japanese_words)

    results.append({
        '言語名': lang_name,
        '言語コード': lang_code,
        '翻訳が必要な日本語単語数': word_count
    })

    print(f"{lang_name:<15} {lang_code:<10} {word_count:>25} 語")

print()
print("=" * 80)
print("詳細リスト")
print("=" * 80)
print()

for lang_code, lang_name in languages.items():
    # 該当言語が空欄の行を抽出
    empty_rows = df[df[lang_code].isna()]

    if len(empty_rows) > 0:
        # その行の日本語単語を取得
        japanese_words = empty_rows['ja'].tolist()

        print(f"【{lang_name} ({lang_code})】 {len(japanese_words)} 語")
        print("-" * 80)

        for i, word in enumerate(japanese_words, 1):
            print(f"  {i:2d}. {word}")

        print()

print("=" * 80)

# CSVファイルに保存
output_df = pd.DataFrame(results)
output_path = 'for_claude/japanese_words_count_by_language.csv'
output_df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"結果を {output_path} に保存しました")
print("=" * 80)
