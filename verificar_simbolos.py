import yfinance as yf

symbols = [
    "EURUSD=X", "EURNZD=X", "GBPNZD=X", "GBPJPY=X", "NG=F", "GC=F", "SOL-USD", "USDNOK=X", "USDCHF=X", "USDSEK=X",
    "EURSEK=X", "GBPAUD=X", "AUDNZD=X", "NZDUSD=X", "EURCAD=X", "AUDUSD=X", "EURAUD=X", "CADJPY=X", "CL=F", "^RUT",
    "^GSPC", "^DJI", "BTC-USD", "ETH-USD", "PA=F", "^STOXX50E"
]

for symbol in symbols:
    print(f"⏳ Verificando {symbol}...")
    try:
        data = yf.download(symbol, period="5d", interval="1d")
        if data.empty:
            print(f"⚠️  {symbol}: No hay datos disponibles o símbolo incorrecto.")
        else:
            print(f"✅ {symbol}: Datos OK.")
    except Exception as e:
        print(f"❌ {symbol}: Error - {e}")
