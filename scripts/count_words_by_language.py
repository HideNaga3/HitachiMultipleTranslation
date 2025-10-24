"""
国（言語）ごとに翻訳済みの単語数と空欄の単語数を集計するスクリプト
"""

import pandas as pd

# CSVファイルを読み込み
csv_path = 'output/全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("国（言語）ごとの単語数集計")
print("=" * 80)
print()

# 言語リスト
languages = {
    'ja': '日本語',
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

print(f"{'言語名':<15} {'言語コード':<10} {'翻訳済み':>8} {'空欄':>6} {'総数':>6} {'カバレッジ':>10}")
print("-" * 80)

for lang_code, lang_name in languages.items():
    # 翻訳済み（空欄でない）単語数
    filled_count = df[lang_code].notna().sum()

    # 空欄の単語数
    empty_count = df[lang_code].isna().sum()

    # 総数
    total_count = len(df)

    # カバレッジ
    coverage = (filled_count / total_count) * 100

    results.append({
        '言語名': lang_name,
        '言語コード': lang_code,
        '翻訳済み': filled_count,
        '空欄': empty_count,
        '総数': total_count,
        'カバレッジ': coverage
    })

    print(f"{lang_name:<15} {lang_code:<10} {filled_count:>8} {empty_count:>6} {total_count:>6} {coverage:>9.1f}%")

print()
print("=" * 80)
print("サマリー")
print("=" * 80)
print(f"総単語数: {len(df)} 語")
print()
print("空欄が多い順:")
for result in sorted(results, key=lambda x: x['空欄'], reverse=True):
    if result['空欄'] > 0:
        print(f"  {result['言語名']:<15}: {result['空欄']:>3} 語が未翻訳")

print()
print("カバレッジが高い順:")
for result in sorted(results, key=lambda x: x['カバレッジ'], reverse=True):
    print(f"  {result['言語名']:<15}: {result['カバレッジ']:>5.1f}%")

print()
print("=" * 80)

# CSVファイルに保存
output_df = pd.DataFrame(results)
output_path = 'for_claude/language_word_count.csv'
output_df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"結果を {output_path} に保存しました")
print("=" * 80)
