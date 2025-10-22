# -*- coding: utf-8 -*-
"""
抽出したCSVファイルから有効な単語リストのみを抽出してクリーンなCSVを作成するスクリプト
"""

import pandas as pd
from pathlib import Path
import os
import re

def clean_csv(csv_path, output_dir="output_cleaned"):
    """
    CSVファイルから有効な単語リストのみを抽出してクリーンなCSVを作成

    Args:
        csv_path (str): 入力CSVファイルのパス
        output_dir (str): 出力ディレクトリ
    """
    # 出力ディレクトリを作成
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # ファイル名を取得
    csv_filename = Path(csv_path).stem

    # 言語名を抽出（例: 【全課統合版】英語_げんばのことば_建設関連職種_27cols → 英語）
    language_match = re.search(r'【全課統合版】(.+?)_', csv_filename)
    if language_match:
        language = language_match.group(1)
    else:
        language = csv_filename

    print(f"\n{'='*80}")
    print(f"処理中: {language}")
    print(f"{'='*80}\n")

    # CSVを読み込み
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    print(f"元の行数: {len(df)}")
    print(f"元の列数: {len(df.columns)}")

    # 不要な列を除外（Column_X形式の列、Table, Unnamed列、長い説明文の列）
    # 注意: Page列は保持する（PDFページ番号として必要）
    exclude_patterns = [
        'Column_',
        'Table',
        'Unnamed',
    ]

    # No.列は必須（多言語対応）
    # 各言語での番号列名: No., Số (ベトナム語), 번호 (韓国語), หมายเลข (タイ語) など
    number_col_candidates = ['No.', 'Số', '번호', 'หมายเลข', 'नंबर']
    number_col = None

    for candidate in number_col_candidates:
        if candidate in df.columns:
            number_col = candidate
            break

    if number_col is None:
        print(f"警告: 番号列が見つかりません（候補: {', '.join(number_col_candidates)}）")
        return None

    try:
        print(f"番号列として使用: {number_col}")
    except UnicodeEncodeError:
        print(f"番号列を検出（表示できません）")

    # No. 列に統一（後続の処理のため）
    if number_col != 'No.':
        df['No.'] = df[number_col]
        exclude_patterns.append(number_col)  # 元の列名は除外リストに追加

    # 除外する列を特定
    exclude_cols = []
    for col in df.columns:
        # Column_X パターン
        if any(pattern in str(col) for pattern in exclude_patterns):
            exclude_cols.append(col)
            continue
        # 長い文字列（説明文）の列
        if len(str(col)) > 200:  # 200文字以上は説明文とみなす
            exclude_cols.append(col)
            continue

    # 保持する列（除外列以外）
    keep_cols = [col for col in df.columns if col not in exclude_cols]

    try:
        print(f"保持する列: {', '.join(keep_cols)}")
    except UnicodeEncodeError:
        print(f"保持する列数: {len(keep_cols)}")

    # データのクリーニング
    cleaned_df = df[keep_cols].copy()

    # フィルタリング条件:
    # 1. No. 列が数値または数値変換可能
    # 2. No. 列の値が "No." や "番号" などのヘッダー文字列でない
    # 3. 行の大部分が空でない（有効なデータがある）

    def is_valid_row(row):
        # No.のチェック
        no_val = str(row['No.']).strip()
        if pd.isna(row['No.']) or no_val == '' or no_val == 'nan':
            return False

        # ヘッダー行を除外（No.が "No." や "番号" などの文字列）
        # 多言語対応: No., 番号, Num, など
        header_keywords = ['no.', 'no', '番号', 'ばんごう', 'num', 'number', 'номер']
        if no_val.lower() in header_keywords:
            return False

        # No.が数値に変換可能かチェック
        try:
            num = float(no_val)
            # 数値が妥当な範囲か（1〜10000程度）
            if num < 0 or num > 10000:
                return False
        except (ValueError, TypeError):
            return False

        # 行の有効性チェック: No.以外の列で少なくとも1つは有効なデータがあるか
        # （全て空の行を除外）
        other_cols = [col for col in cleaned_df.columns if col != 'No.']
        has_data = False
        for col in other_cols:
            val = str(row[col]).strip()
            if not pd.isna(row[col]) and val != '' and val != 'nan' and len(val) > 0:
                has_data = True
                break

        return has_data

    # 有効な行のみフィルタリング
    mask = cleaned_df.apply(is_valid_row, axis=1)
    cleaned_df = cleaned_df[mask].copy()

    # No.列を数値に変換
    cleaned_df['No.'] = pd.to_numeric(cleaned_df['No.'], errors='coerce')

    # NaN行を削除（数値変換に失敗した行）
    cleaned_df = cleaned_df.dropna(subset=['No.'])

    # No.でソート
    cleaned_df = cleaned_df.sort_values('No.').reset_index(drop=True)

    # No.を整数に変換
    cleaned_df['No.'] = cleaned_df['No.'].astype(int)

    print(f"\nクリーニング後の行数: {len(cleaned_df)}")
    print(f"削除された行数: {len(df) - len(cleaned_df)}")
    try:
        print(f"保持された列: {', '.join(keep_cols)}")
    except UnicodeEncodeError:
        print(f"保持された列数: {len(keep_cols)}")

    if len(cleaned_df) == 0:
        print("警告: 有効なデータが見つかりませんでした")
        return None

    # サンプルデータを表示
    print(f"\nサンプルデータ（最初の5行）:")
    try:
        print(cleaned_df.head().to_string(index=False))
    except UnicodeEncodeError:
        print("[文字エンコーディングの問題で表示できません]")

    # クリーンなCSVとして保存
    output_filename = f"{language}_cleaned.csv"
    output_filepath = output_path / output_filename

    cleaned_df.to_csv(output_filepath, index=False, encoding='utf-8-sig')
    print(f"\n保存完了: {output_filepath}")
    print(f"総単語数: {len(cleaned_df)}")

    return output_filepath

def main():
    """メイン処理"""
    # output/ フォルダ内のすべてのCSVファイルを処理
    output_dir = Path("output")
    csv_files = list(output_dir.glob("*.csv"))

    if not csv_files:
        print("エラー: output/ フォルダにCSVファイルが見つかりません")
        return

    print(f"処理対象ファイル数: {len(csv_files)}")

    results = []
    for csv_file in sorted(csv_files):
        result = clean_csv(csv_file)
        if result:
            results.append(result)

    print(f"\n{'='*80}")
    print(f"全処理完了")
    print(f"{'='*80}")
    print(f"\n成功: {len(results)} ファイル")
    print(f"失敗: {len(csv_files) - len(results)} ファイル")

    if results:
        print(f"\n出力ファイル:")
        for result in results:
            try:
                print(f"  - {result}")
            except UnicodeEncodeError:
                print(f"  - {result.name}")

if __name__ == "__main__":
    main()
