import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def crea_file_esempio(nome_file, data_inizio, giorni):
    """Crea un file Excel di esempio con dati di prezzi elettrici"""
    
    # Genera date
    date_range = pd.date_range(start=data_inizio, periods=giorni*24, freq='H')
    
    # Genera dati
    dati = []
    for i, data in enumerate(date_range):
        # Prezzo base con stagionalità
        prezzo_base = 50 + 20 * np.sin(2 * np.pi * data.hour / 24)  # Variazione oraria
        prezzo_base += 10 * np.sin(2 * np.pi * data.dayofweek / 7)   # Variazione settimanale
        prezzo_base += 15 * np.sin(2 * np.pi * data.month / 12)      # Variazione mensile
        
        # Aggiungi rumore
        prezzo_base += np.random.normal(0, 5)
        
        # Assicurati che sia positivo
        prezzo_base = max(10, prezzo_base)
        
        dati.append({
            'Data': data.strftime('%d/%m/%Y'),
            'Ora': data.hour + 1,
            'Italia': f"{prezzo_base:.2f}".replace('.', ',')
        })
    
    # Crea DataFrame
    df = pd.DataFrame(dati)
    
    # Salva in Excel
    df.to_excel(nome_file, index=False)
    print(f"✅ Creato file: {nome_file} con {len(df)} righe")

# Crea i file di esempio
file_list = [
    ("20200701_20210701_MGP_PrezziZonali.xlsx", "2020-07-01", 365),
    ("20210701_20220701_MGP_PrezziZonali.xlsx", "2021-07-01", 365),
    ("20220701_20230701_MGP_PrezziZonali.xlsx", "2022-07-01", 365),
    ("20250716_20250716_MGP_PrezziZonali.xlsx", "2025-07-16", 1)
]

for nome_file, data_inizio, giorni in file_list:
    crea_file_esempio(nome_file, data_inizio, giorni)

print("\n🎉 Tutti i file di esempio sono stati creati!")
print("Ora puoi eseguire il sistema di previsione.") 