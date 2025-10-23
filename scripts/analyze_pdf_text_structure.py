# -*- coding: utf-8 -*-
"""
PDFの内部テキスト構造を詳しく分析

pdfplumberでテキストを直接抽出して、
カンボジア語の翻訳データがどのように保存されているかを調べます。
"""

import pdfplumber
import pandas as pd

def analyze_pdf_page(page, page_num):
    """
    1ページのテキスト構造を詳しく分析

    Args:
        page: pdfplumberのPageオブジェクト
        page_num: ページ番号
    """
    print(f"\n{'=' * 80}")
    print(f"ページ {page_num} の分析")
    print(f"{'=' * 80}")

    # すべてのテキストを取得
    text = page.extract_text()
    print(f"\nページ全体のテキスト（最初の500文字）:")
    try:
        print(text[:500] if text else "[テキストなし]")
    except:
        print("[カンボジア語・表示不可]")

    # 文字オブジェクトを取得（座標付き）
    chars = page.chars
    print(f"\n文字オブジェクト数: {len(chars)}")

    if chars:
        # カンボジア語文字を探す（Unicodeブロック: 0x1780-0x17FF）
        khmer_chars = [c for c in chars if '\u1780' <= c.get('text', '') <= '\u17FF']
        print(f"カンボジア語文字数: {len(khmer_chars)}")

        # サンプルを表示
        if khmer_chars:
            print(f"\nカンボジア語文字のサンプル（最初の10文字）:")
            for i, char in enumerate(khmer_chars[:10]):
                x0, y0 = char.get('x0', 0), char.get('top', 0)
                text_val = char.get('text', '')
                fontname = char.get('fontname', '?')
                try:
                    print(f"  {i}: '{text_val}' @ ({x0:.1f}, {y0:.1f}) font={fontname}")
                except:
                    print(f"  {i}: [表示不可] @ ({x0:.1f}, {y0:.1f}) font={fontname}")

    # 行ごとにテキストを抽出
    print(f"\n行ごとのテキスト抽出:")

    # テキストを位置でグループ化
    if chars:
        # y座標でソート
        chars_sorted = sorted(chars, key=lambda c: (c.get('top', 0), c.get('x0', 0)))

        # 行をグループ化（y座標が近いものを同じ行とみなす）
        lines = []
        current_line = []
        current_y = None
        tolerance = 5  # y座標の許容差

        for char in chars_sorted:
            y = char.get('top', 0)

            if current_y is None or abs(y - current_y) <= tolerance:
                current_line.append(char)
                current_y = y
            else:
                if current_line:
                    lines.append(current_line)
                current_line = [char]
                current_y = y

        if current_line:
            lines.append(current_line)

        print(f"検出された行数: {len(lines)}")

        # 最初の10行を表示
        print(f"\n最初の10行のテキスト:")
        for i, line in enumerate(lines[:10]):
            line_text = ''.join([c.get('text', '') for c in line])
            x_positions = [c.get('x0', 0) for c in line]

            try:
                print(f"\n  行{i}: '{line_text}'")
            except:
                print(f"\n  行{i}: [カンボジア語・表示不可]")

            print(f"    文字数: {len(line)}, X位置範囲: {min(x_positions):.1f} - {max(x_positions):.1f}")

            # カンボジア語文字を含む場合
            khmer_in_line = [c for c in line if '\u1780' <= c.get('text', '') <= '\u17FF']
            if khmer_in_line:
                khmer_text = ''.join([c.get('text', '') for c in khmer_in_line])
                try:
                    print(f"    カンボジア語: '{khmer_text}'")
                except:
                    print(f"    カンボジア語: [表示不可] ({len(khmer_in_line)}文字)")

def main():
    """メイン処理"""
    pdf_file = "建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf"

    print("=" * 80)
    print("PDFテキスト構造分析")
    print("=" * 80)
    print(f"\nPDFファイル: {pdf_file}")

    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        print(f"総ページ数: {total_pages}")

        # 最初の3ページを詳しく分析
        for page_num in range(1, min(4, total_pages + 1)):
            page = pdf.pages[page_num - 1]
            analyze_pdf_page(page, page_num)

    print(f"\n{'=' * 80}")
    print("分析完了")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    main()
