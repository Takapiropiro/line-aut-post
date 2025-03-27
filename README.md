# LINE公式アカウント自動投稿システム利用マニュアル

## 概要

このシステムは、LINE公式アカウント「毎日1分Chat GPT新聞」用の自動投稿システムです。GitHub Actionsを使用して毎日21:00（日本時間）に自動的に投稿を行います。

## システム構成

- **line_auto_post.py**: メイン実行スクリプト
- **content.json**: 投稿内容を管理するJSONファイル
- **.github/workflows/line_auto_post.yml**: GitHub Actions設定ファイル

## セットアップ方法

### 1. GitHubリポジトリの作成

1. GitHubアカウントにログイン
2. 新しいリポジトリを作成（例: `line-auto-post`）
3. 以下のファイルをリポジトリにアップロード:
   - `line_auto_post.py`
   - `content.json`
   - `.github/workflows/line_auto_post.yml`

### 2. LINE Messaging APIの設定

1. [LINE Developers Console](https://developers.line.biz/console/)にログイン
2. 「毎日1分Chat GPT新聞」のチャネルを選択
3. 「Messaging API設定」タブを開く
4. 「チャネルアクセストークン（長期）」を発行

### 3. GitHubシークレットの設定

1. GitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」を開く
2. 「New repository secret」をクリック
3. 以下の情報を入力:
   - Name: `LINE_CHANNEL_ACCESS_TOKEN`
   - Secret: 発行したチャネルアクセストークン
4. 「Add secret」をクリック

## 投稿内容の管理

投稿内容は `content.json` ファイルで管理します。このファイルは以下の形式のJSONオブジェクトの配列です:

```json
[
  {
    "date": "YYYY-MM-DD",  // 特定の日付に投稿する場合（オプション）
    "text": "投稿するテキスト",
    "image_url": "画像のURL（オプション）"
  },
  ...
]
```

### 投稿内容の追加方法

1. GitHubリポジトリの `content.json` ファイルを開く
2. 「Edit」ボタンをクリック
3. 新しい投稿内容を追加
4. 「Commit changes」をクリック

### 日付指定について

- `date` フィールドを指定すると、その日付に投稿されます
- `date` フィールドを省略すると、配列内の順番に基づいて循環的に投稿されます

## 手動実行方法

自動スケジュール以外に手動で投稿を実行したい場合:

1. GitHubリポジトリの「Actions」タブを開く
2. 「LINE Auto Post」ワークフローを選択
3. 「Run workflow」ボタンをクリック
4. 「Run workflow」を再度クリックして実行

## トラブルシューティング

### 投稿が実行されない場合

1. GitHubリポジトリの「Actions」タブで実行ログを確認
2. チャネルアクセストークンが正しく設定されているか確認
3. `content.json` ファイルの形式が正しいか確認

### エラーメッセージの確認方法

1. GitHubリポジトリの「Actions」タブを開く
2. 失敗したワークフローをクリック
3. 「post」ジョブをクリック
4. 「Run auto post script」ステップを展開してエラーメッセージを確認

## 注意事項

- LINE Messaging APIの無料枠には1か月あたりの送信メッセージ数に制限があります
- 画像URLは公開されているURLである必要があります（GitHubのraw URLなども使用可能）
- チャネルアクセストークンは定期的に更新することをお勧めします

## サポート

問題が解決しない場合は、GitHubリポジトリのIssuesで質問してください。
