"""
ベトナム語CSVから余分な行（Page=12, 番号=空欄, 単語=空欄）を削除
"""
import pandas as pd
import os
from datetime import datetime

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
backup_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output_backup'

filename = 'ベトナム語_pdfplumber_抽出_最終版.csv'
csv_path = os.path.join(output_dir, filename)
backup_path = os.path.join(backup_dir, f"{filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")

print("=" * 80)
print("ベトナム語CSVから余分な行を削除")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# CSVを読み込み
df = pd.read_csv(csv_path, encoding='utf-8-sig')
print(f"元のデータ: {len(df)}行")

# バックアップ
os.makedirs(backup_dir, exist_ok=True)
df.to_csv(backup_path, index=False, encoding='utf-8-sig')
print(f"バックアップ: {backup_path}")
print()

# 削除する行を特定: Page=12, 番号=空欄, 単語=空欄
delete_rows = []

for idx, row in df.iterrows():
    # Page=12 かつ 番号と単語が空欄（NaN）
    page = row.iloc[1]
    number = row.iloc[2]
    word = row.iloc[3]

    if page == 12 and pd.isna(number) and pd.isna(word):
        delete_rows.append(idx)
        print(f"削除対象: 行{idx+1} - Page={page}")

if not delete_rows:
    print("[情報] 削除対象の行が見つかりませんでした")
else:
    print(f"\n削除対象行数: {len(delete_rows)}行")

    # 行を削除
    new_df = df.drop(delete_rows).reset_index(drop=True)

    print(f"新しいデータ: {len(new_df)}行 ({len(df) - len(new_df)}行削除)")

    # 保存
    new_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"[成功] 保存完了: {csv_path}")

print("\n" + "=" * 80)
print("処理完了")
print("=" * 80)
