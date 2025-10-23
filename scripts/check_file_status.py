"""ファイル状況を確認"""
from pathlib import Path

print("=" * 80)
print("ファイル状況確認")
print("=" * 80)
print()

# outputディレクトリのCSVファイル
print("【outputディレクトリのCSVファイル】")
output_dir = Path('output')
csv_files = sorted(output_dir.glob('*.csv'))
for file in csv_files:
    print(f"  - {file.name}")
print(f"  合計: {len(csv_files)}個")
print()

# output_backupディレクトリのCSVファイル
print("【output_backupディレクトリのCSVファイル】")
backup_dir = Path('output_backup')
if backup_dir.exists():
    backup_files = sorted(backup_dir.glob('*.csv'))
    for file in backup_files:
        print(f"  - {file.name}")
    print(f"  合計: {len(backup_files)}個")
else:
    print("  ディレクトリが存在しません")
print()

# from_excelファイルを検索
print("【from_excelファイルの場所】")
from_excel_files = list(Path('.').glob('**/*from_excel.csv'))
if from_excel_files:
    for file in from_excel_files:
        print(f"  - {file}")
else:
    print("  見つかりません")
print()

# タイ語ファイルを検索
print("【タイ語関連CSVファイルの場所】")
thai_files = list(Path('.').glob('**/*タイ語*.csv'))
for file in thai_files:
    print(f"  - {file}")
print(f"  合計: {len(thai_files)}個")
