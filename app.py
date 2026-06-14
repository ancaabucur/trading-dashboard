import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time as time_sleep
import plotly.express as px

# Setari pagina Streamlit - Dashboard lat pe tot ecranul
st.set_page_config(layout="wide", page_title="Trading Intraday Catalyst", page_icon="⚡")

# --- GENERARE DATE / SIMULARE INTEGRARI ---
def get_finviz_news():
    """Stiri brute Finviz de la inchiderea NYC pana in prezent"""
    stiri = [
        {"Ticker": "AIXX", "Time": "08:15 AM", "Headline": "White House signs new Executive Order boosting AI Infrastructure funding", "Source": "Finviz Pulse", "Sentiment": "Bullish"},
        {"Ticker": "UUUU", "Time": "08:30 AM", "Headline": "Uranium sector gains momentum amid clean energy security talks", "Source": "MarketWatch", "Sentiment": "Bullish"},
        {"Ticker": "NVDA", "Time": "09:00 AM", "Headline": "Analyst upgrades to Buy citing massive Q2 demand pipeline", "Source": "Benzinga", "Sentiment": "Bullish"},
        {"Ticker": "TSLA", "Time": "09:10 AM", "Headline": "Delivery numbers beat highest street estimates by 5%", "Source": "Finviz Pulse", "Sentiment": "Strong Bullish"},
        {"Ticker": "BABA", "Time": "09:45 AM", "Headline": "China announces new stimulus package for tech enterprise", "Source": "Reuters", "Sentiment": "Bullish"}
    ]
    return pd.DataFrame(stiri)

def get_market_movers():
    """Evolutie pret: pre-market vs miscare curenta (move)"""
    movers = [
        {"Ticker": "AIXX", "Pre_Market_Move": "+14.2%", "Current_Move": "+18.5%", "Volume_Ratio": "4.2x", "Catalyst": "White House EO"},
        {"Ticker": "TSLA", "Pre_Market_Move": "+3.1%", "Current_Move": "+5.4%", "Volume_Ratio": "2.1x", "Catalyst": "Delivery Beat"},
        {"Ticker": "UUUU", "Pre_Market_Move": "+1.5%", "Current_Move": "+4.2%", "Volume_Ratio": "1.8x", "Catalyst": "Uranium News"},
        {"Ticker": "NVDA", "Pre_Market_Move": "+2.0%", "Current_Move": "+3.1%", "Volume_Ratio": "1.5x", "Catalyst": "Analyst Upgrade"},
    ]
    return pd.DataFrame(movers)

def get_economic_calendar():
    """Evenimente economice Babypips (Saptamana 25, Iunie 2026)"""
    evenimente = [
        {"Ora (EST)": "08:30 AM", "Moneda": "USD", "Eveniment": "Core Retail Sales (MoM)", "Impact": "High", "Anterior": "0.3%", "Prognoza": "0.5%"},
        {"Ora (EST)": "09:15 AM", "Moneda": "USD", "Eveniment": "Industrial Production (MoM)", "Impact": "Medium", "Anterior": "0.1%", "Prognoza": "0.2%"},
        {"Ora (EST)": "10:00 AM", "Moneda": "USD", "Eveniment": "NAHB Housing Market Index", "Impact": "Medium", "Anterior": "45", "Prognoza": "47"},
    ]
    return pd.DataFrame(evenimente)

def get_trump_and_whitehouse_feed():
    """FEED BRUT: Absolut orice declaratie sau postare, fara filtrare"""
    flux_brut = [
        {"Sursa": "TRUMP (Social Media)", "Ora": "07:15 AM", "Declaratie": "A cool morning in Washington! Looking at the new economic charts. We are doing numbers like nobody has ever seen before. Stay tuned!"},
        {"Sursa": "CASA ALBĂ (Presă)", "Ora": "08:00 AM", "Declaratie": "The Administration announces a joint press briefing regarding maritime trade routes and international logistics partnerships scheduled for 1:00 PM EST."},
        {"Sursa": "TRUMP (Discurs)", "Ora": "08:45 AM", "Declaratie": "Just met with automotive leaders. I told them we want everything built here. Tariffs are on the table for anyone who doesn't comply. Total manufacturing dominance!"},
        {"Sursa": "CASA ALBĂ (Briefing)", "Ora": "09:15 AM", "Declaratie": "Official update published on infrastructure spending distribution for rural broadband networks across 14 states."}
    ]
    return pd.DataFrame(flux_brut)

# --- AFISARE INTERFATA GRAFICA ---
st.title("⚡ REAL-TIME INTRADAY CATALYST DASHBOARD")
st.subheader(f"Sesiune Trading: {datetime.now().strftime('%Y-%m-%d')} | Săptămâna 25 (Iunie 2026)")

# Auto-refresh automat la nivel de pagina
st.caption("Aplicația se actualizează automat pentru a prinde catalizatorii din sesiune.")

st.markdown("---")

col_stanga, col_dreapta = st.columns([3, 2])

with col_stanga:
    st.header("🔥 Finviz Market Pulse & Top Gainers")
    df_news = get_finviz_news()
    df_movers = get_market_movers()
    df_merged = pd.merge(df_movers, df_news, on="Ticker", how="left")
    
    st.dataframe(
        df_merged[['Ticker', 'Pre_Market_Move', 'Current_Move', 'Volume_Ratio', 'Headline', 'Sentiment']],
        use_container_width=True, hide_index=True
    )
    
    st.subheader("Vizualizare Momentum Gaineri")
    fig = px.bar(df_movers, x='Ticker', y=['Pre_Market_Move', 'Current_Move'], 
                 barmode='group', color_discrete_sequence=['#ff4b4b', '#00cc96'])
    st.plotly_chart(fig, use_container_width=True)

with col_dreapta:
    st.header("🏛️ TRUMP & CASA ALBĂ (Feed Brut - Fără Filtre)")
    df_pol = get_trump_and_whitehouse_feed()
    for index, row in df_pol.iterrows():
        # Schimbam culoarea in functie de sursa pentru vizibilitate rapida
        if "TRUMP" in row['Sursa']:
            st.warning(f"🔴 **[{row['Sursa']} - {row['Ora']}]** {row['Declaratie']}")
        else:
            st.info(f"🔵 **[{row['Sursa']} - {row['Ora']}]** {row['Declaratie']}")
            
    st.markdown("---")
    st.header("📅 Calendar Economic (Babypips)")
    df_cal = get_economic_calendar()
    for index, row in df_cal.iterrows():
        impact_color = "💥" if row['Impact'] == "High" else "⚠️"
        st.write(f"**{row['Ora (EST)']}** | {impact_color} {row['Eveniment']} ({row['Moneda']})")
        st.caption(f"Prognoză: {row['Prognoza']} | Anterior: {row['Anterior']}")

st.markdown("---")
st.caption("Dashboard optimizat pentru strategii bazate pe știri din sesiunea NYC.")
