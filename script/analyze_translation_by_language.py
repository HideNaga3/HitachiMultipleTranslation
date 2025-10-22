"""統合CSVの翻訳列を言語別に詳細分析"""
import pandas as pd
import sys

# 出力をファイルにリダイレクト
sys.stdout = open('for_claude/translation_analysis.txt', 'w', encoding='utf-8')

# 統合CSVを読み込み
df = pd.read_csv('output_cleaned/全言語統合.csv', encoding='utf-8-sig')

print("=" * 80)
print("全言語統合CSV - 翻訳列の言語別データ状況")
print("=" * 80)
print()

# 言語別の統計を取得
languages = df['言語'].unique()

summary_data = []

for lang in sorted(languages):
    lang_df = df[df['言語'] == lang]
    total = len(lang_df)

    # 翻訳列が空でない行数
    translation_filled = lang_df['翻訳'].notna().sum()
    translation_filled_and_not_empty = (lang_df['翻訳'].notna() & (lang_df['翻訳'].astype(str).str.strip() != '')).sum()

    # 空の行数
    translation_empty = total - translation_filled_and_not_empty

    # パーセンテージ
    filled_pct = translation_filled_and_not_empty / total * 100 if total > 0 else 0
    empty_pct = translation_empty / total * 100 if total > 0 else 0

    summary_data.append({
        '言語': lang,
        '総行数': total,
        '翻訳データあり': translation_filled_and_not_empty,
        '翻訳データなし': translation_empty,
        '翻訳充足率': f'{filled_pct:.1f}%',
        '空欄率': f'{empty_pct:.1f}%'
    })

# データフレームで表示
summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))
print()

# カンボジア語とタイ語の詳細
print("=" * 80)
print("カンボジア語の翻訳列サンプル（最初の10行）")
print("=" * 80)
khmer_df = df[df['言語'] == 'カンボジア語']
khmer_sample = khmer_df[['番号', '単語', '翻訳']].head(10)
print(khmer_sample.to_string(index=False))
print()

print("=" * 80)
print("タイ語の翻訳列サンプル（翻訳データがある行のみ、最初の10行）")
print("=" * 80)
thai_df = df[df['言語'] == 'タイ語']
thai_with_translation = thai_df[thai_df['翻訳'].notna() & (thai_df['翻訳'].astype(str).str.strip() != '')]
thai_sample = thai_with_translation[['番号', '単語', '翻訳']].head(10)
print(thai_sample.to_string(index=False))
print()

# 統計サマリー
print("=" * 80)
print("全体統計")
print("=" * 80)
total_rows = len(df)
total_translation_filled = (df['翻訳'].notna() & (df['翻訳'].astype(str).str.strip() != '')).sum()
total_translation_empty = total_rows - total_translation_filled

print(f"総行数: {total_rows}")
print(f"翻訳データあり: {total_translation_filled}行 ({total_translation_filled/total_rows*100:.1f}%)")
print(f"翻訳データなし: {total_translation_empty}行 ({total_translation_empty/total_rows*100:.1f}%)")
print()
