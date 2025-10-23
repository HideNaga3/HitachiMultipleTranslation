"""
Google Translation API接続確認スクリプト
APIキーの有効性とIP制限をチェック
"""
import requests
from dotenv import load_dotenv
import os
from datetime import datetime


def check_api_connection():
    """
    Google Translation APIの接続確認を行う

    Returns:
        bool: 接続成功の場合True、失敗の場合False
    """
    print("=" * 60)
    print("Google Translation API 接続確認")
    print("=" * 60)
    print(f"\n確認開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 環境変数読み込み
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("[ERROR] GOOGLE_API_KEYが.envファイルに設定されていません")
        return False

    print(f"[INFO] APIキーを読み込みました（長さ: {len(api_key)}文字）")

    # 簡単な翻訳テスト（1単語のみ）
    print("\n[TEST] 翻訳テスト実行中...")
    print("       テスト単語: 'test' → 日本語\n")

    base_url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "key": api_key,
        "q": "test",
        "target": "ja",
        "format": "text"
    }

    try:
        response = requests.post(base_url, params=params, timeout=10)

        print(f"[INFO] HTTPステータスコード: {response.status_code}")

        if response.status_code == 200:
            # 成功
            data = response.json()
            translation = data["data"]["translations"][0]["translatedText"]

            print("\n" + "-" * 60)
            print("[SUCCESS] API接続成功")
            print("-" * 60)
            print(f"翻訳結果: 'test' → '{translation}'")
            print("-" * 60)
            print("\n[OK] Google Translation APIは正常に動作しています")
            print("=" * 60)
            return True

        elif response.status_code == 403:
            # IP制限エラー
            try:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message", "不明なエラー")

                print("\n" + "-" * 60)
                print("[ERROR] API接続失敗（403 Forbidden）")
                print("-" * 60)
                print(f"エラー内容: {error_message}")
                print("-" * 60)

                if "IP address restriction" in error_message:
                    print("\n[原因] APIキーにIP制限が設定されています")
                    print("\n[対処方法]")
                    print("1. Google Cloud Console にアクセス")
                    print("   https://console.cloud.google.com/")
                    print("2. [APIとサービス] → [認証情報] を開く")
                    print("3. 該当のAPIキーを選択")
                    print("4. [アプリケーションの制限] で以下のいずれかを実施:")
                    print("   - IP制限を解除する")
                    print("   - 現在のIPアドレスを許可リストに追加する")
                elif "API key not valid" in error_message:
                    print("\n[原因] APIキーが無効です")
                    print("\n[対処方法]")
                    print("1. APIキーが正しいか確認")
                    print("2. Translation APIが有効化されているか確認")
                else:
                    print("\n[原因] アクセスが拒否されました")

            except Exception as e:
                print(f"\n[ERROR] エラー詳細の解析に失敗: {e}")

            print("=" * 60)
            return False

        elif response.status_code == 400:
            # リクエストエラー
            try:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message", "不明なエラー")

                print("\n" + "-" * 60)
                print("[ERROR] API接続失敗（400 Bad Request）")
                print("-" * 60)
                print(f"エラー内容: {error_message}")
                print("-" * 60)
                print("\n[原因] リクエストパラメータが不正です")
                print("=" * 60)

            except Exception as e:
                print(f"\n[ERROR] エラー詳細の解析に失敗: {e}")

            return False

        else:
            # その他のエラー
            print("\n" + "-" * 60)
            print(f"[ERROR] API接続失敗（ステータスコード: {response.status_code}）")
            print("-" * 60)

            try:
                error_data = response.json()
                print(f"エラー詳細: {error_data}")
            except:
                print(f"レスポンス: {response.text[:200]}")

            print("=" * 60)
            return False

    except requests.exceptions.Timeout:
        print("\n[ERROR] タイムアウトエラー")
        print("       APIサーバーへの接続がタイムアウトしました")
        print("=" * 60)
        return False

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] 接続エラー")
        print("       インターネット接続を確認してください")
        print("=" * 60)
        return False

    except Exception as e:
        print("\n[ERROR] 予期しないエラーが発生しました")
        print(f"       {type(e).__name__}: {e}")
        print("=" * 60)
        return False


def get_current_ip():
    """
    現在のグローバルIPアドレスを取得
    """
    print("\n" + "=" * 60)
    print("現在のIPアドレス確認")
    print("=" * 60)

    try:
        # IPv4アドレス取得
        print("\n[INFO] IPv4アドレスを取得中...")
        response_v4 = requests.get("https://api.ipify.org?format=json", timeout=5)
        if response_v4.status_code == 200:
            ipv4 = response_v4.json().get("ip")
            print(f"[IPv4] {ipv4}")
        else:
            print("[IPv4] 取得失敗")
    except Exception as e:
        print(f"[IPv4] 取得エラー: {e}")

    try:
        # IPv6アドレス取得
        print("\n[INFO] IPv6アドレスを取得中...")
        response_v6 = requests.get("https://api64.ipify.org?format=json", timeout=5)
        if response_v6.status_code == 200:
            ipv6 = response_v6.json().get("ip")
            print(f"[IPv6] {ipv6}")
        else:
            print("[IPv6] 取得失敗")
    except Exception as e:
        print(f"[IPv6] 取得エラー: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # IPアドレス確認
    get_current_ip()

    # API接続確認
    print("\n")
    success = check_api_connection()

    # 終了コード
    exit(0 if success else 1)
