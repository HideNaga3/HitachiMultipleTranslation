"""
OCRを使用してPDFから正しいクメール文字を抽出
"""

import sys
import io
import pandas as pd
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import re
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("OCRを使用してクメール文字を抽出")
print("="*80)

# Tesseractのパス設定（Windowsの場合）
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# サポート言語を確認
try:
    langs = pytesseract.get_languages()
    print(f"\nTesseractサポート言語: {', '.join(langs)}")

    if 'khm' in langs:
        print("✓ クメール語（khm）サポートあり")
    else:
        print("⚠ クメール語（khm）サポートなし")
        print("\nTesseractにクメール語データをインストールする必要があります:")
        print("https://github.com/tesseract-ocr/tessdata")
        sys.exit(1)

except Exception as e:
    print(f"⚠ Tesseractが見つかりません: {e}")
    print("\nTesseractをインストールしてください:")
    print("https://github.com/tesseract-ocr/tesseract")
    sys.exit(1)

# PDFファイル
pdf_path = Path('建設関連PDF') / '【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

print(f"\nPDFファイル: {pdf_path.name}")

# CID含有データを読み込む
cid_data_path = Path('output') / 'CIDコード含有データ_全22件.csv'
cid_data_df = pd.read_csv(cid_data_path, encoding='utf-8-sig')

print(f"CID含有データ: {len(cid_data_df)}件")

# PDFを開く
doc = fitz.open(pdf_path)

print(f"\n総ページ数: {len(doc)}")

print("\n" + "="*80)
print("サンプルページでOCRテスト（ページ1）")
print("="*80)

# 最初のページでテスト
page = doc[0]

# ページを画像に変換（高解像度）
zoom = 2.0  # 解像度を上げる
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)

# PIL Imageに変換
img_data = pix.tobytes("png")
img = Image.open(io.BytesIO(img_data))

print(f"\n画像サイズ: {img.size}")
print("OCR実行中...")

# OCR実行（クメール語）
try:
    # クメール語 + 英語の組み合わせ
    ocr_text = pytesseract.image_to_string(img, lang='khm+eng')
    print(f"\nOCR結果（最初の500文字）:")
    print(ocr_text[:500])

    # OCRで取得したテキストをファイルに保存
    output_ocr = Path('output') / 'OCR結果_ページ1.txt'
    output_ocr.write_text(ocr_text, encoding='utf-8')
    print(f"\n保存先: {output_ocr}")

except Exception as e:
    print(f"⚠ OCRエラー: {e}")

doc.close()

print("\n" + "="*80)
print("テスト完了")
print("="*80)
print("\n【次のステップ】")
print("OCRの精度を確認後、全ページでCID箇所のみを抽出する機能を実装")
