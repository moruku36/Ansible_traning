# Ansible学習用リポジトリ

このリポジトリは、Ansibleの学習を目的として作成された例題集です。段階的にAnsibleの機能を学べるように構成されています。

## 前提条件

- Ansible 2.9以上がインストールされていること
- macOS/Linux環境（Windowsの場合はWSL推奨）

## ファイル構成

### 基本例題
- `01-basic-file-operations.yaml` - 基本的なファイル操作
- `02-conditions-and-loops.yaml` - 条件分岐とループ
- `03-handlers-and-error-handling.yaml` - ハンドラーとエラー処理
- `04-templates-and-variables.yaml` - テンプレートと変数

### ロール例題
- `05-roles-example.yaml` - ロールを使用した構成管理
- `roles/` - ロールディレクトリ
  - `common/` - 共通設定ロール
  - `webserver/` - Webサーバーロール

### 実践例題
- `06-docker-environment.yaml` - Docker環境の構築

### テンプレート
- `templates/` - Jinja2テンプレートファイル

## 学習順序

### 1. 基本概念の理解
```bash
# 基本的なファイル操作
ansible-playbook -i hosts.ini 01-basic-file-operations.yaml

# 条件分岐とループ
ansible-playbook -i hosts.ini 02-conditions-and-loops.yaml

# ハンドラーとエラー処理
ansible-playbook -i hosts.ini 03-handlers-and-error-handling.yaml
```

### 2. テンプレートと変数
```bash
# テンプレートと変数の使用
ansible-playbook -i hosts.ini 04-templates-and-variables.yaml
```

### 3. ロールの理解
```bash
# ロールを使用した構成管理
ansible-playbook -i hosts.ini 05-roles-example.yaml
```

### 4. 実践的な例題
```bash
# Docker環境の構築（注意：管理者権限が必要）
sudo ansible-playbook -i hosts.ini 06-docker-environment.yaml
```

## 学習のポイント

### 各例題で学べること

#### 01-basic-file-operations.yaml
- `file`モジュールによるディレクトリ作成
- `copy`モジュールによるファイル作成
- `stat`モジュールによるファイル情報取得
- `slurp`モジュールによるファイル内容読み取り
- `debug`モジュールによる情報表示

#### 02-conditions-and-loops.yaml
- `when`条件による条件分岐
- `loop`による繰り返し処理
- 変数の定義と使用
- 複雑な条件式

#### 03-handlers-and-error-handling.yaml
- `notify`によるハンドラー呼び出し
- `ignore_errors`によるエラー無視
- `block`/`rescue`/`always`によるエラー処理
- `fail`モジュールによる意図的な失敗

#### 04-templates-and-variables.yaml
- Jinja2テンプレートの使用
- 複雑な変数構造
- テンプレート内でのループと条件分岐

#### 05-roles-example.yaml
- ロールの構造と使用方法
- ロール間の依存関係
- ハンドラーの定義

#### 06-docker-environment.yaml
- 実践的なアプリケーションデプロイ
- Dockerとの連携
- 複雑なタスクの組み合わせ

## 実行時の注意点

1. **権限**: 一部の例題は管理者権限が必要です
2. **環境依存**: macOSとLinuxで動作が異なる場合があります
3. **ネットワーク**: Docker例題はインターネット接続が必要です

## トラブルシューティング

### よくある問題

1. **権限エラー**
   ```bash
   sudo ansible-playbook -i hosts.ini [プレイブック名]
   ```

2. **モジュールが見つからない**
   ```bash
   pip install ansible[all]
   ```

3. **テンプレートエラー**
   - テンプレートファイルの構文を確認
   - 変数名のスペルを確認

## 次のステップ

この例題を理解した後は、以下のような実践的なプロジェクトに挑戦してみてください：

1. 本格的なWebアプリケーションのデプロイ
2. 複数サーバー環境の構築
3. CI/CDパイプラインとの連携
4. クラウド環境でのAnsible活用

## 参考資料

- [Ansible公式ドキュメント](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Jinja2テンプレート](https://jinja.palletsprojects.com/)
