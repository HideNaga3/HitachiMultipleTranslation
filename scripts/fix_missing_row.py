"""
カンボジア語とタイ語のCSVに欠損している「健康保険」の行を挿入
"""
import pandas as pd
import os
from datetime import datetime

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
backup_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output_backup'

# バックアップディレクトリ作成
os.makedirs(backup_dir, exist_ok=True)

# 対象言語
languages = {
    'カンボジア語': 'カンボジア語_pdfplumber_抽出_最終版.csv',
    'タイ語': 'タイ語_pdfplumber_抽出_最終版.csv',
}

print("=" * 80)
print("カンボジア語・タイ語CSVに「健康保険」行を挿入")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

for lang, filename in languages.items():
    print(f"\n{'=' * 80}")
    print(f"{lang} 処理中...")
    print("=" * 80)

    csv_path = os.path.join(output_dir, filename)
    backup_path = os.path.join(backup_dir, f"{filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")

    # CSVを読み込み
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"元のデータ: {len(df)}行")

    # 既に「4,12,健康保険」が存在するかチェック
    already_exists = False
    for idx, row in df.iterrows():
        if row.iloc[1] == 4 and row.iloc[2] == 12 and row.iloc[3] == '健康保険':
            already_exists = True
            print(f"[スキップ] 既に「健康保険」の行が存在します（行{idx+1}）")
            break

    if already_exists:
        continue

    # バックアップ
    df.to_csv(backup_path, index=False, encoding='utf-8-sig')
    print(f"バックアップ: {backup_path}")

    # 挿入する行のインデックスを探す
    # 「4,11,雇用保険」の次に「4,12,健康保険」を挿入
    insert_index = None

    for idx, row in df.iterrows():
        # Page=4, 番号=11 の行を探す
        if row.iloc[1] == 4 and row.iloc[2] == 11 and row.iloc[3] == '雇用保険':
            insert_index = idx + 1
            print(f"挿入位置: 行{insert_index + 1} (「{row.iloc[3]}」の次)")
            break

    if insert_index is None:
        print(f"[ERROR] 挿入位置が見つかりません")
        continue

    # 新しい行を作成（健康保険）
    # 列: 言語, Page, 番号, 単語, 翻訳
    new_row = {
        df.columns[0]: lang,      # 言語
        df.columns[1]: 4,          # Page
        df.columns[2]: 12,         # 番号
        df.columns[3]: '健康保険',  # 単語
        df.columns[4]: ''          # 翻訳（空欄）
    }

    print(f"挿入する行: {new_row}")

    # 新しい行を挿入
    # df.loc[insert_index:] を1つ下にずらして、insert_index に新しい行を挿入
    df1 = df.iloc[:insert_index]
    df2 = df.iloc[insert_index:]

    new_df = pd.concat([df1, pd.DataFrame([new_row]), df2], ignore_index=True)

    print(f"新しいデータ: {len(new_df)}行 (+{len(new_df) - len(df)})")

    # 保存
    new_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"[成功] 保存完了: {csv_path}")

print("\n" + "=" * 80)
print("処理完了")
print("=" * 80)
