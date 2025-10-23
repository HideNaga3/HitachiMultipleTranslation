"""
Google Translation APIがサポートする言語一覧を取得してJSONに保存
"""
from translator import get_supported_languages
import json
from pathlib import Path
from datetime import datetime


def save_supported_languages():
    """
    サポート言語一覧を取得してJSONファイルに保存
    """
    print("=" * 60)
    print("Google Translation API サポート言語取得")
    print("=" * 60)
    print(f"\n開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        # 日本語表記で言語一覧を取得
        print("[INFO] 言語一覧を取得中（日本語表記）...")
        languages_ja = get_supported_languages(target_lang="ja")

        # 英語表記でも取得
        print("[INFO] 言語一覧を取得中（英語表記）...")
        languages_en = get_supported_languages(target_lang="en")

        # 言語コードをキーにして統合
        languages_dict = {}
        for lang_ja, lang_en in zip(languages_ja, languages_en):
            code = lang_ja["language"]
            languages_dict[code] = {
                "code": code,
                "name_ja": lang_ja["name"],
                "name_en": lang_en["name"]
            }

        # リスト形式に変換
        languages_list = list(languages_dict.values())

        # 言語コードでソート
        languages_list.sort(key=lambda x: x["code"])

        # 結果の概要
        total_count = len(languages_list)
        print(f"\n[INFO] 取得完了: {total_count}言語")

        # 最初の10言語を表示
        print("\n[サンプル] 最初の10言語:")
        print("-" * 60)
        for i, lang in enumerate(languages_list[:10], 1):
            print(f"{i:2d}. [{lang['code']:5s}] {lang['name_ja']:20s} ({lang['name_en']})")
        print(f"... 他 {total_count - 10}言語")
        print("-" * 60)

        # JSONファイルに保存
        output_dir = Path(__file__).parent.parent / "for_claude"
        output_dir.mkdir(exist_ok=True)

        json_file = output_dir / "supported_languages.json"

        json_data = {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_count": total_count,
            "languages": languages_list
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        print(f"\n[OK] JSON保存完了")
        print(f"保存先: {json_file}")
        print(f"言語数: {total_count}言語")
        print(f"終了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n[ERROR] エラーが発生しました: {e}")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = save_supported_languages()
    exit(0 if success else 1)
