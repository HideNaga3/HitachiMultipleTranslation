"""
タイ語データの日本語列順序を基準に、全データを並び替え
統合CSV（比較用）のタイ語データを基準とする
"""
import pandas as pd
import os
from datetime import datetime

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'

# 統合CSV（比較用）を読み込み
unified_csv = os.path.join(output_dir, '全言語統合_比較用.csv')
unified_df = pd.read_csv(unified_csv, encoding='utf-8-sig')

print("=" * 80)
print("タイ語データの日本語列順序を基準に並び替え")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# タイ語データのみ抽出
thai_df = unified_df[unified_df['言語'] == 'タイ語'].copy()

# タイ語の日本語列の順序をリスト化（これがマスター順序）
# 重複を削除して順序を保持
thai_order = thai_df['日本語'].drop_duplicates().tolist()

print(f"統合CSV総行数: {len(unified_df)}行")
print(f"タイ語データ: {len(thai_df)}行")
print(f"日本語順序リスト: {len(thai_order)}個")
print()

# サンプル表示
print("日本語順序リスト（先頭10件）:")
for i, word in enumerate(thai_order[:10], 1):
    print(f"  {i:3d}. {word}")
print()

print("=" * 80)
print("全データの並び替え")
print("=" * 80)
print()

# 日本語列をCategoricalに変換（タイ語順序を基準）
unified_df['日本語'] = pd.Categorical(
    unified_df['日本語'],
    categories=thai_order,
    ordered=True
)

# 言語別、日本語順でソート
unified_df_sorted = unified_df.sort_values(['言語', '日本語']).copy()

# カテゴリーを通常の文字列に戻す
unified_df_sorted['日本語'] = unified_df_sorted['日本語'].astype(str)

# 個別言語CSVを出力
print("=" * 80)
print("個別言語CSVの出力")
print("=" * 80)
print()

for lang in sorted(unified_df_sorted['言語'].unique()):
    lang_df = unified_df_sorted[unified_df_sorted['言語'] == lang].copy()

    # 列順を整理（言語列は不要）
    if 'ファイル名' in lang_df.columns:
        column_order = ['ファイル名', 'ページ', '番号', '日本語', '翻訳']
    else:
        column_order = ['ページ', '番号', '日本語', '翻訳']

    available_columns = [col for col in column_order if col in lang_df.columns]
    lang_df = lang_df[available_columns]

    # 保存
    lang_output = os.path.join(output_dir, f'{lang}_タイ語順序.csv')
    lang_df.to_csv(lang_output, index=False, encoding='utf-8-sig')

    print(f"[{lang}] {len(lang_df):4d}行 → {lang_output}")

print()

# 統合CSV作成
print("=" * 80)
print("統合CSV作成")
print("=" * 80)
print()

# 行IDを振り直し
unified_df_sorted['行ID'] = range(1, len(unified_df_sorted) + 1)

# 列順を整理
column_order = ['行ID', 'ファイル名', '言語', 'ページ', '番号', '日本語', '翻訳']
available_columns = [col for col in column_order if col in unified_df_sorted.columns]
unified_df_sorted = unified_df_sorted[available_columns]

# 保存
output_filepath = os.path.join(output_dir, '全言語統合_タイ語順序.csv')
unified_df_sorted.to_csv(output_filepath, index=False, encoding='utf-8-sig')

print(f"並び替え後: {len(unified_df_sorted)}行")
print(f"保存: {output_filepath}")
print()

# 言語別行数を確認
print("言語別行数:")
lang_counts = unified_df_sorted['言語'].value_counts().sort_index()
for lang, count in lang_counts.items():
    print(f"  {lang:15s}: {count:4d}行")
print()

# タイ語順序に存在しない日本語の確認
all_japanese = set(unified_df['日本語'])
missing_in_thai = all_japanese - set(thai_order)
if missing_in_thai and missing_in_thai != {'nan'}:
    print(f"⚠ タイ語順序に存在しない日本語: {len(missing_in_thai)}個")
    for word in list(missing_in_thai)[:10]:
        print(f"  - {word}")
    print()

# 並び替え結果のサンプル表示（各言語の先頭5件）
print("=" * 80)
print("並び替え結果サンプル（各言語の先頭5件）")
print("=" * 80)
print()

for lang in sorted(unified_df_sorted['言語'].unique()):
    lang_df = unified_df_sorted[unified_df_sorted['言語'] == lang]
    print(f"【{lang}】")
    for i, (idx, row) in enumerate(lang_df.head(5).iterrows(), 1):
        jp = row['日本語']
        print(f"  {i}. {jp}")
    print()

print("=" * 80)
print("並び替え完了")
print("=" * 80)
