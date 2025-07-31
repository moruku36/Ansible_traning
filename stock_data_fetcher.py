"""
日本の株価データを取得するためのクラス
参考: https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/
"""

import os
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
from typing import Optional, Dict, List
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JapaneseStockDataFetcher:
    """日本の株価データを取得するクラス"""
    
    def __init__(self, data_dir: str = "stock_data"):
        """
        初期化
        
        Args:
            data_dir (str): データ保存ディレクトリ
        """
        self.data_dir = data_dir
        self._create_data_directory()
    
    def _create_data_directory(self):
        """データ保存ディレクトリを作成"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"データディレクトリを作成しました: {self.data_dir}")
    
    def get_stock_data_stooq(self, 
                            ticker_symbol: str, 
                            start_date: str = None, 
                            end_date: str = None) -> pd.DataFrame:
        """
        Stooqから株価データを取得
        
        Args:
            ticker_symbol (str): 銘柄コード（例: "7203" for Toyota）
            start_date (str): 開始日（YYYY-MM-DD形式）
            end_date (str): 終了日（YYYY-MM-DD形式）
            
        Returns:
            pd.DataFrame: 株価データ
        """
        try:
            # デフォルト日付設定
            if start_date is None:
                start_date = '2022-01-01'
            if end_date is None:
                end_date = dt.date.today().strftime('%Y-%m-%d')
            
            # 銘柄コードの形式を調整
            ticker_symbol_dr = f"{ticker_symbol}.JP"
            
            logger.info(f"Stooqからデータを取得中: {ticker_symbol} ({start_date} - {end_date})")
            
            # データ取得
            df = web.DataReader(
                ticker_symbol_dr, 
                data_source='stooq', 
                start=start_date, 
                end=end_date
            )
            
            # 銘柄コード列を追加
            df.insert(0, "code", ticker_symbol, allow_duplicates=False)
            
            # 日付でソート（新しい順）
            df = df.sort_index(ascending=False)
            
            logger.info(f"データ取得成功: {len(df)}件")
            return df
            
        except Exception as e:
            logger.error(f"Stooqからのデータ取得に失敗: {e}")
            return pd.DataFrame()
    
    def get_stock_data_yahoo(self, 
                            ticker_symbol: str, 
                            start_date: str = None, 
                            end_date: str = None) -> pd.DataFrame:
        """
        Yahoo Financeから株価データを取得
        
        Args:
            ticker_symbol (str): 銘柄コード（例: "7203.T" for Toyota）
            start_date (str): 開始日（YYYY-MM-DD形式）
            end_date (str): 終了日（YYYY-MM-DD形式）
            
        Returns:
            pd.DataFrame: 株価データ
        """
        try:
            # デフォルト日付設定
            if start_date is None:
                start_date = '2022-01-01'
            if end_date is None:
                end_date = dt.date.today().strftime('%Y-%m-%d')
            
            # 銘柄コードの形式を調整（.Tを追加）
            if not ticker_symbol.endswith('.T'):
                ticker_symbol_yahoo = f"{ticker_symbol}.T"
            else:
                ticker_symbol_yahoo = ticker_symbol
            
            logger.info(f"Yahoo Financeからデータを取得中: {ticker_symbol_yahoo} ({start_date} - {end_date})")
            
            # データ取得
            ticker = yf.Ticker(ticker_symbol_yahoo)
            df = ticker.history(start=start_date, end=end_date)
            
            # 列名を統一
            df.columns = [col.title() for col in df.columns]
            
            # 銘柄コード列を追加
            df.insert(0, "code", ticker_symbol.replace('.T', ''), allow_duplicates=False)
            
            # 日付でソート（新しい順）
            df = df.sort_index(ascending=False)
            
            logger.info(f"データ取得成功: {len(df)}件")
            return df
            
        except Exception as e:
            logger.error(f"Yahoo Financeからのデータ取得に失敗: {e}")
            return pd.DataFrame()
    
    def get_realtime_price(self, ticker_symbol: str) -> Dict:
        """
        リアルタイム株価を取得
        
        Args:
            ticker_symbol (str): 銘柄コード
            
        Returns:
            Dict: リアルタイム株価情報
        """
        try:
            # Yahoo Financeからリアルタイムデータを取得
            if not ticker_symbol.endswith('.T'):
                ticker_symbol_yahoo = f"{ticker_symbol}.T"
            else:
                ticker_symbol_yahoo = ticker_symbol
            
            ticker = yf.Ticker(ticker_symbol_yahoo)
            info = ticker.info
            
            # 基本情報を取得
            realtime_data = {
                'code': ticker_symbol.replace('.T', ''),
                'name': info.get('longName', 'N/A'),
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'timestamp': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 価格変化を計算
            if realtime_data['current_price'] and realtime_data['previous_close']:
                change = realtime_data['current_price'] - realtime_data['previous_close']
                change_percent = (change / realtime_data['previous_close']) * 100
                realtime_data['change'] = change
                realtime_data['change_percent'] = change_percent
            
            logger.info(f"リアルタイムデータ取得成功: {ticker_symbol}")
            return realtime_data
            
        except Exception as e:
            logger.error(f"リアルタイムデータ取得に失敗: {e}")
            return {}
    
    def save_to_csv(self, df: pd.DataFrame, ticker_symbol: str, source: str = "stooq"):
        """
        データをCSVファイルに保存
        
        Args:
            df (pd.DataFrame): 保存するデータ
            ticker_symbol (str): 銘柄コード
            source (str): データソース（stooq または yahoo）
        """
        if df.empty:
            logger.warning("保存するデータがありません")
            return
        
        filename = f"{source}_stock_data_{ticker_symbol}_{dt.date.today()}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        df.to_csv(filepath, encoding='utf-8-sig')
        logger.info(f"データを保存しました: {filepath}")
    
    def get_multiple_stocks(self, 
                           ticker_symbols: List[str], 
                           start_date: str = None, 
                           end_date: str = None,
                           source: str = "stooq") -> Dict[str, pd.DataFrame]:
        """
        複数銘柄のデータを一括取得
        
        Args:
            ticker_symbols (List[str]): 銘柄コードのリスト
            start_date (str): 開始日
            end_date (str): 終了日
            source (str): データソース
            
        Returns:
            Dict[str, pd.DataFrame]: 銘柄コードをキーとしたデータ辞書
        """
        results = {}
        
        for symbol in ticker_symbols:
            logger.info(f"銘柄 {symbol} のデータを取得中...")
            
            if source.lower() == "stooq":
                data = self.get_stock_data_stooq(symbol, start_date, end_date)
            elif source.lower() == "yahoo":
                data = self.get_stock_data_yahoo(symbol, start_date, end_date)
            else:
                logger.error(f"サポートされていないデータソース: {source}")
                continue
            
            if not data.empty:
                results[symbol] = data
                self.save_to_csv(data, symbol, source)
            else:
                logger.warning(f"銘柄 {symbol} のデータ取得に失敗しました")
        
        return results 