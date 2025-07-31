"""
Streamlitを使用した株価データ可視化アプリケーション
参考: https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import datetime as dt
from stock_data_fetcher import JapaneseStockDataFetcher

# ページ設定
st.set_page_config(
    page_title="日本株価データ取得アプリ",
    page_icon="📈",
    layout="wide"
)

# タイトル
st.title("📈 日本株価データ取得アプリ")
st.markdown("参考: [Pythonで日本の株価を取得する方法](https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/)")

# 株価データ取得クラスのインスタンスを作成
@st.cache_resource
def get_fetcher():
    return JapaneseStockDataFetcher()

fetcher = get_fetcher()

# 主要な日本株の銘柄コード
MAJOR_STOCKS = {
    "7203": "トヨタ自動車",
    "6758": "ソニーグループ", 
    "9984": "ソフトバンクグループ",
    "6861": "キーエンス",
    "6954": "ファナック",
    "7974": "任天堂",
    "8306": "三菱UFJフィナンシャル・グループ",
    "9433": "KDDI",
    "9432": "NTT",
    "4502": "武田薬品工業",
    "6501": "日立製作所",
    "6502": "東芝",
    "6752": "パナソニック",
    "7267": "ホンダ",
    "7733": "オリンパス"
}

# サイドバー
st.sidebar.header("設定")

# タブ選択
tab1, tab2, tab3, tab4 = st.tabs(["📊 株価チャート", "💰 リアルタイム株価", "📈 複数銘柄比較", "📋 データダウンロード"])

with tab1:
    st.header("📊 株価チャート")
    
    # 銘柄選択
    selected_stock = st.selectbox(
        "銘柄を選択してください",
        options=list(MAJOR_STOCKS.keys()),
        format_func=lambda x: f"{x} - {MAJOR_STOCKS[x]}"
    )
    
    # 期間選択
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "開始日",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
            "終了日",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # データソース選択
    data_source = st.radio(
        "データソース",
        ["Yahoo Finance", "Stooq"],
        horizontal=True
    )
    
    if st.button("📊 チャートを表示"):
        with st.spinner("データを取得中..."):
            if data_source == "Yahoo Finance":
                df = fetcher.get_stock_data_yahoo(selected_stock, str(start_date), str(end_date))
            else:
                df = fetcher.get_stock_data_stooq(selected_stock, str(start_date), str(end_date))
            
            if not df.empty:
                # 日付でソート（古い順）
                df_sorted = df.sort_index()
                
                # キャンドルスティックチャート
                fig = go.Figure(data=[go.Candlestick(
                    x=df_sorted.index,
                    open=df_sorted['Open'],
                    high=df_sorted['High'],
                    low=df_sorted['Low'],
                    close=df_sorted['Close'],
                    name="株価"
                )])
                
                fig.update_layout(
                    title=f"{MAJOR_STOCKS[selected_stock]} ({selected_stock}) 株価チャート",
                    xaxis_title="日付",
                    yaxis_title="株価 (円)",
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 出来高チャート
                fig_volume = go.Figure(data=[go.Bar(
                    x=df_sorted.index,
                    y=df_sorted['Volume'],
                    name="出来高"
                )])
                
                fig_volume.update_layout(
                    title="出来高",
                    xaxis_title="日付",
                    yaxis_title="出来高",
                    height=300
                )
                
                st.plotly_chart(fig_volume, use_container_width=True)
                
                # 統計情報
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("最新終値", f"¥{df_sorted['Close'].iloc[-1]:,.0f}")
                with col2:
                    st.metric("最高値", f"¥{df_sorted['High'].max():,.0f}")
                with col3:
                    st.metric("最安値", f"¥{df_sorted['Low'].min():,.0f}")
                with col4:
                    st.metric("平均終値", f"¥{df_sorted['Close'].mean():,.0f}")
                
            else:
                st.error("データの取得に失敗しました。")

with tab2:
    st.header("💰 リアルタイム株価")
    
    # 銘柄選択
    realtime_stock = st.selectbox(
        "銘柄を選択してください",
        options=list(MAJOR_STOCKS.keys()),
        format_func=lambda x: f"{x} - {MAJOR_STOCKS[x]}",
        key="realtime_stock"
    )
    
    if st.button("🔄 リアルタイムデータを更新"):
        with st.spinner("リアルタイムデータを取得中..."):
            realtime_data = fetcher.get_realtime_price(realtime_stock)
            
            if realtime_data and realtime_data['current_price']:
                # メトリクス表示
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "現在値",
                        f"¥{realtime_data['current_price']:,.0f}",
                        delta=f"{realtime_data.get('change', 0):,.0f}" if 'change' in realtime_data else None
                    )
                
                with col2:
                    st.metric("前日終値", f"¥{realtime_data['previous_close']:,.0f}")
                
                with col3:
                    st.metric("出来高", f"{realtime_data['volume']:,}")
                
                # 詳細情報
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("基本情報")
                    st.write(f"**会社名:** {realtime_data['name']}")
                    st.write(f"**銘柄コード:** {realtime_data['code']}")
                    st.write(f"**始値:** ¥{realtime_data['open']:,.0f}")
                    st.write(f"**高値:** ¥{realtime_data['day_high']:,.0f}")
                    st.write(f"**安値:** ¥{realtime_data['day_low']:,.0f}")
                
                with col2:
                    st.subheader("財務指標")
                    st.write(f"**時価総額:** ¥{realtime_data['market_cap']:,.0f}")
                    st.write(f"**PER:** {realtime_data['pe_ratio']:.2f}")
                    st.write(f"**配当利回り:** {realtime_data['dividend_yield']*100:.2f}%")
                    st.write(f"**取得時刻:** {realtime_data['timestamp']}")
                
                # 価格変化の可視化
                if 'change' in realtime_data and realtime_data['change'] != 0:
                    fig = go.Figure()
                    
                    # 前日終値と現在値の比較
                    fig.add_trace(go.Bar(
                        x=['前日終値', '現在値'],
                        y=[realtime_data['previous_close'], realtime_data['current_price']],
                        marker_color=['lightblue', 'lightgreen' if realtime_data['change'] > 0 else 'lightcoral']
                    ))
                    
                    fig.update_layout(
                        title="価格比較",
                        yaxis_title="株価 (円)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.error("リアルタイムデータの取得に失敗しました。")

with tab3:
    st.header("📈 複数銘柄比較")
    
    # 複数銘柄選択
    selected_stocks = st.multiselect(
        "比較する銘柄を選択してください（最大5銘柄）",
        options=list(MAJOR_STOCKS.keys()),
        format_func=lambda x: f"{x} - {MAJOR_STOCKS[x]}",
        default=["7203", "6758", "9984"]
    )
    
    if len(selected_stocks) > 5:
        st.warning("最大5銘柄まで選択できます。")
        selected_stocks = selected_stocks[:5]
    
    # 期間選択
    col1, col2 = st.columns(2)
    with col1:
        compare_start_date = st.date_input(
            "開始日",
            value=datetime.now() - timedelta(days=90),
            max_value=datetime.now(),
            key="compare_start"
        )
    with col2:
        compare_end_date = st.date_input(
            "終了日",
            value=datetime.now(),
            max_value=datetime.now(),
            key="compare_end"
        )
    
    if st.button("📈 比較チャートを表示") and selected_stocks:
        with st.spinner("複数銘柄のデータを取得中..."):
            all_data = {}
            
            for stock in selected_stocks:
                df = fetcher.get_stock_data_yahoo(stock, str(compare_start_date), str(compare_end_date))
                if not df.empty:
                    # 終値を正規化（開始日を100とする）
                    df_sorted = df.sort_index()
                    normalized_close = (df_sorted['Close'] / df_sorted['Close'].iloc[0]) * 100
                    all_data[stock] = normalized_close
            
            if all_data:
                # 比較チャート
                fig = go.Figure()
                
                for stock, data in all_data.items():
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data.values,
                        mode='lines',
                        name=f"{stock} - {MAJOR_STOCKS[stock]}",
                        line=dict(width=2)
                    ))
                
                fig.update_layout(
                    title="複数銘柄比較（正規化終値）",
                    xaxis_title="日付",
                    yaxis_title="正規化価格（開始日=100）",
                    height=600,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 統計比較表
                st.subheader("統計比較")
                comparison_data = []
                
                for stock in selected_stocks:
                    if stock in all_data:
                        data = all_data[stock]
                        comparison_data.append({
                            "銘柄コード": stock,
                            "会社名": MAJOR_STOCKS[stock],
                            "期間最高値": f"{data.max():.2f}",
                            "期間最安値": f"{data.min():.2f}",
                            "期間変動率": f"{((data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100):.2f}%"
                        })
                
                if comparison_data:
                    comparison_df = pd.DataFrame(comparison_data)
                    st.dataframe(comparison_df, use_container_width=True)
            else:
                st.error("データの取得に失敗しました。")

with tab4:
    st.header("📋 データダウンロード")
    
    # ダウンロード設定
    col1, col2 = st.columns(2)
    
    with col1:
        download_stock = st.selectbox(
            "ダウンロードする銘柄",
            options=list(MAJOR_STOCKS.keys()),
            format_func=lambda x: f"{x} - {MAJOR_STOCKS[x]}",
            key="download_stock"
        )
        
        download_source = st.radio(
            "データソース",
            ["Yahoo Finance", "Stooq"],
            key="download_source"
        )
    
    with col2:
        download_start = st.date_input(
            "開始日",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now(),
            key="download_start"
        )
        
        download_end = st.date_input(
            "終了日",
            value=datetime.now(),
            max_value=datetime.now(),
            key="download_end"
        )
    
    if st.button("📥 データをダウンロード"):
        with st.spinner("データを取得中..."):
            if download_source == "Yahoo Finance":
                df = fetcher.get_stock_data_yahoo(download_stock, str(download_start), str(download_end))
            else:
                df = fetcher.get_stock_data_stooq(download_stock, str(download_start), str(download_end))
            
            if not df.empty:
                # CSVダウンロード
                csv = df.to_csv(index=True, encoding='utf-8-sig')
                st.download_button(
                    label="📄 CSVファイルをダウンロード",
                    data=csv,
                    file_name=f"{download_stock}_{download_source.lower()}_{download_start}_{download_end}.csv",
                    mime="text/csv"
                )
                
                # データプレビュー
                st.subheader("データプレビュー")
                st.dataframe(df.head(10), use_container_width=True)
                
                # 基本統計
                st.subheader("基本統計")
                st.write(df.describe())
                
            else:
                st.error("データの取得に失敗しました。")

# フッター
st.markdown("---")
st.markdown("**参考資料:** [Pythonで日本の株価を取得する方法](https://techblog.gmo-ap.jp/2022/06/07/pythonstockdata/)")
st.markdown("**データソース:** Yahoo Finance, Stooq") 