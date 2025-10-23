"""
複数ファイル一括翻訳のテストスクリプト
"""
import sys
from pathlib import Path

# scriptsディレクトリをモジュール検索パスに追加
sys.path.insert(0, str(Path(__file__).parent))

from batch_translator import (
    check_csv_structure,
    check_excel_structure,
    translate_from_multiple_csv,
    translate_from_multiple_excel
)


def test_csv_structure_check():
    """CSVファイルの列構造チェックのテスト"""
    print("=" * 70)
    print("[テスト1] CSV列構造チェック")
    print("=" * 70)

    test_data_dir = Path(__file__).parent.parent / "test_data"
    csv_files = [
        str(test_data_dir / "test_words_single_column.csv"),
        str(test_data_dir / "test_words_multi_column.csv")
    ]

    try:
        result = check_csv_structure(csv_files)
        print(f"\n[結果]")
        print(f"  全ファイル一致: {result['is_valid']}")
        print(f"  基準列名: {result['column_names']}")
        print(f"  列数: {result['column_count']}")

        if not result['is_valid']:
            print(f"\n[不一致ファイル]")
            for error_file in result['error_files']:
                print(f"  - {Path(error_file).name}")

        for file_info in result['files']:
            status = "OK" if file_info['is_match'] else "NG"
            print(f"\n  [{status}] {Path(file_info['path']).name}")
            print(f"    列名: {file_info['column_names']}")
            print(f"    列数: {file_info['column_count']}")

    except Exception as e:
        print(f"[ERROR] {e}")


def test_excel_structure_check():
    """Excelファイルの列構造チェックのテスト"""
    print("\n" + "=" * 70)
    print("[テスト2] Excel列構造チェック")
    print("=" * 70)

    test_data_dir = Path(__file__).parent.parent / "test_data"
    excel_files = [
        str(test_data_dir / "test_words_single_column.xlsx"),
        str(test_data_dir / "test_words_multi_column.xlsx")
    ]

    try:
        result = check_excel_structure(excel_files)
        print(f"\n[結果]")
        print(f"  全ファイル一致: {result['is_valid']}")
        print(f"  基準列名: {result['column_names']}")
        print(f"  列数: {result['column_count']}")

        if not result['is_valid']:
            print(f"\n[不一致ファイル]")
            for error_file in result['error_files']:
                print(f"  - {Path(error_file).name}")

        for file_info in result['files']:
            status = "OK" if file_info['is_match'] else "NG"
            print(f"\n  [{status}] {Path(file_info['path']).name}")
            print(f"    列名: {file_info['column_names']}")
            print(f"    列数: {file_info['column_count']}")

    except Exception as e:
        print(f"[ERROR] {e}")


def test_multiple_csv_translation():
    """複数CSVファイルの一括翻訳テスト（1つのCSVにまとめて出力）"""
    print("\n" + "=" * 70)
    print("[テスト3] 複数CSV一括翻訳（1つのCSVに統合）")
    print("=" * 70)

    test_data_dir = Path(__file__).parent.parent / "test_data"

    # 同じ構造のファイルのみを選択（単一列のみ）
    csv_files = [
        str(test_data_dir / "test_words_single_column.csv")
    ]

    # テスト用に複数ファイルがない場合はスキップ
    if len(csv_files) < 2:
        print("\n[INFO] 複数のCSVファイルが必要です。")
        print("  同じ構造のCSVファイルを複数作成してから実行してください。")
        print("\n[想定される出力形式]")
        print("  CSV列: ファイル名, 元の日本語, 中間言語, 中間言語の翻訳, 日本語への逆翻訳, 完全一致")
        print("  全ファイルの翻訳結果が1つのCSVファイルにまとめられます")
        return

    try:
        result = translate_from_multiple_csv(
            file_paths=csv_files,
            column_index=0,
            intermediate_lang="en",
            check_structure=True
        )

        print(f"\n[処理結果]")
        print(f"  出力ファイル: {result['output_file']}")
        print(f"  総ファイル数: {result['total_files']}")
        print(f"  総翻訳件数: {result['total_count']}")
        print(f"  完全一致: {result['perfect_match_count']}件")
        print(f"  完全一致率: {result['perfect_match_rate']:.1f}%")
        print(f"  成功: {result['success_count']}ファイル")
        print(f"  エラー: {result['error_count']}ファイル")

        if result['errors']:
            print(f"\n[エラー詳細]")
            for error in result['errors']:
                print(f"  {Path(error['file']).name}: {error['error']}")

    except ValueError as e:
        print(f"\n[INFO] {e}")
    except Exception as e:
        print(f"\n[ERROR] {e}")


def test_multiple_excel_translation():
    """複数Excelファイルの一括翻訳テスト（1つのCSVにまとめて出力）"""
    print("\n" + "=" * 70)
    print("[テスト4] 複数Excel一括翻訳（1つのCSVに統合）")
    print("=" * 70)

    test_data_dir = Path(__file__).parent.parent / "test_data"

    # 同じ構造のファイルのみを選択（単一列のみ）
    excel_files = [
        str(test_data_dir / "test_words_single_column.xlsx")
    ]

    # テスト用に複数ファイルがない場合はスキップ
    if len(excel_files) < 2:
        print("\n[INFO] 複数のExcelファイルが必要です。")
        print("  同じ構造のExcelファイルを複数作成してから実行してください。")
        print("\n[想定される出力形式]")
        print("  CSV列: ファイル名, 元の日本語, 中間言語, 中間言語の翻訳, 日本語への逆翻訳, 完全一致")
        print("  全ファイルの翻訳結果が1つのCSVファイルにまとめられます")
        return

    try:
        result = translate_from_multiple_excel(
            file_paths=excel_files,
            column_index=0,
            intermediate_lang="en",
            check_structure=True
        )

        print(f"\n[処理結果]")
        print(f"  出力ファイル: {result['output_file']}")
        print(f"  総ファイル数: {result['total_files']}")
        print(f"  総翻訳件数: {result['total_count']}")
        print(f"  完全一致: {result['perfect_match_count']}件")
        print(f"  完全一致率: {result['perfect_match_rate']:.1f}%")
        print(f"  成功: {result['success_count']}ファイル")
        print(f"  エラー: {result['error_count']}ファイル")

        if result['errors']:
            print(f"\n[エラー詳細]")
            for error in result['errors']:
                print(f"  {Path(error['file']).name}: {error['error']}")

    except ValueError as e:
        print(f"\n[INFO] {e}")
    except Exception as e:
        print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("複数ファイル一括翻訳 テストプログラム")
    print("=" * 70)

    # テスト1: CSV列構造チェック
    test_csv_structure_check()

    # テスト2: Excel列構造チェック
    test_excel_structure_check()

    # テスト3: 複数CSV一括翻訳（実際の翻訳はIP制限により実行しない）
    # test_multiple_csv_translation()

    # テスト4: 複数Excel一括翻訳（実際の翻訳はIP制限により実行しない）
    # test_multiple_excel_translation()

    print("\n" + "=" * 70)
    print("テスト完了")
    print("=" * 70)
    print("\n[注意]")
    print("  実際の翻訳テスト（テスト3, 4）を実行する場合は、")
    print("  Google Cloud ConsoleでIPアドレスの制限を解除してから、")
    print("  該当のコメントアウトを解除してください。")
    print("=" * 70)
