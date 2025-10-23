"""
一括翻訳機能のテストスクリプト
CSV/Excelファイルからの読み込みと翻訳をテスト
"""
from pathlib import Path
from batch_translator import translate_from_csv, translate_from_excel
from datetime import datetime


def test_csv_translation():
    """
    CSVファイルからの翻訳テスト
    """
    print("=" * 70)
    print("CSVファイル翻訳テスト")
    print("=" * 70)

    test_dir = Path(__file__).parent.parent / "test_data"

    # テスト1: 単一列のCSV（列インデックス0）
    print("\n[テスト1] 単一列CSV（列インデックス=0）")
    csv_file1 = test_dir / "test_words_single_column.csv"
    if csv_file1.exists():
        try:
            result = translate_from_csv(
                input_file=str(csv_file1),
                column_index=0,
                intermediate_lang="en"
            )
            print(f"  入力ファイル: {result['input_file']}")
            print(f"  出力ファイル: {result['output_file']}")
            print(f"  処理件数: {result['total_count']}件")
            print(f"  完全一致: {result['perfect_match_count']}件 ({result['perfect_match_rate']:.1f}%)")
            print("  [OK] テスト完了")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print(f"  [SKIP] テストファイルが見つかりません: {csv_file1}")

    # テスト2: 複数列のCSV（列インデックス2）
    print("\n[テスト2] 複数列CSV（列インデックス=2）")
    csv_file2 = test_dir / "test_words_multi_column.csv"
    if csv_file2.exists():
        try:
            result = translate_from_csv(
                input_file=str(csv_file2),
                column_index=2,
                intermediate_lang="en"
            )
            print(f"  入力ファイル: {result['input_file']}")
            print(f"  出力ファイル: {result['output_file']}")
            print(f"  処理件数: {result['total_count']}件")
            print(f"  完全一致: {result['perfect_match_count']}件 ({result['perfect_match_rate']:.1f}%)")
            print("  [OK] テスト完了")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print(f"  [SKIP] テストファイルが見つかりません: {csv_file2}")

    print("\n" + "=" * 70)


def test_excel_translation():
    """
    Excelファイルからの翻訳テスト
    """
    print("\n" + "=" * 70)
    print("Excelファイル翻訳テスト")
    print("=" * 70)

    test_dir = Path(__file__).parent.parent / "test_data"

    # テスト1: 単一列のExcel（列インデックス0）
    print("\n[テスト1] 単一列Excel（列インデックス=0）")
    excel_file1 = test_dir / "test_words_single_column.xlsx"
    if excel_file1.exists():
        try:
            result = translate_from_excel(
                input_file=str(excel_file1),
                column_index=0,
                intermediate_lang="en"
            )
            print(f"  入力ファイル: {result['input_file']}")
            print(f"  出力ファイル: {result['output_file']}")
            print(f"  処理件数: {result['total_count']}件")
            print(f"  完全一致: {result['perfect_match_count']}件 ({result['perfect_match_rate']:.1f}%)")
            print("  [OK] テスト完了")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print(f"  [SKIP] テストファイルが見つかりません: {excel_file1}")

    # テスト2: 複数列のExcel（列インデックス2）
    print("\n[テスト2] 複数列Excel（列インデックス=2）")
    excel_file2 = test_dir / "test_words_multi_column.xlsx"
    if excel_file2.exists():
        try:
            result = translate_from_excel(
                input_file=str(excel_file2),
                column_index=2,
                intermediate_lang="en"
            )
            print(f"  入力ファイル: {result['input_file']}")
            print(f"  出力ファイル: {result['output_file']}")
            print(f"  処理件数: {result['total_count']}件")
            print(f"  完全一致: {result['perfect_match_count']}件 ({result['perfect_match_rate']:.1f}%)")
            print("  [OK] テスト完了")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print(f"  [SKIP] テストファイルが見つかりません: {excel_file2}")

    # テスト3: 複数シートのExcel（シート指定）
    print("\n[テスト3] 複数シートExcel（シート指定='価値観'、列インデックス=0）")
    excel_file3 = test_dir / "test_words_multi_sheet.xlsx"
    if excel_file3.exists():
        try:
            result = translate_from_excel(
                input_file=str(excel_file3),
                column_index=0,
                intermediate_lang="en",
                sheet_name="価値観"
            )
            print(f"  入力ファイル: {result['input_file']}")
            print(f"  出力ファイル: {result['output_file']}")
            print(f"  処理件数: {result['total_count']}件")
            print(f"  完全一致: {result['perfect_match_count']}件 ({result['perfect_match_rate']:.1f}%)")
            print("  [OK] テスト完了")
        except Exception as e:
            print(f"  [ERROR] {e}")
    else:
        print(f"  [SKIP] テストファイルが見つかりません: {excel_file3}")

    print("\n" + "=" * 70)


def test_different_languages():
    """
    異なる中間言語でのテスト
    """
    print("\n" + "=" * 70)
    print("複数言語での翻訳テスト")
    print("=" * 70)

    test_dir = Path(__file__).parent.parent / "test_data"
    csv_file = test_dir / "test_words_single_column.csv"

    if not csv_file.exists():
        print(f"  [SKIP] テストファイルが見つかりません: {csv_file}")
        return

    test_languages = [
        ("en", "英語"),
        ("zh-CN", "中国語（簡体字）"),
        ("ko", "韓国語"),
        ("fr", "フランス語"),
        ("de", "ドイツ語")
    ]

    for lang_code, lang_name in test_languages:
        print(f"\n[テスト] 中間言語: {lang_name} ({lang_code})")
        try:
            result = translate_from_csv(
                input_file=str(csv_file),
                column_index=0,
                intermediate_lang=lang_code
            )
            print(f"  出力ファイル: {Path(result['output_file']).name}")
            print(f"  処理件数: {result['total_count']}件")
            print(f"  完全一致: {result['perfect_match_count']}件 ({result['perfect_match_rate']:.1f}%)")
            print("  [OK] テスト完了")
        except Exception as e:
            print(f"  [ERROR] {e}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    start_time = datetime.now()

    print("\n" + "=" * 70)
    print("一括翻訳機能 - 総合テスト")
    print("=" * 70)
    print(f"開始時刻: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # CSVテスト
    test_csv_translation()

    # Excelテスト
    test_excel_translation()

    # 複数言語テスト
    test_different_languages()

    end_time = datetime.now()
    elapsed = end_time - start_time

    print("\n" + "=" * 70)
    print("[OK] すべてのテストが完了しました")
    print("=" * 70)
    print(f"終了時刻: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"実行時間: {elapsed.total_seconds():.1f}秒")
    print("=" * 70)
