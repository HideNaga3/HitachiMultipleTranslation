"""
全言語CSVから完全な空欄行を削除
条件: NO（番号）AND 単語 AND 翻訳 がすべて空欄（trim/clean後）
"""
import pandas as pd
import os
from datetime import datetime

def is_empty_value(value):
    """値が空かどうか判定（trim/clean後）"""
    if pd.isna(value):
        return True
    if isinstance(value, str):
        cleaned = str(value).strip()
        return cleaned == '' or cleaned.lower() == 'nan'
    return False

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
backup_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output_backup'

# 対象ファイル（8言語）
filenames = [
    '英語_pdfplumber_抽出_最終版.csv',
    'タガログ語_pdfplumber_抽出_最終版.csv',
    'カンボジア語_pdfplumber_抽出_最終版.csv',
    '中国語_pdfplumber_抽出_最終版.csv',
    'インドネシア語_pdfplumber_抽出_最終版.csv',
    'ミャンマー語_pdfplumber_抽出_最終版.csv',
    'タイ語_pdfplumber_抽出_最終版.csv',
    'ベトナム語_pdfplumber_抽出_最終版.csv',
]

print("=" * 80)
print("全言語CSVから完全空欄行を削除")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

total_deleted = 0

for filename in filenames:
    print(f"\n{'=' * 80}")
    print(f"{filename}")
    print("=" * 80)

    csv_path = os.path.join(output_dir, filename)
    backup_path = os.path.join(backup_dir, f"{filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")

    # CSVを読み込み
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"元のデータ: {len(df)}行")

    # 削除する行を特定
    delete_rows = []

    for idx, row in df.iterrows():
        number = row.iloc[2]  # 番号
        word = row.iloc[3]    # 単語
        translation = row.iloc[4]  # 翻訳

        # 3つすべてが空欄の場合
        if is_empty_value(number) and is_empty_value(word) and is_empty_value(translation):
            delete_rows.append(idx)

    if not delete_rows:
        print("[情報] 削除対象の行なし")

    else:
        # バックアップ
        os.makedirs(backup_dir, exist_ok=True)
        df.to_csv(backup_path, index=False, encoding='utf-8-sig')
        print(f"バックアップ: {backup_path}")

        print(f"削除対象行数: {len(delete_rows)}行")

        # 行を削除
        new_df = df.drop(delete_rows).reset_index(drop=True)

        print(f"新しいデータ: {len(new_df)}行 ({len(df) - len(new_df)}行削除)")

        # 保存
        new_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"[成功] 保存完了")

        total_deleted += len(delete_rows)

print("\n" + "=" * 80)
print("処理完了")
print("=" * 80)
print(f"総削除行数: {total_deleted}行")
print()
