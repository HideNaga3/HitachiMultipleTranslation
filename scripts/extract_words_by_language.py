"""
国（言語）ごとに翻訳が必要な日本語単語を抽出するスクリプト

各言語で翻訳が空欄の日本語単語をリストアップし、
言語ごとにCSVファイルとして出力します。
"""

import pandas as pd
import os

# CSVファイルを読み込み
csv_path = 'output/全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("国（言語）ごとに翻訳が必要な日本語単語を抽出")
print("=" * 80)
print()

# 出力ディレクトリを作成
output_dir = 'for_claude/words_to_translate'
os.makedirs(output_dir, exist_ok=True)

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

# 各言語について処理
for lang_code, lang_name in languages.items():
    # 該当言語が空欄の行を抽出
    empty_rows = df[df[lang_code].isna()]

    if len(empty_rows) > 0:
        # 日本語単語のリストを取得
        japanese_words = empty_rows['ja'].tolist()

        # 行番号も取得（CSVの実際の行番号 = インデックス + 2）
        row_numbers = [idx + 2 for idx in empty_rows.index]

        # DataFrameを作成
        output_df = pd.DataFrame({
            'CSV行番号': row_numbers,
            '日本語': japanese_words
        })

        # CSVファイルに保存
        output_file = os.path.join(output_dir, f'{lang_code}_{lang_name}_翻訳必要単語.csv')
        output_df.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"{lang_name} ({lang_code}): {len(japanese_words)}語")
        print(f"  → {output_file}")
        print()

        # テキストファイルにも保存（見やすい形式）
        txt_file = os.path.join(output_dir, f'{lang_code}_{lang_name}_翻訳必要単語.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"{lang_name} ({lang_code}) - 翻訳が必要な日本語単語\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"総数: {len(japanese_words)}語\n\n")
            f.write("-" * 80 + "\n")

            for i, (row_num, word) in enumerate(zip(row_numbers, japanese_words), 1):
                f.write(f"{i:3d}. [行{row_num}] {word}\n")

        print(f"  → {txt_file}")
        print()
    else:
        print(f"{lang_name} ({lang_code}): 翻訳が必要な単語はありません（全て翻訳済み）")
        print()

print("=" * 80)
print(f"全ての抽出結果を {output_dir}/ に保存しました")
print("=" * 80)
