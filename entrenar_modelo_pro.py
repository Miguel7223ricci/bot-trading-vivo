import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

print("✅ Entrenamiento de modelo PRO iniciado...")

# ✅ 1️⃣ Leer archivo generado en el paso anterior
csv_file = "historial_senales_etiquetado_pro.csv"
df = pd.read_csv(csv_file)
print(f"✅ Archivo cargado: {csv_file}")
print(df.head())

# ✅ 2️⃣ Filtrar solo GANANCIA/PERDIDA
df = df[df['Resultado'].isin(['GANANCIA', 'PERDIDA'])]
print(f"✅ Filtrado: {len(df)} registros válidos.")

# ✅ 3️⃣ Codificar Dirección (BUY=1, SELL=0)
df['Direccion_Num'] = df['Dirección'].apply(lambda x: 1 if x == 'BUY' else 0)

# ✅ 4️⃣ Definir features y target
features = ['ATR', 'EMA_Rapida', 'EMA_Lenta', 'RSI', 'Direccion_Num']
X = df[features]
y = df['Resultado']

print("\n✅ Features (X):")
print(X.head())

print("\n✅ Target (y):")
print(y.head())

# ✅ 5️⃣ Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✅ Tamaño entrenamiento: {len(X_train)}")
print(f"✅ Tamaño prueba: {len(X_test)}")

# ✅ 6️⃣ Entrenar RandomForest
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)
print("\n✅ Modelo entrenado con éxito.")

# ✅ 7️⃣ Evaluar
y_pred = model.predict(X_test)
print("\n✅ Reporte de clasificación:")
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Precisión del modelo: {accuracy:.2f}")

# ✅ 8️⃣ Guardar modelo
joblib.dump(model, 'modelo_trained_rf_pro.pkl')
print("\n✅ Modelo guardado como 'modelo_trained_rf_pro.pkl'")
