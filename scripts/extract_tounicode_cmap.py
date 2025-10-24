"""
ToUnicode CMMapを展開してCIDからUnicodeへのマッピングを抽出
"""

import sys
import io
from pathlib import Path
import fitz  # PyMuPDF
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("ToUnicode CMMapを展開")
print("="*80)

pdf_path = Path('建設関連PDF') / '【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

print(f"\nPDFファイル: {pdf_path.name}")

# PDFを開く
doc = fitz.open(pdf_path)

print(f"総ページ数: {len(doc)}")

# LeelawadeeUIフォント（カンボジア語用）を探す
print("\n" + "="*80)
print("カンボジア語フォント（LeelawadeeUI）を探索")
print("="*80)

target_fonts = []

for page_num in range(min(5, len(doc))):  # 最初の5ページを確認
    page = doc[page_num]
    fonts = page.get_fonts(full=True)

    for font in fonts:
        xref = font[0]
        name = font[3]
        font_type = font[1]
        encoding = font[2]

        if 'LeelawadeeUI' in name:
            target_fonts.append({
                'xref': xref,
                'name': name,
                'type': font_type,
                'encoding': encoding,
                'page': page_num + 1
            })
            print(f"\n✓ 発見: {name} (xref:{xref}, ページ:{page_num + 1})")

print(f"\n総LeelawadeeUIフォント数: {len(target_fonts)}")

# 最初のLeelawadeeUIフォントで試す
if target_fonts:
    print("\n" + "="*80)
    print("ToUnicodeマッピングを抽出")
    print("="*80)

    for font_info in target_fonts[:3]:  # 最初の3つ
        xref = font_info['xref']
        name = font_info['name']

        print(f"\n【{name} (xref:{xref})】")

        try:
            # フォントオブジェクトを取得
            obj = doc.xref_object(xref)

            # ToUnicodeエントリを探す
            if 'ToUnicode' in obj:
                print("✓ ToUnicodeマッピングあり")

                # ToUnicodeのxrefを抽出
                match = re.search(r'/ToUnicode\s+(\d+)\s+\d+\s+R', obj)
                if match:
                    tounicode_xref = int(match.group(1))
                    print(f"ToUnicode xref: {tounicode_xref}")

                    # ToUnicodeストリームを取得（圧縮されている）
                    try:
                        # ストリームデータを取得（自動展開）
                        tounicode_stream = doc.xref_stream(tounicode_xref)

                        if tounicode_stream:
                            # バイトデータをUTF-8でデコード
                            try:
                                cmap_text = tounicode_stream.decode('utf-8', errors='ignore')
                            except:
                                # Latin-1でデコード
                                cmap_text = tounicode_stream.decode('latin-1', errors='ignore')

                            print(f"\nCMapサイズ: {len(cmap_text)} bytes")
                            print(f"\nCMap内容（最初の1000文字）:")
                            print(cmap_text[:1000])

                            # CMapをファイルに保存
                            output_dir = Path('output') / 'extracted_cmaps'
                            output_dir.mkdir(exist_ok=True)

                            output_path = output_dir / f"CMap_{name.replace('/', '_')}_{xref}.txt"
                            output_path.write_text(cmap_text, encoding='utf-8')
                            print(f"\n保存: {output_path.name}")

                            # CIDからUnicodeへのマッピングを抽出
                            print("\n" + "="*60)
                            print("CID→Unicodeマッピングを解析")
                            print("="*60)

                            # <CID> <Unicode>のパターンを探す
                            # 例: <0001> <0E01>
                            mappings = []

                            # beginbfcharセクションを探す
                            bfchar_pattern = r'beginbfchar\s+(.*?)\s+endbfchar'
                            bfchar_matches = re.findall(bfchar_pattern, cmap_text, re.DOTALL)

                            for section in bfchar_matches:
                                # <CID> <Unicode>のペアを抽出
                                pairs = re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', section)
                                for cid_hex, unicode_hex in pairs:
                                    cid = int(cid_hex, 16)

                                    # 結合文字の処理（4桁ずつに分割）
                                    unicode_chars = []
                                    for i in range(0, len(unicode_hex), 4):
                                        char_hex = unicode_hex[i:i+4]
                                        try:
                                            unicode_chars.append(chr(int(char_hex, 16)))
                                        except ValueError:
                                            pass

                                    unicode_char = ''.join(unicode_chars)
                                    mappings.append((cid, unicode_char, unicode_hex))

                            # beginbfrangeセクションも探す
                            bfrange_pattern = r'beginbfrange\s+(.*?)\s+endbfrange'
                            bfrange_matches = re.findall(bfrange_pattern, cmap_text, re.DOTALL)

                            for section in bfrange_matches:
                                # <開始CID> <終了CID> <開始Unicode>のパターン
                                ranges = re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', section)
                                for start_cid_hex, end_cid_hex, start_unicode_hex in ranges:
                                    start_cid = int(start_cid_hex, 16)
                                    end_cid = int(end_cid_hex, 16)

                                    # 結合文字の処理（4桁ずつに分割）
                                    if len(start_unicode_hex) > 4:
                                        # 結合文字の場合はスキップ（連続マッピングには使えない）
                                        continue

                                    start_unicode = int(start_unicode_hex, 16)

                                    for i in range(end_cid - start_cid + 1):
                                        cid = start_cid + i
                                        unicode_char = chr(start_unicode + i)
                                        unicode_hex = f"{start_unicode + i:04X}"
                                        mappings.append((cid, unicode_char, unicode_hex))

                            print(f"\n抽出されたマッピング数: {len(mappings)}")

                            if mappings:
                                # サンプル表示
                                print("\nマッピングサンプル（最初の20件）:")
                                for cid, unicode_char, unicode_hex in mappings[:20]:
                                    print(f"  CID {cid:4d} → U+{unicode_hex} ({unicode_char})")

                                # マッピングをCSVに保存
                                import pandas as pd
                                mapping_df = pd.DataFrame(mappings, columns=['CID', 'Unicode文字', 'Unicode16進'])
                                mapping_csv = output_dir / f"CIDマッピング_{name.replace('/', '_')}_{xref}.csv"
                                mapping_df.to_csv(mapping_csv, index=False, encoding='utf-8-sig')
                                print(f"\nマッピングCSV保存: {mapping_csv.name}")

                                # 問題のCIDコード（540, 544, 559など）を探す
                                print("\n" + "="*60)
                                print("問題のCIDコードを検索")
                                print("="*60)

                                problem_cids = [540, 544, 545, 559, 564, 572, 598, 622, 625, 630,
                                                635, 636, 640, 645, 647, 671, 676, 688, 690, 693,
                                                694, 698, 717, 719, 726, 801, 813, 814, 817, 819,
                                                822, 843]

                                for cid in problem_cids:
                                    found = [m for m in mappings if m[0] == cid]
                                    if found:
                                        unicode_char, unicode_hex = found[0][1], found[0][2]
                                        print(f"  (cid:{cid}) → U+{unicode_hex} ({unicode_char})")
                                    else:
                                        print(f"  (cid:{cid}) → ⚠ マッピングなし")

                        else:
                            print("⚠ ToUnicodeストリームが空")

                    except Exception as e:
                        print(f"⚠ ToUnicodeストリーム取得エラー: {e}")
                else:
                    print("⚠ ToUnicode xrefが見つかりません")
            else:
                print("⚠ ToUnicodeマッピングなし")

        except Exception as e:
            print(f"⚠ オブジェクト取得エラー: {e}")

else:
    print("\n⚠ LeelawadeeUIフォントが見つかりません")

doc.close()

print("\n" + "="*80)
print("完了")
print("="*80)
