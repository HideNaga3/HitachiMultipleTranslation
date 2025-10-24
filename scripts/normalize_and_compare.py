"""
Unicode正規化とスペース統一後の比較
並び順はpdfplumber（import CSV）に合わせる
"""

import pandas as pd
from pathlib import Path
import sys
import io
import unicodedata
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def normalize_text(text):
    """テキストの正規化：Unicode正規化 + スペース統一"""
    if pd.isna(text) or text == '' or text == 'nan':
        return ''

    text = str(text)

    # Unicode正規化（NFKC: 互換文字を標準形に）
    text = unicodedata.normalize('NFKC', text)

    # 改行をスペースに変換
    text = text.replace('\n', ' ')

    # 複数スペースを1つに統一
    text = re.sub(r'\s+', ' ', text)

    # 前後の空白を削除
    text = text.strip()

    return text

print("="*80)
print("Unicode正規化 + スペース統一後の比較")
print("="*80)

# ファイル読み込み
pymupdf_csv = Path('output') / 'カンボジア語_pymupdf_整形版.csv'
pdfplumber_csv = Path('output') / '全言語統合_テンプレート_インポート用.csv'

pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')
pdfplumber_df = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

print(f"\nPyMuPDF: {len(pymupdf_df)}行")
print(f"pdfplumber: {len(pdfplumber_df)}行")

# 正規化を適用
print("\n正規化を適用中...")

# PyMuPDFデータ
pymupdf_normalized = pymupdf_df.copy()
pymupdf_normalized['日本語_正規化'] = pymupdf_normalized['日本語'].apply(normalize_text)
pymupdf_normalized['翻訳_正規化'] = pymupdf_normalized['翻訳'].apply(normalize_text)

# pdfplumberデータ
pdfplumber_normalized = pdfplumber_df.copy()
pdfplumber_normalized['日本語_正規化'] = pdfplumber_normalized['ja'].apply(normalize_text)
pdfplumber_normalized['翻訳_正規化'] = pdfplumber_normalized['km'].apply(normalize_text)

print("正規化完了")

# pdfplumberの並び順（インデックス）を保持
pdfplumber_normalized['元の順序'] = pdfplumber_normalized.index

# 日本語_正規化でマージ（重複を処理）
# PyMuPDFに重複がある場合は最初の1つを使用
pymupdf_unique = pymupdf_normalized.drop_duplicates(subset=['日本語_正規化'], keep='first')

print(f"\n重複除外後:")
print(f"  PyMuPDF: {len(pymupdf_unique)}語（元{len(pymupdf_normalized)}行）")

# マージ
merged = pdfplumber_normalized.merge(
    pymupdf_unique[['日本語_正規化', '翻訳_正規化', 'Page', 'No']],
    on='日本語_正規化',
    how='left',
    suffixes=('_pdf', '_py')
)

# pdfplumberの並び順でソート
merged = merged.sort_values('元の順序').reset_index(drop=True)

print(f"\nマージ結果: {len(merged)}行")

# PyMuPDFに対応データがない行をカウント
no_pymupdf = merged['翻訳_正規化_py'].isna().sum()
print(f"PyMuPDFに対応データなし: {no_pymupdf}行")

# 比較（PyMuPDFデータがある行のみ）
merged_valid = merged[merged['翻訳_正規化_py'].notna()].copy()

print(f"\n比較対象: {len(merged_valid)}行")

# 一致判定
merged_valid['日本語一致'] = merged_valid['日本語_正規化'] == merged_valid['日本語_正規化']
merged_valid['翻訳一致'] = merged_valid['翻訳_正規化_pdf'] == merged_valid['翻訳_正規化_py']

# 統計
ja_match = merged_valid['日本語一致'].sum()
trans_match = merged_valid['翻訳一致'].sum()
trans_diff = len(merged_valid) - trans_match

print(f"\n" + "="*80)
print("比較結果（正規化後）")
print("="*80)
print(f"日本語一致: {ja_match}/{len(merged_valid)} ({ja_match/len(merged_valid)*100:.1f}%)")
print(f"翻訳一致: {trans_match}/{len(merged_valid)} ({trans_match/len(merged_valid)*100:.1f}%)")
print(f"翻訳不一致: {trans_diff}/{len(merged_valid)} ({trans_diff/len(merged_valid)*100:.1f}%)")

# 不一致のみ抽出
mismatches = merged_valid[merged_valid['翻訳一致'] == False].copy()

if len(mismatches) > 0:
    print(f"\n翻訳不一致のサンプル（最初の10件）:")
    for idx, row in mismatches.head(10).iterrows():
        print(f"\n{idx+1}. {row['ja']} (PyMuPDF: Page {row['Page']}, No {row['No']})")
        print(f"   pdfplumber: {row['翻訳_正規化_pdf'][:60]}")
        print(f"   PyMuPDF   : {row['翻訳_正規化_py'][:60]}")

# 最終CSVを作成（pdfplumberの並び順）
final_df = merged[['ja', '翻訳_正規化_pdf', '翻訳_正規化_py', 'Page', 'No']].copy()
final_df.columns = ['日本語', 'pdfplumber値（正規化後）', 'PyMuPDF値（正規化後）', 'Page', 'No']

# PyMuPDFにデータがない行は空欄
final_df['PyMuPDF値（正規化後）'] = final_df['PyMuPDF値（正規化後）'].fillna('')

# 一致判定列を追加
final_df['一致'] = (final_df['pdfplumber値（正規化後）'] == final_df['PyMuPDF値（正規化後）']) & (final_df['PyMuPDF値（正規化後）'] != '')

# 保存
output_csv = Path('output') / '正規化比較結果_import順.csv'
final_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

print(f"\n" + "="*80)
print("保存完了")
print("="*80)
print(f"保存先: {output_csv}")
print(f"行数: {len(final_df)}")
print(f"並び順: pdfplumber（インポートCSV）の順序")

# 統計サマリーをCSVに保存
summary_data = {
    '項目': [
        'pdfplumber総行数',
        'PyMuPDF総行数（重複除外前）',
        'PyMuPDF重複除外後',
        '比較対象行数',
        '日本語一致',
        '翻訳一致',
        '翻訳不一致',
        '一致率'
    ],
    '件数': [
        len(pdfplumber_df),
        len(pymupdf_df),
        len(pymupdf_unique),
        len(merged_valid),
        ja_match,
        trans_match,
        trans_diff,
        f"{trans_match/len(merged_valid)*100:.1f}%"
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_csv = Path('output') / '正規化比較_統計.csv'
summary_df.to_csv(summary_csv, index=False, encoding='utf-8-sig')

print(f"統計データ: {summary_csv}")
print("="*80)
