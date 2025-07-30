import pandas as pd
import numpy as np
from datetime import timedelta
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def carica_dati_sicuro(file_list):
    """Carica i dati con gestione degli errori"""
    df_list = []
    for file_path in file_list:
        try:
            print(f"📂 Caricamento: {file_path}")
            df_temp = pd.read_excel(file_path, skiprows=0)
            
            # Verifica se il file ha le colonne necessarie
            if "Italia" not in df_temp.columns:
                print(f"⚠️  File {file_path} non contiene la colonna 'Italia'")
                continue
                
            df_temp = df_temp[["Data", "Ora", "Italia"]]
            df_list.append(df_temp)
            print(f"✅ Caricato: {len(df_temp)} righe")
            
        except FileNotFoundError:
            print(f"❌ File non trovato: {file_path}")
        except Exception as e:
            print(f"❌ Errore nel caricamento {file_path}: {e}")
    
    if not df_list:
        raise ValueError("Nessun file valido trovato!")
    
    return pd.concat(df_list, ignore_index=True)

def pulisci_dati(df):
    """Pulizia e validazione dei dati"""
    print(f"🧹 Pulizia dati: {len(df)} righe iniziali")
    
    # Conversione sicura delle date
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
    
    # Conversione sicura delle ore
    df["Ora"] = pd.to_numeric(df["Ora"], errors="coerce")
    
    # Conversione sicura dei prezzi
    df["Prezzo"] = df["Italia"].astype(str).str.replace(",", ".").astype(float)
    
    # Rimuovi colonna originale
    df.drop(columns=["Italia"], inplace=True)
    
    # Filtra dati validi
    df = df.dropna()
    
    # Rimuovi outlier estremi (prezzi negativi o troppo alti)
    df = df[(df["Prezzo"] > 0) & (df["Prezzo"] < 1000)]
    
    # Verifica ore valide (1-24)
    df = df[(df["Ora"] >= 1) & (df["Ora"] <= 24)]
    
    print(f"✅ Dati puliti: {len(df)} righe finali")
    return df

def crea_features_avanzate(df):
    """Crea features più sofisticate per migliorare le previsioni"""
    print("🔧 Creazione features avanzate...")
    
    # Features temporali base
    df["GiornoSettimana"] = df["Data"].dt.dayofweek
    df["Mese"] = df["Data"].dt.month
    df["GiornoAnno"] = df["Data"].dt.dayofyear
    df["SettimanaAnno"] = df["Data"].dt.isocalendar().week
    
    # Features cicliche per ora e giorno
    df["Ora_Sin"] = np.sin(2 * np.pi * df["Ora"] / 24)
    df["Ora_Cos"] = np.cos(2 * np.pi * df["Ora"] / 24)
    df["GiornoSettimana_Sin"] = np.sin(2 * np.pi * df["GiornoSettimana"] / 7)
    df["GiornoSettimana_Cos"] = np.cos(2 * np.pi * df["GiornoSettimana"] / 7)
    
    # Ordina per data e ora
    df = df.sort_values(by=["Data", "Ora"])
    
    # Lags temporali
    df["Prezzo_Lag_1h"] = df["Prezzo"].shift(1)
    df["Prezzo_Lag_2h"] = df["Prezzo"].shift(2)
    df["Prezzo_Lag_3h"] = df["Prezzo"].shift(3)
    df["Prezzo_Lag_6h"] = df["Prezzo"].shift(6)
    df["Prezzo_Lag_12h"] = df["Prezzo"].shift(12)
    df["Prezzo_Lag_24h"] = df["Prezzo"].shift(24)
    
    # Medie mobili
    df["Prezzo_MA_3h"] = df["Prezzo"].rolling(window=3, min_periods=1).mean()
    df["Prezzo_MA_6h"] = df["Prezzo"].rolling(window=6, min_periods=1).mean()
    df["Prezzo_MA_24h"] = df["Prezzo"].rolling(window=24, min_periods=1).mean()
    
    # Deviazione standard mobile
    df["Prezzo_Std_6h"] = df["Prezzo"].rolling(window=6, min_periods=1).std()
    
    # Features per ora del giorno
    df["Is_Peak_Hour"] = ((df["Ora"] >= 8) & (df["Ora"] <= 20)).astype(int)
    df["Is_Night_Hour"] = ((df["Ora"] >= 22) | (df["Ora"] <= 6)).astype(int)
    
    # Rimuovi righe con valori mancanti
    df = df.dropna()
    
    print(f"✅ Features create: {len(df)} righe finali")
    return df

