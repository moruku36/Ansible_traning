"""
日本株価データ取得アプリの使用例
参考: https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/
"""

from stock_data_fetcher import JapaneseStockDataFetcher
import datetime as dt

def main():
    """使用例のメイン関数"""
    
    print("=== 日本株価データ取得アプリ 使用例 ===")
    print("参考: https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/")
    print()
    
    # 株価データ取得クラスのインスタンスを作成
    fetcher = JapaneseStockDataFetcher()
    
    # 例1: トヨタ自動車の株価データをStooqから取得
    print("例1: トヨタ自動車の株価データをStooqから取得")
    print("-" * 50)
    
    toyota_stooq = fetcher.get_stock_data_stooq("7203", "2024-01-01", "2024-12-31")
    if not toyota_stooq.empty:
        print(f"取得件数: {len(toyota_stooq)}件")
        print("最新5件:")
        print(toyota_stooq.head())
        print()
        
        # CSVファイルに保存
        fetcher.save_to_csv(toyota_stooq, "7203", "stooq")
    
    # 例2: ソニーグループの株価データをYahoo Financeから取得
    print("例2: ソニーグループの株価データをYahoo Financeから取得")
    print("-" * 50)
    
    sony_yahoo = fetcher.get_stock_data_yahoo("6758", "2024-01-01", "2024-12-31")
    if not sony_yahoo.empty:
        print(f"取得件数: {len(sony_yahoo)}件")
        print("最新5件:")
        print(sony_yahoo.head())
        print()
        
        # CSVファイルに保存
        fetcher.save_to_csv(sony_yahoo, "6758", "yahoo")
    
    # 例3: リアルタイム株価を取得
    print("例3: トヨタ自動車のリアルタイム株価を取得")
    print("-" * 50)
    
    toyota_realtime = fetcher.get_realtime_price("7203")
    if toyota_realtime:
        print(f"銘柄コード: {toyota_realtime['code']}")
        print(f"会社名: {toyota_realtime['name']}")
        print(f"現在値: ¥{toyota_realtime['current_price']:,.0f}")
        print(f"前日終値: ¥{toyota_realtime['previous_close']:,.0f}")
        if 'change' in toyota_realtime:
            change_symbol = "▲" if toyota_realtime['change'] > 0 else "▼"
            print(f"変動: {change_symbol}¥{toyota_realtime['change']:,.0f} ({toyota_realtime['change_percent']:+.2f}%)")
        print(f"出来高: {toyota_realtime['volume']:,}")
        print(f"取得時刻: {toyota_realtime['timestamp']}")
        print()
    
    # 例4: 複数銘柄の一括取得
    print("例4: 複数銘柄の一括取得（Yahoo Finance）")
    print("-" * 50)
    
    major_stocks = ["7203", "6758", "9984"]  # トヨタ、ソニー、ソフトバンク
    results = fetcher.get_multiple_stocks(major_stocks, source="yahoo")
    
    print(f"取得完了: {len(results)}銘柄")
    for symbol, data in results.items():
        print(f"{symbol}: {len(data)}件のデータを取得")
    print()
    
    # 例5: データの統計情報を表示
    print("例5: トヨタ自動車の統計情報")
    print("-" * 50)
    
    if not toyota_stooq.empty:
        print("基本統計:")
        print(f"期間: {toyota_stooq.index.min()} 〜 {toyota_stooq.index.max()}")
        print(f"最高値: ¥{toyota_stooq['High'].max():,.0f}")
        print(f"最安値: ¥{toyota_stooq['Low'].min():,.0f}")
        print(f"平均終値: ¥{toyota_stooq['Close'].mean():,.0f}")
        print(f"標準偏差: ¥{toyota_stooq['Close'].std():,.0f}")
        print()
        
        # 価格変化率の計算
        first_close = toyota_stooq['Close'].iloc[-1]  # 最新の終値
        last_close = toyota_stooq['Close'].iloc[0]    # 最古の終値
        total_return = ((first_close - last_close) / last_close) * 100
        print(f"期間総リターン: {total_return:+.2f}%")
    
    print("=== 使用例完了 ===")

if __name__ == "__main__":
    main() 