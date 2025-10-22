"""Excelファイルの列構造を詳しく分析"""
import pandas as pd
import sys

# ファイル出力
sys.stdout = open('for_claude/excel_structure_detail.txt', 'w', encoding='utf-8')

# タイ語Excelを分析
excel_file = r'tmp\【全課統合版】タイ語_げんばのことば_建設関連職種.xlsx'

print("=" * 80)
print(f"Excelファイル構造の詳細分析: タイ語")
print("=" * 80)
print()

# ヘッダーなしで読み込み
df_raw = pd.read_excel(excel_file, sheet_name='Table 1', header=None)

print(f"総行数: {len(df_raw)}")
print(f"総列数: {len(df_raw.columns)}")
print()

# 最初の10行を確認
print("【最初の10行】")
for idx in range(min(10, len(df_raw))):
    print(f"\n行{idx}:")
    row = df_raw.iloc[idx]
    for col_idx, val in enumerate(row[:20]):  # 最初の20列
        if pd.notna(val) and str(val).strip() != '':
            # 列名をアルファベットに変換（A=0, B=1, C=2...）
            col_letter = chr(65 + col_idx) if col_idx < 26 else f"A{chr(65 + col_idx - 26)}"
            print(f"  {col_letter}列（{col_idx}）: {val}")

print()
print("=" * 80)

# ヘッダー行を特定
print("【ヘッダー行の特定】")
header_row_idx = None
for idx in range(min(10, len(df_raw))):
    row = df_raw.iloc[idx]
    if 'No.' in row.values:
        header_row_idx = idx
        print(f"ヘッダー行: 行{idx}")
        break

if header_row_idx is not None:
    print()
    print("【ヘッダー行の全列】")
    header_row = df_raw.iloc[header_row_idx]
    for col_idx, val in enumerate(header_row):
        if pd.notna(val) and str(val).strip() != '':
            col_letter = chr(65 + col_idx) if col_idx < 26 else f"A{chr(65 + col_idx - 26)}"
            print(f"  {col_letter}列（{col_idx}）: {val}")

    # データ行のサンプル
    print()
    print("【データ行のサンプル（最初の3行）】")
    for data_row_offset in range(1, 4):
        data_row_idx = header_row_idx + data_row_offset
        if data_row_idx < len(df_raw):
            print(f"\nデータ行{data_row_offset}（行{data_row_idx}）:")
            data_row = df_raw.iloc[data_row_idx]
            for col_idx, val in enumerate(data_row[:20]):
                if pd.notna(val) and str(val).strip() != '':
                    col_letter = chr(65 + col_idx) if col_idx < 26 else f"A{chr(65 + col_idx - 26)}"
                    header_name = header_row.iloc[col_idx] if pd.notna(header_row.iloc[col_idx]) else '(ヘッダーなし)'
                    print(f"  {col_letter}列（{col_idx}）[{header_name}]: {val}")

print()
print("=" * 80)