def ottimizza_modello(X, y):
    """Ottimizza il modello con cross-validation"""
    print("🤖 Ottimizzazione modello...")
    
    # Split dei dati
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False, random_state=42
    )
    
    # Standardizzazione delle features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Modello ottimizzato
    model = XGBRegressor(
        n_estimators=200,          # Più alberi
        learning_rate=0.03,         # Learning rate più basso
        max_depth=6,                # Profondità aumentata
        subsample=0.8,              # Subsampling
        colsample_bytree=0.8,       # Feature sampling
        gamma=0.2,                  # Min split loss
        reg_lambda=1.5,             # L2 regularization
        reg_alpha=0.5,              # L1 regularization
        random_state=42,
        verbosity=0,
        early_stopping_rounds=20    # Early stopping
    )
    
    # Training con early stopping
    model.fit(
        X_train_scaled, y_train,
        eval_set=[(X_test_scaled, y_test)],
        verbose=False
    )
    
    # Valutazione
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"✅ MAE: {mae:.2f} €/MWh")
    print(f"✅ RMSE: {rmse:.2f} €/MWh")
    
    return model, scaler, mae

def previsione_futura(model, scaler, df, giorni=7):
    """Crea previsioni future più accurate"""
    print(f"🔮 Previsione per i prossimi {giorni} giorni...")
    
    last_date = df["Data"].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=giorni, freq="D")
    
    # Usa gli ultimi valori reali per i lag
    ultimi_prezzi = df["Prezzo"].tail(24).values
    ultimi_prezzi_24h = df["Prezzo"].tail(48).values
    
    future_rows = []
    for i, date in enumerate(future_dates):
        for ora in range(1, 25):
            # Calcola indici per i lag
            idx_1h = (i * 24 + ora - 1) % len(ultimi_prezzi)
            idx_24h = (i * 24 + ora - 1) % len(ultimi_prezzi_24h)
            
            future_rows.append({
                "Data": date,
                "Ora": ora,
                "GiornoSettimana": date.dayofweek,
                "Mese": date.month,
                "GiornoAnno": date.dayofyear,
                "SettimanaAnno": date.isocalendar()[1],
                "Ora_Sin": np.sin(2 * np.pi * ora / 24),
                "Ora_Cos": np.cos(2 * np.pi * ora / 24),
                "GiornoSettimana_Sin": np.sin(2 * np.pi * date.dayofweek / 7),
                "GiornoSettimana_Cos": np.cos(2 * np.pi * date.dayofweek / 7),
                "Prezzo_Lag_1h": ultimi_prezzi[idx_1h] if idx_1h < len(ultimi_prezzi) else df["Prezzo"].mean(),
                "Prezzo_Lag_2h": ultimi_prezzi[max(0, idx_1h-1)] if idx_1h > 0 else df["Prezzo"].mean(),
                "Prezzo_Lag_3h": ultimi_prezzi[max(0, idx_1h-2)] if idx_1h > 1 else df["Prezzo"].mean(),
                "Prezzo_Lag_6h": ultimi_prezzi[max(0, idx_1h-5)] if idx_1h > 4 else df["Prezzo"].mean(),
                "Prezzo_Lag_12h": ultimi_prezzi[max(0, idx_1h-11)] if idx_1h > 10 else df["Prezzo"].mean(),
                "Prezzo_Lag_24h": ultimi_prezzi_24h[idx_24h] if idx_24h < len(ultimi_prezzi_24h) else df["Prezzo"].mean(),
                "Prezzo_MA_3h": df["Prezzo"].tail(3).mean(),
                "Prezzo_MA_6h": df["Prezzo"].tail(6).mean(),
                "Prezzo_MA_24h": df["Prezzo"].tail(24).mean(),
                "Prezzo_Std_6h": df["Prezzo"].tail(6).std(),
                "Is_Peak_Hour": 1 if 8 <= ora <= 20 else 0,
                "Is_Night_Hour": 1 if ora >= 22 or ora <= 6 else 0
            })
    
    df_future = pd.DataFrame(future_rows)
    
    # Features per il modello
    feature_cols = [
        "Ora", "GiornoSettimana", "Mese", "GiornoAnno", "SettimanaAnno",
        "Ora_Sin", "Ora_Cos", "GiornoSettimana_Sin", "GiornoSettimana_Cos",
        "Prezzo_Lag_1h", "Prezzo_Lag_2h", "Prezzo_Lag_3h", "Prezzo_Lag_6h", 
        "Prezzo_Lag_12h", "Prezzo_Lag_24h", "Prezzo_MA_3h", "Prezzo_MA_6h", 
        "Prezzo_MA_24h", "Prezzo_Std_6h", "Is_Peak_Hour", "Is_Night_Hour"
    ]
    
    X_future = df_future[feature_cols]
    X_future_scaled = scaler.transform(X_future)
    df_future["Prezzo_Previsto"] = model.predict(X_future_scaled)
    
    return df_future

