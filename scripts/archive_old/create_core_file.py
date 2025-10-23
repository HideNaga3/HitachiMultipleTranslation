"""
core_filesディレクトリに詳細CSVを出力
"""
import pandas as pd
import os
import shutil

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
output_dir = os.path.join(project_root, 'output')
core_files_dir = os.path.join(project_root, 'core_files')

# core_filesディレクトリ作成
os.makedirs(core_files_dir, exist_ok=True)

print("=" * 80)
print("core_filesディレクトリへの出力")
print("=" * 80)
print()

# 翻訳数付きテンプレート（ベトナム語順）を使用
source_file = os.path.join(output_dir, 'intermediate', '全言語統合_テンプレート形式_翻訳数付き_ベトナム語順.csv')

# ファイルが存在するか確認
if not os.path.exists(source_file):
    # intermediateになければoutputを確認
    source_file = os.path.join(output_dir, '全言語統合_テンプレート形式_翻訳数付き_ベトナム語順.csv')

if not os.path.exists(source_file):
    # それでもなければ翻訳数なしを使用
    source_file = os.path.join(output_dir, 'intermediate', '全言語統合_テンプレート形式_ベトナム語順.csv')

if not os.path.exists(source_file):
    source_file = os.path.join(output_dir, '全言語統合_テンプレート形式_ベトナム語順.csv')

print(f"ソースファイル: {os.path.basename(source_file)}")

# CSVを読み込み
df = pd.read_csv(source_file, encoding='utf-8-sig')

print(f"行数: {len(df)}行")
print(f"列数: {len(df.columns)}列")
print()

print("列名:")
for i, col in enumerate(df.columns):
    print(f"  {i+1:2d}. {col[:50]}")  # 50文字まで表示

print()

# core_filesに出力
output_file = os.path.join(core_files_dir, 'output_csv_template_utf8bom.csv')

# UTF-8 BOMで保存
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"出力: {output_file}")
print()

# ファイルサイズ確認
size_kb = os.path.getsize(output_file) / 1024
print(f"ファイルサイズ: {size_kb:.2f} KB")
print()

print("=" * 80)
print("完了")
print("=" * 80)
