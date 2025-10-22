"""タイ語Excelファイルから正しい形式でCSVを抽出"""
import pandas as pd
import sys

# 出力をファイルにリダイレクト
output_log = open('for_claude/thai_excel_extraction.txt', 'w', encoding='utf-8')

# Excelファイルのパス
excel_file = r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\temp_files\【全課統合版】タイ語_げんばのことば_建設関連職種.xlsx"

print("=" * 80, file=output_log)
print("タイ語Excelファイルからのデータ抽出", file=output_log)
print("=" * 80, file=output_log)
print(file=output_log)

# Excelファイルを読み込み（ヘッダーなし）
df_raw = pd.read_excel(excel_file, sheet_name='Table 1', header=None)

print(f"元の行数: {len(df_raw)}", file=output_log)
print(f"元の列数: {len(df_raw.columns)}", file=output_log)
print(file=output_log)

# 行1（インデックス1）がヘッダー行
# 行0はタイトル行なのでスキップ
# 行2以降がデータ行

# ヘッダー行を確認
header_row = df_raw.iloc[1]
print("ヘッダー行:", file=output_log)
for i, val in enumerate(header_row):
    if pd.notna(val):
        print(f"  列{i}: {val}", file=output_log)
print(file=output_log)

# 重要な列のインデックスを特定
# No. = 列0
# ศัพท์（単語） = 列2
# อ่านว่า（読み方） = 列6
# ค าแปล（翻訳） = 列9
# หมายเหตุ（備考） = 列15
# ตัวอย่าง（例文） = 列23

# データ行を抽出（行2以降）
df_data = df_raw.iloc[2:].copy()

# 必要な列を抽出して、日本語列名に変換
df_extracted = pd.DataFrame()
df_extracted['番号'] = df_data.iloc[:, 0]  # No.
df_extracted['単語'] = df_data.iloc[:, 2]  # ศัพท์
df_extracted['読み方（ひらがな）'] = df_data.iloc[:, 6]  # อ่านว่า
df_extracted['翻訳'] = df_data.iloc[:, 9]  # ค าแปล
df_extracted['備考'] = df_data.iloc[:, 15]  # หมายเหตุ
df_extracted['例文'] = df_data.iloc[:, 23]  # ตัวอย่าง

# インデックスをリセット
df_extracted = df_extracted.reset_index(drop=True)

# NaNを空文字列に置換
df_extracted = df_extracted.fillna('')

# 番号が空の行、または番号が"No."の行（ヘッダー行）を除外
df_extracted = df_extracted[
    (df_extracted['番号'] != '') &
    (df_extracted['番号'] != 'No.') &
    (df_extracted['番号'].astype(str) != 'No.')
]

# 番号を数値型に変換できる行のみを残す（データ行の検証）
def is_valid_number(val):
    try:
        float(str(val))
        return True
    except:
        return False

df_extracted = df_extracted[df_extracted['番号'].apply(is_valid_number)]

# インデックスをリセット
df_extracted = df_extracted.reset_index(drop=True)

print(f"抽出後の行数: {len(df_extracted)}", file=output_log)
print(file=output_log)

# 翻訳列のデータ状況を確認
translation_filled = (df_extracted['翻訳'] != '').sum()
translation_empty = (df_extracted['翻訳'] == '').sum()
total = len(df_extracted)

print(f"翻訳データあり: {translation_filled}行 / {total}行 ({translation_filled/total*100:.1f}%)", file=output_log)
print(f"翻訳データなし: {translation_empty}行 / {total}行 ({translation_empty/total*100:.1f}%)", file=output_log)
print(file=output_log)

# サンプルデータを表示
print("抽出データのサンプル（最初の10行）:", file=output_log)
print(df_extracted.head(10).to_string(index=False), file=output_log)
print(file=output_log)

# CSVファイルに保存
output_file = 'output/【全課統合版】タイ語_げんばのことば_建設関連職種_from_excel.csv'
df_extracted.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"保存完了: {output_file}", file=output_log)
print("=" * 80, file=output_log)

output_log.close()

# コンソールにも結果を表示
print(f"抽出完了: {len(df_extracted)}行")
print(f"翻訳データあり: {translation_filled}行 ({translation_filled/total*100:.1f}%)")
print(f"保存先: {output_file}")
