"""
テンプレート形式CSV（pivot済み）をベトナム語順序で並び替え
ベトナム語にない日本語も保持する
"""
import pandas as pd
import os
from datetime import datetime

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

print("=" * 80)
print("テンプレート形式CSVをベトナム語順序で並び替え")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. 統合CSVからベトナム語の日本語順序を取得
unified_csv = os.path.join(output_dir, '全言語統合_比較用.csv')
unified_df = pd.read_csv(unified_csv, encoding='utf-8-sig')

vietnamese_df = unified_df[unified_df['言語'] == 'ベトナム語'].copy()
vietnamese_order = vietnamese_df['日本語'].drop_duplicates().tolist()

print(f"ベトナム語の日本語順序: {len(vietnamese_order)}個")
print()

# 2. テンプレート形式CSVを読み込み
template_csv = os.path.join(output_dir, '全言語統合_テンプレート形式.csv')
template_df = pd.read_csv(template_csv, encoding='utf-8-sig')

print(f"テンプレートCSV: {len(template_df)}行 x {len(template_df.columns)}列")
print()

# 3. テンプレートCSVの全日本語を取得
template_japanese = template_df['ja'].unique().tolist()
print(f"テンプレートCSVのユニーク日本語: {len(template_japanese)}個")
print()

# 4. ベトナム語にない日本語を抽出
vietnamese_set = set(vietnamese_order)
not_in_vietnamese = [ja for ja in template_japanese if ja not in vietnamese_set]

print(f"ベトナム語にない日本語: {len(not_in_vietnamese)}個")
if len(not_in_vietnamese) > 0:
    print("ベトナム語にない日本語（先頭10個）:")
    for i, ja in enumerate(not_in_vietnamese[:10], 1):
        print(f"  {i:2d}. {ja}")
print()

# 5. カテゴリ順序を作成（ベトナム語順序 + ベトナム語にない日本語）
category_order = vietnamese_order + not_in_vietnamese

print(f"カテゴリ順序の総数: {len(category_order)}個")
print()

# 6. ja列をCategoricalに変換
template_df['ja'] = pd.Categorical(
    template_df['ja'],
    categories=category_order,
    ordered=True
)

# 7. ja列でソート
template_df_sorted = template_df.sort_values('ja').copy()

# 8. Categoricalを文字列に戻す
template_df_sorted['ja'] = template_df_sorted['ja'].astype(str)

# 9. 保存
output_file = os.path.join(output_dir, '全言語統合_テンプレート形式_ベトナム語順序.csv')
template_df_sorted.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"並び替え後: {len(template_df_sorted)}行")
print(f"保存: {output_file}")
print()

# 10. 先頭10件と末尾10件を表示
print("並び替え後の先頭10件（日本語）:")
for i, ja in enumerate(template_df_sorted['ja'].head(10), 1):
    print(f"  {i:2d}. {ja}")
print()

print("並び替え後の末尾10件（日本語）:")
tail_start = len(template_df_sorted) - 9
for i, ja in enumerate(template_df_sorted['ja'].tail(10), tail_start):
    print(f"  {i:3d}. {ja}")
print()

# 11. 翻訳数付きCSVも並び替え
template_count_csv = os.path.join(output_dir, '全言語統合_テンプレート形式_翻訳数付き.csv')
if os.path.exists(template_count_csv):
    print("=" * 80)
    print("翻訳数付きCSVも並び替え")
    print("=" * 80)
    print()

    template_count_df = pd.read_csv(template_count_csv, encoding='utf-8-sig')

    # ja列をCategoricalに変換
    template_count_df['ja'] = pd.Categorical(
        template_count_df['ja'],
        categories=category_order,
        ordered=True
    )

    # ja列でソート
    template_count_df_sorted = template_count_df.sort_values('ja').copy()

    # Categoricalを文字列に戻す
    template_count_df_sorted['ja'] = template_count_df_sorted['ja'].astype(str)

    # 保存
    output_count_file = os.path.join(output_dir, '全言語統合_テンプレート形式_翻訳数付き_ベトナム語順序.csv')
    template_count_df_sorted.to_csv(output_count_file, index=False, encoding='utf-8-sig')

    print(f"並び替え後: {len(template_count_df_sorted)}行")
    print(f"保存: {output_count_file}")
    print()

# 12. ベトナム語のみの24語が含まれているか確認
vietnamese_only_terms = [
    'けれん', '不安定', '墜落', '感電', '確認'
]

print("=" * 80)
print("ベトナム語のみの用語が含まれているか確認")
print("=" * 80)
print()

for term in vietnamese_only_terms:
    term_row = template_df_sorted[template_df_sorted['ja'] == term]
    if len(term_row) > 0:
        print(f"{term}: 存在（行番号={term_row.index[0] + 1}）")
    else:
        print(f"{term}: 不在")

print()
print("=" * 80)
print("並び替え完了")
print("=" * 80)
