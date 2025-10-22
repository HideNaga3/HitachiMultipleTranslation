"""タイ語CSVファイルを置き換える"""
import shutil
import os
from pathlib import Path

# ディレクトリ作成
backup_dir = Path('output_backup')
backup_dir.mkdir(exist_ok=True)

output_dir = Path('output')

# 旧タイ語CSVファイルをバックアップに移動
old_thai_files = list(output_dir.glob('*タイ語*.csv'))
print(f"バックアップ対象ファイル: {len(old_thai_files)}個")

for file in old_thai_files:
    backup_path = backup_dir / file.name
    shutil.move(str(file), str(backup_path))
    print(f"  移動: {file.name} -> output_backup/")

# 新しいタイ語CSVファイルを適切な名前でコピー
source_file = output_dir / '【全課統合版】タイ語_げんばのことば_建設関連職種_from_excel.csv'
target_file = output_dir / '【全課統合版】タイ語_げんばのことば_建設関連職種_6cols.csv'

if source_file.exists():
    shutil.copy(str(source_file), str(target_file))
    print(f"\nコピー完了:")
    print(f"  元: {source_file.name}")
    print(f"  先: {target_file.name}")
else:
    print(f"\nエラー: ソースファイルが見つかりません: {source_file}")

# 確認
print(f"\n現在のタイ語CSVファイル:")
thai_files = list(output_dir.glob('*タイ語*.csv'))
for file in thai_files:
    print(f"  - {file.name}")
