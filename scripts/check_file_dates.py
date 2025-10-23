"""
outputフォルダ内のファイルの更新日時を確認するスクリプト
"""

import os
from datetime import datetime

output_dir = 'output'

print("=" * 80)
print("outputフォルダ内のファイル（更新日時順）")
print("=" * 80)
print()

# 全ファイルを取得
all_files = []
for root, dirs, files in os.walk(output_dir):
    for file in files:
        file_path = os.path.join(root, file)
        file_stat = os.stat(file_path)
        file_size = file_stat.st_size
        file_mtime = datetime.fromtimestamp(file_stat.st_mtime)

        all_files.append({
            'path': file_path,
            'name': file,
            'size': file_size,
            'mtime': file_mtime
        })

# 更新日時でソート（新しい順）
all_files.sort(key=lambda x: x['mtime'], reverse=True)

# 上位30件を表示
print(f"総ファイル数: {len(all_files)}")
print()
print("最新30件:")
print("-" * 80)
print(f"{'No':<4} {'更新日時':<20} {'サイズ':<12} {'ファイル名'}")
print("-" * 80)

for i, f in enumerate(all_files[:30], 1):
    size_kb = f['size'] / 1024
    mtime_str = f['mtime'].strftime('%Y/%m/%d %H:%M:%S')
    print(f"{i:<4} {mtime_str:<20} {size_kb:>8.1f} KB  {f['name']}")

print()
print("=" * 80)

# インポート用CSVの確認
print("インポート用CSVの詳細")
print("=" * 80)
print()

import_csv = 'output/全言語統合_テンプレート_インポート用.csv'
if os.path.exists(import_csv):
    stat = os.stat(import_csv)
    mtime = datetime.fromtimestamp(stat.st_mtime)
    print(f"ファイル名: 全言語統合_テンプレート_インポート用.csv")
    print(f"更新日時: {mtime.strftime('%Y/%m/%d %H:%M:%S')}")
    print(f"サイズ: {stat.st_size / 1024:.1f} KB")
    print()
    print("このファイルが最新のインポート用データです")
else:
    print("インポート用CSVが見つかりません")

print()
print("=" * 80)
