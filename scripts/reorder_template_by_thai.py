"""
テンプレート形式CSV（pivot済み）をタイ語順序で並び替え
"""
import pandas as pd
import os
from datetime import datetime

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'

print("=" * 80)
print("テンプレート形式CSVをタイ語順序で並び替え")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. 統合CSVからタイ語の日本語順序を取得
unified_csv = os.path.join(output_dir, '全言語統合_比較用.csv')
unified_df = pd.read_csv(unified_csv, encoding='utf-8-sig')

thai_df = unified_df[unified_df['言語'] == 'タイ語'].copy()
thai_order = thai_df['日本語'].drop_duplicates().tolist()

print(f"タイ語の日本語順序: {len(thai_order)}個")
print()

# 2. テンプレート形式CSVを読み込み
template_csv = os.path.join(output_dir, '全言語統合_テンプレート形式.csv')
template_df = pd.read_csv(template_csv, encoding='utf-8-sig')

print(f"テンプレートCSV: {len(template_df)}行 x {len(template_df.columns)}列")
print()

# 3. ja列をCategoricalに変換（タイ語順序を基準）
template_df['ja'] = pd.Categorical(
    template_df['ja'],
    categories=thai_order,
    ordered=True
)

# 4. ja列でソート
template_df_sorted = template_df.sort_values('ja').copy()

# 5. Categoricalを文字列に戻す
template_df_sorted['ja'] = template_df_sorted['ja'].astype(str)

# 6. 保存
output_file = os.path.join(output_dir, '全言語統合_テンプレート形式_タイ語順序.csv')
template_df_sorted.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"並び替え後: {len(template_df_sorted)}行")
print(f"保存: {output_file}")
print()

# 7. 先頭10件を表示
print("並び替え後の先頭10件（日本語）:")
for i, ja in enumerate(template_df_sorted['ja'].head(10), 1):
    print(f"  {i:2d}. {ja}")
print()

# 8. 翻訳数付きCSVも並び替え
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
        categories=thai_order,
        ordered=True
    )

    # ja列でソート
    template_count_df_sorted = template_count_df.sort_values('ja').copy()

    # Categoricalを文字列に戻す
    template_count_df_sorted['ja'] = template_count_df_sorted['ja'].astype(str)

    # 保存
    output_count_file = os.path.join(output_dir, '全言語統合_テンプレート形式_翻訳数付き_タイ語順序.csv')
    template_count_df_sorted.to_csv(output_count_file, index=False, encoding='utf-8-sig')

    print(f"並び替え後: {len(template_count_df_sorted)}行")
    print(f"保存: {output_count_file}")
    print()

print("=" * 80)
print("並び替え完了")
print("=" * 80)
