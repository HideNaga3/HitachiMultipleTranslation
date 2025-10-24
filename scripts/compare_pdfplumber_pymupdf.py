"""
pdfplumberとPyMuPDFの抽出結果を詳細比較
- CIDコードによる不一致をカウント
- それ以外の不一致をカウント
"""

import pandas as pd
import re
from pathlib import Path

print("="*80)
print("pdfplumber vs PyMuPDF 詳細比較")
print("="*80)

# CSVファイル読み込み
pdfplumber_csv = Path('output') / '全言語統合_テンプレート_インポート用.csv'
pymupdf_csv = Path('output') / 'test_カンボジア語_pymupdf抽出.csv'

# データ読み込み
pdfplumber_df = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')
pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')

print(f"\npdfplumberデータ: {len(pdfplumber_df)}行")
print(f"PyMuPDFデータ: {len(pymupdf_df)}行")

# PyMuPDFデータを整形（日本語と翻訳のみ）
pymupdf_clean = pymupdf_df[['Column_1', 'Column_3']].copy()
pymupdf_clean.columns = ['japanese', 'translation_pymupdf']
pymupdf_clean = pymupdf_clean.dropna(subset=['japanese'])
# 空白除去
pymupdf_clean['japanese'] = pymupdf_clean['japanese'].str.strip()
pymupdf_clean['translation_pymupdf'] = pymupdf_clean['translation_pymupdf'].fillna('')

# pdfplumberデータ（日本語とカンボジア語）
pdfplumber_clean = pdfplumber_df[['ja', 'km']].copy()
pdfplumber_clean.columns = ['japanese', 'translation_pdfplumber']
pdfplumber_clean['japanese'] = pdfplumber_clean['japanese'].str.strip()
pdfplumber_clean['translation_pdfplumber'] = pdfplumber_clean['translation_pdfplumber'].fillna('')

print(f"\nクリーニング後:")
print(f"  pdfplumber: {len(pdfplumber_clean)}行")
print(f"  PyMuPDF: {len(pymupdf_clean)}行")

# 日本語単語でマージ
merged = pdfplumber_clean.merge(
    pymupdf_clean,
    on='japanese',
    how='outer',
    indicator=True
)

print(f"\nマージ結果:")
print(f"  両方に存在: {len(merged[merged['_merge'] == 'both'])}語")
print(f"  pdfplumberのみ: {len(merged[merged['_merge'] == 'left_only'])}語")
print(f"  PyMuPDFのみ: {len(merged[merged['_merge'] == 'right_only'])}語")

# 両方に存在する単語で比較
both_df = merged[merged['_merge'] == 'both'].copy()

print(f"\n" + "="*80)
print("翻訳の比較（両方に存在する{0}語）".format(len(both_df)))
print("="*80)

# CIDコードパターン
cid_pattern = r'\(cid:\d+\)'

# 比較結果を格納
results = {
    'perfect_match': 0,           # 完全一致
    'cid_mismatch': 0,            # CIDコードによる不一致
    'cid_mismatch_examples': [],  # CIDコード不一致の例
    'other_mismatch': 0,          # その他の不一致
    'other_mismatch_examples': [],# その他の不一致の例
    'both_empty': 0,              # 両方とも空
}

for idx, row in both_df.iterrows():
    japanese = row['japanese']
    trans_pdf = str(row['translation_pdfplumber']).strip()
    trans_py = str(row['translation_pymupdf']).strip()

    # 両方とも空
    if trans_pdf == '' and trans_py == '':
        results['both_empty'] += 1
        continue

    # 完全一致
    if trans_pdf == trans_py:
        results['perfect_match'] += 1
        continue

    # 不一致の場合
    # pdfplumberにCIDコードが含まれているか
    has_cid_pdf = bool(re.search(cid_pattern, trans_pdf))

    if has_cid_pdf:
        # CIDコードによる不一致
        results['cid_mismatch'] += 1
        if len(results['cid_mismatch_examples']) < 10:
            results['cid_mismatch_examples'].append({
                'japanese': japanese,
                'pdfplumber': trans_pdf,
                'pymupdf': trans_py,
                'cid_codes': re.findall(cid_pattern, trans_pdf)
            })
    else:
        # その他の不一致
        results['other_mismatch'] += 1
        if len(results['other_mismatch_examples']) < 10:
            results['other_mismatch_examples'].append({
                'japanese': japanese,
                'pdfplumber': trans_pdf,
                'pymupdf': trans_py
            })

# 結果表示
print(f"\n【比較結果サマリー】")
print(f"  完全一致: {results['perfect_match']}語")
print(f"  CIDコードによる不一致: {results['cid_mismatch']}語")
print(f"  その他の不一致: {results['other_mismatch']}語")
print(f"  両方とも空: {results['both_empty']}語")

total = len(both_df)
print(f"\n一致率: {results['perfect_match'] / total * 100:.1f}%")
print(f"CID起因の不一致率: {results['cid_mismatch'] / total * 100:.1f}%")
print(f"その他の不一致率: {results['other_mismatch'] / total * 100:.1f}%")

# CIDコードによる不一致の例
if results['cid_mismatch'] > 0:
    print(f"\n" + "="*80)
    print("CIDコードによる不一致の例（最初の10件）")
    print("="*80)
    for i, example in enumerate(results['cid_mismatch_examples'], 1):
        print(f"\n{i}. 日本語: {example['japanese']}")
        print(f"   pdfplumber: {example['pdfplumber'][:80]}")
        print(f"   PyMuPDF   : {example['pymupdf'][:80]}")
        print(f"   CIDコード : {example['cid_codes']}")

# その他の不一致の例
if results['other_mismatch'] > 0:
    print(f"\n" + "="*80)
    print("その他の不一致の例（最初の10件）")
    print("="*80)
    for i, example in enumerate(results['other_mismatch_examples'], 1):
        print(f"\n{i}. 日本語: {example['japanese']}")
        print(f"   pdfplumber: {example['pdfplumber'][:80]}")
        print(f"   PyMuPDF   : {example['pymupdf'][:80]}")

# pdfplumberのみに存在する単語
if len(merged[merged['_merge'] == 'left_only']) > 0:
    print(f"\n" + "="*80)
    print("pdfplumberのみに存在する単語（最初の10件）")
    print("="*80)
    left_only = merged[merged['_merge'] == 'left_only']['japanese'].head(10)
    for word in left_only:
        print(f"  {word}")

# PyMuPDFのみに存在する単語
if len(merged[merged['_merge'] == 'right_only']) > 0:
    print(f"\n" + "="*80)
    print("PyMuPDFのみに存在する単語（最初の10件）")
    print("="*80)
    right_only = merged[merged['_merge'] == 'right_only']['japanese'].head(10)
    for word in right_only:
        print(f"  {word}")

print("\n" + "="*80)
print("比較完了")
print("="*80)
