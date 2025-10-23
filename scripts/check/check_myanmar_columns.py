"""ミャンマー語Excelの列名を確認するスクリプト"""
import pandas as pd
from pathlib import Path

EXCEL_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\建設関係Excel")

# ミャンマー語Excelの列名を確認
filename = "【全課統合版】ミャンマー語_げんばのことば_建設関連職種.xlsx"
filepath = EXCEL_DIR / filename

print(f"ファイル: {filename}")
print("="*80)

# header=Noneで全データを読み込み
df = pd.read_excel(filepath, sheet_name=0, header=None)

print(f"\n行数: {len(df)}")
print(f"列数: {len(df.columns)}")

# "No." を探す
print(f"\n'No.'を探しています...")
for i in range(min(20, len(df))):
    for j in range(len(df.columns)):
        val = df.iloc[i, j]
        if pd.notna(val) and str(val).strip() == 'No.':
            print(f"  'No.'が見つかりました: 行{i}, 列{j}")
            print(f"\n  この行の値（列0-30）:")
            for k in range(min(30, len(df.columns))):
                val_k = df.iloc[i, k]
                if pd.notna(val_k) and str(val_k).strip() != '':
                    print(f"    列{k}: {repr(val_k)}")

            # データ行の例を表示
            if i + 1 < len(df):
                print(f"\n  次の行（データ行）の値:")
                for k in range(min(30, len(df.columns))):
                    val_k = df.iloc[i+1, k]
                    if pd.notna(val_k) and str(val_k).strip() != '':
                        print(f"    列{k}: {repr(val_k)}")
            break
    else:
        continue
    break

# header=2で読み込んで列名を確認
print(f"\n\nheader=2で読み込んだときの列名:")
df2 = pd.read_excel(filepath, sheet_name=0, header=2)
print(f"列数: {len(df2.columns)}")
for i, col in enumerate(df2.columns):
    if pd.notna(col) and str(col).strip() != '' and not str(col).startswith('Unnamed'):
        print(f"  列{i}: {repr(col)}")
