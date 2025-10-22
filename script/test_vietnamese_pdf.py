# ベトナム語PDFの構造を確認するテストスクリプト
import pdfplumber
import json
import sys

# UTF-8で出力
output_file = 'for_claude/vietnamese_test.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

pdf_path = '建設関連PDF/【全課統合版】ベトナム語_げんばのことば_建設関連職種.pdf'

with pdfplumber.open(pdf_path) as pdf:
    print(f"総ページ数: {len(pdf.pages)}\n")

    # 最初の10ページを確認
    for page_num in range(min(10, len(pdf.pages))):
        page = pdf.pages[page_num]
        print(f"{'='*60}")
        print(f"ページ {page_num + 1}")
        print(f"{'='*60}")

        tables = page.extract_tables()

        if tables:
            print(f"表の数: {len(tables)}")

            for table_num, table in enumerate(tables, 1):
                print(f"\n--- 表 {table_num} ---")
                print(f"行数: {len(table)}")
                if table:
                    print(f"列数: {len(table[0])}")
                    print(f"\n1行目（ヘッダー）:")
                    print(table[0])

                    if len(table) > 1:
                        print(f"\n2行目（データ）:")
                        print(table[1])

                    # 空行除外後の行数
                    non_empty_table = [record for record in table if any(field is not None and str(field).strip() != '' for field in record)]
                    print(f"\n空行除外後の行数: {len(non_empty_table)}")

                    # 1行目の非None要素数
                    if non_empty_table:
                        first_row = non_empty_table[0]
                        first_row_str = [str(cell).strip() if cell is not None else '' for cell in first_row]
                        non_empty_cells = [cell for cell in first_row_str if cell != '' and cell != 'None']
                        print(f"1行目の非空セル数: {len(non_empty_cells)}")

                        # "No."が含まれているか確認
                        has_no = any('No.' in cell or 'No' == cell or 'Số' in cell for cell in first_row_str)
                        print(f"「No.」または「Số」を含む: {has_no}")

        else:
            print("表が見つかりません")

        print()

sys.stdout.close()
