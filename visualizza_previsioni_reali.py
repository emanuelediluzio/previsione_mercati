import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Configurazione per i grafici
plt.style.use('default')
sns.set_palette("husl")

def visualizza_previsioni_reali():
    """Visualizza le previsioni con dati reali"""
    
    # Carica i dati
    df = pd.read_excel('previsione_italia_trading_dati_reali.xlsx')
    df['Data'] = pd.to_datetime(df['Data'])
    df['DataOra'] = df['Data'] + pd.to_timedelta(df['Ora'] - 1, unit='h')
    
    # Crea figura con subplot
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('📊 Previsioni Prezzi Elettrici Italia - Dati Reali (2022-2025)', fontsize=16, fontweight='bold')
    
    # 1. Andamento temporale
    ax1 = axes[0, 0]
    ax1.plot(df['DataOra'], df['Prezzo_Previsto'], linewidth=2, color='#2E86AB')
    ax1.set_title('⚡ Andamento Prezzi nel Tempo', fontweight='bold')
    ax1.set_xlabel('Data e Ora')
    ax1.set_ylabel('Prezzo (€/MWh)')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Aggiungi statistiche
    ax1.axhline(y=df['Prezzo_Previsto'].mean(), color='red', linestyle='--', alpha=0.7, label=f'Media: {df["Prezzo_Previsto"].mean():.1f} €/MWh')
    ax1.legend()
    
    # 2. Distribuzione per ora del giorno
    ax2 = axes[0, 1]
    ore_stats = df.groupby('Ora')['Prezzo_Previsto'].mean()
    bars = ax2.bar(ore_stats.index, ore_stats.values, color='#A23B72', alpha=0.8)
    ax2.set_title('🕐 Prezzi Medi per Ora del Giorno', fontweight='bold')
    ax2.set_xlabel('Ora del Giorno')
    ax2.set_ylabel('Prezzo Medio (€/MWh)')
    ax2.grid(True, alpha=0.3)
    
    # Evidenzia ore di picco
    for i, (ora, prezzo) in enumerate(ore_stats.items()):
        if 8 <= ora <= 20:
            bars[i].set_color('#F18F01')
    
    # 3. Distribuzione per giorno settimana
    ax3 = axes[1, 0]
    giorni_stats = df.groupby('GiornoSettimana')['Prezzo_Previsto'].mean()
    giorni_nomi = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
    bars = ax3.bar(giorni_nomi, giorni_stats.values, color='#C73E1D', alpha=0.8)
    ax3.set_title('📅 Prezzi Medi per Giorno Settimana', fontweight='bold')
    ax3.set_xlabel('Giorno della Settimana')
    ax3.set_ylabel('Prezzo Medio (€/MWh)')
    ax3.grid(True, alpha=0.3)
    
    # 4. Box plot per ora del giorno
    ax4 = axes[1, 1]
    df_box = df.copy()
    df_box['Ora_Label'] = df_box['Ora'].astype(str) + 'h'
    sns.boxplot(data=df_box, x='Ora_Label', y='Prezzo_Previsto', ax=ax4, palette='Set3')
    ax4.set_title('📦 Distribuzione Prezzi per Ora', fontweight='bold')
    ax4.set_xlabel('Ora del Giorno')
    ax4.set_ylabel('Prezzo (€/MWh)')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('previsioni_grafico_reali.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Stampa statistiche dettagliate
    print("\n" + "="*60)
    print("📊 STATISTICHE DETTAGLIATE PREVISIONI (DATI REALI)")
    print("="*60)
    
    print(f"\n💰 PREZZI GENERALI:")
    print(f"   • Media: {df['Prezzo_Previsto'].mean():.2f} €/MWh")
    print(f"   • Mediana: {df['Prezzo_Previsto'].median():.2f} €/MWh")
    print(f"   • Massimo: {df['Prezzo_Previsto'].max():.2f} €/MWh")
    print(f"   • Minimo: {df['Prezzo_Previsto'].min():.2f} €/MWh")
    print(f"   • Deviazione Standard: {df['Prezzo_Previsto'].std():.2f} €/MWh")
    
    print(f"\n🕐 ORE DI PICCO (8-20):")
    peak_hours = df[df['Is_Peak_Hour'] == 1]['Prezzo_Previsto']
    print(f"   • Media ore di picco: {peak_hours.mean():.2f} €/MWh")
    print(f"   • Ore notturne: {df[df['Is_Night_Hour'] == 1]['Prezzo_Previsto'].mean():.2f} €/MWh")
    
    print(f"\n📅 GIORNI PIÙ COSTOSI:")
    giorni_costi = df.groupby('GiornoSettimana')['Prezzo_Previsto'].mean().sort_values(ascending=False)
    for i, (giorno, prezzo) in enumerate(giorni_costi.items()):
        nome_giorno = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica'][giorno]
        print(f"   {i+1}. {nome_giorno}: {prezzo:.2f} €/MWh")
    
    print(f"\n⏰ ORE PIÙ COSTOSE:")
    ore_costi = df.groupby('Ora')['Prezzo_Previsto'].mean().sort_values(ascending=False)
    for i, (ora, prezzo) in enumerate(ore_costi.head(5).items()):
        print(f"   {i+1}. Ore {ora}: {prezzo:.2f} €/MWh")
    
    print(f"\n💡 CONSIGLI OPERATIVI:")
    print(f"   • Migliori ore per consumo: {ore_costi.index[0]}-{ore_costi.index[1]}h")
    print(f"   • Peggiori ore per consumo: {ore_costi.index[-1]}-{ore_costi.index[-2]}h")
    print(f"   • Giorno migliore: {['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica'][giorni_costi.index[-1]]}")
    print(f"   • Giorno peggiore: {['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica'][giorni_costi.index[0]]}")
    
    print(f"\n📈 CONFRONTO CON DATI STORICI:")
    print(f"   • Prezzo medio previsto: {df['Prezzo_Previsto'].mean():.2f} €/MWh")
    print(f"   • Prezzo medio storico: 170.10 €/MWh")
    print(f"   • Differenza: {df['Prezzo_Previsto'].mean() - 170.10:.2f} €/MWh")
    print(f"   • Trend: {'📉 In calo' if df['Prezzo_Previsto'].mean() < 170.10 else '📈 In aumento'}")

if __name__ == "__main__":
    visualizza_previsioni_reali() 