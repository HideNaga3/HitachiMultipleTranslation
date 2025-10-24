"""
PDFからCIDマッピングを抽出
PyMuPDFとpdfminerを使ってフォント情報を取得
"""

import sys
import io
from pathlib import Path
import pdfplumber
import fitz  # PyMuPDF

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("PDFフォント情報からCIDマッピングを抽出")
print("="*80)

pdf_path = Path('建設関連PDF') / '【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

print(f"\nPDFファイル: {pdf_path.name}")

# ===== 方法1: pdfplumber =====
print("\n" + "="*80)
print("方法1: pdfplumber でフォント情報を取得")
print("="*80)

try:
    with pdfplumber.open(pdf_path) as pdf:
        # 最初のページを確認
        page = pdf.pages[0]

        print(f"\n総ページ数: {len(pdf.pages)}")
        print(f"ページ1のサイズ: {page.width} x {page.height}")

        # フォント情報を取得
        if hasattr(page, 'fonts'):
            print(f"\nフォント情報:")
            for font_name, font_info in page.fonts.items():
                print(f"\nフォント名: {font_name}")
                print(f"  情報: {font_info}")

        # 文字情報を取得
        if hasattr(page, 'chars'):
            chars = page.chars[:10]  # 最初の10文字
            print(f"\n文字情報（最初の10文字）:")
            for i, char in enumerate(chars):
                print(f"\n  文字{i+1}:")
                print(f"    text: {char.get('text', 'N/A')}")
                print(f"    fontname: {char.get('fontname', 'N/A')}")
                print(f"    size: {char.get('size', 'N/A')}")

except Exception as e:
    print(f"pdfplumberでのエラー: {e}")

# ===== 方法2: PyMuPDF =====
print("\n" + "="*80)
print("方法2: PyMuPDF でフォント情報を取得")
print("="*80)

try:
    doc = fitz.open(pdf_path)
    page = doc[0]

    print(f"\n総ページ数: {len(doc)}")

    # フォント情報を取得
    font_list = page.get_fonts()
    print(f"\nフォント一覧: {len(font_list)}個")

    for i, font in enumerate(font_list[:5]):  # 最初の5個
        print(f"\nフォント{i+1}:")
        print(f"  xref: {font[0]}")
        print(f"  name: {font[3]}")
        print(f"  type: {font[1]}")
        print(f"  encoding: {font[2]}")

    # テキストを抽出してフォント情報を確認
    text_dict = page.get_text("dict")

    print(f"\nテキストブロック数: {len(text_dict.get('blocks', []))}")

    # 最初のテキストブロックを詳細表示
    blocks = text_dict.get('blocks', [])
    if len(blocks) > 0:
        first_block = blocks[0]
        if 'lines' in first_block:
            print(f"\n最初のテキストブロックの詳細:")
            for line_idx, line in enumerate(first_block['lines'][:3]):
                print(f"\n  行{line_idx+1}:")
                for span in line.get('spans', []):
                    text = span.get('text', '')
                    font = span.get('font', '')
                    print(f"    text: {text}")
                    print(f"    font: {font}")
                    print(f"    size: {span.get('size', 0)}")

    doc.close()

except Exception as e:
    print(f"PyMuPDFでのエラー: {e}")

# ===== 方法3: pdfminer.six =====
print("\n" + "="*80)
print("方法3: pdfminer.six で低レベルなPDF解析")
print("="*80)

try:
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTChar, LTTextBox

    for page_num, page_layout in enumerate(extract_pages(pdf_path)):
        if page_num > 0:  # 最初のページのみ
            break

        print(f"\nページ {page_num + 1}:")

        char_count = 0
        for element in page_layout:
            if isinstance(element, LTTextBox):
                for text_line in element:
                    for char in text_line:
                        if isinstance(char, LTChar):
                            char_count += 1
                            if char_count <= 10:  # 最初の10文字
                                print(f"\n  文字{char_count}:")
                                print(f"    text: {char.get_text()}")
                                print(f"    font: {char.fontname}")
                                print(f"    size: {char.size}")
                                # CIDフォントの場合
                                if hasattr(char, 'cid'):
                                    print(f"    cid: {char.cid}")

        print(f"\n総文字数: {char_count}")

except Exception as e:
    print(f"pdfminerでのエラー: {e}")

# ===== CIDマッピングの可能性 =====
print("\n" + "="*80)
print("CIDマッピング取得の可能性")
print("="*80)

print("""
【結論】

1. pdfplumber:
   - フォント情報へのアクセスは限定的
   - CIDマッピングは直接取得できない

2. PyMuPDF:
   - フォント情報は取得可能
   - ただしCID→Unicode変換マッピングは提供していない

3. pdfminer.six:
   - より低レベルなアクセスが可能
   - PDFの内部構造を解析できる
   - CIDフォント情報にアクセス可能

【次のステップ】

CIDマッピングを取得するには：

方法A: PDFの埋め込みフォントを抽出して解析
  - フォントファイル（.ttf, .otf等）を抽出
  - フォントのCMap（Character Map）を解析
  - 高度なPDF知識が必要

方法B: 既知のCIDコードを元PDFと照合して手動でマッピング作成
  - 発見された22件のCIDコードのみ
  - 元PDFから正しい文字をコピー
  - マッピングテーブルを作成
  - 現実的かつ確実

方法C: pdfminerを使ってCIDフォント情報を詳細解析
  - より複雑だが、自動化の可能性あり
""")

print("\n" + "="*80)
print("調査完了")
print("="*80)
