import os
import json
import requests

def test_line_message_api():
    """
    LINE Messaging APIの動作確認テスト
    
    注意: このテストは実際にLINEにメッセージを送信します
    テスト用のチャネルアクセストークンを使用するか、
    本番環境で実行する場合は注意してください
    """
    print("LINE Messaging APIテストを開始します...")
    
    # 環境変数からチャネルアクセストークンを取得
    channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    if not channel_access_token:
        print("エラー: LINE_CHANNEL_ACCESS_TOKENが設定されていません")
        print("テスト方法: export LINE_CHANNEL_ACCESS_TOKEN='あなたのトークン' を実行してから再度テストしてください")
        return False
    
    # テスト用メッセージ
    test_message = {
        "type": "text",
        "text": "【テスト】これは自動投稿システムのテストメッセージです。"
    }
    
    # APIリクエスト
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'
    }
    data = {
        "messages": [test_message]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        # レスポンスの確認
        if response.status_code == 200:
            print("✅ テストメッセージの送信に成功しました")
            return True
        else:
            print(f"❌ テストメッセージの送信に失敗しました: ステータスコード {response.status_code}")
            print(f"エラー詳細: {response.text}")
            return False
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        return False

def test_content_json_format():
    """
    content.jsonファイルの形式をテスト
    """
    print("content.jsonファイルのテストを開始します...")
    
    try:
        with open('content.json', 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        if not isinstance(content, list):
            print("❌ content.jsonはリスト形式である必要があります")
            return False
            
        if len(content) == 0:
            print("❌ content.jsonに投稿内容が含まれていません")
            return False
            
        # 各投稿内容の検証
        for i, item in enumerate(content):
            if not isinstance(item, dict):
                print(f"❌ 投稿アイテム {i+1} はオブジェクト形式である必要があります")
                return False
                
            if 'text' not in item:
                print(f"❌ 投稿アイテム {i+1} に 'text' フィールドがありません")
                return False
                
            if 'date' in item:
                # 日付形式の検証 (YYYY-MM-DD)
                date = item['date']
                if not isinstance(date, str) or len(date) != 10 or date[4] != '-' or date[7] != '-':
                    print(f"❌ 投稿アイテム {i+1} の日付形式が不正です: {date}")
                    print("日付は 'YYYY-MM-DD' 形式である必要があります")
                    return False
        
        print(f"✅ content.jsonの検証に成功しました: {len(content)}件の投稿内容を確認")
        return True
        
    except FileNotFoundError:
        print("❌ content.jsonファイルが見つかりません")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ content.jsonの解析に失敗しました: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {str(e)}")
        return False

def test_main_script():
    """
    メインスクリプト (line_auto_post.py) の動作テスト
    """
    print("line_auto_post.pyのテストを開始します...")
    
    try:
        # スクリプトのインポートテスト
        import line_auto_post
        
        # 関数の存在確認
        required_functions = ['load_content', 'get_todays_content', 'main']
        for func in required_functions:
            if not hasattr(line_auto_post, func):
                print(f"❌ line_auto_post.py に必要な関数 '{func}' が見つかりません")
                return False
        
        # LineMessagingAPIクラスの確認
        if not hasattr(line_auto_post, 'LineMessagingAPI'):
            print("❌ line_auto_post.py に 'LineMessagingAPI' クラスが見つかりません")
            return False
            
        print("✅ line_auto_post.pyの検証に成功しました")
        return True
        
    except ImportError:
        print("❌ line_auto_post.pyのインポートに失敗しました")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {str(e)}")
        return False

def run_all_tests():
    """
    全てのテストを実行
    """
    print("=== LINE自動投稿システムテスト開始 ===")
    
    tests = [
        ("メインスクリプトのテスト", test_main_script),
        ("投稿内容JSONのテスト", test_content_json_format),
        ("LINE Messaging APIテスト", test_line_message_api)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        result = test_func()
        results.append((name, result))
    
    print("\n=== テスト結果サマリー ===")
    all_passed = True
    for name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 全てのテストに合格しました！")
    else:
        print("\n⚠️ 一部のテストに失敗しました。上記のエラーメッセージを確認してください。")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
