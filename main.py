import streamlit as st
import matplotlib.pyplot as plt

# Titre de l'application
st.title("📈 Simulateur de placement financier")

# Barre latérale pour les paramètres
st.sidebar.header("Paramètres")
montant_initial = st.sidebar.number_input("Montant initial (€)", min_value=0, value=1000, step=100)
versement_mensuel = st.sidebar.number_input("Versement mensuel (€)", min_value=0, value=200, step=10)
taux_interet_annuel = st.sidebar.number_input("Taux d'intérêt annuel (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
duree_annees = st.sidebar.slider("Durée (années)", min_value=1, max_value=50, value=10)

# Calcul dynamique
def calcul_placement(montant_initial, versement_mensuel, taux_interet_annuel, duree_annees):
    mensualite = []
    interets = []
    solde = montant_initial
 
    if versement_mensuel == 0:
        # Cas sans versement : intérêts calculés annuellement
        for annee in range(1, duree_annees + 1):
            interet_annuel = solde * (taux_interet_annuel / 100)
            solde += interet_annuel
            mensualite.append(montant_initial)  # Les versements restent constants (montant initial)
            interets.append(solde - montant_initial)
    else:
        # Cas avec versements mensuels
        taux_mensuel = taux_interet_annuel / 12 / 100
        for mois in range(1, duree_annees * 12 + 1):
            interet_mensuel = solde * taux_mensuel
            solde += versement_mensuel + interet_mensuel
            mensualite.append(versement_mensuel * mois + montant_initial)
            interets.append(solde - mensualite[-1])

    return mensualite, interets, solde

# Résultats
mensualite, interets, capital_final = calcul_placement(montant_initial, versement_mensuel, taux_interet_annuel, duree_annees)

# Tracé des courbes (aire empilée)
fig, ax = plt.subplots(figsize=(10, 6))

if versement_mensuel == 0:
    annees = range(1, duree_annees + 1)
    ax.fill_between(annees, 0, mensualite, label="Versements", color="royalblue", alpha=0.6)
    ax.fill_between(annees, mensualite, [m + i for m, i in zip(mensualite, interets)], 
                    label="Intérêts", color="gold", alpha=0.6)
    ax.set_xlabel("Années", fontsize=12)
else:
    mois = range(1, duree_annees * 12 + 1)
    ax.fill_between(mois, 0, mensualite, label="Versements", color="royalblue", alpha=0.6)
    ax.fill_between(mois, mensualite, [m + i for m, i in zip(mensualite, interets)], 
                    label="Intérêts", color="gold", alpha=0.6)
    ax.set_xlabel("Mois", fontsize=12)

# Titre et labels
ax.set_title("Évolution du placement", fontsize=16, pad=20)
ax.set_ylabel("Montant (€)", fontsize=12)
ax.legend(loc="upper left", fontsize=12)

# Ligne des graduations
ax.grid(color="gray", linestyle="--", linewidth=0.5)

# Affichage du graphique
st.pyplot(fig)

# Résumé des résultats
st.write("### Résumé 📋")
st.write(f"- **Capital final :** {capital_final:,.2f} €")
st.write(f"- **Montant total des versements :** {mensualite[-1]:,.2f} €")
st.write(f"- **Montant total des intérêts générés :** {interets[-1]:,.2f} €")
