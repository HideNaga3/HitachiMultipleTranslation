# -*- coding: utf-8 -*-
"""
全言語のクリーンCSVを1つに統合するスクリプト

機能:
1. 8言語のCSVファイルを読み込み
2. 言語列を追加
3. ヘッダーを日本語に統一
4. 1つのCSVに結合して保存
"""

import pandas as pd
from pathlib import Path
import re

# 各言語のファイル名と言語名のマッピング
LANGUAGE_MAPPING = {
    '英語_cleaned.csv': '英語',
    'タガログ語_cleaned.csv': 'タガログ語',
    'カンボジア語_cleaned.csv': 'カンボジア語',
    '中国語_cleaned.csv': '中国語',
    'インドネシア語_cleaned.csv': 'インドネシア語',
    'ミャンマー語_cleaned.csv': 'ミャンマー語',
    'タイ語_cleaned.csv': 'タイ語',
    'ベトナム語_cleaned.csv': 'ベトナム語',
}

def get_japanese_column_name(col_name):
    """
    各言語の列名を日本語の列名にマッピング

    Args:
        col_name (str): 元の列名

    Returns:
        str: 日本語の列名
    """
    col_lower = str(col_name).lower()

    # No. → 番号
    if col_name == 'No.':
        return '番号'

    # Page → PDFページ番号
    if col_name == 'Page':
        return 'PDFページ番号'

    # 単語/語彙
    if any(keyword in col_lower for keyword in [
        'word', 'phrase', 'kosakata', 'talasalitaan', 'từ vựng',
        'ခ ေါဟာရ', '词汇', 'វាក', 'ศพ'
    ]):
        return '単語'

    # 翻訳
    if any(keyword in col_lower for keyword in [
        'translation', 'terjemahan', 'pagsasalin', 'dịch',
        'ဘာသာ', '中文词意', 'របក', 'คา แปล', 'แปล'
    ]) or '译' in col_name or 'ြန' in col_name:
        return '翻訳'

    # 読み方（ひらがな）
    if any(keyword in col_lower for keyword in [
        'how to read', 'hiragana', 'cara membaca', 'paano magbasa',
        'cách đọc', 'စာဖတ', '读音', '假名', 'មបៀប', 'មរៀរ', 'วธิ', 'วิธ', 'อา่ น', 'อ่าน'
    ]):
        return '読み方（ひらがな）'

    # 備考/注解
    if any(keyword in col_lower for keyword in [
        'note', 'annotasyon', 'anotasi', 'chú thích',
        'မှတ', '注解', 'ចាំណា', 'ចំ', 'ความค', 'เหตุ'
    ]):
        return '備考'

    # 例文/例句
    if any(keyword in col_lower for keyword in [
        'example', 'contoh', 'halimbawa', 'ví dụ',
        'ဥြမာ', '例句', 'ឧទាហ', 'ตว', 'อย่าง'
    ]):
        return '例文'

    # 写真
    if any(keyword in col_lower for keyword in [
        'picture', 'foto', 'larawan', 'ảnh',
        '照片', 'រូប', 'ภาพ'
    ]):
        return '写真'

    # 標識/記号
    if any(keyword in col_lower for keyword in [
        'sign', 'tanda', 'palatandaan', 'biển',
        'အမှတ', '标识', 'សញ្ញា', 'เครอื่ ง', 'หมาย'
    ]):
        return '標識'

    # マッチしない場合はそのまま返す
    return col_name

