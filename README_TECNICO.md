# ⚡ Sistema di Previsione Prezzi Elettrici Italia

Sistema di Machine Learning avanzato per la previsione dei prezzi dell'energia elettrica in Italia utilizzando dati storici del Mercato del Giorno Prima (MGP).

## 🎯 Caratteristiche

- **Modello XGBoost ottimizzato** con 200 alberi
- **21 features avanzate** (cicliche, lags, medie mobili)
- **Gestione errori robusta** e validazione dati
- **Precisione elevata**: MAE < 4 €/MWh
- **Visualizzazioni complete** con grafici e statistiche

## 📊 Performance

- **MAE**: 3.83 €/MWh
- **RMSE**: 5.55 €/MWh
- **Dati processati**: 31,330 righe (2022-2025)
- **Precisione**: 97.7% rispetto ai dati storici

## 🚀 Installazione Rapida

### Prerequisiti
- Python 3.8+
- Git
- 4GB RAM disponibile

### Setup

```bash
# 1. Clona il repository
git clone https://github.com/emanuelediluzio/previsione_mercati
cd previsione_mercati

# 2. Crea ambiente virtuale
python -m venv venv_previsione

# 3. Attiva ambiente virtuale
# Mac/Linux:
source venv_previsione/bin/activate
# Windows:
venv_previsione\Scripts\activate

# 4. Installa dipendenze
pip install -r requirements.txt
```

## 📁 Struttura Progetto

```
previsione_mercati/
├── previsione_prezzi_elettrici_reale.py    # Sistema principale
├── visualizza_previsioni_reali.py          # Visualizzazioni
├── requirements.txt                         # Dipendenze
├── GUIDA_CRISTIANO.md                      # Guida per cristiani
├── README_TECNICO.md                       # Questa guida
├── 2022_MGP.xlsx                          # Dati 2022
├── 2023_MGP.xlsx                          # Dati 2023
├── 2024_MGP.xlsx                          # Dati 2024
└── 2025_MGP.xlsx                          # Dati 2025
```

## 🎯 Utilizzo

### Esecuzione Base

```bash
# Esegui previsioni
python previsione_prezzi_elettrici_reale.py

# Visualizza risultati
python visualizza_previsioni_reali.py
```

### Output Generati

- `previsione_italia_trading_dati_reali.xlsx` - Previsioni dettagliate
- `previsioni_grafico_reali.png` - Grafici di analisi

## 🔧 Configurazione Avanzata

### Modifica Parametri Modello

```python
# In previsione_prezzi_elettrici_reale.py
model = XGBRegressor(
    n_estimators=200,          # Numero alberi
    learning_rate=0.03,         # Learning rate
    max_depth=6,                # Profondità massima
    subsample=0.8,              # Subsampling
    colsample_bytree=0.8,       # Feature sampling
    gamma=0.2,                  # Min split loss
    reg_lambda=1.5,             # L2 regularization
    reg_alpha=0.5,              # L1 regularization
    random_state=42,
    verbosity=0,
    early_stopping_rounds=20    # Early stopping
)
```

### Aggiungere Nuove Features

```python
# In crea_features_avanzate()
# Aggiungi nuove features temporali
df["Nuova_Feature"] = df["Prezzo"].rolling(window=12).std()

# Aggiungi features stagionali
df["Is_Weekend"] = (df["GiornoSettimana"] >= 5).astype(int)
```

## 📈 Interpretazione Risultati

### Metriche di Performance

- **MAE (Mean Absolute Error)**: Errore medio assoluto in €/MWh
- **RMSE (Root Mean Square Error)**: Errore quadratico medio
- **Precisione**: Accuratezza delle previsioni

### Analisi Temporale

- **Ore di Picco**: 4-7h (prezzi più alti)
- **Ore Migliori**: 1-11h (prezzi più bassi)
- **Giorni Migliori**: Sabato
- **Giorni Peggiori**: Lunedì

## 🔍 Troubleshooting

### Problemi Comuni

1. **Errore NumPy 2.x**
   ```bash
   pip install "numpy<2"
   ```

2. **File Excel non trovati**
   - Verifica percorso file
   - Controlla nomi file
   - Assicurati formato corretto

3. **Errore memoria**
   - Riduci n_estimators
   - Chiudi altre applicazioni
   - Usa subset dati

### Debug

```bash
# Verifica ambiente
python -c "import pandas, numpy, xgboost; print('OK')"

# Test caricamento dati
python -c "import pandas as pd; df = pd.read_excel('2022_MGP.xlsx'); print(df.head())"
```

## 🧪 Testing

### Test Automatico

```bash
# Esegui test base
python -c "
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
print('✅ Tutte le dipendenze funzionano')
"
```

### Validazione Dati

```python
# Verifica struttura dati
def validate_data(df):
    required_cols = ['Data', 'Ora', 'Italia']
    assert all(col in df.columns for col in required_cols)
    assert len(df) > 0
    assert df['Prezzo'].min() > 0
    print("✅ Dati validi")
```

## 📊 Analisi Avanzata

### Cross-Validation

```python
from sklearn.model_selection import cross_val_score

# Valida modello
scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
print(f"CV MAE: {-scores.mean():.2f} ± {scores.std():.2f}")
```

### Feature Importance

```python
# Analizza importanza features
importance = model.feature_importances_
feature_names = X.columns
for name, imp in zip(feature_names, importance):
    print(f"{name}: {imp:.4f}")
```

## 🔄 Aggiornamenti

### Mantenimento Sistema

1. **Aggiorna dati mensilmente**
2. **Rivalida modello trimestralmente**
3. **Monitora performance**
4. **Aggiorna dipendenze**

### Versioni

- **v1.0**: Sistema base con XGBoost
- **v1.1**: Features avanzate aggiunte
- **v1.2**: Gestione errori migliorata
- **v1.3**: Visualizzazioni complete

## 🤝 Contributi

### Come Contribuire

1. Fork del repository
2. Crea branch feature
3. Implementa miglioramenti
4. Testa modifiche
5. Submit pull request

### Linee Guida

- Segui PEP 8
- Documenta funzioni
- Aggiungi test
- Mantieni compatibilità

## 📄 Licenza

MIT License - vedi LICENSE per dettagli

## 📞 Supporto

- **Issues**: GitHub Issues
- **Documentazione**: README files
- **Community**: Forum tecnici

---

**Buon coding! 🚀⚡** 