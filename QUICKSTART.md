# Ansible学習クイックスタートガイド

このガイドでは、Ansibleの学習を始めるための最短経路をご案内します。

## 1. 環境準備

### Ansibleのインストール確認
```bash
ansible --version
```

### インストールされていない場合
```bash
# macOS
brew install ansible

# Ubuntu/Debian
sudo apt update
sudo apt install ansible

# CentOS/RHEL
sudo yum install ansible
```

## 2. 最初の一歩

### 基本的なファイル操作を試す
```bash
ansible-playbook -i hosts.ini 01-basic-file-operations.yaml
```

このプレイブックでは以下を学べます：
- ディレクトリの作成
- ファイルの作成
- ファイル情報の取得
- ファイル内容の読み取り

## 3. 段階的な学習

### Step 1: 条件分岐とループ
```bash
ansible-playbook -i hosts.ini 02-conditions-and-loops.yaml
```

### Step 2: エラー処理
```bash
ansible-playbook -i hosts.ini 03-handlers-and-error-handling.yaml
```

### Step 3: テンプレート
```bash
ansible-playbook -i hosts.ini 04-templates-and-variables.yaml
```

### Step 4: ロール（上級者向け）
```bash
ansible-playbook -i hosts.ini 05-roles-example.yaml
```

## 4. 実践的な例題

### Docker環境の構築（管理者権限が必要）
```bash
sudo ansible-playbook -i hosts.ini 06-docker-environment.yaml
```

## 5. 学習のコツ

### プレイブックの構造を理解する
```yaml
---
- name: プレイブック名
  hosts: 対象ホスト
  tasks:
    - name: タスク名
      モジュール名:
        パラメータ: 値
```

### よく使うモジュール
- `file`: ファイル・ディレクトリ操作
- `copy`: ファイルコピー
- `template`: テンプレート処理
- `package`: パッケージ管理
- `service`: サービス管理
- `debug`: デバッグ情報表示

### 変数の使い方
```yaml
vars:
  my_var: "値"
  my_list:
    - item1
    - item2
```

### 条件分岐
```yaml
- name: 条件付きタスク
  debug:
    msg: "条件が真の場合のみ実行"
  when: condition == true
```

### ループ
```yaml
- name: ループ処理
  debug:
    msg: "{{ item }}"
  loop:
    - item1
    - item2
```

## 6. トラブルシューティング

### よくあるエラーと対処法

1. **権限エラー**
   ```bash
   sudo ansible-playbook -i hosts.ini [プレイブック名]
   ```

2. **モジュールが見つからない**
   ```bash
   pip install ansible[all]
   ```

3. **構文エラー**
   - YAMLのインデントを確認
   - コロンとスペースの位置を確認

4. **変数エラー**
   - 変数名のスペルを確認
   - 変数が定義されているか確認

## 7. 次のステップ

基本をマスターしたら：

1. **実際のサーバーで試す**
   - 複数サーバー環境の構築
   - 本格的なアプリケーションデプロイ

2. **高度な機能を学ぶ**
   - カスタムモジュールの作成
   - プラグインの開発
   - Ansible Tower/AWXの活用

3. **CI/CDとの連携**
   - GitHub Actionsとの連携
   - Jenkinsとの連携

## 8. 参考資料

- [Ansible公式ドキュメント](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)

## 9. 練習問題

各プレイブックを実行した後、以下のような変更を試してみてください：

1. ファイルの内容を変更する
2. 新しい条件を追加する
3. ループの対象を変更する
4. 新しい変数を追加する
5. エラー処理を追加する

これにより、Ansibleの理解がより深まります。 