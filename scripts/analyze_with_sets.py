"""
setを使って一致・不一致を分析
"""

import pandas as pd
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("set集合演算による分析")
print("="*80)

# ファイル読み込み
pymupdf_csv = Path('output') / 'カンボジア語_pymupdf_整形版.csv'
pdfplumber_csv = Path('output') / '全言語統合_テンプレート_インポート用.csv'

pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')
pdfplumber_df = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

print(f"\nPyMuPDF: {len(pymupdf_df)}行")
print(f"pdfplumber: {len(pdfplumber_df)}行")

# 日本語単語のsetを作成
pymupdf_words = set(pymupdf_df['日本語'].dropna().str.strip())
pdfplumber_words = set(pdfplumber_df['ja'].dropna().str.strip())

print(f"\n【集合の大きさ】")
print(f"PyMuPDFのユニーク単語: {len(pymupdf_words)}語")
print(f"pdfplumberのユニーク単語: {len(pdfplumber_words)}語")

# 積集合（両方に存在）
both = pymupdf_words & pdfplumber_words

# 差集合
only_pymupdf = pymupdf_words - pdfplumber_words
only_pdfplumber = pdfplumber_words - pymupdf_words

print(f"\n" + "="*80)
print("集合演算の結果")
print("="*80)
print(f"両方に存在（積集合）: {len(both)}語")
print(f"PyMuPDFのみ（差集合）: {len(only_pymupdf)}語")
print(f"pdfplumberのみ（差集合）: {len(only_pdfplumber)}語")

# 割合
total_unique = len(pymupdf_words | pdfplumber_words)
print(f"\n全ユニーク単語数（和集合）: {total_unique}語")
print(f"一致率: {len(both)/total_unique*100:.1f}%")

# 詳細表示
if len(only_pymupdf) > 0:
    print(f"\n" + "="*80)
    print(f"PyMuPDFのみに存在する単語（最初の20件）")
    print("="*80)
    for i, word in enumerate(sorted(only_pymupdf)[:20], 1):
        # PyMuPDFでの出現回数
        count = (pymupdf_df['日本語'] == word).sum()
        print(f"{i:2}. {word} ({count}回)")

if len(only_pdfplumber) > 0:
    print(f"\n" + "="*80)
    print(f"pdfplumberのみに存在する単語（最初の20件）")
    print("="*80)
    for i, word in enumerate(sorted(only_pdfplumber)[:20], 1):
        # pdfplumberでの出現回数
        count = (pdfplumber_df['ja'] == word).sum()
        print(f"{i:2}. {word} ({count}回)")

# 翻訳の比較（両方に存在する単語のみ）
print(f"\n" + "="*80)
print(f"翻訳の比較（両方に存在する{len(both)}語）")
print("="*80)

# 両方に存在する単語について翻訳を比較
comparison_results = []

for word in sorted(both):
    # PyMuPDFから取得（重複がある場合は最初の1つ）
    py_row = pymupdf_df[pymupdf_df['日本語'] == word].iloc[0]
    py_trans = str(py_row['翻訳']).strip()
    py_page = py_row['Page']
    py_no = py_row['No']

    # pdfplumberから取得
    pdf_row = pdfplumber_df[pdfplumber_df['ja'] == word].iloc[0]
    pdf_trans = str(pdf_row['km']).strip()

    # 改行を削除して比較
    py_trans_clean = py_trans.replace('\n', ' ').strip()
    pdf_trans_clean = pdf_trans.replace('\n', ' ').strip()

    is_match = py_trans_clean == pdf_trans_clean

    comparison_results.append({
        '日本語': word,
        'PyMuPDF値': py_trans_clean,
        'pdfplumber値': pdf_trans_clean,
        '一致': is_match,
        'Page': py_page,
        'No': py_no
    })

comparison_df = pd.DataFrame(comparison_results)

# 一致・不一致の統計
match_count = comparison_df['一致'].sum()
mismatch_count = len(comparison_df) - match_count

print(f"翻訳一致: {match_count}語 ({match_count/len(comparison_df)*100:.1f}%)")
print(f"翻訳不一致: {mismatch_count}語 ({mismatch_count/len(comparison_df)*100:.1f}%)")

# 不一致のサンプル
mismatches = comparison_df[comparison_df['一致'] == False]
if len(mismatches) > 0:
    print(f"\n翻訳不一致のサンプル（最初の10件）:")
    for idx, row in mismatches.head(10).iterrows():
        print(f"\n  {row['日本語']} (Page:{row['Page']}, No:{row['No']})")
        print(f"    PyMuPDF   : {row['PyMuPDF値'][:60]}")
        print(f"    pdfplumber: {row['pdfplumber値'][:60]}")

# 結果をCSVに保存
output_both = Path('output') / '両方に存在する単語.csv'
output_only_py = Path('output') / 'PyMuPDFのみの単語.csv'
output_only_pdf = Path('output') / 'pdfplumberのみの単語.csv'
output_comparison = Path('output') / '翻訳比較_両方存在.csv'

# 両方に存在する単語
both_df = pd.DataFrame({'日本語': sorted(both)})
both_df.to_csv(output_both, index=False, encoding='utf-8-sig')

# PyMuPDFのみ
if len(only_pymupdf) > 0:
    only_py_df = pd.DataFrame({'日本語': sorted(only_pymupdf)})
    only_py_df.to_csv(output_only_py, index=False, encoding='utf-8-sig')

# pdfplumberのみ
if len(only_pdfplumber) > 0:
    only_pdf_df = pd.DataFrame({'日本語': sorted(only_pdfplumber)})
    only_pdf_df.to_csv(output_only_pdf, index=False, encoding='utf-8-sig')

# 翻訳比較
comparison_df.to_csv(output_comparison, index=False, encoding='utf-8-sig')

print(f"\n" + "="*80)
print("保存完了")
print("="*80)
print(f"1. 両方に存在: {output_both}")
print(f"2. PyMuPDFのみ: {output_only_py}")
print(f"3. pdfplumberのみ: {output_only_pdf}")
print(f"4. 翻訳比較: {output_comparison}")
print("="*80)
