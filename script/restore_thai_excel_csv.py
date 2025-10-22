"""Excelから抽出したタイ語CSVをoutputディレクトリに配置"""
import shutil
from pathlib import Path

backup_dir = Path('output_backup')
output_dir = Path('output')

# from_excelファイルをコピー
source_file = backup_dir / '【全課統合版】タイ語_げんばのことば_建設関連職種_from_excel.csv'
target_file = output_dir / '【全課統合版】タイ語_げんばのことば_建設関連職種_6cols.csv'

if source_file.exists():
    shutil.copy(str(source_file), str(target_file))
    print(f"コピー成功:")
    print(f"  元: {source_file}")
    print(f"  先: {target_file}")
    print(f"  ファイルサイズ: {target_file.stat().st_size:,} bytes")
else:
    print(f"エラー: ソースファイルが見つかりません: {source_file}")

# 確認
print(f"\noutputディレクトリのタイ語CSVファイル:")
thai_files = sorted(output_dir.glob('*タイ語*.csv'))
for file in thai_files:
    size = file.stat().st_size
    print(f"  - {file.name} ({size:,} bytes)")
print(f"  合計: {len(thai_files)}個")

print(f"\noutputディレクトリの全CSVファイル数: {len(list(output_dir.glob('*.csv')))}個")
