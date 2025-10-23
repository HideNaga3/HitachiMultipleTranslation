"""
core_filesディレクトリに詳細CSVを出力
"""
import pandas as pd
import os
import glob

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
output_dir = os.path.join(project_root, 'output')
core_files_dir = os.path.join(project_root, 'core_files')

# core_filesディレクトリ作成
os.makedirs(core_files_dir, exist_ok=True)

print("=" * 80)
print("core_filesディレクトリへの出力")
print("=" * 80)
print()

# intermediate フォルダ内の全CSVを検索
csv_files = glob.glob(os.path.join(output_dir, 'intermediate', '*.csv'))

# 39列のファイルを探す
target_file = None
for csv_file in csv_files:
    try:
        df_test = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=1)
        if len(df_test.columns) == 39:
            # ベトナム語順を優先
            if 'ベトナム' in os.path.basename(csv_file):
                target_file = csv_file
                break
    except:
        pass

# 見つからない場合は翻訳数付きで38列を探す
if not target_file:
    for csv_file in csv_files:
        try:
            df_test = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=1)
            if len(df_test.columns) == 38 and 'ベトナム' in os.path.basename(csv_file):
                target_file = csv_file
                break
        except:
            pass

if not target_file:
    print("エラー: 適切なファイルが見つかりません")
    exit(1)

print(f"ソースファイル: {os.path.basename(target_file)}")

# CSVを読み込み
df = pd.read_csv(target_file, encoding='utf-8-sig')

print(f"行数: {len(df)}行")
print(f"列数: {len(df.columns)}列")
print()

print("列名（最初の20列）:")
for i, col in enumerate(df.columns[:20]):
    print(f"  {i+1:2d}. {col}")

print(f"  ...")
print(f"  {len(df.columns)}. {df.columns[-1]}")

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