def merge_all_csvs(input_dir="output_cleaned", output_file="output_cleaned/全言語統合.csv"):
    """
    全言語のCSVファイルを1つに統合

    Args:
        input_dir (str): 入力ディレクトリ
        output_file (str): 出力ファイルパス
    """
    input_path = Path(input_dir)
    all_dataframes = []

    print("="*80)
    print("全言語CSV統合処理")
    print("="*80)

    for filename, language_name in LANGUAGE_MAPPING.items():
        csv_file = input_path / filename

        if not csv_file.exists():
            print(f"警告: ファイルが見つかりません - {filename}")
            continue

        print(f"\n処理中: {language_name}")

        # CSVを読み込み
        df = pd.read_csv(csv_file, encoding='utf-8-sig')

        # 言語列を追加
        df.insert(0, '言語', language_name)

        # 列名を日本語に変換
        new_columns = {}
        japanese_col_counts = {}  # 日本語列名の出現回数をカウント

        for col in df.columns:
            if col == '言語':
                continue
            new_col = get_japanese_column_name(col)

            # 重複チェック
            if new_col in japanese_col_counts:
                japanese_col_counts[new_col] += 1
                # 重複する場合は番号を付ける
                new_col = f"{new_col}_{japanese_col_counts[new_col]}"
            else:
                japanese_col_counts[new_col] = 1

            new_columns[col] = new_col

        df.rename(columns=new_columns, inplace=True)

        # 重複列を統合（同じ意味の列なので、空でない値を優先して1つに統合）
        final_df = df[['言語']].copy()
        processed_cols = set()

        for col in df.columns:
            if col == '言語':
                continue

            # 番号付き列名（例: '備考_2'）の場合、ベース名（'備考'）を取得
            base_col = col.split('_')[0] if '_' in col and col.split('_')[-1].isdigit() else col

            if base_col in processed_cols:
                continue

            # 同じベース名を持つ列を全て取得
            related_cols = [c for c in df.columns if c.startswith(base_col) and
                           (c == base_col or (c.startswith(f"{base_col}_") and c.split('_')[-1].isdigit()))]

            if len(related_cols) == 1:
                # 重複なし
                final_df[base_col] = df[col]
            else:
                # 重複あり：複数列を統合
                merged_series = df[related_cols[0]]
                for related_col in related_cols[1:]:
                    # 空でない値で上書き
                    mask = df[related_col].notna() & (df[related_col] != '')
                    merged_series[mask] = df[related_col][mask]

                final_df[base_col] = merged_series

            processed_cols.add(base_col)

        df = final_df

        print(f"  元の行数: {len(df)}")
        try:
            print(f"  変換後の列: {list(df.columns)}")
        except UnicodeEncodeError:
            print(f"  変換後の列数: {len(df.columns)}")

        all_dataframes.append(df)

    if not all_dataframes:
        print("\n エラー: 統合するデータがありません")
        return None

    print(f"\n{'='*80}")
    print("統合処理中...")
    print(f"{'='*80}\n")

    # 全てのDataFrameを統合
    # 列が完全に一致しない場合があるため、全ての列を収集
    all_columns = set()
    for df in all_dataframes:
        all_columns.update(df.columns)

    # 列の順序を定義（言語列を最初に）
    standard_columns = [
        '言語', '番号', '単語', '翻訳', '読み方（ひらがな）',
        '備考', '例文', '写真', '標識'
    ]

    # 標準列以外の列を追加
    extra_columns = [col for col in all_columns if col not in standard_columns]
    ordered_columns = standard_columns + extra_columns

    # 各DataFrameに不足している列を追加
    for i, df in enumerate(all_dataframes):
        for col in ordered_columns:
            if col not in df.columns:
                df[col] = ''
        # 列の順序を統一
        all_dataframes[i] = df[ordered_columns]

    # 統合
    merged_df = pd.concat(all_dataframes, ignore_index=True)

    # 存在しない列を削除（全てNaNの列）
    merged_df = merged_df.dropna(axis=1, how='all')

    print(f"統合結果（全列）:")
    print(f"  総行数: {len(merged_df)}")
    print(f"  総列数: {len(merged_df.columns)}")
    try:
        print(f"  列名: {list(merged_df.columns)}")
    except UnicodeEncodeError:
        print(f"  列名: [エンコーディングエラー]")

    # 必要な列だけを抽出
    required_columns = ['言語', '番号', 'PDFページ番号', '単語', '翻訳']

    # 存在しない列をチェック
    missing_cols = [col for col in required_columns if col not in merged_df.columns]
    if missing_cols:
        print(f"\n警告: 以下の列が見つかりません: {missing_cols}")
        # 存在する列だけを使用
        required_columns = [col for col in required_columns if col in merged_df.columns]

    # 必要な列だけに絞り込み
    merged_df = merged_df[required_columns]

    print(f"\n絞り込み後:")
    print(f"  総行数: {len(merged_df)}")
    print(f"  総列数: {len(merged_df.columns)}")
    print(f"  列名: {list(merged_df.columns)}")

    # データのトリム処理（文字列列の前後の空白を削除）
    print(f"\nデータのトリム処理中...")
    for col in merged_df.columns:
        if merged_df[col].dtype == 'object':  # 文字列列のみ
            merged_df[col] = merged_df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # 列の順番を変更
    desired_order = ['言語', 'PDFページ番号', '番号', '単語', '翻訳']
    # 存在する列だけを並べ替え
    column_order = [col for col in desired_order if col in merged_df.columns]
    merged_df = merged_df[column_order]

    print(f"\n列順変更後:")
    print(f"  列順: {list(merged_df.columns)}")

    # データの並び替え：言語 → PDFページ番号 → 番号
    print(f"\nデータの並び替え中（言語 → PDFページ番号 → 番号）...")
    sort_columns = []
    if '言語' in merged_df.columns:
        sort_columns.append('言語')
    if 'PDFページ番号' in merged_df.columns:
        sort_columns.append('PDFページ番号')
    if '番号' in merged_df.columns:
        sort_columns.append('番号')

    if sort_columns:
        merged_df = merged_df.sort_values(by=sort_columns).reset_index(drop=True)

    print(f"\n最終結果:")
    print(f"  総行数: {len(merged_df)}")
    print(f"  総列数: {len(merged_df.columns)}")
    print(f"  列順: {list(merged_df.columns)}")

    # 言語別の行数を表示
    print(f"\n言語別の行数:")
    for language in merged_df['言語'].unique():
        count = len(merged_df[merged_df['言語'] == language])
        print(f"  {language}: {count}行")

    # サンプルデータを表示
    print(f"\nサンプルデータ（最初の10行）:")
    try:
        # 必要な列が全て含まれている場合
        if all(col in merged_df.columns for col in ['言語', '番号', 'PDFページ番号', '単語', '翻訳']):
            print(merged_df.head(10).to_string(index=False))
        else:
            print(merged_df.head(10).to_string(index=False))
    except Exception as e:
        print(f"  [表示エラー: {e}]")

    # CSVに保存
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)

    merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n保存完了: {output_path}")
    print(f"ファイルサイズ: {output_path.stat().st_size:,} bytes")

    return output_path

def main():
    """メイン処理"""
    result = merge_all_csvs()

    if result:
        print(f"\n{'='*80}")
        print("全処理完了")
        print(f"{'='*80}")

if __name__ == "__main__":
    main()
