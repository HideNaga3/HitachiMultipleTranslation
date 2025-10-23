"""
Google Cloud Translation APIを使用した翻訳スクリプト
REST API版（APIキー認証）
"""
import requests
from dotenv import load_dotenv
import os
from typing import Optional


# .envファイルから環境変数を読み込み
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
BASE_URL = "https://translation.googleapis.com/language/translate/v2"


def translate_words(words: list[str], source_lang: Optional[str] = None, target_lang: str = "ja") -> list[str]:
    """
    複数単語をまとめて翻訳

    Args:
        words (list[str]): 翻訳する単語のリスト
        source_lang (str): ソース言語コード（Noneの場合は自動検出）
        target_lang (str): ターゲット言語コード（デフォルト: "ja"）

    Returns:
        list[str]: 翻訳結果のリスト

    Raises:
        Exception: 翻訳APIエラー

    例:
        # 英語から日本語
        translate_words(["hello", "world"], source_lang="en", target_lang="ja")

        # 日本語から英語
        translate_words(["こんにちは", "世界"], source_lang="ja", target_lang="en")

        # 自動検出
        translate_words(["hello", "world"], target_lang="ja")
    """
    if not words:
        return []

    try:
        params = {
            "key": API_KEY,
            "q": words,
            "target": target_lang,
            "format": "text"
        }
        if source_lang:
            params["source"] = source_lang

        response = requests.post(BASE_URL, params=params)

        if response.status_code != 200:
            error_msg = f"APIエラー: ステータスコード {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg += f" - {error_data['error'].get('message', '不明なエラー')}"
            except:
                pass
            raise Exception(error_msg)

        data = response.json()
        translations = data["data"]["translations"]
        return [t["translatedText"] for t in translations]
    except requests.exceptions.RequestException as e:
        raise Exception(f"翻訳エラー: 通信エラーが発生しました")
    except KeyError as e:
        raise Exception(f"翻訳エラー: レスポンスの形式が不正です")
    except Exception as e:
        if "APIエラー" in str(e):
            raise
        raise Exception(f"翻訳エラー: {str(e)}")


def translate_text(text: str, source_lang: Optional[str] = None, target_lang: str = "ja") -> str:
    """
    単一テキストを翻訳

    Args:
        text (str): 翻訳するテキスト
        source_lang (str): ソース言語コード（Noneの場合は自動検出）
        target_lang (str): ターゲット言語コード（デフォルト: "ja"）

    Returns:
        str: 翻訳結果

    Raises:
        Exception: 翻訳APIエラー

    例:
        # 英語から日本語
        translate_text("Hello", source_lang="en", target_lang="ja")

        # 日本語から英語
        translate_text("こんにちは", source_lang="ja", target_lang="en")

        # 自動検出
        translate_text("Hello", target_lang="ja")
    """
    if not text:
        return ""

    # translate_wordsを利用
    results = translate_words([text], source_lang=source_lang, target_lang=target_lang)
    return results[0] if results else ""


def detect_language(text: str) -> dict:
    """
    テキストの言語を検出

    Args:
        text (str): 検出対象のテキスト

    Returns:
        dict: 言語情報（language, confidence）

    Raises:
        Exception: 言語検出エラー
    """
    if not text:
        return {"language": None, "confidence": 0}

    try:
        detect_url = f"{BASE_URL}/detect"
        params = {
            "key": API_KEY,
            "q": text
        }
        response = requests.post(detect_url, params=params)
        response.raise_for_status()

        data = response.json()
        detection = data["data"]["detections"][0][0]
        return {
            "language": detection["language"],
            "confidence": detection["confidence"]
        }
    except Exception as e:
        raise Exception(f"言語検出エラー: {e}")


def round_trip_translate(text: str, intermediate_lang: str = "en") -> dict:
    """
    往復翻訳を実行（日本語→他言語→日本語）

    日本語のテキストを指定した言語に翻訳し、それを再度日本語に戻します。
    翻訳の精度確認や、他言語でどのように表現されるかを確認するために使用します。

    Args:
        text (str): 翻訳する日本語テキスト
        intermediate_lang (str): 中間言語コード（デフォルト: "en"）

    Returns:
        dict: 翻訳結果
            {
                "original": 元の日本語,
                "intermediate_lang": 中間言語コード,
                "intermediate_text": 中間言語の翻訳,
                "back_translation": 日本語に戻した翻訳,
                "is_perfect_match": 完全一致フラグ（True/False）
            }

    Raises:
        Exception: 翻訳APIエラー

    例:
        # 日本語→英語→日本語
        result = round_trip_translate("こんにちは", "en")
        print(result["intermediate_text"])  # Hello
        print(result["back_translation"])   # こんにちは
        print(result["is_perfect_match"])   # True/False

        # 日本語→中国語→日本語
        result = round_trip_translate("ありがとう", "zh-CN")
    """
    if not text:
        return {
            "original": "",
            "intermediate_lang": intermediate_lang,
            "intermediate_text": "",
            "back_translation": "",
            "is_perfect_match": False
        }

    try:
        # ステップ1: 日本語 → 中間言語
        intermediate_text = translate_text(text, source_lang="ja", target_lang=intermediate_lang)

        # ステップ2: 中間言語 → 日本語
        back_translation = translate_text(intermediate_text, source_lang=intermediate_lang, target_lang="ja")

        # 完全一致判定
        is_perfect_match = (text == back_translation)

        return {
            "original": text,
            "intermediate_lang": intermediate_lang,
            "intermediate_text": intermediate_text,
            "back_translation": back_translation,
            "is_perfect_match": is_perfect_match
        }

    except Exception as e:
        raise Exception(f"往復翻訳エラー: {e}")


