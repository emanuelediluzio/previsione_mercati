# ⚡ Sistema di Previsione Prezzi Elettrici Italia

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MAE](https://img.shields.io/badge/MAE-3.83%20€/MWh-brightgreen.svg)]()

Sistema di **Machine Learning** avanzato per la previsione dei prezzi dell'energia elettrica in Italia utilizzando dati storici del Mercato del Giorno Prima (MGP).

## 🎯 Caratteristiche Principali

- **🤖 Modello XGBoost ottimizzato** con 200 alberi
- **📊 21 features avanzate** (cicliche, lags, medie mobili)
- **🛡️ Gestione errori robusta** e validazione dati
- **🎯 Precisione elevata**: MAE < 4 €/MWh
- **📈 Visualizzazioni complete** con grafici e statistiche

## 📊 Performance

| Metrica | Valore |
|---------|--------|
| **MAE** | 3.83 €/MWh |
| **RMSE** | 5.55 €/MWh |
| **Dati processati** | 31,330 righe (2022-2025) |
| **Precisione** | 97.7% |

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
├── 📄 previsione_prezzi_elettrici_reale.py    # Sistema principale
├── 📊 visualizza_previsioni_reali.py          # Visualizzazioni
├── 📦 requirements.txt                        # Dipendenze
├── ⚡ README_TECNICO.md                       # Guida tecnica
├── 📈 2022_MGP.xlsx                           # Dati 2022
├── 📈 2023_MGP.xlsx                           # Dati 2023
├── 📈 2024_MGP.xlsx                           # Dati 2024
└── 📈 2025_MGP.xlsx                           # Dati 2025
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

## 📈 Risultati Esempio

### Previsioni per i Prossimi 7 Giorni
- **Prezzo medio previsto**: 113.96 €/MWh
- **Range**: 91.78 - 131.35 €/MWh
- **Trend**: 📉 In calo rispetto alla media storica

### Analisi Temporale
- **Ore di Picco**: 4-7h (prezzi più alti)
- **Ore Migliori**: 1-11h (prezzi più bassi)
- **Giorno migliore**: Sabato
- **Giorno peggiore**: Lunedì


## 🔍 Troubleshooting

### Problemi Comuni

1. **Errore NumPy 2.x**
   ```bash
   pip install "numpy<2"
   ```

2. **File Excel non trovati**
   - Verifica che i file Excel siano nella cartella corretta
   - Controlla i nomi dei file

3. **Errore di memoria**
   - Chiudi altre applicazioni
   - Riduci il numero di alberi nel modello


---

**"Ogni cosa che fate, fatela di cuore, come per il Signore e non per gli uomini"** - Colossesi 3:23

**Buon lavoro!**
