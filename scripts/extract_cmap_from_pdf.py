"""
PDFフォントからCMap（CIDからUnicodeへのマッピング）を抽出
"""

import sys
import io
from pathlib import Path
import fitz  # PyMuPDF

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("PDFフォントからCMapを抽出")
print("="*80)

pdf_path = Path('建設関連PDF') / '【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

print(f"\nPDFファイル: {pdf_path.name}")

# PDFを開く
doc = fitz.open(pdf_path)

print(f"総ページ数: {len(doc)}")

print("\n" + "="*80)
print("フォント情報の抽出")
print("="*80)

# 全ページのフォントを収集
all_fonts = {}

for page_num in range(len(doc)):
    page = doc[page_num]
    fonts = page.get_fonts(full=True)

    for font in fonts:
        xref = font[0]
        name = font[3]
        font_type = font[1]
        encoding = font[2]

        if xref not in all_fonts:
            all_fonts[xref] = {
                'name': name,
                'type': font_type,
                'encoding': encoding,
                'pages': [page_num + 1]
            }
        else:
            if page_num + 1 not in all_fonts[xref]['pages']:
                all_fonts[xref]['pages'].append(page_num + 1)

print(f"\n総フォント数: {len(all_fonts)}")

print("\n【フォント一覧】")
for xref, font_info in all_fonts.items():
    print(f"\nxref: {xref}")
    print(f"  名前: {font_info['name']}")
    print(f"  タイプ: {font_info['type']}")
    print(f"  エンコーディング: {font_info['encoding']}")
    print(f"  使用ページ: {font_info['pages'][:5]}{'...' if len(font_info['pages']) > 5 else ''}")

print("\n" + "="*80)
print("フォントファイルの抽出")
print("="*80)

# フォントデータを抽出
fonts_dir = Path('output') / 'extracted_fonts'
fonts_dir.mkdir(exist_ok=True)

extracted_count = 0

for xref, font_info in all_fonts.items():
    try:
        # フォントデータを抽出
        font_buffer = doc.extract_font(xref)

        if font_buffer:
            ext = font_buffer[0]  # 拡張子
            font_bytes = font_buffer[1]  # フォントバイト

            if font_bytes:
                font_name = font_info['name'].replace('/', '_').replace('\\', '_')
                output_path = fonts_dir / f"{font_name}_{xref}.{ext}"

                output_path.write_bytes(font_bytes)
                print(f"✓ 抽出: {output_path.name} ({len(font_bytes)} bytes)")
                extracted_count += 1
            else:
                print(f"⚠ xref {xref}: フォントデータが空")
        else:
            print(f"⚠ xref {xref}: フォント抽出失敗")

    except Exception as e:
        print(f"⚠ xref {xref}: エラー - {e}")

print(f"\n抽出完了: {extracted_count}/{len(all_fonts)} フォント")

print("\n" + "="*80)
print("CMap情報の抽出試行")
print("="*80)

# サンプルとして最初のページのテキストをdict形式で取得
page = doc[0]
text_dict = page.get_text("dict")

print(f"\nテキストブロック数: {len(text_dict.get('blocks', []))}")

# CIDフォントを使用しているspanを探す
cid_fonts_used = set()

for block in text_dict.get('blocks', []):
    if 'lines' in block:
        for line in block['lines']:
            for span in line.get('spans', []):
                font = span.get('font', '')
                text = span.get('text', '')

                # CIDフォントかチェック
                if 'CID' in font or 'Identity' in font:
                    cid_fonts_used.add(font)

if cid_fonts_used:
    print(f"\nCIDフォント使用例: {', '.join(list(cid_fonts_used)[:5])}")
else:
    print("\n⚠ CIDフォントが見つかりません")

print("\n" + "="*80)
print("PDFオブジェクトの詳細調査")
print("="*80)

# PyMuPDFでPDFの内部構造を直接調査
# xrefからオブジェクトを取得

for xref in list(all_fonts.keys())[:3]:  # 最初の3つのフォントを調査
    print(f"\n【xref {xref}】")

    try:
        # オブジェクトを取得
        obj = doc.xref_object(xref)
        print(f"オブジェクト情報:")
        print(obj[:500] if len(obj) > 500 else obj)  # 最初の500文字

        # ToUnicodeエントリを探す
        if 'ToUnicode' in obj:
            print("\n✓ ToUnicodeマッピングが存在！")

            # ToUnicodeのxrefを抽出
            import re
            match = re.search(r'/ToUnicode\s+(\d+)\s+\d+\s+R', obj)
            if match:
                tounicode_xref = int(match.group(1))
                print(f"ToUnicode xref: {tounicode_xref}")

                # ToUnicodeストリームを取得
                try:
                    tounicode_obj = doc.xref_object(tounicode_xref)
                    print(f"\nToUnicodeストリーム:")
                    print(tounicode_obj[:1000] if len(tounicode_obj) > 1000 else tounicode_obj)

                    # CMapデータを保存
                    cmap_path = fonts_dir / f"ToUnicode_{xref}.txt"
                    cmap_path.write_text(tounicode_obj, encoding='utf-8', errors='ignore')
                    print(f"\n保存: {cmap_path.name}")

                except Exception as e:
                    print(f"ToUnicodeストリーム取得エラー: {e}")

        else:
            print("⚠ ToUnicodeマッピングなし")

    except Exception as e:
        print(f"オブジェクト取得エラー: {e}")

doc.close()

print("\n" + "="*80)
print("完了")
print("="*80)

print("\n【結果】")
print(f"1. 抽出されたフォント: {fonts_dir}")
print(f"2. CMap情報があれば、ToUnicode_*.txtとして保存")
print("\n【次のステップ】")
print("ToUnicodeファイルが存在する場合、CIDからUnicodeへのマッピングを解析")
