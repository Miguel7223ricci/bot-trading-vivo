import yfinance as yf
import pandas as pd
import numpy as np
import joblib
import time
from whatsapp_sender import enviar_whatsapp  # ✅ ENVÍO POR WHATSAPP

# ✅ CONFIGURACIÓN
activos_tickers = {
    "EURUSD": "EURUSD=X",
    "EURNZD": "EURNZD=X",
    "GBPNZD": "GBPNZD=X",
    "GBPJPY": "GBPJPY=X",
    "NATGAS": "NG=F",
    "GOLD": "GC=F",
    "SOLANA": "SOL-USD",
    "USDNOK": "USDNOK=X",
    "USDCHF": "USDCHF=X",
    "USDSEK": "USDSEK=X",
    "EURSEK": "EURSEK=X",
    "GBPAUD": "GBPAUD=X",
    "AUDNZD": "AUDNZD=X",
    "NZDUSD": "NZDUSD=X",
    "EURCAD": "EURCAD=X",
    "AUDUSD": "AUDUSD=X",
    "EURAUD": "EURAUD=X",
    "CADJPY": "CADJPY=X",
    "WTI": "CL=F",
    "US2000": "^RUT",
    "US500": "^GSPC",
    "US30": "^DJI",
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "PALLADIUM": "PA=F",
    "EU50": "^STOXX50E"
}

ema_rapida_period = 34
ema_lenta_period = 89
atr_window = 20
rsi_period = 14
umbral_confianza_ml = 0.55

modelo = joblib.load('modelo_trained_rf_pro.pkl')

def calcular_factor_atr(atr):
    if atr < 0.001:
        return 1.5
    elif atr < 0.002:
        return 2.0
    else:
        return 2.5

def calcular_indicadores(df):
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=atr_window).mean()

    df['EMA_Rapida'] = df['Close'].ewm(span=ema_rapida_period, adjust=False).mean()
    df['EMA_Lenta'] = df['Close'].ewm(span=ema_lenta_period, adjust=False).mean()

    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['Soporte'] = df['Low'].rolling(window=20).min()
    df['Resistencia'] = df['High'].rolling(window=20).max()

    return df

def evaluar_señales(activo, df):
    señales = []
    if df.isnull().values.any():
        return []

    rango_high = df['High'].iloc[:40].max()
    rango_low = df['Low'].iloc[:40].min()
    rango_londres_high = df['High'].iloc[40:80].max()
    rango_londres_low = df['Low'].iloc[40:80].min()

    precio = df['Close'].iloc[-1]
    atr = df['ATR'].iloc[-1]
    ema_rapida = df['EMA_Rapida'].iloc[-1]
    ema_lenta = df['EMA_Lenta'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    soporte = df['Soporte'].iloc[-1]
    resistencia = df['Resistencia'].iloc[-1]

    if np.isnan([atr, ema_rapida, ema_lenta, rsi, soporte, resistencia]).any():
        return []

    rompe_asiatico = precio > rango_high or precio < rango_low
    rompe_londres = precio > rango_londres_high or precio < rango_londres_low

    if not (rompe_asiatico or rompe_londres):
        return []

    if ema_rapida <= ema_lenta:
        return []

    if rsi >= 75 or rsi <= 25:
        return []

    rango_rompido = "Asiatico" if rompe_asiatico else "Londres"
    factor_atr = calcular_factor_atr(atr)
    stop_loss = max(precio - (factor_atr * atr), soporte)
    tp1 = precio + (atr * 1.5)
    tp2 = min(precio + (atr * 3.0), resistencia)

    input_modelo = pd.DataFrame([{
        'ATR': atr,
        'EMA_Rapida': ema_rapida,
        'EMA_Lenta': ema_lenta,
        'RSI': rsi,
        'Direccion_Num': 1
    }])
    proba = modelo.predict_proba(input_modelo)[0]
    idx_ganancia = list(modelo.classes_).index('GANANCIA')
    prob_ganancia = proba[idx_ganancia]

    if prob_ganancia < umbral_confianza_ml:
        return []

    mensaje = f"""
📈 *SEÑAL DETECTADA*
🔹 Activo: {activo}
🔹 Dirección: BUY
💵 Precio actual: {precio:.5f}
🛑 Stop Loss: {stop_loss:.5f}
🎯 TP1: {tp1:.5f}
🎯 TP2: {tp2:.5f}
📊 ATR: {atr:.5f}
📈 EMA Rápida: {ema_rapida:.5f}
📉 EMA Lenta: {ema_lenta:.5f}
📍 RSI: {rsi:.2f}
📉 Soporte: {soporte:.5f}
📈 Resistencia: {resistencia:.5f}
🕒 Rango: {rango_rompido}
🤖 ML: {prob_ganancia:.2f}
"""
    señales.append(mensaje)
    return señales

def monitorear():
    print("✅ Iniciando monitoreo en vivo (versión PRO + WhatsApp).")
    for nombre, ticker in activos_tickers.items():
        print(f"\n✅ Verificando {nombre}...")
        try:
            df = yf.download(ticker, interval="4h", period="60d")
            if df.empty or len(df) < 100:
                print(f"⚠️ Sin suficientes datos para {nombre}")
                continue
            df.reset_index(inplace=True)
            df = calcular_indicadores(df)
            señales = evaluar_señales(nombre, df)
            for mensaje in señales:
                enviar_whatsapp(mensaje)  # ✅ ENVÍA WHATSAPP
        except Exception as e:
            print(f"⚠️ Error con {nombre}: {e}")

if __name__ == "__main__":
    monitorear()
