"""
テンプレートCSVから必要な列のみを抽出
（日本語 + 8言語の翻訳列のみ）
"""
import pandas as pd
import os
from datetime import datetime

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'

print("=" * 80)
print("テンプレートCSVから必要な列のみを抽出")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 必要な列（日本語 + 8言語）
required_columns = [
    'ja',      # 日本語
    'en',      # 英語
    'fil-PH',  # タガログ語
    'zh',      # 中国語
    'th',      # タイ語
    'vi',      # ベトナム語
    'my',      # ミャンマー語
    'id',      # インドネシア語
    'km'       # カンボジア語
]

print("必要な列:")
for i, col in enumerate(required_columns, 1):
    print(f"  {i}. {col}")
print()

# ベトナム語順序のテンプレートCSVを読み込み
input_csv = os.path.join(output_dir, '全言語統合_テンプレート形式_ベトナム語順序.csv')
df = pd.read_csv(input_csv, encoding='utf-8-sig')

print(f"元のCSV: {len(df)}行 x {len(df.columns)}列")
print()

# 必要な列のみを抽出
df_template_only = df[required_columns].copy()

print(f"抽出後: {len(df_template_only)}行 x {len(df_template_only.columns)}列")
print()

# 保存
output_file = os.path.join(output_dir, '全言語統合_テンプレート_インポート用.csv')
df_template_only.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"保存: {output_file}")
print()

# 先頭3件を確認（ファイルに保存）
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'
sample_file = os.path.join(for_claude_dir, 'template_sample.txt')
with open(sample_file, 'w', encoding='utf-8') as f:
    f.write("先頭3件:\n")
    f.write(df_template_only.head(3).to_string())
print(f"先頭3件をファイルに保存: {sample_file}")
print()

# データ確認
print("=" * 80)
print("データ確認")
print("=" * 80)
print()

# 各列の空欄数を確認
print("各列の空欄数:")
for col in required_columns:
    empty_count = df_template_only[col].isna().sum()
    filled_count = len(df_template_only) - empty_count
    percentage = (filled_count / len(df_template_only)) * 100
    print(f"  {col:10s}: {filled_count:3d}/{len(df_template_only)} ({percentage:5.1f}%)")

print()
print("=" * 80)
print("完了")
print("=" * 80)