def round_trip_translate_batch(texts: list[str], intermediate_lang: str = "en") -> list[dict]:
    """
    複数テキストの往復翻訳を実行（日本語→他言語→日本語）

    Args:
        texts (list[str]): 翻訳する日本語テキストのリスト
        intermediate_lang (str): 中間言語コード（デフォルト: "en"）

    Returns:
        list[dict]: 翻訳結果のリスト（各要素にis_perfect_matchを含む）

    Raises:
        Exception: 翻訳APIエラー

    例:
        texts = ["こんにちは", "ありがとう", "さようなら"]
        results = round_trip_translate_batch(texts, "en")
    """
    if not texts:
        return []

    try:
        # ステップ1: 日本語 → 中間言語（一括）
        intermediate_texts = translate_words(texts, source_lang="ja", target_lang=intermediate_lang)

        # ステップ2: 中間言語 → 日本語（一括）
        back_translations = translate_words(intermediate_texts, source_lang=intermediate_lang, target_lang="ja")

        # 結果を整形
        results = []
        for original, intermediate, back in zip(texts, intermediate_texts, back_translations):
            is_perfect_match = (original == back)
            results.append({
                "original": original,
                "intermediate_lang": intermediate_lang,
                "intermediate_text": intermediate,
                "back_translation": back,
                "is_perfect_match": is_perfect_match
            })

        return results

    except Exception as e:
        raise Exception(f"往復翻訳エラー: {e}")


def get_supported_languages(target_lang: str = "ja") -> list[dict]:
    """
    サポートされている言語の一覧を取得

    Args:
        target_lang (str): 表示言語コード（デフォルト: "ja"）

    Returns:
        list[dict]: 言語情報のリスト（language, name）

    Raises:
        Exception: API呼び出しエラー
    """
    try:
        languages_url = f"{BASE_URL}/languages"
        params = {
            "key": API_KEY,
            "target": target_lang
        }
        response = requests.get(languages_url, params=params)
        response.raise_for_status()

        data = response.json()
        return [
            {"language": lang["language"], "name": lang["name"]}
            for lang in data["data"]["languages"]
        ]
    except Exception as e:
        raise Exception(f"言語一覧取得エラー: {e}")


if __name__ == "__main__":
    # テスト実行
    print("=" * 50)
    print("Google Translation API テスト")
    print("=" * 50)

    # 複数単語の翻訳テスト（英日）
    print("\n[テスト1] 複数単語の翻訳（英語→日本語）")
    words = ["strength", "peace", "future", "hope"]
    try:
        translations = translate_words(words, source_lang="en", target_lang="ja")
        for src, dst in zip(words, translations):
            print(f"{src} → {dst}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # 複数単語の翻訳テスト（日英）
    print("\n[テスト2] 複数単語の翻訳（日本語→英語）")
    words_ja = ["強さ", "平和", "未来", "希望"]
    try:
        translations = translate_words(words_ja, source_lang="ja", target_lang="en")
        for src, dst in zip(words_ja, translations):
            print(f"{src} → {dst}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # 単一テキストの翻訳テスト（英日）
    print("\n[テスト3] 単一テキストの翻訳（英語→日本語）")
    try:
        text = "Hello, how are you?"
        result = translate_text(text, source_lang="en", target_lang="ja")
        print(f"{text} → {result}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # 単一テキストの翻訳テスト（日英）
    print("\n[テスト4] 単一テキストの翻訳（日本語→英語）")
    try:
        text = "こんにちは、お元気ですか？"
        result = translate_text(text, source_lang="ja", target_lang="en")
        print(f"{text} → {result}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # 言語検出テスト
    print("\n[テスト5] 言語検出")
    try:
        text = "こんにちは"
        lang_info = detect_language(text)
        print(f"テキスト: {text}")
        print(f"検出言語: {lang_info['language']}")
        print(f"信頼度: {lang_info['confidence']:.2f}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # サポート言語一覧（最初の10件のみ表示）
    print("\n[テスト6] サポートされている言語（最初の10件）")
    try:
        languages = get_supported_languages("ja")
        for i, lang in enumerate(languages[:10]):
            print(f"{lang['language']}: {lang['name']}")
        print(f"... 合計 {len(languages)} 言語")
    except Exception as e:
        print(f"[ERROR] {e}")

    print("\n" + "=" * 50)
    print("テスト完了")
    print("=" * 50)
