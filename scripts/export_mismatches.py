"""
pdfplumberとPyMuPDFの不一致データをCSVで保存
形式: 日本語, pdfplumber値, PyMuPDF値
"""

import pandas as pd
from pathlib import Path

print("="*80)
print("不一致データのエクスポート")
print("="*80)

# ファイル読み込み
pymupdf_csv = Path('output') / 'カンボジア語_pymupdf_整形版.csv'
pdfplumber_csv = Path('output') / '全言語統合_テンプレート_インポート用.csv'
output_csv = Path('output') / '不一致データ_pdfplumber_vs_pymupdf.csv'

pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')
pdfplumber_df = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

print(f"\nPyMuPDF整形版: {len(pymupdf_df)}行")
print(f"pdfplumber最終版: {len(pdfplumber_df)}行")

# データ整形
pymupdf_km = pymupdf_df[['日本語', '翻訳', 'Page', 'No']].copy()
pymupdf_km.columns = ['日本語', 'PyMuPDF値', 'Page', 'No']

pdfplumber_km = pdfplumber_df[['ja', 'km']].copy()
pdfplumber_km.columns = ['日本語', 'pdfplumber値']

# マージ
merged = pdfplumber_km.merge(pymupdf_km, on='日本語', how='inner')

print(f"\n両方に存在する単語: {len(merged)}語")

# 不一致のみを抽出
mismatches = []

for idx, row in merged.iterrows():
    ja = row['日本語']
    pdf_val = str(row['pdfplumber値']).strip()
    py_val = str(row['PyMuPDF値']).strip()
    page = row['Page']
    no = row['No']

    # nanチェック
    if pdf_val == 'nan':
        pdf_val = ''
    if py_val == 'nan':
        py_val = ''

    # 不一致の場合のみ追加
    if pdf_val != py_val:
        mismatches.append({
            '日本語': ja,
            'pdfplumber値': pdf_val,
            'PyMuPDF値': py_val,
            'Page': page,
            'No': no
        })

print(f"不一致件数: {len(mismatches)}件")

# DataFrameに変換
if mismatches:
    mismatch_df = pd.DataFrame(mismatches)

    # CSV保存
    mismatch_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

    print(f"\n保存完了: {output_csv}")
    print(f"ファイルサイズ: {output_csv.stat().st_size / 1024:.1f} KB")

    # サンプル表示
    print(f"\n【不一致データのサンプル（最初の10件）】")
    print("="*80)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 60)

    for idx, row in mismatch_df.head(10).iterrows():
        print(f"\n{idx+1}. {row['日本語']} (Page:{row['Page']}, No:{row['No']})")
        print(f"   pdfplumber: {row['pdfplumber値'][:60]}")
        print(f"   PyMuPDF   : {row['PyMuPDF値'][:60]}")

    # CIDコードを含む不一致の件数
    import re
    cid_pattern = r'\(cid:\d+\)'
    cid_count = mismatch_df['pdfplumber値'].astype(str).str.contains(cid_pattern, regex=True).sum()

    print(f"\n" + "="*80)
    print("統計")
    print("="*80)
    print(f"総不一致件数: {len(mismatch_df)}")
    print(f"CIDコードを含む不一致: {cid_count}件 ({cid_count/len(mismatch_df)*100:.1f}%)")
    print(f"その他の不一致: {len(mismatch_df) - cid_count}件 ({(len(mismatch_df) - cid_count)/len(mismatch_df)*100:.1f}%)")

else:
    print("\n不一致データはありません（全て一致）")

print("\n" + "="*80)
print("エクスポート完了")
print("="*80)
