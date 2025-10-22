# -*- coding: utf-8 -*-
"""
camelot-pyを使用してカンボジア語PDFから表を抽出してテスト

camelot-pyの特徴：
- Pythonのみで動作（Java不要）
- 2つの抽出モード：
  - lattice: 線ベースの表検出
  - stream: テキストベースの表検出
- 高精度な表構造検出

このスクリプトでは、camelot-pyで抽出した結果とpdfplumberを比較します。
"""

import camelot
import pandas as pd
from pathlib import Path
import os

def extract_tables_with_camelot(pdf_path, output_csv, flavor='stream'):
    """
    camelot-pyでPDFから表を抽出

    Args:
        pdf_path (str): PDFファイルのパス
        output_csv (str): 出力CSVファイルパス
        flavor (str): 抽出モード ('lattice' or 'stream')
    """
    print(f"PDFファイル: {pdf_path}")
    print(f"抽出モード: {flavor}")
    print("\ncamelot-pyで表を抽出中...")

    try:
        # すべてのページから表を抽出
        # flavor='stream': テキストベースの抽出（線なしの表に対応）
        # flavor='lattice': 線ベースの抽出（線ありの表に対応）
        tables = camelot.read_pdf(
            pdf_path,
            pages='all',
            flavor=flavor,
        )

        print(f"\n抽出した表の数: {len(tables)}")

        if len(tables) == 0:
            print("警告: 表が見つかりませんでした")
            return None

        # 各表の情報を表示
        all_tables = []

        for idx, table in enumerate(tables, 1):
            df = table.df

            if df is not None and len(df) > 0:
                print(f"\n表 {idx}:")
                print(f"  行数: {len(df)}")
                print(f"  列数: {len(df.columns)}")
                print(f"  精度スコア: {table.accuracy:.2f}")
                print(f"  形状: {table.shape}")

                # ヘッダー行を最初の行として使用
                if len(df) > 0:
                    headers = df.iloc[0].tolist()
                    data_rows = df.iloc[1:].values.tolist()

                    # ヘッダーをクリーニング
                    headers = [str(h) if h and str(h).strip() else f"Column_{i}"
                               for i, h in enumerate(headers)]

                    # DataFrameを再構築
                    df_clean = pd.DataFrame(data_rows, columns=headers)

                    # 空行をスキップ
                    df_clean = df_clean[df_clean.apply(lambda row: any(cell and str(cell).strip() for cell in row), axis=1)]

                    if len(df_clean) > 0:
                        # 列名を表示
                        try:
                            print(f"  列名: {list(df_clean.columns)[:10]}")  # 最初の10列のみ
                        except UnicodeEncodeError:
                            print(f"  列名: [カンボジア語・表示不可]")

                        # サンプルデータを表示
                        print(f"  サンプル（最初の行）:")
                        row = df_clean.iloc[0]
                        for col_idx, col in enumerate(df_clean.columns[:10]):  # 最初の10列のみ
                            val = row[col]
                            if pd.notna(val) and str(val).strip():
                                try:
                                    print(f"    列{col_idx} '{col}': {str(val)[:50]}")
                                except:
                                    print(f"    列{col_idx}: [カンボジア語データ]")

                        all_tables.append(df_clean)

        if not all_tables:
            print("警告: 有効な表が見つかりませんでした")
            return None

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

    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()
        return None

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
        non_empty = df[translation_col].notna() & (df[translation_col] != '') & (df[translation_col] != ' ')
        count = non_empty.sum()
        ratio = count / len(df) * 100 if len(df) > 0 else 0

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
    print("camelot-pyでカンボジア語PDFを抽出テスト")
    print("=" * 80)

    # まずstreamモードで試す（テキストベース、線なしの表に対応）
    csv_file_stream = output_dir / "カンボジア語_camelot_stream_extracted.csv"
    df_camelot_stream = extract_tables_with_camelot(pdf_file, csv_file_stream, flavor='stream')

    if df_camelot_stream is not None:
        # 翻訳データを分析
        col, count, ratio = analyze_translation_column(df_camelot_stream, "カンボジア語（camelot-stream）")

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

            print(f"\ncamelot-stream結果:")
            print(f"  行数: {len(df_camelot_stream)}")
            print(f"  列数: {len(df_camelot_stream.columns)}")

            # 翻訳データ数を比較
            print(f"\n翻訳データの比較:")

            # pdfplumberの翻訳列
            pdfplumber_translation_col = None
            for c in df_pdfplumber.columns:
                if 'របក' in str(c):
                    pdfplumber_translation_col = c
                    break

            if pdfplumber_translation_col:
                pdf_trans_count = (df_pdfplumber[pdfplumber_translation_col].notna() &
                                   (df_pdfplumber[pdfplumber_translation_col] != '')).sum()
                pdf_trans_ratio = pdf_trans_count / len(df_pdfplumber) * 100
                print(f"  pdfplumber: {pdf_trans_count}/{len(df_pdfplumber)} ({pdf_trans_ratio:.1f}%)")

            # camelotの結果
            if col:
                print(f"  camelot-stream: {count}/{len(df_camelot_stream)} ({ratio:.1f}%)")

                if ratio > pdf_trans_ratio:
                    print(f"\n結果:")
                    print(f"  ✓ camelot-pyの方が翻訳データが多く抽出できています！")
                    print(f"    差分: {ratio - pdf_trans_ratio:.1f}%")
                elif ratio == pdf_trans_ratio:
                    print(f"\n結果:")
                    print(f"  同等の抽出結果です")
                else:
                    print(f"\n結果:")
                    print(f"  pdfplumberの方が翻訳データが多く抽出できています")
                    print(f"    差分: {pdf_trans_ratio - ratio:.1f}%")

    print("\n" + "=" * 80)
    print("完了")
    print("=" * 80)

if __name__ == "__main__":
    main()
