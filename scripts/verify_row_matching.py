"""
Page, No, 日本語の3つで正しくマッチング
同じ位置のデータを比較する
"""

import pandas as pd
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("行の正しいマッチング検証")
print("="*80)

# ファイル読み込み
pymupdf_csv = Path('output') / 'カンボジア語_pymupdf_整形版.csv'
pdfplumber_csv = Path('output') / '全言語統合_テンプレート_インポート用.csv'

pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')
pdfplumber_df = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

print(f"\nPyMuPDF: {len(pymupdf_df)}行")
print(f"pdfplumber: {len(pdfplumber_df)}行")

# pdfplumberは行番号がない
# PyMuPDFのデータを基準に、日本語でマッチング
print("\n【問題確認】pdfplumberデータに行番号がない")
print(f"pdfplumber列: {list(pdfplumber_df.columns)}")
print(f"PyMuPDF列: {list(pymupdf_df.columns)}")

# 日本語をキーにしてマージ（現在の方法）
print("\n" + "="*80)
print("現在の方法：日本語のみでマッチング")
print("="*80)

pymupdf_clean = pymupdf_df[['日本語', '翻訳', 'Page', 'No']].copy()
pymupdf_clean.columns = ['日本語', 'PyMuPDF値', 'Page', 'No']

pdfplumber_clean = pdfplumber_df[['ja', 'km']].copy()
pdfplumber_clean.columns = ['日本語', 'pdfplumber値']

# 日本語でマージ
merged_ja = pdfplumber_clean.merge(pymupdf_clean, on='日本語', how='inner')

print(f"マッチング結果: {len(merged_ja)}件")

# 同じ日本語が複数回出現する場合をチェック
ja_counts_pdf = pdfplumber_clean['日本語'].value_counts()
ja_counts_py = pymupdf_clean['日本語'].value_counts()

duplicates_pdf = ja_counts_pdf[ja_counts_pdf > 1]
duplicates_py = ja_counts_py[ja_counts_py > 1]

print(f"\npdfplumberで重複する日本語: {len(duplicates_pdf)}語")
print(f"PyMuPDFで重複する日本語: {len(duplicates_py)}語")

if len(duplicates_pdf) > 0 or len(duplicates_py) > 0:
    print("\n【警告】同じ日本語が複数回出現しています！")
    print("→ 日本語だけでマッチングすると、異なる箇所のデータを比較している可能性")

    # 重複例を表示
    if len(duplicates_pdf) > 0:
        print(f"\npdfplumberの重複例（最初の5件）:")
        for word, count in duplicates_pdf.head(5).items():
            print(f"  {word}: {count}回")

    if len(duplicates_py) > 0:
        print(f"\nPyMuPDFの重複例（最初の5件）:")
        for word, count in duplicates_py.head(5).items():
            print(f"  {word}: {count}回")

# 正しい方法：行番号順にマッチング
print("\n" + "="*80)
print("正しい方法：行番号順にマッチング")
print("="*80)

# PyMuPDFを行番号順にソート
pymupdf_sorted = pymupdf_df.sort_values(['Page', 'No']).reset_index(drop=True)

# pdfplumberも行番号順（元々の順序を保持）
pdfplumber_sorted = pdfplumber_df.reset_index(drop=True)

print(f"PyMuPDF（ソート後）: {len(pymupdf_sorted)}行")
print(f"pdfplumber: {len(pdfplumber_sorted)}行")

# 行番号で直接マッチング
min_rows = min(len(pymupdf_sorted), len(pdfplumber_sorted))
print(f"\n比較可能な行数: {min_rows}行")

# 行ごとに比較
matches = []
for i in range(min_rows):
    py_row = pymupdf_sorted.iloc[i]
    pdf_row = pdfplumber_sorted.iloc[i]

    py_ja = str(py_row['日本語']).strip()
    pdf_ja = str(pdf_row['ja']).strip()
    py_trans = str(py_row['翻訳']).strip()
    pdf_trans = str(pdf_row['km']).strip()

    matches.append({
        'index': i,
        'PyMuPDF日本語': py_ja,
        'pdfplumber日本語': pdf_ja,
        'PyMuPDF値': py_trans,
        'pdfplumber値': pdf_trans,
        'Page': py_row['Page'],
        'No': py_row['No'],
        '日本語一致': py_ja == pdf_ja,
        '翻訳一致': py_trans == pdf_trans
    })

matches_df = pd.DataFrame(matches)

# 統計
ja_match_count = matches_df['日本語一致'].sum()
trans_match_count = matches_df['翻訳一致'].sum()

print(f"\n【統計】")
print(f"日本語一致: {ja_match_count}/{min_rows} ({ja_match_count/min_rows*100:.1f}%)")
print(f"翻訳一致: {trans_match_count}/{min_rows} ({trans_match_count/min_rows*100:.1f}%)")

# 日本語は一致するが翻訳が不一致
ja_match_trans_diff = matches_df[(matches_df['日本語一致'] == True) & (matches_df['翻訳一致'] == False)]
print(f"\n日本語一致 & 翻訳不一致: {len(ja_match_trans_diff)}件")

# 日本語が不一致
ja_diff = matches_df[matches_df['日本語一致'] == False]
print(f"日本語不一致: {len(ja_diff)}件")

if len(ja_diff) > 0:
    print("\n【警告】日本語が一致しない行があります！")
    print("→ pdfplumberとPyMuPDFで異なる行数または順序で抽出されています")
    print(f"\n日本語不一致の例（最初の5件）:")
    for idx, row in ja_diff.head(5).iterrows():
        print(f"  行{row['index']}: PyMuPDF='{row['PyMuPDF日本語']}' vs pdfplumber='{row['pdfplumber日本語']}'")

# 結果を保存
output_csv = Path('output') / '行番号マッチング結果.csv'
ja_match_trans_diff.to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f"\n結果を保存: {output_csv}")
print(f"日本語一致&翻訳不一致のデータのみ保存しました")

print("\n" + "="*80)
print("検証完了")
print("="*80)
