"""
複数CSVファイル一括翻訳の実行テスト
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from batch_translator import translate_from_multiple_csv


if __name__ == "__main__":
    print("=" * 70)
    print("複数CSV一括翻訳テスト")
    print("=" * 70)

    test_data_dir = Path(__file__).parent.parent / "test_data"

    # テスト用CSVファイル
    csv_files = [
        str(test_data_dir / "emotions.csv"),
        str(test_data_dir / "nature.csv"),
        str(test_data_dir / "colors.csv")
    ]

    print(f"\n[対象ファイル]")
    for f in csv_files:
        print(f"  - {Path(f).name}")

    print("\n[翻訳開始]")
    try:
        result = translate_from_multiple_csv(
            file_paths=csv_files,
            column_index=0,
            intermediate_lang="en",
            check_structure=True
        )

        print("\n" + "=" * 70)
        print("[処理結果]")
        print("=" * 70)
        print(f"出力ファイル: {result['output_file']}")
        print(f"総ファイル数: {result['total_files']}")
        print(f"総翻訳件数: {result['total_count']}")
        print(f"完全一致: {result['perfect_match_count']}件 ({result['perfect_match_rate']:.1f}%)")
        print(f"成功: {result['success_count']}ファイル")
        print(f"エラー: {result['error_count']}ファイル")

        if result['errors']:
            print(f"\n[エラー詳細]")
            for error in result['errors']:
                print(f"  {Path(error['file']).name}: {error['error']}")

        print("=" * 70)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
