"""
日本の株価データ取得プログラム
参考: https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/

使用方法:
    python main.py
"""

import datetime as dt
from stock_data_fetcher import JapaneseStockDataFetcher
import pandas as pd

def main():
    """メイン実行関数"""
    
    # 株価データ取得クラスのインスタンスを作成
    fetcher = JapaneseStockDataFetcher()
    
    # 主要な日本株の銘柄コード
    major_stocks = [
        "7203",  # トヨタ自動車
        "6758",  # ソニーグループ
        "9984",  # ソフトバンクグループ
        "6861",  # キーエンス
        "6954",  # ファナック
        "7974",  # 任天堂
        "8306",  # 三菱UFJフィナンシャル・グループ
        "9433",  # KDDI
        "9432",  # NTT
        "4502",  # 武田薬品工業
    ]
    
    print("=== 日本の株価データ取得プログラム ===")
    print("参考: https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/")
    print()
    
    while True:
        print("\n選択してください:")
        print("1. 単一銘柄の株価データを取得（Stooq）")
        print("2. 単一銘柄の株価データを取得（Yahoo Finance）")
        print("3. リアルタイム株価を取得")
        print("4. 複数銘柄のデータを一括取得")
        print("5. 主要銘柄のリアルタイム株価を表示")
        print("0. 終了")
        
        choice = input("\n選択 (0-5): ").strip()
        
        if choice == "0":
            print("プログラムを終了します。")
            break
            
        elif choice == "1":
            # Stooqから単一銘柄データ取得
            ticker = input("銘柄コードを入力してください（例: 7203）: ").strip()
            if ticker:
                print(f"\n{ticker}の株価データをStooqから取得中...")
                df = fetcher.get_stock_data_stooq(ticker)
                if not df.empty:
                    print("\n取得したデータ（最新5件）:")
                    print(df.head())
                    fetcher.save_to_csv(df, ticker, "stooq")
                else:
                    print("データの取得に失敗しました。")
                    
        elif choice == "2":
            # Yahoo Financeから単一銘柄データ取得
            ticker = input("銘柄コードを入力してください（例: 7203）: ").strip()
            if ticker:
                print(f"\n{ticker}の株価データをYahoo Financeから取得中...")
                df = fetcher.get_stock_data_yahoo(ticker)
                if not df.empty:
                    print("\n取得したデータ（最新5件）:")
                    print(df.head())
                    fetcher.save_to_csv(df, ticker, "yahoo")
                else:
                    print("データの取得に失敗しました。")
                    
        elif choice == "3":
            # リアルタイム株価取得
            ticker = input("銘柄コードを入力してください（例: 7203）: ").strip()
            if ticker:
                print(f"\n{ticker}のリアルタイム株価を取得中...")
                realtime_data = fetcher.get_realtime_price(ticker)
                if realtime_data:
                    print("\n=== リアルタイム株価情報 ===")
                    print(f"銘柄コード: {realtime_data['code']}")
                    print(f"会社名: {realtime_data['name']}")
                    print(f"現在値: ¥{realtime_data['current_price']:,.0f}")
                    print(f"前日終値: ¥{realtime_data['previous_close']:,.0f}")
                    if 'change' in realtime_data:
                        change_symbol = "▲" if realtime_data['change'] > 0 else "▼"
                        print(f"変動: {change_symbol}¥{realtime_data['change']:,.0f} ({realtime_data['change_percent']:+.2f}%)")
                    print(f"始値: ¥{realtime_data['open']:,.0f}")
                    print(f"高値: ¥{realtime_data['day_high']:,.0f}")
                    print(f"安値: ¥{realtime_data['day_low']:,.0f}")
                    print(f"出来高: {realtime_data['volume']:,}")
                    print(f"時価総額: ¥{realtime_data['market_cap']:,.0f}")
                    print(f"PER: {realtime_data['pe_ratio']:.2f}")
                    print(f"配当利回り: {realtime_data['dividend_yield']*100:.2f}%")
                    print(f"取得時刻: {realtime_data['timestamp']}")
                else:
                    print("リアルタイムデータの取得に失敗しました。")
                    
        elif choice == "4":
            # 複数銘柄の一括取得
            print("\n主要銘柄のデータを一括取得しますか？")
            print("1. Stooqから取得")
            print("2. Yahoo Financeから取得")
            print("3. カスタム銘柄リスト")
            
            sub_choice = input("選択 (1-3): ").strip()
            
            if sub_choice == "1":
                print("\n主要銘柄のデータをStooqから一括取得中...")
                results = fetcher.get_multiple_stocks(major_stocks, source="stooq")
                print(f"取得完了: {len(results)}銘柄")
                
            elif sub_choice == "2":
                print("\n主要銘柄のデータをYahoo Financeから一括取得中...")
                results = fetcher.get_multiple_stocks(major_stocks, source="yahoo")
                print(f"取得完了: {len(results)}銘柄")
                
            elif sub_choice == "3":
                custom_stocks = input("銘柄コードをカンマ区切りで入力してください（例: 7203,6758,9984）: ").strip()
                if custom_stocks:
                    stock_list = [s.strip() for s in custom_stocks.split(",")]
                    source = input("データソースを選択してください（stooq/yahoo）: ").strip().lower()
                    if source in ["stooq", "yahoo"]:
                        print(f"\n{len(stock_list)}銘柄のデータを{source}から一括取得中...")
                        results = fetcher.get_multiple_stocks(stock_list, source=source)
                        print(f"取得完了: {len(results)}銘柄")
                    else:
                        print("無効なデータソースです。")
                        
        elif choice == "5":
            # 主要銘柄のリアルタイム株価を一括表示
            print("\n主要銘柄のリアルタイム株価を取得中...")
            print("\n" + "="*80)
            print(f"{'銘柄コード':<8} {'会社名':<20} {'現在値':<12} {'変動':<15} {'出来高':<12}")
            print("="*80)
            
            for ticker in major_stocks[:5]:  # 最初の5銘柄のみ表示
                realtime_data = fetcher.get_realtime_price(ticker)
                if realtime_data and realtime_data['current_price']:
                    name = realtime_data['name'][:18] + "..." if len(realtime_data['name']) > 20 else realtime_data['name']
                    current_price = f"¥{realtime_data['current_price']:,.0f}"
                    
                    if 'change' in realtime_data:
                        change_symbol = "▲" if realtime_data['change'] > 0 else "▼"
                        change_str = f"{change_symbol}¥{realtime_data['change']:,.0f} ({realtime_data['change_percent']:+.2f}%)"
                    else:
                        change_str = "N/A"
                    
                    volume = f"{realtime_data['volume']:,}" if realtime_data['volume'] else "N/A"
                    
                    print(f"{realtime_data['code']:<8} {name:<20} {current_price:<12} {change_str:<15} {volume:<12}")
                else:
                    print(f"{ticker:<8} {'取得失敗':<20} {'N/A':<12} {'N/A':<15} {'N/A':<12}")
            
            print("="*80)
            print(f"取得時刻: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        else:
            print("無効な選択です。0-5の数字を入力してください。")

if __name__ == "__main__":
    main() 