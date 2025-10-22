# -*- coding: utf-8 -*-
"""
tabula-pyを使用してカンボジア語PDFから表を抽出してテスト

tabula-pyの特徴：
- Java実装（高速・安定）
- 表構造の自動検出
- 複数ページ対応
- 列の区切りを正確に検出

このスクリプトでは、tabula-pyで抽出した結果とpdfplumberを比較します。
"""

import tabula
import pandas as pd
from pathlib import Path
import os

def extract_tables_with_tabula(pdf_path, output_csv):
    """
    tabula-pyでPDFから表を抽出

    Args:
        pdf_path (str): PDFファイルのパス
        output_csv (str): 出力CSVファイルパス
    """
    print(f"PDFファイル: {pdf_path}")
    print("\ntabula-pyで表を抽出中...")

    # すべてのページから表を抽出
    # pages='all': 全ページ
    # multiple_tables=True: 1ページに複数の表がある場合に対応
    # lattice=False, stream=True: テキストベースの抽出（線なしの表に対応）
    tables = tabula.read_pdf(
        pdf_path,
        pages='all',
        multiple_tables=True,
        lattice=False,  # 線ベースではなくテキストベースで検出
        stream=True,    # テキスト位置から表を推測
        encoding='utf-8'
    )

    print(f"\n抽出した表の数: {len(tables)}")

    if not tables:
        print("警告: 表が見つかりませんでした")
        return None

    # 各表の情報を表示
    all_tables = []
    max_columns = 0

    for idx, df in enumerate(tables, 1):
        if df is not None and len(df) > 0:
            print(f"\n表 {idx}:")
            print(f"  行数: {len(df)}")
            print(f"  列数: {len(df.columns)}")

            # 列名を表示
            try:
                print(f"  列名: {list(df.columns)[:10]}")  # 最初の10列のみ
            except UnicodeEncodeError:
                print(f"  列名: [カンボジア語・表示不可]")

            # サンプルデータを表示
            if len(df) > 0:
                print(f"  サンプル（最初の行）:")
                row = df.iloc[0]
                for col_idx, col in enumerate(df.columns[:10]):  # 最初の10列のみ
                    val = row[col]
                    if pd.notna(val):
                        try:
                            print(f"    列{col_idx}: {str(val)[:50]}")
                        except:
                            print(f"    列{col_idx}: [カンボジア語データ]")

            all_tables.append(df)

            if len(df.columns) > max_columns:
                max_columns = len(df.columns)

    # すべての表を統合
    print(f"\n表を統合中...")

    # すべての列名を収集
    all_columns = set()
    for df in all_tables:
        all_columns.update(df.columns)

    # 各DataFrameに不足している列を追加
    for i, df in enumerate(all_tables):
        for col in all_columns:
            if col not in df.columns:
                df[col] = ""
        all_tables[i] = df

    # 統合
    combined_df = pd.concat(all_tables, ignore_index=True)

    # CSVに保存
    combined_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

    print(f"\n統合完了:")
    print(f"  総行数: {len(combined_df)}")
    print(f"  総列数: {len(combined_df.columns)}")
    print(f"  出力ファイル: {output_csv}")

    return combined_df

