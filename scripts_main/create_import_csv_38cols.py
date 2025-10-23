"""
翻訳言語数を除いた38列のインポート用CSVを作成
"""
import pandas as pd
import os

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
core_files_dir = os.path.join(project_root, 'core_files')
deliverables_dir = os.path.join(project_root, '成果物_20251023')

print("=" * 80)
print("インポート用CSV作成（38列）")
print("=" * 80)
print()

# core_filesのCSVを読み込み
source_file = os.path.join(core_files_dir, 'output_csv_template_utf8bom.csv')
df = pd.read_csv(source_file, encoding='utf-8-sig')

print(f"ソースファイル: {os.path.basename(source_file)}")
print(f"行数: {len(df)}行")
print(f"列数: {len(df.columns)}列")
print()

# 翻訳言語数列を削除
if '翻訳言語数' in df.columns:
    df_import = df.drop(columns=['翻訳言語数'])
    print("翻訳言語数列を削除")
else:
    df_import = df.copy()
    print("警告: 翻訳言語数列が見つかりません")

print()
print(f"インポート用CSV:")
print(f"  行数: {len(df_import)}行")
print(f"  列数: {len(df_import.columns)}列")
print()

print("列名:")
for i, col in enumerate(df_import.columns):
    print(f"  {i+1:2d}. {col}")

print()

# 成果物フォルダに保存
output_file = os.path.join(deliverables_dir, '01_全言語統合_テンプレート_インポート用.csv')
df_import.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"出力: {output_file}")

# ファイルサイズ確認
size_kb = os.path.getsize(output_file) / 1024
print(f"ファイルサイズ: {size_kb:.2f} KB")
print()

print("=" * 80)
print("完了")
print("=" * 80)
print()
print(f"インポート用CSV: {len(df_import)}行 x {len(df_import.columns)}列")
