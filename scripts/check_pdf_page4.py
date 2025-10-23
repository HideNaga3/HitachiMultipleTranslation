"""
カンボジア語とタイ語のPDF Page 4を確認して「健康保険」の翻訳を取得
"""
import pdfplumber
import os

# PDFファイルパス
pdf_files = {
    'カンボジア語': r'C:\python_script\test_space\MitsubishiMultipleTranslation\建設関連PDF\【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf',
    'タイ語': r'C:\python_script\test_space\MitsubishiMultipleTranslation\建設関連PDF\【全課統合版】タイ語_げんばのことば_建設関連職種.pdf',
}

# 出力ファイル
output_file = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude\pdf_page4_check.txt'

def write_output(message):
    """ファイルに出力"""
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

# ファイルをクリア
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('')

write_output("=" * 80)
write_output("カンボジア語・タイ語PDF Page 4-6 のテーブル内容確認")
write_output("=" * 80)
write_output("")

for lang, pdf_path in pdf_files.items():
    write_output(f"\n{'=' * 80}")
    write_output(f"{lang}")
    write_output("=" * 80)

    with pdfplumber.open(pdf_path) as pdf:
        # Page 4-6 を確認
        for page_num in [4, 5, 6]:
            if page_num <= len(pdf.pages):
                page = pdf.pages[page_num - 1]
                write_output(f"\n--- Page {page_num} ---")

                tables = page.extract_tables()

                if tables:
                    for table_idx, table in enumerate(tables, 1):
                        write_output(f"\nTable {table_idx}: {len(table)} rows")

                        # テーブルの全行を表示
                        for row_idx, row in enumerate(table):
                            # 行番号と内容を表示（最初の4列程度）
                            row_preview = ' | '.join([str(cell)[:30] if cell else '' for cell in row[:6]])
                            write_output(f"  Row {row_idx}: {row_preview}")
                else:
                    write_output("  テーブルなし")

write_output("\n" + "=" * 80)
write_output("確認完了")
write_output("=" * 80)
write_output(f"結果ファイル: {output_file}")