def analyze_translation_column(df, lang_name="カンボジア語"):
    """
    翻訳列のデータ数を分析

    Args:
        df (DataFrame): 分析するDataFrame
        lang_name (str): 言語名
    """
    print(f"\n{lang_name}翻訳データ分析:")

    # 翻訳列を探す
    translation_col = None
    translation_keywords = ['របក', '翻訳', 'translation', 'แปล']

    for col in df.columns:
        col_str = str(col)
        if any(keyword in col_str for keyword in translation_keywords):
            translation_col = col
            break

    if translation_col:
        # データ数をカウント
        non_empty = df[translation_col].notna() & (df[translation_col] != '')
        count = non_empty.sum()
        ratio = count / len(df) * 100

        try:
            print(f"  翻訳列: '{translation_col}'")
        except UnicodeEncodeError:
            print(f"  翻訳列: [カンボジア語列名]")

        print(f"  データ数: {count}/{len(df)} ({ratio:.1f}%)")

        # サンプルを表示
        if count > 0:
            print(f"  サンプル（最初の5件）:")
            sample_indices = df[non_empty].head(5).index
            for idx in sample_indices:
                val = df.loc[idx, translation_col]
                try:
                    print(f"    行{idx}: {str(val)[:50]}")
                except:
                    print(f"    行{idx}: [カンボジア語データ]")

        return translation_col, count, ratio
    else:
        print(f"  警告: 翻訳列が見つかりません")
        print(f"  列名一覧:")
        for i, col in enumerate(df.columns[:20]):  # 最初の20列のみ
            try:
                print(f"    {i}: '{col}'")
            except UnicodeEncodeError:
                print(f"    {i}: [カンボジア語列名]")

        return None, 0, 0

def main():
    """メイン処理"""
    pdf_file = "建設関連PDF/【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    if not os.path.exists(pdf_file):
        print(f"エラー: PDFファイルが見つかりません - {pdf_file}")
        return

    print("=" * 80)
    print("tabula-pyでカンボジア語PDFを抽出テスト")
    print("=" * 80)

    # tabula-pyで抽出
    csv_file = output_dir / "カンボジア語_tabula_extracted.csv"
    df_tabula = extract_tables_with_tabula(pdf_file, csv_file)

    if df_tabula is not None:
        # 翻訳データを分析
        analyze_translation_column(df_tabula, "カンボジア語（tabula）")

        # pdfplumberの結果と比較
        print("\n" + "=" * 80)
        print("pdfplumberとの比較")
        print("=" * 80)

        pdfplumber_csv = "output/【全課統合版】カンボジア語_げんばのことば_建設関連職種_improved_56cols.csv"
        if os.path.exists(pdfplumber_csv):
            df_pdfplumber = pd.read_csv(pdfplumber_csv, encoding='utf-8-sig')

            print(f"\npdfplumber結果:")
            print(f"  行数: {len(df_pdfplumber)}")
            print(f"  列数: {len(df_pdfplumber.columns)}")

            print(f"\ntabula結果:")
            print(f"  行数: {len(df_tabula)}")
            print(f"  列数: {len(df_tabula.columns)}")

            # 翻訳データ数を比較
            print(f"\n翻訳データの比較:")

            # pdfplumberの翻訳列
            pdfplumber_translation_col = None
            for col in df_pdfplumber.columns:
                if 'របក' in str(col):
                    pdfplumber_translation_col = col
                    break

            if pdfplumber_translation_col:
                pdf_trans_count = (df_pdfplumber[pdfplumber_translation_col].notna() &
                                   (df_pdfplumber[pdfplumber_translation_col] != '')).sum()
                pdf_trans_ratio = pdf_trans_count / len(df_pdfplumber) * 100
                print(f"  pdfplumber: {pdf_trans_count}/{len(df_pdfplumber)} ({pdf_trans_ratio:.1f}%)")

            # tabulaの翻訳列
            tabula_translation_col, tabula_trans_count, tabula_trans_ratio = \
                analyze_translation_column(df_tabula, "tabula")

            if tabula_translation_col:
                print(f"\n結果:")
                if tabula_trans_ratio > pdf_trans_ratio:
                    print(f"  ✓ tabula-pyの方が翻訳データが多く抽出できています！")
                    print(f"    差分: {tabula_trans_ratio - pdf_trans_ratio:.1f}%")
                elif tabula_trans_ratio == pdf_trans_ratio:
                    print(f"  同等の抽出結果です")
                else:
                    print(f"  pdfplumberの方が翻訳データが多く抽出できています")
                    print(f"    差分: {pdf_trans_ratio - tabula_trans_ratio:.1f}%")

    print("\n" + "=" * 80)
    print("完了")
    print("=" * 80)

if __name__ == "__main__":
    main()
