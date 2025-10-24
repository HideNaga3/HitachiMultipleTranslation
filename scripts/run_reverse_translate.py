"""
逆翻訳Excel作成スクリプト（実行用）
import用CSVを入力すると逆翻訳Excelが出力される
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.reverse_translate_excel import create_reverse_translation_excel

if __name__ == "__main__":
    print("=" * 80)
    print("逆翻訳Excel作成")
    print("=" * 80)
    print()

    # デフォルトのファイルパス
    input_csv = project_root / 'output' / '全言語統合_テンプレート_インポート用.csv'
    output_excel = project_root / 'output' / '逆翻訳_検証結果.xlsx'

    # コマンドライン引数がある場合は上書き
    if len(sys.argv) > 1:
        input_csv = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_excel = Path(sys.argv[2])

    print(f"入力CSV: {input_csv}")
    print(f"出力Excel: {output_excel}")
    print()

    # 実行
    result = create_reverse_translation_excel(
        input_csv=str(input_csv),
        output_excel=str(output_excel),
        verbose=True
    )

    print()
    print("=" * 80)
    print("結果サマリー")
    print("=" * 80)
    print(f"入力ファイル: {result['input_csv']}")
    print(f"出力ファイル: {result['output_excel']}")
    print(f"処理行数: {result['row_count']}行")
    print(f"翻訳した列: {', '.join(result['translated_columns'])}")
    print()
