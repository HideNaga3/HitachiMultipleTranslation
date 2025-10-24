"""
ベトナム語のPage・番号データを抽出し、インポート用CSVに統合するスクリプト
"""

import pandas as pd
import sys

# 出力先をファイルに変更
output_file = 'for_claude/vietnamese_order_extraction.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

print("=" * 80)
print("ベトナム語のPage・番号データ抽出")
print("=" * 80)
print()

# 1. 全言語統合_pdfplumber_最終版.csvからベトナム語のみを抽出
pdfplumber_csv = 'output/intermediate/全言語統合_pdfplumber_最終版.csv'
df_pdfplumber = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

print(f"読み込み: {pdfplumber_csv}")
print(f"  総行数: {len(df_pdfplumber)}")
print(f"  列: {list(df_pdfplumber.columns)}")
print()

# ベトナム語のみを抽出
df_vi = df_pdfplumber[df_pdfplumber['言語'] == 'ベトナム語'].copy()
print(f"ベトナム語の行数: {len(df_vi)}")
print()

# 2. インポート用CSVを読み込み
import_csv = 'output/全言語統合_テンプレート_インポート用.csv'
df_import = pd.read_csv(import_csv, encoding='utf-8-sig')

print(f"読み込み: {import_csv}")
print(f"  総行数: {len(df_import)}")
print(f"  列: {list(df_import.columns)}")
print()

# 3. 日本語単語で照合
print("=" * 80)
print("日本語単語で照合")
print("=" * 80)
print()

# インポート用CSVの日本語列名を確認
ja_col = 'ja' if 'ja' in df_import.columns else '日本語'
print(f"インポート用CSVの日本語列: {ja_col}")
print()

# ベトナム語CSVの単語列とインポート用の日本語列を照合
matched_count = 0
unmatched_words = []

# ベトナム語CSVの単語をキーにしたマッピングを作成
vi_word_to_page_no = {}
for _, row in df_vi.iterrows():
    word = str(row['単語']).strip()
    vi_word_to_page_no[word] = {
        'Page': row['Page'],
        '番号': row['番号']
    }

# インポート用CSVの各行に対してマッチング
results = []
for idx, row in df_import.iterrows():
    ja_word = str(row[ja_col]).strip()

    if ja_word in vi_word_to_page_no:
        matched_count += 1
        results.append({
            'CSV行': idx + 2,  # ヘッダー行を考慮して+2
            '日本語': ja_word,
            'Page': vi_word_to_page_no[ja_word]['Page'],
            '番号': vi_word_to_page_no[ja_word]['番号'],
            'マッチ': '✓'
        })
    else:
        unmatched_words.append({
            'CSV行': idx + 2,
            '日本語': ja_word,
            'Page': '',
            '番号': '',
            'マッチ': '✗'
        })
        results.append({
            'CSV行': idx + 2,
            '日本語': ja_word,
            'Page': '',
            '番号': '',
            'マッチ': '✗'
        })

print(f"マッチした単語数: {matched_count} / {len(df_import)}")
print(f"マッチしない単語数: {len(unmatched_words)}")
print()

# 4. マッチしない単語を表示
if unmatched_words:
    print("=" * 80)
    print("マッチしない単語（最初の20件）")
    print("=" * 80)
    print()
    for i, item in enumerate(unmatched_words[:20], 1):
        print(f"{i:2d}. [CSV行{item['CSV行']}] {item['日本語']}")
    if len(unmatched_words) > 20:
        print(f"... 他 {len(unmatched_words) - 20} 件")
    print()

# 5. マッチング結果を保存
print("=" * 80)
print("マッチング結果を保存")
print("=" * 80)
print()

df_results = pd.DataFrame(results)
output_csv = 'output/intermediate/日本語_ベトナム語Page番号マッピング.csv'
df_results.to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f"保存先: {output_csv}")
print()

# 6. 統計情報
print("=" * 80)
print("統計情報")
print("=" * 80)
print()
print(f"インポート用CSV行数: {len(df_import)}")
print(f"ベトナム語PDF抽出行数: {len(df_vi)}")
print(f"マッチング成功率: {matched_count / len(df_import) * 100:.1f}%")
print()

# Page・番号の範囲
if matched_count > 0:
    matched_df = df_results[df_results['マッチ'] == '✓']
    print(f"Page範囲: {matched_df['Page'].min():.0f} ～ {matched_df['Page'].max():.0f}")
    print(f"番号範囲: {matched_df['番号'].min():.1f} ～ {matched_df['番号'].max():.1f}")
    print()

print("=" * 80)

sys.stdout.close()
print(f"結果を {output_file} に保存しました", file=sys.__stdout__)
