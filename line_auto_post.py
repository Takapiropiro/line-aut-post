import os
import requests
import json
from datetime import datetime, timedelta

class LineMessagingAPI:
    """LINE Messaging APIを使用してメッセージを送信するクラス"""
    
    def __init__(self, channel_access_token):
        """
        初期化
        
        Args:
            channel_access_token (str): LINE Messaging APIのチャネルアクセストークン
        """
        self.channel_access_token = channel_access_token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {channel_access_token}'
        }
        self.base_url = 'https://api.line.me/v2/bot/message'
    
    def broadcast_message(self, messages):
        """
        全ての友だちにメッセージをブロードキャスト
        
        Args:
            messages (list): 送信するメッセージのリスト
            
        Returns:
            dict: APIレスポンス
        """
        url = f"{self.base_url}/broadcast"
        data = {
            "messages": messages
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json() if response.text else {"status": response.status_code}
    
    def create_text_message(self, text):
        """
        テキストメッセージを作成
        
        Args:
            text (str): 送信するテキスト
            
        Returns:
            dict: テキストメッセージオブジェクト
        """
        return {
            "type": "text",
            "text": text
        }
    
    def create_image_message(self, image_url, preview_url=None):
        """
        画像メッセージを作成
        
        Args:
            image_url (str): 画像のURL
            preview_url (str, optional): プレビュー画像のURL
            
        Returns:
            dict: 画像メッセージオブジェクト
        """
        if preview_url is None:
            preview_url = image_url
            
        return {
            "type": "image",
            "originalContentUrl": image_url,
            "previewImageUrl": preview_url
        }

def load_content(file_path):
    """
    投稿内容をJSONファイルから読み込む
    
    Args:
        file_path (str): JSONファイルのパス
        
    Returns:
        list: 投稿内容のリスト
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"JSONの解析に失敗しました: {file_path}")
        return []

def get_todays_content(content_list):
    """
    今日の投稿内容を取得
    
    Args:
        content_list (list): 投稿内容のリスト
        
    Returns:
        dict: 今日の投稿内容
    """
    # 現在の日付を取得
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 日付に対応する投稿内容を探す
    for content in content_list:
        if content.get('date') == today:
            return content
    
    # 日付指定がない場合は、インデックスを使用
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(content_list)
    return content_list[index]

def main():
    """メイン関数"""
    # 環境変数からチャネルアクセストークンを取得
    channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    if not channel_access_token:
        print("エラー: LINE_CHANNEL_ACCESS_TOKENが設定されていません")
        return
    
    # 投稿内容を読み込む
    content_list = load_content('content.json')
    if not content_list:
        print("エラー: 投稿内容が読み込めませんでした")
        return
    
    # 今日の投稿内容を取得
    todays_content = get_todays_content(content_list)
    
    # LINE Messaging APIクライアントを初期化
    line_client = LineMessagingAPI(channel_access_token)
    
    # メッセージを作成
    messages = []
    
    # テキストメッセージを追加
    if 'text' in todays_content:
        messages.append(line_client.create_text_message(todays_content['text']))
    
    # 画像メッセージを追加
    if 'image_url' in todays_content:
        messages.append(line_client.create_image_message(todays_content['image_url']))
    
    # メッセージを送信
    if messages:
        response = line_client.broadcast_message(messages)
        print(f"送信結果: {response}")
    else:
        print("送信するメッセージがありません")

if __name__ == "__main__":
    main()
