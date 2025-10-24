"""
CIDコード含有データを抽出し、マッピングテーブル作成の準備
"""

import pandas as pd
from pathlib import Path
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("CIDコード抽出とマッピングテーブル作成")
print("="*80)

# CSVファイル読み込み
csv_path = Path('output') / '全言語統合_テンプレート_インポート用.csv'
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print(f"\n総行数: {len(df)}")

# CIDコードのパターン
cid_pattern = r'\(cid:\d+\)'

# CIDコードを含む行を抽出
cid_rows = df[df['km'].astype(str).str.contains(cid_pattern, regex=True, na=False)].copy()

print(f"CIDコードを含む行: {len(cid_rows)}件")

# CIDコードを全て抽出
all_cids = []
for idx, row in cid_rows.iterrows():
    text = str(row['km'])
    cids = re.findall(cid_pattern, text)
    for cid in cids:
        all_cids.append({
            '日本語': row['ja'],
            'カンボジア語（CID含む）': text,
            'CIDコード': cid,
            'CID番号': int(cid.replace('(cid:', '').replace(')', ''))
        })

cid_df = pd.DataFrame(all_cids)

# ユニークなCIDコード
unique_cids = cid_df['CIDコード'].unique()
print(f"\nユニークなCIDコード: {len(unique_cids)}種類")
print(f"CID出現総数: {len(cid_df)}回")

# CIDコードごとの出現回数
cid_counts = cid_df['CIDコード'].value_counts()

print(f"\n" + "="*80)
print("CIDコード出現頻度")
print("="*80)
for cid, count in cid_counts.items():
    cid_num = int(cid.replace('(cid:', '').replace(')', ''))
    print(f"{cid} (番号:{cid_num}): {count}回")

# サンプル表示
print(f"\n" + "="*80)
print("CIDコード含有例（全22件）")
print("="*80)

for idx, row in cid_rows.iterrows():
    print(f"\n{idx+1}. {row['ja']}")
    text = row['km']
    # CIDコードをハイライト
    highlighted = re.sub(r'(\(cid:\d+\))', r'【\1】', text)
    print(f"   {highlighted}")

# マッピングテーブルのテンプレート作成
print(f"\n" + "="*80)
print("CIDマッピングテーブル（手動入力用）")
print("="*80)

mapping_template = []
for cid in sorted(unique_cids, key=lambda x: int(x.replace('(cid:', '').replace(')', ''))):
    cid_num = int(cid.replace('(cid:', '').replace(')', ''))

    # このCIDを含む単語の例
    examples = cid_df[cid_df['CIDコード'] == cid]['日本語'].head(3).tolist()

    mapping_template.append({
        'CIDコード': cid,
        'CID番号': cid_num,
        '出現回数': cid_counts[cid],
        '正しい文字': '',  # 手動入力
        '例（日本語）': ', '.join(examples),
        '備考': ''
    })

mapping_df = pd.DataFrame(mapping_template)

# CSVに保存
output_cid_rows = Path('output') / 'CIDコード含有データ_全22件.csv'
output_mapping = Path('output') / 'CIDマッピングテーブル_入力用.csv'

cid_rows.to_csv(output_cid_rows, index=False, encoding='utf-8-sig')
mapping_df.to_csv(output_mapping, index=False, encoding='utf-8-sig')

print(f"\n保存完了:")
print(f"1. CID含有データ: {output_cid_rows}")
print(f"2. マッピングテーブル: {output_mapping}")

print(f"\n【次のステップ】")
print(f"1. {output_mapping} を開く")
print(f"2. 元のPDF（カンボジア語_げんばのことば.pdf）を開く")
print(f"3. 各CIDコードについて：")
print(f"   - 該当ページを確認")
print(f"   - 正しいクメール文字をコピー")
print(f"   - '正しい文字'列に貼り付け")
print(f"4. 保存後、自動置換スクリプトを実行")

print("\n" + "="*80)

# PyMuPDFで同じ箇所を確認してみる
print("\n【参考】PyMuPDFでの抽出結果")
print("="*80)

pymupdf_csv = Path('output') / 'カンボジア語_pymupdf_整形版.csv'
if pymupdf_csv.exists():
    pymupdf_df = pd.read_csv(pymupdf_csv, encoding='utf-8-sig')

    print(f"\nPyMuPDF抽出データから、CIDがあった単語を検索:")
    for idx, row in cid_rows.head(5).iterrows():
        ja = row['ja']
        pdf_text = row['km']

        # PyMuPDFで同じ単語を検索
        pymupdf_row = pymupdf_df[pymupdf_df['日本語'] == ja]

        if len(pymupdf_row) > 0:
            py_text = pymupdf_row.iloc[0]['翻訳']
            print(f"\n{ja}:")
            print(f"  pdfplumber: {pdf_text}")
            print(f"  PyMuPDF   : {py_text}")
        else:
            print(f"\n{ja}: PyMuPDFにデータなし")

print("\n" + "="*80)
print("完了")
print("="*80)
