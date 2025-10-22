"""XMLとExcelファイルの存在を確認"""
from pathlib import Path
import sys

# ファイル出力にリダイレクト
sys.stdout = open('for_claude/available_formats.txt', 'w', encoding='utf-8')

print("=" * 80)
print("利用可能なファイル形式の確認")
print("=" * 80)
print()

# 各言語のファイル形式を確認
languages = ['英語', 'タガログ語', 'カンボジア語', '中国語', 'インドネシア語', 'ミャンマー語', 'タイ語', 'ベトナム語']

pdf_dir = Path('建設関連PDF')
temp_dir = Path('temp_files')

results = {}

for lang in languages:
    results[lang] = {
        'PDF': [],
        'Excel': [],
        'XML': []
    }

    # PDFファイルを検索
    pdf_files = list(pdf_dir.glob(f'*{lang}*.pdf'))
    for f in pdf_files:
        results[lang]['PDF'].append(f.name)

    # Excelファイルを検索（両ディレクトリ）
    excel_files_pdf = list(pdf_dir.glob(f'*{lang}*.xlsx'))
    excel_files_temp = list(temp_dir.glob(f'*{lang}*.xlsx'))
    for f in excel_files_pdf + excel_files_temp:
        results[lang]['Excel'].append(f.name)

    # XMLファイルを検索（両ディレクトリ）
    xml_files_pdf = list(pdf_dir.glob(f'*{lang}*.xml'))
    xml_files_temp = list(temp_dir.glob(f'*{lang}*.xml'))
    for f in xml_files_pdf + xml_files_temp:
        results[lang]['XML'].append(f.name)

# 結果を表形式で表示
print("【言語別ファイル形式の存在状況】")
print()
print(f"{'言語':<15} {'PDF':<5} {'Excel':<5} {'XML':<5}")
print("-" * 80)

for lang in languages:
    pdf_count = len(results[lang]['PDF'])
    excel_count = len(results[lang]['Excel'])
    xml_count = len(results[lang]['XML'])

    pdf_mark = '✓' if pdf_count > 0 else '✗'
    excel_mark = '✓' if excel_count > 0 else '✗'
    xml_mark = '✓' if xml_count > 0 else '✗'

    print(f"{lang:<15} {pdf_mark:<5} {excel_mark:<5} {xml_mark:<5}")

print()
print("=" * 80)
print("【詳細リスト】")
print("=" * 80)

for lang in languages:
    if results[lang]['Excel'] or results[lang]['XML']:
        print(f"\n{lang}:")

        if results[lang]['Excel']:
            print("  Excelファイル:")
            for f in results[lang]['Excel']:
                print(f"    - {f}")

        if results[lang]['XML']:
            print("  XMLファイル:")
            for f in results[lang]['XML']:
                print(f"    - {f}")

print()
print("=" * 80)

# サマリー
excel_langs = [lang for lang in languages if results[lang]['Excel']]
xml_langs = [lang for lang in languages if results[lang]['XML']]

print("【サマリー】")
print(f"Excelファイルがある言語 ({len(excel_langs)}言語): {', '.join(excel_langs)}")
print(f"XMLファイルがある言語 ({len(xml_langs)}言語): {', '.join(xml_langs)}")
