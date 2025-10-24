"""
pdfplumberとPyMuPDFの抽出結果を比較
特にCIDコードがあった箇所を確認
"""

import pandas as pd
from pathlib import Path

print("="*80)
print("pdfplumber vs PyMuPDF 抽出結果の比較")
print("="*80)

# pdfplumberで抽出したCSV
pdfplumber_csv = Path('output') / 'カンボジア語_pdfplumber_抽出_最終版.csv'
# PyMuPDFで抽出したCSV
pymupdf_csv = Path('output') / 'test_カンボジア語_pymupdf抽出.csv'

# 両方のファイルが存在するか確認
if not pdfplumber_csv.exists():
    print(f"[!] pdfplumberのCSVが見つかりません: {pdfplumber_csv}")
    # 代わりに統合CSVから検索
    print("\n統合CSVからカンボジア語データを検索します...")
    unified_csv = Path('output') / '全言語統合_pdfplumber_最終版.csv'
    if unified_csv.exists():
        unified_df = pd.read_csv(unified_csv, encoding='utf-8-sig')
        # カンボジア語のみ抽出
        pdfplumber_df = unified_df[unified_df['language'] == 'カンボジア語'].copy()
        print(f"カンボジア語のデータ: {len(pdfplumber_df)}行")
    else:
        print(f"[!] 統合CSVも見つかりません: {unified_csv}")
        pdfplumber_df = None
else:
    pdfplumber_df = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

if not pymupdf_csv.exists():
    print(f"[!] PyMuPDFのCSVが見つかりません: {pymupdf_csv}")
    pymupdf_df = None
else:
    pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')

if pdfplumber_df is None or pymupdf_df is None:
    print("\n比較に必要なファイルが見つかりません")
    exit(1)

# PyMuPDFデータの整形（日本語と翻訳のみ抽出）
pymupdf_clean = pymupdf_df[['Column_1', 'Column_3']].copy()
pymupdf_clean.columns = ['japanese', 'translation']
pymupdf_clean = pymupdf_clean.dropna(subset=['japanese'])

print(f"\npdfplumberデータ: {len(pdfplumber_df)}行")
print(f"PyMuPDFデータ: {len(pymupdf_clean)}行")

# CIDコードを含む行を検索（pdfplumber）
import re
cid_pattern = r'\(cid:\d+\)'

if 'translation' in pdfplumber_df.columns:
    pdfplumber_cid = pdfplumber_df[
        pdfplumber_df['translation'].astype(str).str.contains(cid_pattern, regex=True, na=False)
    ]
else:
    # 全列を検索
    pdfplumber_cid_mask = False
    for col in pdfplumber_df.columns:
        if pdfplumber_df[col].dtype == 'object':
            pdfplumber_cid_mask |= pdfplumber_df[col].astype(str).str.contains(cid_pattern, regex=True, na=False)
    pdfplumber_cid = pdfplumber_df[pdfplumber_cid_mask]

print(f"\npdfplumberでCIDコードを含む行: {len(pdfplumber_cid)}行")

if len(pdfplumber_cid) > 0:
    print("\nCIDコードがあった単語（最初の10件）:")
    for idx, row in pdfplumber_cid.head(10).iterrows():
        if 'japanese' in row and 'translation' in row:
            japanese = row['japanese']
            translation = row['translation']
        else:
            # 列名が異なる場合
            japanese = row.get('word', row.get('単語', '?'))
            translation = str(row.values)

        # CIDコードを抽出
        cid_codes = re.findall(cid_pattern, str(translation))
        print(f"  {japanese}: {translation[:100]}")
        print(f"    -> CIDコード: {cid_codes}")

# 同じ単語をPyMuPDFデータから検索
print("\n" + "="*80)
print("PyMuPDFで同じ単語がどう抽出されているか確認")
print("="*80)

# pdfplumberでCIDがあった単語の最初の5件
sample_words = []
for idx, row in pdfplumber_cid.head(5).iterrows():
    if 'japanese' in row:
        word = row['japanese']
    else:
        # 他の列名を試す
        for col in ['word', '単語', 'Column_1']:
            if col in row:
                word = row[col]
                break
        else:
            continue

    if pd.notna(word):
        sample_words.append(word)

for word in sample_words:
    print(f"\n日本語: {word}")

    # pdfplumberの結果
    if 'japanese' in pdfplumber_df.columns:
        pdf_row = pdfplumber_df[pdfplumber_df['japanese'] == word]
    else:
        pdf_row = None
        for col in ['word', '単語', 'Column_1']:
            if col in pdfplumber_df.columns:
                pdf_row = pdfplumber_df[pdfplumber_df[col] == word]
                if len(pdf_row) > 0:
                    break

    if pdf_row is not None and len(pdf_row) > 0:
        trans_col = 'translation' if 'translation' in pdf_row.columns else pdf_row.columns[3]
        pdf_trans = pdf_row.iloc[0][trans_col]
        print(f"  pdfplumber: {pdf_trans}")

    # PyMuPDFの結果
    py_row = pymupdf_clean[pymupdf_clean['japanese'] == word]
    if len(py_row) > 0:
        py_trans = py_row.iloc[0]['translation']
        print(f"  PyMuPDF   : {py_trans}")
    else:
        print(f"  PyMuPDF   : (見つかりません)")

print("\n" + "="*80)
print("比較完了")
print("="*80)
