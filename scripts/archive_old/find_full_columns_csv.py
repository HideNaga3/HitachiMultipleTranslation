"""
列数の多いCSVファイルを探す
"""
import pandas as pd
import os
import glob

project_root = r'C:\python_script\test_space\MitsubishiMultipleTranslation'
output_dir = os.path.join(project_root, 'output')

# outputとintermediateのCSVを全て確認
csv_files = glob.glob(os.path.join(output_dir, '*.csv'))
csv_files += glob.glob(os.path.join(output_dir, 'intermediate', '*.csv'))

print("=" * 80)
print("CSVファイルの列数確認")
print("=" * 80)
print()

file_info = []

for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig', nrows=1)
        cols = len(df.columns)
        file_info.append({
            'file': os.path.basename(csv_file),
            'path': csv_file,
            'columns': cols
        })
    except Exception as e:
        pass

# 列数でソート
file_info.sort(key=lambda x: x['columns'], reverse=True)

print("列数の多い順:")
print("-" * 80)
for info in file_info[:15]:  # 上位15件
    print(f"{info['columns']:3d}列: {info['file']}")

print()
print("=" * 80)

# 40列前後のファイルを詳しく確認
print()
print("40列前後のファイル詳細:")
print("=" * 80)

for info in file_info:
    if 35 <= info['columns'] <= 50:
        print()
        print(f"ファイル: {info['file']}")
        print(f"列数: {info['columns']}列")
        print(f"パス: {info['path']}")

        # ヘッダーを表示
        df = pd.read_csv(info['path'], encoding='utf-8-sig', nrows=0)
        print("ヘッダー:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1:2d}. {col}")