def main():
    """Funzione principale con gestione degli errori"""
    try:
        print("🚀 Avvio sistema di previsione prezzi elettrici...")
        
        # === 1. CARICA I FILE EXCEL ===
        file_list = [
            "20200701_20210701_MGP_PrezziZonali.xlsx",
            "20210701_20220701_MGP_PrezziZonali.xlsx",
            "20220701_20230701_MGP_PrezziZonali.xlsx",
            "20250716_20250716_MGP_PrezziZonali.xlsx"
        ]
        
        df = carica_dati_sicuro(file_list)
        
        # === 2. PULIZIA E TRASFORMAZIONI ===
        df = pulisci_dati(df)
        
        # === 3. FEATURES AVANZATE ===
        df = crea_features_avanzate(df)
        
        # === 4. MODELLO OTTIMIZZATO ===
        feature_cols = [
            "Ora", "GiornoSettimana", "Mese", "GiornoAnno", "SettimanaAnno",
            "Ora_Sin", "Ora_Cos", "GiornoSettimana_Sin", "GiornoSettimana_Cos",
            "Prezzo_Lag_1h", "Prezzo_Lag_2h", "Prezzo_Lag_3h", "Prezzo_Lag_6h", 
            "Prezzo_Lag_12h", "Prezzo_Lag_24h", "Prezzo_MA_3h", "Prezzo_MA_6h", 
            "Prezzo_MA_24h", "Prezzo_Std_6h", "Is_Peak_Hour", "Is_Night_Hour"
        ]
        
        X = df[feature_cols]
        y = df["Prezzo"]
        
        model, scaler, mae = ottimizza_modello(X, y)
        
        # === 5. PREVISIONE FUTURA ===
        df_future = previsione_futura(model, scaler, df, giorni=7)
        
        # === 6. SALVA IN EXCEL ===
        output_file = "previsione_italia_trading_ottimizzata.xlsx"
        df_future.to_excel(output_file, index=False)
        
        print(f"\n📁 File salvato: {output_file}")
        print(f"📊 Previsioni create per {len(df_future)} ore")
        print(f"💰 Prezzo medio previsto: {df_future['Prezzo_Previsto'].mean():.2f} €/MWh")
        print(f"📈 Prezzo massimo previsto: {df_future['Prezzo_Previsto'].max():.2f} €/MWh")
        print(f"📉 Prezzo minimo previsto: {df_future['Prezzo_Previsto'].min():.2f} €/MWh")
        
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        print("💡 Verifica che i file Excel siano presenti nella directory corrente")

if __name__ == "__main__":
    main() 