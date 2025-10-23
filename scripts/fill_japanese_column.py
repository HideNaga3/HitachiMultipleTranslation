"""
統合CSVの日本語列を上の値でfill
対象: NO空欄 & 日本語空欄 & 翻訳あり の行
"""
import pandas as pd
import os
from datetime import datetime

def is_empty_value(value):
    """値が空かどうか判定"""
    if pd.isna(value):
        return True
    if isinstance(value, str):
        cleaned = str(value).strip()
        return cleaned == '' or cleaned.lower() == 'nan'
    return False

# ファイルパス
output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
backup_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output_backup'
csv_path = os.path.join(output_dir, '全言語統合_比較用.csv')
backup_path = os.path.join(backup_dir, f"全言語統合_比較用.csv.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")

print("=" * 80)
print("統合CSV 日本語列のfill処理")
print("=" * 80)
print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# CSVを読み込み
df = pd.read_csv(csv_path, encoding='utf-8-sig')
print(f"元のデータ: {len(df)}行")
print()

# バックアップ
os.makedirs(backup_dir, exist_ok=True)
df.to_csv(backup_path, index=False, encoding='utf-8-sig')
print(f"バックアップ: {backup_path}")
print()

# 対象行を特定: NO空 & 日本語空 & 翻訳あり
target_rows = []

for idx, row in df.iterrows():
    no = row['番号']
    jp = row['日本語']
    translated = row['翻訳']

    no_empty = is_empty_value(no)
    jp_empty = is_empty_value(jp)
    tr_empty = is_empty_value(translated)

    # パターン2: NO空 & 日本語空 & 翻訳あり
    if no_empty and jp_empty and not tr_empty:
        target_rows.append(idx)

print(f"対象行数: {len(target_rows)}行")
print()

if len(target_rows) > 0:
    print("対象行のサンプル（修正前）:")
    for i, idx in enumerate(target_rows[:5], 1):
        row = df.iloc[idx]
        print(f"{i}. 行ID={row['行ID']}, 言語={row['言語']}, Page={row['ページ']}")
        print()

    # fill処理を実行
    print("=" * 80)
    print("fill処理実行中...")
    print("=" * 80)
    print()

    filled_count = 0

    for idx in target_rows:
        # 直前の行の日本語列の値を取得
        if idx > 0:
            prev_jp = df.at[idx - 1, '日本語']

            # 前の行も空欄でない場合のみfill
            if not is_empty_value(prev_jp):
                df.at[idx, '日本語'] = prev_jp
                filled_count += 1
            else:
                # 前の行も空欄の場合は、さらに前を探す
                for i in range(idx - 2, -1, -1):
                    candidate_jp = df.at[i, '日本語']
                    if not is_empty_value(candidate_jp):
                        df.at[idx, '日本語'] = candidate_jp
                        filled_count += 1
                        break

    print(f"fill完了: {filled_count}行を更新")
    print()

    # 結果のサンプル表示
    print("対象行のサンプル（修正後）:")
    for i, idx in enumerate(target_rows[:5], 1):
        row = df.iloc[idx]
        print(f"{i}. 行ID={row['行ID']}, 言語={row['言語']}, Page={row['ページ']}, 日本語={row['日本語']}")
        print()

    # 保存
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"[成功] 保存完了: {csv_path}")

else:
    print("[情報] 対象行が見つかりませんでした")

print()
print("=" * 80)
print("処理完了")
print("=" * 80)
