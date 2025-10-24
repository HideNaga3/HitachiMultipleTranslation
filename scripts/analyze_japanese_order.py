"""
日本語単語列の並び順を分析するスクリプト

以下を調査：
1. 現在の並び順の規則性（五十音順、CSV行番号順、カテゴリー順など）
2. 並び替えの基準となる情報があるか
3. Pandasのカテゴリー型での並び替えが必要か
"""

import pandas as pd
import sys

# 出力先をファイルに変更
output_file = 'for_claude/japanese_order_analysis.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

# CSVファイルを読み込み
csv_path = 'output/全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("日本語単語列の並び順分析")
print("=" * 80)
print()

# 最初の30語を表示
print("最初の30語:")
print("-" * 80)
for i in range(min(30, len(df))):
    print(f"{i+1:3d}. [行{i+2:3d}] {df.iloc[i]['ja']}")
print()

# 五十音順かどうかチェック
print("=" * 80)
print("五十音順チェック")
print("=" * 80)
print()

ja_words = df['ja'].tolist()
sorted_ja_words = sorted(ja_words)

# 元の順序と五十音順を比較
is_sorted = ja_words == sorted_ja_words

if is_sorted:
    print("✓ 完全に五十音順です")
else:
    print("✗ 五十音順ではありません")
    print()
    print("五十音順との違い（最初の10件）:")
    print("-" * 80)
    for i in range(min(10, len(ja_words))):
        original = ja_words[i]
        sorted_word = sorted_ja_words[i]
        if original != sorted_word:
            print(f"  行{i+2}: 実際={original:<30} 五十音順={sorted_word}")

print()

# ユニークな翻訳が必要な37語の並び順を確認
print("=" * 80)
print("翻訳が必要な37語の並び順")
print("=" * 80)
print()

unique_words_df = pd.read_csv('for_claude/unique_words_to_translate.csv', encoding='utf-8-sig')
unique_words = unique_words_df['日本語'].tolist()
csv_rows = unique_words_df['CSV行番号'].tolist()

print("現在の並び順（五十音順）:")
print("-" * 80)
for i, (word, row) in enumerate(zip(unique_words, csv_rows), 1):
    print(f"{i:2d}. [CSV行{row:>3}] {word}")

print()

# CSV行番号順に並べ替えた場合
print("CSV行番号順に並べ替えた場合:")
print("-" * 80)

sorted_by_row = unique_words_df.sort_values('CSV行番号')
for i, row in enumerate(sorted_by_row.itertuples(), 1):
    print(f"{i:2d}. [CSV行{row.CSV行番号:>3}] {row.日本語}")

print()

# 空欄言語数でグループ化
print("=" * 80)
print("空欄言語数でグループ化")
print("=" * 80)
print()

sorted_by_empty = unique_words_df.sort_values(['空欄言語数', 'CSV行番号'], ascending=[False, True])

current_group = None
for i, row in enumerate(sorted_by_empty.itertuples(), 1):
    if row.空欄言語数 != current_group:
        current_group = row.空欄言語数
        print(f"\n【{current_group}言語で空欄】")
        print("-" * 80)

    print(f"{i:2d}. [CSV行{row.CSV行番号:>3}] {row.日本語}")

print()

# 結論
print("=" * 80)
print("結論と推奨")
print("=" * 80)
print()

print("現在の並び順:")
print("  - 37語のユニークリストは五十音順でソートされています")
print("  - 元のCSVは五十音順ではありません")
print()

print("並び替えの選択肢:")
print("  1. CSV行番号順: 元のCSVの順序を維持")
print("  2. 五十音順: 現在の並び順（検索しやすい）")
print("  3. 空欄言語数順: 翻訳の優先度で並べる（多くの言語で必要な単語が先）")
print()

print("Pandasカテゴリー型について:")
print("  - 現在のCSVには「カテゴリー」列は存在しません")
print("  - 意味的なカテゴリー（安全、動作、専門用語など）を追加する場合は、")
print("    カテゴリー列を新規作成してから、カテゴリー型で並び替え可能です")
print()

# カテゴリー別グループ化の提案
print("=" * 80)
print("カテゴリー分類の提案")
print("=" * 80)
print()

# 手動でカテゴリーを定義（例）
categories = {
    '安全関連': ['感電', '感電する', '感電（する）', '防止', '防止する', '防止（する）',
                 '予防', '予防する', '予防（する）', '転倒', '転倒する', '転倒（する）',
                 '転落', '転落する', '転落（する）', '落下', '落下する', '落下（する）',
                 '墜落', '墜落する', '墜落（する）'],
    '状態': ['不安定', '不安定な', '不安定（な）'],
    '動作': ['確認', '確認する', '嘔吐', '嘔吐する', '嘔吐（する）', '準備'],
    '保険': ['健康保険'],
    '専門用語': ['丸セパレーター（丸セパ）', '丸セパレーター （丸セパ）',
                 'けれん', 'ケレン',
                 '基礎型枠（メタルフォー ム）', '基礎型枠 （メタルフォーム）']
}

print("提案するカテゴリー分類:")
for category, words in categories.items():
    print(f"\n【{category}】 ({len(words)}語)")
    for word in words:
        if word in unique_words:
            row_num = unique_words_df[unique_words_df['日本語'] == word]['CSV行番号'].values[0]
            print(f"  - [CSV行{row_num:>3}] {word}")

print()
print("=" * 80)

# ファイルを閉じる
sys.stdout.close()
print("分析結果を for_claude/japanese_order_analysis.txt に保存しました", file=sys.__stdout__)
