"""tmpフォルダ内のExcelファイルを確認"""
from pathlib import Path
import pandas as pd
import sys

# ファイル出力
sys.stdout = open('for_claude/tmp_excel_files.txt', 'w', encoding='utf-8')

print("=" * 80)
print("tmpフォルダ内のExcelファイル確認")
print("=" * 80)
print()

tmp_dir = Path('tmp')

if not tmp_dir.exists():
    print(f"エラー: {tmp_dir} フォルダが存在しません")
    sys.exit(1)

# Excelファイルを検索
excel_files = list(tmp_dir.glob('*.xlsx')) + list(tmp_dir.glob('*.xls'))

print(f"【Excelファイル一覧】")
print(f"総数: {len(excel_files)}個")
print()

if len(excel_files) == 0:
    print("Excelファイルが見つかりません")
    sys.exit(0)

# 各ファイルの基本情報を表示
for i, file in enumerate(sorted(excel_files), 1):
    print(f"{i}. {file.name}")
    print(f"   サイズ: {file.stat().st_size:,} bytes")

    # 言語を判定
    lang = None
    for lang_name in ['英語', 'タガログ語', 'カンボジア語', '中国語', 'インドネシア語', 'ミャンマー語', 'タイ語', 'ベトナム語']:
        if lang_name in file.name:
            lang = lang_name
            break

    if lang:
        print(f"   言語: {lang}")

    # シート情報を取得
    try:
        xls = pd.ExcelFile(file)
        print(f"   シート数: {len(xls.sheet_names)}")
        print(f"   シート名: {xls.sheet_names}")

        # 最初のシートの行数・列数を取得
        if len(xls.sheet_names) > 0:
            df = pd.read_excel(file, sheet_name=xls.sheet_names[0], header=None)
            print(f"   最初のシート: {len(df)}行、{len(df.columns)}列")
    except Exception as e:
        print(f"   エラー: {e}")

    print()

print("=" * 80)
print("【言語別の集計】")

languages = {}
for file in excel_files:
    for lang_name in ['英語', 'タガログ語', 'カンボジア語', '中国語', 'インドネシア語', 'ミャンマー語', 'タイ語', 'ベトナム語']:
        if lang_name in file.name:
            if lang_name not in languages:
                languages[lang_name] = []
            languages[lang_name].append(file.name)

for lang in sorted(languages.keys()):
    print(f"\n{lang}: {len(languages[lang])}ファイル")
    for fname in languages[lang]:
        print(f"  - {fname}")

print()
print("=" * 80)
