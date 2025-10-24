"""
outputフォルダ内のベトナム語関連ファイルを一覧表示するスクリプト
"""

import os
import sys

# 出力先をファイルに変更
output_file = 'for_claude/vietnamese_files_list.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

output_dir = 'output'

print("=" * 80)
print("outputフォルダ内のベトナム語関連ファイル")
print("=" * 80)
print()

# 全CSVファイルを取得
csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]

# ベトナム語を含むファイルを抽出
vietnamese_files = [f for f in csv_files if 'ベトナム' in f]

print(f"総CSVファイル数: {len(csv_files)}")
print(f"ベトナム語関連ファイル数: {len(vietnamese_files)}")
print()

if vietnamese_files:
    print("ベトナム語関連ファイル一覧:")
    print("-" * 80)
    for i, f in enumerate(vietnamese_files, 1):
        file_path = os.path.join(output_dir, f)
        file_size = os.path.getsize(file_path)
        print(f"{i:2d}. {f}")
        print(f"    サイズ: {file_size / 1024:.1f} KB")
        print()
else:
    print("ベトナム語関連のCSVファイルが見つかりませんでした")
    print()
    print("全CSVファイル（最初の10件）:")
    print("-" * 80)
    for i, f in enumerate(csv_files[:10], 1):
        print(f"{i:2d}. {f}")

print("=" * 80)

sys.stdout.close()
print(f"結果を {output_file} に保存しました", file=sys.__stdout__)
