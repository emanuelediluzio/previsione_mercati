import pandas as pd
import numpy as np
from datetime import timedelta
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# === 1. CARICA I FILE EXCEL ===
file_list = [
    "20200701_20210701_MGP_PrezziZonali.xlsx",
    "20210701_20220701_MGP_PrezziZonali.xlsx",
    "20220701_20230701_MGP_PrezziZonali.xlsx",
    "20250716_20250716_MGP_PrezziZonali.xlsx"
]

df_list = []
for file_path in file_list:
    df_temp = pd.read_excel(file_path, skiprows=0)
    if "Italia" not in df_temp.columns:
        continue
    df_temp = df_temp[["Data", "Ora", "Italia"]]
    df_list.append(df_temp)

df = pd.concat(df_list, ignore_index=True)

# === 2. PULIZIA E TRASFORMAZIONI ===
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
df["Ora"] = pd.to_numeric(df["Ora"], errors="coerce")
df["Prezzo"] = df["Italia"].astype(str).str.replace(",", ".").astype(float)
df.drop(columns=["Italia"], inplace=True)
df.dropna(inplace=True)

# === 3. FEATURES ===
df["GiornoSettimana"] = df["Data"].dt.dayofweek
df["Mese"] = df["Data"].dt.month
df = df.sort_values(by=["Data", "Ora"])
df["Prezzo_Lag_1h"] = df["Prezzo"].shift(1)
df["Prezzo_Lag_24h"] = df["Prezzo"].shift(24)
df = df.dropna()

# === 4. MODELLO CON 120 ALBERI ===
X = df[["Ora", "GiornoSettimana", "Mese", "Prezzo_Lag_1h", "Prezzo_Lag_24h"]]
y = df["Prezzo"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = XGBRegressor(
    n_estimators=120,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.85,
    colsample_bytree=0.85,
    gamma=0.1,
    reg_lambda=1,
    reg_alpha=0.3,
    random_state=42,
    verbosity=0
)

model.fit(X_train, y_train)

# === 5. CALCOLO ERRORE
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"\n✅ MAE (errore medio assoluto): {mae:.2f} €/MWh")

# === 6. PREVISIONE PER I PROSSIMI 7 GIORNI
last_date = df["Data"].max()
future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=7, freq="D")

future_rows = []
for date in future_dates:
    for ora in range(1, 25):
        future_rows.append({
            "Data": date,
            "Ora": ora,
            "GiornoSettimana": date.dayofweek,
            "Mese": date.month,
            "Prezzo_Lag_1h": df["Prezzo_Lag_1h"].mean(),
            "Prezzo_Lag_24h": df["Prezzo_Lag_24h"].mean()
        })

df_future = pd.DataFrame(future_rows)
X_future = df_future[["Ora", "GiornoSettimana", "Mese", "Prezzo_Lag_1h", "Prezzo_Lag_24h"]]
df_future["Prezzo_Previsto"] = model.predict(X_future)

# === 7. SALVA IN EXCEL
output_file = "previsione_italia_trading_120alberi.xlsx"
df_future.to_excel(output_file, index=False)
print(f"\n📁 File salvato: {output_file}") 