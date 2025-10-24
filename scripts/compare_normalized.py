"""
pdfplumberとPyMuPDFの抽出結果を正規化して比較
スペース、改行を除去して比較
"""

import pandas as pd
import re
from pathlib import Path
import unicodedata

def normalize_text(text):
    """テキストを正規化（スペース、改行除去）"""
    if pd.isna(text) or text == '':
        return ''
    text = str(text)
    # Unicode正規化
    text = unicodedata.normalize('NFKC', text)
    # スペース、改行、タブを除去
    text = re.sub(r'\s+', '', text)
    return text

print("="*80)
print("pdfplumber vs PyMuPDF 正規化比較")
print("="*80)

# CSVファイル読み込み
pdfplumber_csv = Path('output') / '全言語統合_テンプレート_インポート用.csv'
pymupdf_csv = Path('output') / 'test_カンボジア語_pymupdf抽出.csv'

# データ読み込み
pdfplumber_df = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')
pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')

print(f"\npdfplumberデータ: {len(pdfplumber_df)}行")
print(f"PyMuPDFデータ: {len(pymupdf_df)}行")

# PyMuPDFデータを整形
pymupdf_clean = pymupdf_df[['Column_1', 'Column_3']].copy()
pymupdf_clean.columns = ['japanese', 'translation']
pymupdf_clean = pymupdf_clean.dropna(subset=['japanese'])
pymupdf_clean['japanese'] = pymupdf_clean['japanese'].str.strip()

# pdfplumberデータ（日本語とカンボジア語）
pdfplumber_clean = pdfplumber_df[['ja', 'km']].copy()
pdfplumber_clean.columns = ['japanese', 'translation']
pdfplumber_clean['japanese'] = pdfplumber_clean['japanese'].str.strip()

print(f"\nクリーニング後:")
print(f"  pdfplumber: {len(pdfplumber_clean)}行")
print(f"  PyMuPDF: {len(pymupdf_clean)}行")

# 正規化した翻訳列を追加
pdfplumber_clean['translation_normalized'] = pdfplumber_clean['translation'].apply(normalize_text)
pymupdf_clean['translation_normalized'] = pymupdf_clean['translation'].apply(normalize_text)

# 日本語単語でマージ
merged = pdfplumber_clean.merge(
    pymupdf_clean,
    on='japanese',
    how='inner',
    suffixes=('_pdf', '_py')
)

print(f"\n両方に存在する単語: {len(merged)}語")

# CIDコードパターン
cid_pattern = r'\(cid:\d+\)'

# 比較結果
results = {
    'exact_match': 0,                # 完全一致（正規化前）
    'normalized_match': 0,           # 正規化後一致
    'cid_only_diff': 0,              # CIDコードのみが差異
    'cid_and_other_diff': 0,         # CIDコード+その他の差異
    'other_diff': 0,                 # その他の差異のみ
    'both_empty': 0,                 # 両方とも空
}

# 詳細例を保存
examples = {
    'cid_only': [],
    'cid_and_other': [],
    'other': []
}

for idx, row in merged.iterrows():
    japanese = row['japanese']
    trans_pdf = str(row['translation_pdf']).strip()
    trans_py = str(row['translation_py']).strip()
    trans_pdf_norm = row['translation_normalized_pdf']
    trans_py_norm = row['translation_normalized_py']

    # 両方とも空
    if trans_pdf == '' and trans_py == '':
        results['both_empty'] += 1
        continue

    # 完全一致（正規化前）
    if trans_pdf == trans_py:
        results['exact_match'] += 1
        continue

    # 正規化後一致
    if trans_pdf_norm == trans_py_norm:
        results['normalized_match'] += 1
        continue

    # 不一致の詳細分析
    has_cid_pdf = bool(re.search(cid_pattern, trans_pdf))
    has_cid_py = bool(re.search(cid_pattern, trans_py))

    # CIDコードを除去して比較
    trans_pdf_no_cid = re.sub(cid_pattern, '', trans_pdf)
    trans_py_no_cid = re.sub(cid_pattern, '', trans_py)
    trans_pdf_no_cid_norm = normalize_text(trans_pdf_no_cid)
    trans_py_no_cid_norm = normalize_text(trans_py_no_cid)

    if has_cid_pdf and not has_cid_py:
        # pdfplumberにCIDコードあり、PyMuPDFになし
        if trans_pdf_no_cid_norm == trans_py_norm:
            # CIDコードを除けば一致
            results['cid_only_diff'] += 1
            if len(examples['cid_only']) < 5:
                examples['cid_only'].append({
                    'japanese': japanese,
                    'pdf': trans_pdf,
                    'pymupdf': trans_py,
                    'cid_codes': re.findall(cid_pattern, trans_pdf)
                })
        else:
            # CIDコード+その他の差異
            results['cid_and_other_diff'] += 1
            if len(examples['cid_and_other']) < 5:
                examples['cid_and_other'].append({
                    'japanese': japanese,
                    'pdf': trans_pdf,
                    'pymupdf': trans_py
                })
    else:
        # その他の差異のみ
        results['other_diff'] += 1
        if len(examples['other']) < 5:
            examples['other'].append({
                'japanese': japanese,
                'pdf': trans_pdf,
                'pymupdf': trans_py
            })

# 結果をCSVに保存
total = len(merged)
summary_data = {
    '項目': [
        '両方に存在する単語数',
        '完全一致',
        '正規化後一致',
        'CIDコードのみが差異',
        'CIDコード+その他の差異',
        'その他の差異のみ',
        '両方とも空'
    ],
    '件数': [
        total,
        results['exact_match'],
        results['normalized_match'],
        results['cid_only_diff'],
        results['cid_and_other_diff'],
        results['other_diff'],
        results['both_empty']
    ],
    '割合(%)': [
        100.0,
        results['exact_match'] / total * 100,
        results['normalized_match'] / total * 100,
        results['cid_only_diff'] / total * 100,
        results['cid_and_other_diff'] / total * 100,
        results['other_diff'] / total * 100,
        results['both_empty'] / total * 100
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('for_claude/comparison_summary.csv', index=False, encoding='utf-8-sig')

print(f"\n" + "="*80)
print("比較結果サマリー")
print("="*80)
print(summary_df.to_string(index=False))

print(f"\n一致率（完全+正規化後）: {(results['exact_match'] + results['normalized_match']) / total * 100:.1f}%")
print(f"CID関連の差異: {(results['cid_only_diff'] + results['cid_and_other_diff']) / total * 100:.1f}%")

# 詳細例をCSVに保存
if examples['cid_only']:
    cid_df = pd.DataFrame(examples['cid_only'])
    cid_df.to_csv('for_claude/cid_only_examples.csv', index=False, encoding='utf-8-sig')
    print(f"\nCIDのみが差異の例を保存: for_claude/cid_only_examples.csv ({len(examples['cid_only'])}件)")

if examples['other']:
    other_df = pd.DataFrame(examples['other'])
    other_df.to_csv('for_claude/other_diff_examples.csv', index=False, encoding='utf-8-sig')
    print(f"その他の差異の例を保存: for_claude/other_diff_examples.csv ({len(examples['other'])}件)")

print("\n" + "="*80)
print("比較完了 - 結果をCSVに保存しました")
print("="*80)
