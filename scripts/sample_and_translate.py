"""
不一致データの改行削除とサンプル逆翻訳
pdfplumberとPyMuPDFの翻訳精度を比較
"""

import pandas as pd
from pathlib import Path
import sys
import os

# .envからAPIキーを読み込むため、親ディレクトリを追加
sys.path.append(str(Path(__file__).parent.parent))
from dotenv import load_dotenv

# Google Translation API用
sys.path.append(str(Path(__file__).parent.parent / 'scripts_google_translation'))
from scripts.translator import translate_words

# UTF-8出力を強制
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# .envファイルを読み込む
load_dotenv()

print("="*80)
print("不一致データの改行削除とサンプル逆翻訳")
print("="*80)

# CSVファイル読み込み
input_csv = Path('output') / '不一致データ_pdfplumber_vs_pymupdf.csv'
output_csv = Path('output') / '不一致データ_改行削除版.csv'

df = pd.read_csv(input_csv, encoding='utf-8-sig')

print(f"\n元データ: {len(df)}件")

# 改行を削除
df['pdfplumber値_改行削除'] = df['pdfplumber値'].astype(str).str.replace('\n', ' ', regex=False).str.strip()
df['PyMuPDF値_改行削除'] = df['PyMuPDF値'].astype(str).str.replace('\n', ' ', regex=False).str.strip()

# 改行削除後のCSVを保存
df.to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f"\n改行削除版を保存: {output_csv}")

# サンプリング（10件）
sample_df = df.sample(n=min(10, len(df)), random_state=42)

print(f"\n【サンプル10件を選択】")
print("="*80)

# Google Translation APIで逆翻訳
results = []

for idx, row in sample_df.iterrows():
    japanese = row['日本語']
    pdf_text = row['pdfplumber値_改行削除']
    py_text = row['PyMuPDF値_改行削除']
    page = row['Page']
    no = row['No']

    print(f"\n{len(results)+1}. {japanese} (Page:{page}, No:{no})")
    print(f"   pdfplumber: {pdf_text[:50]}...")
    print(f"   PyMuPDF   : {py_text[:50]}...")

    # カンボジア語から日本語に逆翻訳
    try:
        # translate_wordsは複数の単語を一度に翻訳するので、リストで渡す
        pdf_results = translate_words([pdf_text], source_lang='km', target_lang='ja')
        py_results = translate_words([py_text], source_lang='km', target_lang='ja')

        pdf_back = pdf_results[0] if pdf_results else ''
        py_back = py_results[0] if py_results else ''

        print(f"   pdfplumber→ja: {pdf_back}")
        print(f"   PyMuPDF→ja   : {py_back}")

        # 一致判定
        pdf_match = '○' if pdf_back == japanese else '×'
        py_match = '○' if py_back == japanese else '×'

        print(f"   一致: pdfplumber={pdf_match}, PyMuPDF={py_match}")

        results.append({
            '日本語': japanese,
            'Page': page,
            'No': no,
            'pdfplumber値': pdf_text[:60],
            'PyMuPDF値': py_text[:60],
            'pdfplumber逆翻訳': pdf_back,
            'PyMuPDF逆翻訳': py_back,
            'pdfplumber一致': pdf_match,
            'PyMuPDF一致': py_match
        })

    except Exception as e:
        print(f"   エラー: {e}")
        results.append({
            '日本語': japanese,
            'Page': page,
            'No': no,
            'pdfplumber値': pdf_text[:60],
            'PyMuPDF値': py_text[:60],
            'pdfplumber逆翻訳': f'エラー: {e}',
            'PyMuPDF逆翻訳': f'エラー: {e}',
            'pdfplumber一致': '-',
            'PyMuPDF一致': '-'
        })

# 結果をDataFrameに変換
results_df = pd.DataFrame(results)

# CSV保存
results_csv = Path('output') / 'サンプル逆翻訳結果.csv'
results_df.to_csv(results_csv, index=False, encoding='utf-8-sig')

print(f"\n" + "="*80)
print("結果サマリー")
print("="*80)

# 一致率計算
pdf_match_count = (results_df['pdfplumber一致'] == '○').sum()
py_match_count = (results_df['PyMuPDF一致'] == '○').sum()
total = len(results_df)

print(f"サンプル数: {total}件")
print(f"pdfplumber一致率: {pdf_match_count}/{total} ({pdf_match_count/total*100:.1f}%)")
print(f"PyMuPDF一致率: {py_match_count}/{total} ({py_match_count/total*100:.1f}%)")

if py_match_count > pdf_match_count:
    print(f"\n✓ PyMuPDFの方が精度が高い（+{py_match_count - pdf_match_count}件）")
elif pdf_match_count > py_match_count:
    print(f"\n✓ pdfplumberの方が精度が高い（+{pdf_match_count - py_match_count}件）")
else:
    print(f"\n= 両者の精度は同じ")

print(f"\n結果を保存: {results_csv}")
print("="*80)
