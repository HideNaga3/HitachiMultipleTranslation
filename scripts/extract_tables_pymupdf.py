"""
PyMuPDFを使ってPDFから表データを抽出する（pdfplumberの代替）
CIDコード問題を解決
"""

import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path
import sys
import io

# UTF-8出力を強制
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def extract_all_tables_from_pdf(pdf_path, output_path=None):
    """
    PDFから全ページの表を抽出してCSVに保存

    Parameters:
    -----------
    pdf_path : str or Path
        PDFファイルのパス
    output_path : str or Path, optional
        出力CSVファイルのパス（指定しない場合は自動生成）

    Returns:
    --------
    dict : 抽出結果の統計情報
    """
    pdf_path = Path(pdf_path)

    if output_path is None:
        output_path = Path('output') / f'{pdf_path.stem}_pymupdf抽出.csv'
    else:
        output_path = Path(output_path)

    # 出力ディレクトリ作成
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*80}")
    print(f"PDF表抽出: {pdf_path.name}")
    print(f"{'='*80}\n")

    # PDFを開く
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"総ページ数: {total_pages}")

    # 全データを格納するリスト
    all_data = []
    total_tables = 0
    total_rows = 0

    # 各ページを処理
    for page_num in range(total_pages):
        page = doc[page_num]

        # 表を検索
        table_finder = page.find_tables()
        tables = table_finder.tables  # TableFinderからテーブルリストを取得

        if len(tables) > 0:
            print(f"  ページ {page_num + 1}: {len(tables)}個の表を発見")

            for table_idx, table in enumerate(tables):
                # 表データを抽出
                table_data = table.extract()

                if not table_data or len(table_data) < 2:
                    print(f"    表{table_idx + 1}: データなし（スキップ）")
                    continue

                # ヘッダーと行データ
                header = table_data[0]
                rows = table_data[1:]

                # 行数カウント
                total_tables += 1
                total_rows += len(rows)

                # 各行にページ番号と表番号を追加
                for row in rows:
                    # ページ番号、表番号を先頭に追加
                    row_with_meta = [page_num + 1, table_idx + 1] + list(row)
                    all_data.append(row_with_meta)

                print(f"    表{table_idx + 1}: {len(rows)}行 x {len(header)}列")

    doc.close()

    if not all_data:
        print("\n⚠ 表が見つかりませんでした")
        return {
            'success': False,
            'total_pages': total_pages,
            'total_tables': 0,
            'total_rows': 0
        }

    # 各行の列数を確認して最大列数を取得
    max_columns = max(len(row) for row in all_data)
    print(f"\n最大列数: {max_columns}")

    # すべての行を最大列数に揃える（不足分は空文字列で埋める）
    normalized_data = []
    for row in all_data:
        if len(row) < max_columns:
            # 不足分を空文字列で埋める
            normalized_row = list(row) + [''] * (max_columns - len(row))
        else:
            normalized_row = list(row)
        normalized_data.append(normalized_row)

    # ページと表番号の列名
    meta_columns = ['Page', 'Table']

    # 元の表の列数（メタデータを除く）
    original_columns = max_columns - len(meta_columns)

    # 列名を生成
    data_column_names = [f'Column_{i}' for i in range(original_columns)]

    # 全列名
    column_names = meta_columns + data_column_names

    # データフレーム作成
    df = pd.DataFrame(normalized_data, columns=column_names)

    # CIDコードチェック
    cid_count = 0
    for col in df.columns:
        if df[col].dtype == 'object':
            cid_matches = df[col].astype(str).str.contains(r'\(cid:', regex=True, na=False)
            cid_count += cid_matches.sum()

    # CSV出力（UTF-8 BOM）
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    # 統計情報
    print(f"\n{'='*80}")
    print("抽出完了")
    print(f"{'='*80}")
    print(f"総ページ数: {total_pages}")
    print(f"抽出した表の数: {total_tables}")
    print(f"総行数: {total_rows}")
    print(f"CSV行数（ヘッダー含む）: {len(df) + 1}")
    print(f"CSV列数: {len(df.columns)}")
    print(f"CIDコード検出数: {cid_count}")
    print(f"\n出力ファイル: {output_path}")
    print(f"ファイルサイズ: {output_path.stat().st_size / 1024:.1f} KB")

    return {
        'success': True,
        'total_pages': total_pages,
        'total_tables': total_tables,
        'total_rows': total_rows,
        'csv_path': str(output_path),
        'cid_count': cid_count
    }


if __name__ == '__main__':
    # カンボジア語PDFをテスト
    pdf_file = Path('建設関連PDF') / '【全課統合版】カンボジア語_げんばのことば_建設関連職種.pdf'

    result = extract_all_tables_from_pdf(
        pdf_path=pdf_file,
        output_path=Path('output') / 'test_カンボジア語_pymupdf抽出.csv'
    )

    if result['success']:
        print(f"\n✓ 抽出成功")
        if result['cid_count'] == 0:
            print(f"✓ CIDコードなし！")
        else:
            print(f"⚠ CIDコード {result['cid_count']}件検出")
