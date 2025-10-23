"""Excelファイルの列名行を探すスクリプト"""
import pandas as pd
from pathlib import Path

EXCEL_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\建設関係Excel")

# 英語Excelの列名を確認
filename = "【全課統合版】英語_げんばのことば_建設関連職種.xlsx"
filepath = EXCEL_DIR / filename

print(f"ファイル: {filename}")
print("="*80)

# header=Noneで全データを読み込み
df = pd.read_excel(filepath, sheet_name=0, header=None)

print(f"\n行数: {len(df)}")
print(f"列数: {len(df.columns)}")

print(f"\n最初の10行:")
for i in range(min(10, len(df))):
    print(f"\n行{i}:")
    # 最初の15列のみ表示
    for j in range(min(15, len(df.columns))):
        val = df.iloc[i, j]
        if pd.notna(val) and str(val).strip() != '':
            print(f"  列{j}: {val}")

# "No." を探す
print(f"\n\n'No.'を探しています...")
for i in range(min(20, len(df))):
    for j in range(len(df.columns)):
        val = df.iloc[i, j]
        if pd.notna(val) and str(val).strip() == 'No.':
            print(f"  'No.'が見つかりました: 行{i}, 列{j}")
            print(f"\n  この行の値:")
            for k in range(min(30, len(df.columns))):
                val_k = df.iloc[i, k]
                if pd.notna(val_k) and str(val_k).strip() != '':
                    print(f"    列{k}: {val_k}")
            break
