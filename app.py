import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta

# Titre
st.title("📊 Simulateur d'investissement basé sur un actif")


# Dictionnaire des actifs avec leurs tickers
actifs = {
    "Or (Gold Spot USD)": "GC=F",
    "MSCI World (ETF)": "CW8.PA",
    "S&P 500 (ETF)": "SPY",
    "Nasdaq 100 (ETF)": "QQQ",
    "Dow Jones (ETF)": "DIA",
    "FTSE 100 (ETF)": "EWU",
    "CAC 40 (ETF)": "EWQ",
    "DAX 30 (ETF)": "EWG",
    "Euro Stoxx 50 (ETF)": "FEZ",
    "Nikkei 225 (ETF)": "EWJ",
    "Tesla (Action)": "TSLA",
    "Apple (Action)": "AAPL",
    "Amazon (Action)": "AMZN",
    "Microsoft (Action)": "MSFT",
    "Google (Action)": "GOOGL",
    "Meta (Action)": "META",
    "Intel (Action)": "INTC",
    "NVIDIA (Action)": "NVDA",
    "Pfizer (Action)": "PFE",
    "JPMorgan Chase (Action)": "JPM",
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Ripple (XRP)": "XRP-USD",
    "Cardano (ADA)": "ADA-USD",
    "Solana (SOL)": "SOL-USD",
    "Polkadot (DOT)": "DOT-USD",
    "Uniswap (UNI)": "UNI-USD",
    "Dogecoin (DOGE)": "DOGE-USD",
    "Avalanche (AVAX)": "AVAX-USD",
    "L'Oréal (CAC 40)": "OR.PA",
    "TotalEnergies (CAC 40)": "TTE.PA",
    "LVMH (CAC 40)": "MC.PA",
    "Airbus (CAC 40)": "AIR.PA",
    "Danone (CAC 40)": "BN.PA",
    "Kering (CAC 40)": "KER.PA",
    "BNP Paribas (CAC 40)": "BNP.PA",
    "Société Générale (CAC 40)": "GLE.PA",
    "AXA (CAC 40)": "CS.PA",
    "Engie (CAC 40)": "ENGI.PA",
    "Orange (CAC 40)": "ORA.PA",
    "Vivendi (CAC 40)": "VIV.PA",
    "Dassault Systèmes (CAC 40)": "DSY.PA",
    "Schneider Electric (CAC 40)": "SU.PA",
    "Saint-Gobain (CAC 40)": "SGO.PA",
    "Veolia (CAC 40)": "VEOEY.PA",
    "Michelin (CAC 40)": "ML.PA",
    "Carrefour (CAC 40)": "CA.PA",
    "Capgemini (CAC 40)": "CAP.PA",
    "Hermès (CAC 40)": "RMS.PA",
    "Renault (CAC 40)": "RNO.PA",
    "Bouygues (CAC 40)": "EN.PA",
    "Legrand (CAC 40)": "LR.PA",
    "STMicroelectronics (CAC 40)": "STM.PA",
}


actif = st.selectbox("Choisissez un actif", options=list(actifs.keys()))

# Barre latérale pour les paramètres
st.sidebar.header("Paramètres")
montant_initial = st.sidebar.number_input("Montant initial (€)", min_value=0, value=1000, step=100)
versement_mensuel = st.sidebar.number_input("Versement mensuel (€)", min_value=0, value=200, step=10)

# Période personnalisée
st.sidebar.subheader("Période d'investissement")
periode_rapide = st.sidebar.selectbox(
    "Sélectionnez une période rapide",
    options=["Personnalisée", "1 an", "2 ans", "5 ans", "10 ans"]
)
if periode_rapide == "Personnalisée":
    date_debut = st.sidebar.date_input("Date de début", value=date(2010, 1, 1), min_value=date(2000, 1, 1))
    date_fin = st.sidebar.date_input("Date de fin", value=date(2024, 12, 31), min_value=date_debut)
else:
    # Calculer les dates automatiquement
    date_fin = date.today()
    if periode_rapide == "1 an":
        date_debut = date_fin - timedelta(days=365)
    elif periode_rapide == "2 ans":
        date_debut = date_fin - timedelta(days=730)
    elif periode_rapide == "5 ans":
        date_debut = date_fin - timedelta(days=1825)
    elif periode_rapide == "10 ans":
        date_debut = date_fin - timedelta(days=3650)

def recuperer_donnees(actif, date_debut, date_fin):
    if actif in actifs:
        ticker = actifs[actif]
    else:
        st.error("Actif non reconnu.")
        return None

    # Récupération des données avec yfinance
    donnees = yf.download(ticker, start=date_debut, end=date_fin, interval="1mo")
    
    if donnees.empty:
        st.error("Aucune donnée récupérée pour cet actif.")
        return None

    # Vérifier les colonnes disponibles
    if 'Adj Close' in donnees.columns:
        donnees["Rendement"] = donnees["Adj Close"].pct_change()
    elif 'Close' in donnees.columns:
        donnees["Rendement"] = donnees["Close"].pct_change()
    else:
        st.error("Données insuffisantes pour calculer les rendements.")
        return None

    return donnees

# Calcul de l'évolution du capital
def calcul_placement_actif(montant_initial, versement_mensuel, donnees):
    capital = montant_initial
    historique_capital = [capital]
    historique_versements = [montant_initial]
    historique_interets = [0]
    dates = []

    # Itérer sur les rendements historiques
    rendements = donnees["Rendement"].iloc[1:]  # Exclure la première valeur NaN
    dates = rendements.index  # Extraire les dates des rendements

    for rendement in rendements:
        interets = capital * rendement
        capital += versement_mensuel + interets
        historique_capital.append(capital)
        historique_versements.append(historique_versements[-1] + versement_mensuel)
        historique_interets.append(capital - historique_versements[-1])

    return dates, historique_capital, historique_versements, historique_interets

# Affichage
donnees = recuperer_donnees(actif, date_debut, date_fin)
if donnees is not None and not donnees.empty:
    dates, historique_capital, historique_versements, historique_interets = calcul_placement_actif(
        montant_initial, versement_mensuel, donnees
    )

    # Créer le graphique interactif avec Plotly
    fig = go.Figure()
    
    # Ajout des aires empilées
    fig.add_trace(go.Scatter(
        x=dates,
        y=historique_versements,
        mode='lines',
        name='Versements',
        fill='tozeroy',
        line=dict(color='royalblue', width=2),
        hovertemplate='Versements: %{y:,.2f} €<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=historique_capital,
        mode='lines',
        name='Capital final',
        fill='tonexty',
        line=dict(color='gold', width=2),
        hovertemplate='Capital final: %{y:,.2f} €<extra></extra>'
    ))

    # Personnalisation du graphique
    fig.update_layout(
        title=f"Évolution de l'investissement sur {actif}",
        xaxis_title="Temps",
        yaxis_title="Montant (€)",
        xaxis=dict(tickformat="%b %Y"),
        hovermode="x unified",
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
        height=600
    )

    # Affichage du graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Résumé des résultats
    st.write("### Résumé 📋")
    st.write(f"- **Capital final :** {historique_capital[-1]:,.2f} €")
    st.write(f"- **Montant total des versements :** {historique_versements[-1]:,.2f} €")
    st.write(f"- **Montant total des intérêts générés :** {historique_interets[-1]:,.2f} €")
else:
    st.error("Impossible de récupérer les données ou période invalide.")
