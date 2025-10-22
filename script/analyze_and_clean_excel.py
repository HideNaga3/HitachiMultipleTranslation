"""
Excelファイルを分析して、データの少ない列を削除するスクリプト

目的：
1. 各Excelファイルの列ごとのデータ充足率を計算
2. データ充足率が低い列（閾値以下）を削除
3. クリーンアップされたCSVを出力
"""

import pandas as pd
from pathlib import Path
import json

# 設定
EXCEL_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\建設関係Excel")
OUTPUT_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\output_cleaned")
ANALYSIS_DIR = Path(r"C:\Users\永井秀和\Documents\workspace\三菱様_多言語翻訳_202510\for_claude")

# データ充足率の閾値（これ以下の列は削除）
THRESHOLD = 0.10  # 10%未満のデータしかない列は削除

# 出力ディレクトリ作成
OUTPUT_DIR.mkdir(exist_ok=True)
ANALYSIS_DIR.mkdir(exist_ok=True)


def analyze_excel_file(excel_path):
    """
    Excelファイルを分析して、各列のデータ充足率を計算

    Returns:
        dict: 列名と充足率のマッピング
    """
    print(f"\n{'='*80}")
    print(f"分析中: {excel_path.name}")
    print(f"{'='*80}")

    # Excelファイル読み込み（1行目をヘッダーとして）
    df = pd.read_excel(excel_path, sheet_name=0, header=0)

    print(f"総行数: {len(df)}")
    print(f"総列数: {len(df.columns)}")
    print()

    # 各列のデータ充足率を計算
    column_stats = {}

    for col in df.columns:
        # 非空セル数をカウント
        non_empty = df[col].notna().sum()
        # 空文字列も空とみなす
        if df[col].dtype == 'object':
            non_empty_non_blank = (df[col].notna() & (df[col].astype(str).str.strip() != '')).sum()
        else:
            non_empty_non_blank = non_empty

        fill_rate = non_empty_non_blank / len(df) if len(df) > 0 else 0

        column_stats[col] = {
            'non_empty': int(non_empty_non_blank),
            'total': int(len(df)),
            'fill_rate': float(fill_rate)
        }

        # 充足率を表示
        print(f"列: {col}")
        print(f"  データあり: {non_empty_non_blank}/{len(df)} ({fill_rate*100:.1f}%)")

    return column_stats, df


def clean_excel_file(excel_path, threshold=THRESHOLD):
    """
    Excelファイルからデータの少ない列を削除してCSVとして保存

    Args:
        excel_path: Excelファイルのパス
        threshold: データ充足率の閾値（これ以下の列は削除）

    Returns:
        dict: 処理結果の情報
    """
    # 分析
    column_stats, df = analyze_excel_file(excel_path)

    # 削除する列と保持する列を決定
    columns_to_remove = []
    columns_to_keep = []

    for col, stats in column_stats.items():
        if stats['fill_rate'] < threshold:
            columns_to_remove.append(col)
        else:
            columns_to_keep.append(col)

    print(f"\n{'='*80}")
    print(f"削除する列 (充足率 < {threshold*100}%): {len(columns_to_remove)}列")
    print(f"{'='*80}")
    for col in columns_to_remove:
        stats = column_stats[col]
        print(f"  - {col} ({stats['fill_rate']*100:.1f}%)")

    print(f"\n{'='*80}")
    print(f"保持する列 (充足率 >= {threshold*100}%): {len(columns_to_keep)}列")
    print(f"{'='*80}")
    for col in columns_to_keep:
        stats = column_stats[col]
        print(f"  - {col} ({stats['fill_rate']*100:.1f}%)")

    # クリーンアップされたDataFrameを作成
    df_clean = df[columns_to_keep].copy()

    # CSV出力
    output_filename = excel_path.stem + "_cleaned.csv"
    output_path = OUTPUT_DIR / output_filename
    df_clean.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"\n出力完了: {output_path}")
    print(f"  行数: {len(df_clean)}")
    print(f"  列数: {len(df_clean.columns)}")

    return {
        'file': excel_path.name,
        'original_rows': len(df),
        'original_cols': len(df.columns),
        'cleaned_rows': len(df_clean),
        'cleaned_cols': len(df_clean.columns),
        'removed_cols': len(columns_to_remove),
        'columns_removed': columns_to_remove,
        'columns_kept': columns_to_keep,
        'column_stats': column_stats
    }


def main():
    """メイン処理"""
    # Excelファイルを取得
    excel_files = sorted(EXCEL_DIR.glob("*.xlsx"))

    if not excel_files:
        print(f"エラー: {EXCEL_DIR} にExcelファイルが見つかりません")
        return

    print(f"見つかったExcelファイル: {len(excel_files)}個")
    for f in excel_files:
        print(f"  - {f.name}")

    # 全ファイルを処理
    all_results = []

    for excel_file in excel_files:
        try:
            result = clean_excel_file(excel_file, threshold=THRESHOLD)
            all_results.append(result)
        except Exception as e:
            print(f"\nエラー: {excel_file.name} の処理中にエラーが発生しました")
            print(f"  {type(e).__name__}: {e}")

    # 分析結果をJSONとして保存
    analysis_path = ANALYSIS_DIR / "excel_analysis_results.json"
    with open(analysis_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*80}")
    print(f"全体サマリー")
    print(f"{'='*80}")
    print(f"処理したファイル数: {len(all_results)}")
    print(f"分析結果: {analysis_path}")

    # サマリーテーブルを表示
    print(f"\n{'='*80}")
    print("ファイル別サマリー")
    print(f"{'='*80}")
    print(f"{'言語':<15} {'元の列数':<10} {'削除列数':<10} {'残り列数':<10}")
    print(f"{'-'*50}")

    for result in all_results:
        # ファイル名から言語を抽出
        filename = result['file']
        if 'タイ語' in filename:
            lang = 'タイ語'
        elif 'インドネシア語' in filename:
            lang = 'インドネシア語'
        elif 'カンボジア語' in filename:
            lang = 'カンボジア語'
        elif 'タガログ語' in filename:
            lang = 'タガログ語'
        elif 'ベトナム語' in filename:
            lang = 'ベトナム語'
        elif 'ミャンマー語' in filename:
            lang = 'ミャンマー語'
        elif '中国語' in filename:
            lang = '中国語'
        elif '英語' in filename:
            lang = '英語'
        else:
            lang = filename

        print(f"{lang:<15} {result['original_cols']:<10} {result['removed_cols']:<10} {result['cleaned_cols']:<10}")


if __name__ == '__main__':
    main()
