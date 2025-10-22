"""最終CSVファイルの内容を検証"""
import pandas as pd
from pathlib import Path

CSV_FILE = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\output\全言語統合_pdfplumber_最終版.csv")

print(f"ファイル: {CSV_FILE.name}")
print("="*80)

df = pd.read_csv(CSV_FILE, encoding='utf-8-sig')

print(f"\n総行数: {len(df)}")
print(f"総列数: {len(df.columns)}")
print(f"列名: {df.columns.tolist()}")

print(f"\n言語別行数:")
lang_counts = df['言語'].value_counts().sort_index()
for lang, count in lang_counts.items():
    print(f"  {lang}: {count}行")

print(f"\n各言語の最初の3行:")
for lang in sorted(df['言語'].unique()):
    print(f"\n【{lang}】")
    subset = df[df['言語'] == lang].head(3)
    for idx in range(len(subset)):
        row = subset.iloc[idx]
        # エラーを避けるため、簡潔に表示
        print(f"  Page={row['Page']}, 番号={row['番号']}")

# 改行が含まれているかチェック
print(f"\n改行チェック:")
for col in ['単語', '翻訳']:
    has_newline = df[col].astype(str).str.contains('\n').sum()
    print(f"  {col}列: 改行を含む行数 = {has_newline}")

# 前後に空白がある行をチェック
print(f"\n前後空白チェック:")
for col in ['単語', '翻訳']:
    has_space = ((df[col].astype(str) != df[col].astype(str).str.strip())).sum()
    print(f"  {col}列: 前後に空白がある行数 = {has_space}")

print(f"\n翻訳充足率:")
for lang in sorted(df['言語'].unique()):
    subset = df[df['言語'] == lang]
    translation_fill = (subset['翻訳'].notna() & (subset['翻訳'].astype(str).str.strip() != '')).sum()
    translation_rate = translation_fill / len(subset) * 100 if len(subset) > 0 else 0
    print(f"  {lang}: {translation_fill}/{len(subset)} ({translation_rate:.1f}%)")

print(f"\n{'='*80}")
print("検証完了")
