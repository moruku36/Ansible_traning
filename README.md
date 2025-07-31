# 📈 日本株価データ取得アプリ

[GMO NIKKOの技術ブログ](https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/)を参考に作成した、日本の株価データをリアルタイムで取得・可視化するPythonアプリケーションです。

## 🚀 機能

### 📊 株価データ取得
- **Stooq**からの株価データ取得
- **Yahoo Finance**からの株価データ取得
- **リアルタイム株価**の取得
- **複数銘柄**の一括取得

### 📈 データ可視化
- キャンドルスティックチャート
- 出来高チャート
- 複数銘柄比較チャート
- リアルタイム価格表示

### 💾 データ管理
- CSVファイルでのデータ保存
- データダウンロード機能
- 統計情報の表示

## 📋 対応銘柄

主要な日本株15銘柄に対応：

| 銘柄コード | 会社名 |
|-----------|--------|
| 7203 | トヨタ自動車 |
| 6758 | ソニーグループ |
| 9984 | ソフトバンクグループ |
| 6861 | キーエンス |
| 6954 | ファナック |
| 7974 | 任天堂 |
| 8306 | 三菱UFJフィナンシャル・グループ |
| 9433 | KDDI |
| 9432 | NTT |
| 4502 | 武田薬品工業 |
| 6501 | 日立製作所 |
| 6502 | 東芝 |
| 6752 | パナソニック |
| 7267 | ホンダ |
| 7733 | オリンパス |

## 🛠️ インストール

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd japanese-stock-data-app
```

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

## 🎯 使用方法

### 1. コマンドライン版
```bash
python main.py
```

**機能:**
- 単一銘柄の株価データ取得（Stooq/Yahoo Finance）
- リアルタイム株価取得
- 複数銘柄の一括取得
- 主要銘柄のリアルタイム株価表示

### 2. Webアプリケーション版
```bash
streamlit run streamlit_app.py
```

**機能:**
- 📊 株価チャート（キャンドルスティック）
- 💰 リアルタイム株価
- 📈 複数銘柄比較
- 📋 データダウンロード

## 📁 ファイル構成

```
japanese-stock-data-app/
├── requirements.txt          # 依存関係
├── stock_data_fetcher.py     # 株価データ取得クラス
├── main.py                   # コマンドライン版メイン
├── streamlit_app.py          # Webアプリケーション版
├── example_usage.py          # 使用例
├── README.md                 # このファイル
└── stock_data/               # データ保存ディレクトリ（自動作成）
```

## 🔧 技術仕様

### 使用ライブラリ
- **pandas**: データ処理
- **pandas-datareader**: 株価データ取得
- **yfinance**: Yahoo Finance API
- **streamlit**: Webアプリケーション
- **plotly**: インタラクティブチャート
- **matplotlib**: グラフ描画

### データソース
- **Stooq**: ポーランドの金融データサイト
- **Yahoo Finance**: 米国Yahoo Finance

### 取得データ
- Date: 日付
- Open: 始値
- High: 高値
- Low: 安値
- Close: 終値
- Volume: 出来高
- Adj Close: 調整後終値（Yahoo Financeのみ）

## 📊 使用例

### 基本的な株価データ取得
```python
from stock_data_fetcher import JapaneseStockDataFetcher

# インスタンス作成
fetcher = JapaneseStockDataFetcher()

# Stooqからトヨタ自動車のデータを取得
df = fetcher.get_stock_data_stooq("7203", "2024-01-01", "2024-12-31")

# Yahoo Financeからリアルタイムデータを取得
realtime_data = fetcher.get_realtime_price("7203")
```

### 複数銘柄の一括取得
```python
# 主要銘柄の一括取得
stocks = ["7203", "6758", "9984"]
results = fetcher.get_multiple_stocks(stocks, source="yahoo")
```

## ⚠️ 注意事項

1. **データソースの制限**
   - リアルタイムデータは取引時間外の場合、前日終値が表示されます
   - 一部の銘柄でデータが取得できない場合があります

2. **利用制限**
   - データソースの利用規約に従ってください
   - 過度なリクエストは避けてください

3. **投資判断**
   - このアプリケーションは学習・研究目的です
   - 投資判断には十分な調査を行ってください

## 🤝 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🙏 謝辞

- [GMO NIKKO エンジニアブログ](https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/) - 参考資料
- [pandas-datareader](https://pandas-datareader.readthedocs.io/) - データ取得ライブラリ
- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance API
- [Streamlit](https://streamlit.io/) - Webアプリケーションフレームワーク

## 📞 サポート

問題や質問がある場合は、GitHubのIssuesページでお知らせください。
