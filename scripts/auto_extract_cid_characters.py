"""
PDFから正しいクメール文字を自動抽出してCIDマッピングを作成
"""

import sys
import io
import pandas as pd
from pathlib import Path
import fitz  # PyMuPDF
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("PDFから正しいクメール文字を自動抽出")
print("="*80)

# CIDマッピングテーブルを読み込む
mapping_path = Path('output') / 'CIDマッピングテーブル_入力用.csv'
mapping_df = pd.read_csv(mapping_path, encoding='utf-8-sig')

print(f"\nCIDマッピングテーブル: {len(mapping_df)}件")

# CID含有データを読み込む
cid_data_path = Path('output') / 'CIDコード含有データ_全22件.csv'
cid_data_df = pd.read_csv(cid_data_path, encoding='utf-8-sig')

print(f"CID含有データ: {len(cid_data_df)}件")

# PyMuPDFで抽出したデータを読み込む
pymupdf_path = Path('output') / 'カンボジア語_pymupdf_整形版.csv'
pymupdf_df = pd.read_csv(pymupdf_path, encoding='utf-8-sig')

print(f"PyMuPDF抽出データ: {len(pymupdf_df)}件")

# pdfplumberデータを読み込む
pdfplumber_path = Path('output') / '全言語統合_テンプレート_インポート用.csv'
pdfplumber_df = pd.read_csv(pdfplumber_path, encoding='utf-8-sig')

print(f"pdfplumber抽出データ: {len(pdfplumber_df)}件")

print("\n" + "="*80)
print("CIDコードから正しい文字を推定")
print("="*80)

# 各CIDコードについて処理
results = []

for idx, row in mapping_df.iterrows():
    cid_code = row['CIDコード']
    cid_num = row['CID番号']
    examples = row['例（日本語）']

    print(f"\n【{cid_code}】 (例: {examples})")

    # このCIDを含む単語を探す
    cid_words = cid_data_df[cid_data_df['km'].str.contains(re.escape(cid_code), na=False)]

    if len(cid_words) == 0:
        print(f"  ⚠ CIDを含む単語が見つかりません")
        continue

    # 最初の単語で試す
    first_word = cid_words.iloc[0]
    ja_word = first_word['ja']
    km_with_cid = first_word['km']

    print(f"  日本語: {ja_word}")
    print(f"  pdfplumber: {km_with_cid}")

    # PyMuPDFで同じ日本語単語を探す
    pymupdf_match = pymupdf_df[pymupdf_df['日本語'] == ja_word]

    if len(pymupdf_match) == 0:
        print(f"  ⚠ PyMuPDFに該当単語なし")
        results.append({
            'CIDコード': cid_code,
            'CID番号': cid_num,
            '日本語例': ja_word,
            'pdfplumber': km_with_cid,
            'PyMuPDF': '',
            '推定文字': '',
            '信頼度': '低'
        })
        continue

    pymupdf_text = pymupdf_match.iloc[0]['翻訳']
    print(f"  PyMuPDF: {pymupdf_text}")

    # CIDコードの位置を特定
    cid_positions = []
    for match in re.finditer(re.escape(cid_code), km_with_cid):
        cid_positions.append(match.start())

    print(f"  CID位置: {cid_positions}")

    # 簡易的な推定: PyMuPDFのテキストから対応する文字を探す
    # CIDコードの前後の文字列を使って位置を推定
    estimated_chars = []

    for pos in cid_positions:
        # CIDの前後の文字を取得（コンテキスト）
        before = km_with_cid[max(0, pos-3):pos]
        after = km_with_cid[pos+len(cid_code):pos+len(cid_code)+3]

        # CID以外の文字を抽出（コンテキストマッチング用）
        before_clean = re.sub(r'\(cid:\d+\)', '', before)
        after_clean = re.sub(r'\(cid:\d+\)', '', after)

        print(f"    前後コンテキスト: '{before_clean}' [{cid_code}] '{after_clean}'")

        # PyMuPDFのテキストで同じコンテキストを探す
        if before_clean and before_clean in pymupdf_text:
            before_pos = pymupdf_text.find(before_clean)
            # CIDの位置に相当する文字を推定
            estimated_pos = before_pos + len(before_clean)

            if estimated_pos < len(pymupdf_text):
                # 1文字取得（クメール語の結合文字を考慮）
                estimated_char = pymupdf_text[estimated_pos]

                # 次の文字が結合文字かチェック（U+17B6-U+17D3の範囲）
                if estimated_pos + 1 < len(pymupdf_text):
                    next_char = pymupdf_text[estimated_pos + 1]
                    if '\u17b6' <= next_char <= '\u17d3':
                        estimated_char += next_char

                estimated_chars.append(estimated_char)
                print(f"    推定文字: {estimated_char}")
            else:
                print(f"    ⚠ 位置が範囲外")
        else:
            print(f"    ⚠ コンテキストマッチング失敗")

    # 最も頻出する推定文字を選択
    if estimated_chars:
        from collections import Counter
        most_common = Counter(estimated_chars).most_common(1)[0][0]
        confidence = "高" if len(set(estimated_chars)) == 1 else "中"
    else:
        most_common = ""
        confidence = "低"

    results.append({
        'CIDコード': cid_code,
        'CID番号': cid_num,
        '日本語例': ja_word,
        'pdfplumber': km_with_cid,
        'PyMuPDF': pymupdf_text,
        '推定文字': most_common,
        '信頼度': confidence
    })

    print(f"  ✓ 推定完了: {most_common} (信頼度: {confidence})")

# 結果をDataFrameに変換
results_df = pd.DataFrame(results)

# マッピングテーブルを更新
mapping_df = mapping_df.merge(
    results_df[['CIDコード', '推定文字', '信頼度']],
    on='CIDコード',
    how='left'
)

# 保存
output_path = Path('output') / 'CIDマッピング_自動推定結果.csv'
mapping_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n" + "="*80)
print("結果の保存")
print("="*80)
print(f"保存先: {output_path}")

# 統計
print(f"\n【統計】")
print(f"総CIDコード数: {len(results_df)}")
print(f"推定成功（高信頼度）: {len(results_df[results_df['信頼度'] == '高'])}件")
print(f"推定成功（中信頼度）: {len(results_df[results_df['信頼度'] == '中'])}件")
print(f"推定失敗（低信頼度）: {len(results_df[results_df['信頼度'] == '低'])}件")

print(f"\n【警告】")
print("PyMuPDFのテキストも完全に正確ではない可能性があります。")
print("推定結果は参考程度にし、元のPDFと目視確認することを推奨します。")

print("\n" + "="*80)
print("完了")
print("="*80)
