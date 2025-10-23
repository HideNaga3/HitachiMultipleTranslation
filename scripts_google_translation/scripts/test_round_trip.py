"""
往復翻訳のテストスクリプト
日本語 → 他言語 → 日本語
"""
from translator import round_trip_translate, round_trip_translate_batch
import csv
from pathlib import Path
from datetime import datetime


def test_single_round_trip():
    """
    単一テキストの往復翻訳テスト
    """
    print("=" * 70)
    print("往復翻訳テスト（単一）")
    print("=" * 70)

    test_cases = [
        ("こんにちは", "en"),
        ("ありがとうございます", "en"),
        ("おはようございます", "fr"),
        ("さようなら", "de"),
        ("よろしくお願いします", "ko"),
    ]

    print("\n[テスト実行中...]\n")

    for text, lang in test_cases:
        try:
            result = round_trip_translate(text, lang)
            print(f"元の日本語: {result['original']}")
            print(f"  ↓ [{result['intermediate_lang']}]")
            print(f"{result['intermediate_lang']}翻訳: {result['intermediate_text']}")
            print(f"  ↓ [ja]")
            print(f"日本語訳: {result['back_translation']}")
            print("-" * 70)
        except Exception as e:
            print(f"[ERROR] {text} の翻訳に失敗: {e}")
            print("-" * 70)

    print("=" * 70)


def test_batch_round_trip():
    """
    複数テキストの往復翻訳テスト（CSV出力）
    """
    print("\n" + "=" * 70)
    print("往復翻訳テスト（一括処理）")
    print("=" * 70)

    # テスト用の日本語テキスト
    japanese_texts = [
        "平和",
        "希望",
        "未来",
        "勇気",
        "友情",
        "愛情",
        "自由",
        "正義",
        "幸福",
        "知恵"
    ]

    # テストする言語
    test_languages = ["en", "zh-CN", "ko", "fr", "de"]

    print(f"\n日本語テキスト数: {len(japanese_texts)}")
    print(f"テスト言語: {', '.join(test_languages)}")
    print(f"\n[翻訳実行中...]\n")

    all_results = []

    for lang in test_languages:
        try:
            print(f"処理中: 日本語 → {lang} → 日本語")
            results = round_trip_translate_batch(japanese_texts, lang)

            for result in results:
                all_results.append({
                    "元の日本語": result["original"],
                    "中間言語": result["intermediate_lang"],
                    "中間言語の翻訳": result["intermediate_text"],
                    "日本語への逆翻訳": result["back_translation"]
                })

            print(f"  [OK] {len(results)}件の翻訳完了")

        except Exception as e:
            print(f"  [ERROR] {lang} での翻訳に失敗: {e}")

    # 結果のサンプル表示
    print("\n" + "-" * 70)
    print("[結果サンプル] 最初の5件")
    print("-" * 70)
    for i, result in enumerate(all_results[:5], 1):
        print(f"{i}. {result['元の日本語']} "
              f"→ [{result['中間言語']}] {result['中間言語の翻訳']} "
              f"→ [ja] {result['日本語への逆翻訳']}")

    # CSV出力
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = output_dir / f"round_trip_test_{timestamp}.csv"

    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ["元の日本語", "中間言語", "中間言語の翻訳", "日本語への逆翻訳"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print("-" * 70)
    print(f"\n[OK] 往復翻訳テスト完了")
    print(f"処理件数: {len(all_results)}件")
    print(f"CSV出力: {csv_file}")
    print(f"終了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


if __name__ == "__main__":
    # 単一テスト
    test_single_round_trip()

    # 一括テスト
    test_batch_round_trip()
