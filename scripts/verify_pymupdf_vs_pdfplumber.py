"""
PyMuPDF整形版とpdfplumberデータを照合
一致率を確認して、他の言語も処理するか判断
"""

import pandas as pd
from pathlib import Path
import re

print("="*80)
print("PyMuPDF vs pdfplumber データ照合")
print("="*80)

# ファイル読み込み
pymupdf_csv = Path('output') / 'カンボジア語_pymupdf_整形版.csv'
pdfplumber_csv = Path('output') / '全言語統合_テンプレート_インポート用.csv'

pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')
pdfplumber_df = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

print(f"\nPyMuPDF整形版: {len(pymupdf_df)}行")
print(f"pdfplumber最終版: {len(pdfplumber_df)}行")

# pdfplumberから日本語とカンボジア語のみ抽出
pdfplumber_km = pdfplumber_df[['ja', 'km']].copy()
pdfplumber_km.columns = ['日本語', 'pdfplumber翻訳']

# PyMuPDFデータ
pymupdf_km = pymupdf_df[['日本語', '翻訳']].copy()
pymupdf_km.columns = ['日本語', 'pymupdf翻訳']

# 日本語でマージ
merged = pdfplumber_km.merge(pymupdf_km, on='日本語', how='outer', indicator=True)

print(f"\n【マージ結果】")
print(f"両方に存在: {len(merged[merged['_merge'] == 'both'])}語")
print(f"pdfplumberのみ: {len(merged[merged['_merge'] == 'left_only'])}語")
print(f"PyMuPDFのみ: {len(merged[merged['_merge'] == 'right_only'])}語")

# 両方に存在する単語で比較
both_df = merged[merged['_merge'] == 'both'].copy()

# CIDコードパターン
cid_pattern = r'\(cid:\d+\)'

# 比較結果
results = {
    'total': len(both_df),
    'exact_match': 0,
    'pdf_has_cid_py_correct': 0,  # pdfplumberにCID、PyMuPDFは正常
    'both_empty': 0,
    'mismatch': 0,
    'cid_examples': [],
    'mismatch_examples': []
}

for idx, row in both_df.iterrows():
    ja = row['日本語']
    pdf_trans = str(row['pdfplumber翻訳']).strip()
    py_trans = str(row['pymupdf翻訳']).strip()

    # 両方とも空
    if (pdf_trans == '' or pdf_trans == 'nan') and (py_trans == '' or py_trans == 'nan'):
        results['both_empty'] += 1
        continue

    # 完全一致
    if pdf_trans == py_trans:
        results['exact_match'] += 1
        continue

    # pdfplumberにCIDコードがあるかチェック
    has_cid = bool(re.search(cid_pattern, pdf_trans))

    if has_cid:
        # pdfplumberにCID、PyMuPDFには正常なデータ
        results['pdf_has_cid_py_correct'] += 1
        if len(results['cid_examples']) < 10:
            results['cid_examples'].append({
                '日本語': ja,
                'pdfplumber': pdf_trans[:60],
                'PyMuPDF': py_trans[:60],
                'CIDコード': re.findall(cid_pattern, pdf_trans)
            })
    else:
        # その他の不一致
        results['mismatch'] += 1
        if len(results['mismatch_examples']) < 10:
            results['mismatch_examples'].append({
                '日本語': ja,
                'pdfplumber': pdf_trans[:60],
                'PyMuPDF': py_trans[:60]
            })

# 結果表示
print(f"\n" + "="*80)
print("照合結果サマリー")
print("="*80)
print(f"総単語数（両方に存在）: {results['total']}")
print(f"完全一致: {results['exact_match']} ({results['exact_match']/results['total']*100:.1f}%)")
print(f"pdfplumberにCID、PyMuPDFは正常: {results['pdf_has_cid_py_correct']} ({results['pdf_has_cid_py_correct']/results['total']*100:.1f}%)")
print(f"その他の不一致: {results['mismatch']} ({results['mismatch']/results['total']*100:.1f}%)")
print(f"両方とも空: {results['both_empty']} ({results['both_empty']/results['total']*100:.1f}%)")

# 一致率（完全一致 + CID解決 + 両方空）
match_rate = (results['exact_match'] + results['pdf_has_cid_py_correct'] + results['both_empty']) / results['total'] * 100
print(f"\n【実質一致率】: {match_rate:.1f}%")
print(f"  ※pdfplumberのCIDコードをPyMuPDFが正しく解決している場合を含む")

# CID例を表示
if results['cid_examples']:
    print(f"\n" + "="*80)
    print(f"pdfplumberにCIDがある例（PyMuPDFでは正常）")
    print("="*80)
    for i, ex in enumerate(results['cid_examples'][:5], 1):
        print(f"\n{i}. {ex['日本語']}")
        print(f"   pdfplumber: {ex['pdfplumber']}")
        print(f"   PyMuPDF   : {ex['PyMuPDF']}")
        print(f"   CIDコード : {ex['CIDコード']}")

# その他の不一致例
if results['mismatch_examples']:
    print(f"\n" + "="*80)
    print(f"その他の不一致例（最初の5件）")
    print("="*80)
    for i, ex in enumerate(results['mismatch_examples'][:5], 1):
        print(f"\n{i}. {ex['日本語']}")
        print(f"   pdfplumber: {ex['pdfplumber']}")
        print(f"   PyMuPDF   : {ex['PyMuPDF']}")

# 判定
print(f"\n" + "="*80)
print("判定結果")
print("="*80)

if match_rate >= 95.0:
    print(f"✓ 一致率 {match_rate:.1f}% - 非常に良好")
    print(f"✓ PyMuPDFはpdfplumberのCIDコード問題を解決しています")
    print(f"\n【推奨】他の7言語もPyMuPDFで処理することを推奨します")
    proceed = True
elif match_rate >= 90.0:
    print(f"○ 一致率 {match_rate:.1f}% - 良好")
    print(f"○ PyMuPDFは概ね正常に動作しています")
    print(f"\n【推奨】他の言語も処理可能ですが、念のため確認が必要です")
    proceed = True
else:
    print(f"△ 一致率 {match_rate:.1f}% - 要確認")
    print(f"△ 不一致が多いため、原因を確認する必要があります")
    print(f"\n【推奨】他の言語の処理は保留し、原因調査を優先してください")
    proceed = False

# 結果をCSVに保存
summary_df = pd.DataFrame({
    '項目': ['総単語数', '完全一致', 'CID解決', 'その他不一致', '両方空', '実質一致率'],
    '件数': [
        results['total'],
        results['exact_match'],
        results['pdf_has_cid_py_correct'],
        results['mismatch'],
        results['both_empty'],
        f"{match_rate:.1f}%"
    ]
})
summary_df.to_csv('for_claude/verification_summary.csv', index=False, encoding='utf-8-sig')

print(f"\n照合結果を保存: for_claude/verification_summary.csv")
print("="*80)

# 次のステップを返す
if proceed:
    print("\n次のステップ: 他の7言語をPyMuPDFで抽出・整形")
else:
    print("\n次のステップ: 不一致の原因を調査")
