"""
翻訳が必要な全37語が、インポート用CSVのカテゴリー内に存在するか確認するスクリプト

カテゴリーとは、元のCSVの「番号」列や分類を指すと仮定します。
まずはCSVの全体構造を確認します。
"""

import pandas as pd

# CSVファイルを読み込み
csv_path = 'output/全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("CSV構造の確認")
print("=" * 80)
print()

# 列名を表示
print("列名:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")
print()

# 最初の5行を表示（日本語列のみ）
print("最初の5行（日本語列のみ）:")
print(df[['ja']].head())
print()

# CSVに「カテゴリ」や「分類」に相当する列があるか確認
potential_category_cols = []
for col in df.columns:
    if any(keyword in col.lower() for keyword in ['カテゴリ', 'category', '分類', '種別', 'type', 'group']):
        potential_category_cols.append(col)

if potential_category_cols:
    print("カテゴリーに関連する列:")
    for col in potential_category_cols:
        print(f"  - {col}")
        print(f"    ユニーク値: {df[col].nunique()}")
        print(f"    値の例: {df[col].dropna().unique()[:5]}")
        print()
else:
    print("カテゴリーに関連する列は見つかりませんでした")
    print()

print("=" * 80)
print("翻訳が必要な37語の確認")
print("=" * 80)
print()

# 翻訳が必要な37語のユニークリストを読み込み
unique_words_df = pd.read_csv('for_claude/unique_words_to_translate.csv', encoding='utf-8-sig')
unique_words = unique_words_df['日本語'].tolist()

print(f"翻訳が必要な単語数: {len(unique_words)} 語")
print()

# 各単語がCSVに存在するか、どの行にあるかを確認
print("各単語の存在確認:")
print("-" * 80)

for i, word in enumerate(unique_words, 1):
    # CSVで該当する行を検索
    matching_rows = df[df['ja'] == word]

    if len(matching_rows) > 0:
        row_index = matching_rows.index[0]
        csv_row = row_index + 2  # ヘッダーを考慮

        # 該当行の情報を取得
        ja_value = matching_rows.iloc[0]['ja']

        print(f"{i:2d}. {word:<30} [CSV行{csv_row:>4}] ✓")

        # もし他の列に有用な情報があれば表示
        # 例: 番号、分類などがあれば
    else:
        print(f"{i:2d}. {word:<30} [CSV行 なし] ✗")

print()
print("=" * 80)
print("結論")
print("=" * 80)
print()

exists_count = sum(1 for word in unique_words if word in df['ja'].values)
print(f"CSV内に存在: {exists_count} / {len(unique_words)} 語")

if exists_count == len(unique_words):
    print("✓ 全ての単語がCSV内に存在します")
else:
    print("✗ 一部の単語がCSV内に存在しません")

print()
print("=" * 80)
