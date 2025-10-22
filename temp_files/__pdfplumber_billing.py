"""
PDF請求書からデータを抽出してExcelに変換するプログラム

【必要な外部ライブラリのインストール】
pip install pdfplumber
pip install pandas
pip install openpyxl
pip install tqdm

または一括インストール:
pip install pdfplumber pandas openpyxl tqdm

【環境準備】
conda activate base  # または適切な仮想環境をアクティベート
"""

# 必要なライブラリのインポート
import pdfplumber  # PDFファイルからテキストやテーブルを抽出するライブラリ
import pandas as pd  # データフレーム操作用
import os  # ファイル・ディレクトリ操作用
from pathlib import Path  # パス操作用
from datetime import datetime  # 日時処理用
import re  # 正規表現処理用
from tqdm import tqdm  # プログレスバー表示用
import openpyxl  # Excelファイル操作用
from _xl_util import ExcelUtil  # 自作のExcelユーティリティ

# PDF請求書からデータを抽出してExcelに変換するメインプログラム

def get_text(is_debug=False):
    """
    PDF請求書からテーブルデータを抽出してExcelファイルに変換する関数
    Args:
        is_debug (bool): デバッグモードかどうか（デフォルト: False）
    """
    # 拠点マスタデータをExcelファイルから取得
    branch_df = ExcelUtil.get_df_from_table(
            xl_fp=r"C:\Users\agekkegroup\OneDrive - エイジェックグループ\請求書発行用_SharePoint\請求書発行\15_企業名マスタ\管理表_企業コード.xlsx",
            sheet_name='拠点マスタ', table_name='拠点マスタ'
    )
    # 拠点リストを取得（PDFテーブル判定用）
    branchs = branch_df['インデックス無し拠点'].to_list()
    # PDFファイルパスの取得（デバッグモードかどうかで分岐）
    if not is_debug:
        ans = input("PDFパス (t:test): ")
        pdf_dp = ans
        pdf_dp = pdf_dp.replace('"', '')  # パス文字列からダブルクォートを除去
    else:
        # デバッグモード時はテスト用パスを使用
        ans = 't'
        pdf_dp = r"C:\ws\_インボイス請求書発行\_請求書発行作業フォルダ_V3\___60_PDF"

    # 指定されたパスの存在確認
    if not os.path.exists(pdf_dp):
        input("対象パスが見つかりません...")
        return
    # 処理対象ページ範囲の設定
    if not is_debug:
        ans = input('page (ex:2-5, a:all): ')
    else:
        ans = 'a'  # デバッグモード時は全ページ処理

    # ページ範囲の解析と設定
    if ans == 'a':
        page_text = 'all'  # 全ページ処理
    else:
        # ページ範囲指定の形式チェック（例：2-5）
        if not re.fullmatch(r'[0-9]+\-[0-9]+', ans):
            print('不正な入力です')
            return
        else:
            # ページ範囲をゼロベースインデックスに変換
            min = int(ans.split('-')[0]) - 1
            max = int(ans.split('-')[1]) - 1
            page_text = ans
    # 指定されたパスがフォルダかファイルかを判定し、PDFファイルを収集
    is_valid_path = False
    file_objs = []  # 処理対象のPDFファイルオブジェクトリスト
    fobj = Path(pdf_dp).absolute()

    if fobj.is_dir():
        # ディレクトリの場合：配下の全PDFファイルを再帰的に検索
        for pobj in fobj.glob('**/*.pdf'):
            file_objs.append(pobj)
        if not len(file_objs) == 0:
            is_valid_path = True
    elif fobj.is_file():
        # ファイルの場合：PDFファイルかどうかをチェック
        if fobj.suffix == '.pdf':
            is_valid_path = True
            file_objs.append(fobj)

    # 有効なPDFファイルが見つからない場合は終了
    if not is_valid_path:
        print('対象ファイルが見つかりません')
        return
    # 全PDFファイルから抽出したデータを格納するリスト
    all_df = []

    # 各PDFファイルを順次処理
    for i, fobj in enumerate(file_objs):
        f_max = len(file_objs)
        print(f'処理中({i+1}/{f_max}): {str(fobj)}')

        # 出力ファイル用のタイムスタンプを生成
        ts = datetime.now().strftime('%Y%m%d_%H%M_%S')

        # PDFファイルを開いてデータ抽出開始
        with pdfplumber.open(str(fobj)) as pdf:
            # ファイル名から取引先名を正規表現で抽出（例：123456_取引先名御中.pdf）
            client_grp = re.search(r'(?<=\d{6}_)(.*?)御中', str(fobj))
            client = client_grp.group(1)

            # 処理対象ページ範囲を決定
            if page_text == 'all':
                min = 0
                max = len(pdf.pages) - 1
            # テーブルデータのヘッダー定義
            headers = ['拠点', '件名', '数量', '単位', '単価', '金額', '税区分']

            # 指定されたページ範囲を順次処理（プログレスバー付き）
            for page_number in tqdm(range(min, max + 1)):
                page = pdf.pages[page_number]
                table = page.extract_table()  # ページからテーブルデータを抽出

                # テーブルデータが存在する場合の処理
                if table:
                    # 空行を除外（少なくとも1つのフィールドに値があるレコードのみ残す）
                    table = [record for record in table if any(field != '' for field in record)]

                    # デバッグ用のブレークポイント（特定ファイル用）
                    if 'エイジェックグループ' in fobj.name:
                        pass # デバッグ用
                    # テーブル形式の判定と適切な処理を実行
                    if table[0][0] == '拠点':
                        # 1行目がヘッダーの場合：2行目以降をデータとして処理
                        df_buf = pd.DataFrame(table[1:], columns=table[0])
                        df_buf['ファイル名'] = [fobj.name for _ in range(df_buf.shape[0])]
                        df_buf['取引先'] = [client for _ in range(df_buf.shape[0])]
                        all_df.append(df_buf)  # データフレームリストに追加
                    elif table[0][0] in branchs:
                        # 1行目が拠点名の場合：全行をデータとして処理
                        df_buf = pd.DataFrame(table, columns=headers)
                        df_buf['ファイル名'] = [fobj.name for _ in range(df_buf.shape[0])]
                        df_buf['取引先'] = [client for _ in range(df_buf.shape[0])]
                        all_df.append(df_buf)  # データフレームリストに追加
                    else:
                        # 対象外のテーブル形式の場合はスキップ
                        pass
    # 全PDFから抽出したデータフレームを1つに結合
    df_cat = pd.concat(all_df, axis=0)

    # データ型の変換と整形
    df_cat['数量'] = df_cat['数量'].astype(float)  # 数量を数値型に変換
    df_cat['単価'] = df_cat['単価'].astype(float)  # 単価を数値型に変換
    df_cat['金額'] = df_cat['金額'].str.replace(',', '')  # 金額からカンマを除去
    df_cat['金額'] = df_cat['金額'].astype(float)  # 金額を数値型に変換

    # 最終的なカラム順序を指定してデータフレームを整理
    df_cat = df_cat[['拠点', '取引先', '件名', '数量', '単位', '単価', '金額', '税区分', 'ファイル名']]

    # 結果をExcelファイルに出力
    xlp = f'{ts}.xlsx'  # タイムスタンプ付きファイル名
    df_cat.to_excel(xlp, index=False)  # インデックスなしでExcel出力
    ExcelUtil.set_my_config(xlp)  # 独自設定を適用

    # 処理完了メッセージ
    if not is_debug:
        input('完了')  # 本番モード：ユーザーの入力待ち
    else:
        print('完了')  # デバッグモード：メッセージ表示のみ

# メイン実行部：スクリプトが直接実行された場合のエントリーポイント
if __name__ == "__main__":
    get_text(is_debug=True)  # デバッグモードで実行