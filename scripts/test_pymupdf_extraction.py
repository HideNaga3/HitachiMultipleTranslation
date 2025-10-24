"""
PyMuPDFを使ってPDFから表データを抽出するテストスクリプト
CIDコード問題が解決されるか確認
"""

import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path
import sys
import io

# UTF-8出力を強制
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_text_from_page(pdf_path, page_num):
    """指定ページのテキストを抽出"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    text = page.get_text()
    doc.close()
    return text

def extract_tables_from_page(pdf_path, page_num):
    """指定ページの表を抽出"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]

    # PyMuPDFのテーブル抽出機能を使用
    tables = page.find_tables()

    extracted_data = []
    for table_idx, table in enumerate(tables):
        print(f"\n=== ページ {page_num + 1}, 表 {table_idx + 1} ===")
        print(f"行数: {len(table.extract())}")

        # 表データを抽出
        table_data = table.extract()

        # データフレームに変換
        if table_data:
            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            print(f"列数: {len(df.columns)}")
            print(f"\n最初の3行:")
            print(df.head(3))

            extracted_data.append({
                'page': page_num + 1,
                'table': table_idx + 1,
                'dataframe': df
            })

    doc.close()
    return extracted_data

def check_for_cid_codes(text):
    """CIDコードが含まれているかチェック"""
    if '(cid:' in text:
        import re
        cid_codes = re.findall(r'\(cid:\d+\)', text)
        return True, cid_codes
    return False, []

if __name__ == '__main__':
    # カンボジア語PDFのパス
    pdf_path = Path('建設関連PDF') / '【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

    print("=" * 80)
    print("PyMuPDF テスト: カンボジア語PDF")
    print("=" * 80)

    # ページ19（0始まりなので18）をテスト - CIDコードが多いページ
    test_page = 18

    print(f"\n【テスト1】ページ {test_page + 1} のテキスト抽出")
    print("-" * 80)
    text = extract_text_from_page(pdf_path, test_page)

    # CIDコードチェック
    has_cid, cid_list = check_for_cid_codes(text)
    if has_cid:
        print(f"[!] CIDコードが見つかりました: {len(cid_list)}件")
        print(f"   例: {cid_list[:5]}")
    else:
        print("[OK] CIDコードなし!")

    # テキストの一部を表示
    print(f"\nテキストサンプル (最初の500文字):")
    print(text[:500])

    print("\n" + "=" * 80)
    print(f"【テスト2】ページ {test_page + 1} の表抽出")
    print("-" * 80)
    tables = extract_tables_from_page(pdf_path, test_page)

    if tables:
        print(f"\n[OK] {len(tables)}個の表を抽出しました")

        # 最初の表の詳細を確認
        if len(tables) > 0:
            df = tables[0]['dataframe']
            print(f"\n【表の詳細確認】")
            print(f"形状: {df.shape}")
            print(f"\n全データ:")
            print(df.to_string())

            # CIDコードチェック
            df_text = df.to_string()
            has_cid, cid_list = check_for_cid_codes(df_text)
            if has_cid:
                print(f"\n[!] 表内にCIDコードが見つかりました: {len(cid_list)}件")
            else:
                print(f"\n[OK] 表内にCIDコードなし!")
    else:
        print("[!] 表が見つかりませんでした")

    print("\n" + "=" * 80)
    print("テスト完了")
    print("=" * 80)
