import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Configurazione CORS per consentire chiamate API dal frontend
CORS(app, resources={r"/*": {"origins": "*"}})


# ---------------------------------------------------------
# 1) ENDPOINT DI STATO (HEALTHCHECK)
# ---------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "status": "online",
            "version": "6.2.1",
            "node": "Athens-01",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


# ---------------------------------------------------------
# 2) ENDPOINT PER SERVIRE IL CONTENUTO DI MAIN
# ---------------------------------------------------------
@app.route("/api/v1/content/about", methods=["GET"])
def get_about_content():
    try:
        from main import html_content

        return jsonify({"status": "success", "html": html_content})
    except ImportError:
        # Corretto da 444 a 500 (HTTP Standard Internal Server Error)
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Modulo main non trovato o errore di importazione",
                }
            ),
            500,
        )


# ---------------------------------------------------------
# 3) ENDPOINT DI ANALISI DIMOSTRATIVA
# ---------------------------------------------------------
@app.route("/calcola", methods=["POST"])
def calcola():
    data = request.get_json() or {}

    algoritmo = str(data.get("algoritmo", "RGD-ALPHA"))
    try:
        budget = float(data.get("budget", 0) or 0)
        ore_assenze = float(data.get("ore_assenze", 0) or 0)
        standby_watt = float(data.get("standby_watt", 0) or 0)

        # Mappatura e ripiego per compatibilità sia con 'metri_quadri' che con 'volume_dati'/'volume-dati'
        metri_quadri = float(
            data.get("metri_quadri")
            or data.get("volume_dati")
            or data.get("volume-dati")
            or 0
        )
        num_dipendenti = int(data.get("num_dipendenti", 0) or 0)
    except (ValueError, TypeError):
        return jsonify({"error": "Parametri di calcolo non validi"}), 400

    intensita_uso = 0.0
    if num_dipendenti > 0 and metri_quadri > 0:
        intensita_uso = (num_dipendenti / metri_quadri) * 100

    rischio_spreco = (standby_watt * 0.02) + (ore_assenze * 0.5)
    if budget > 0:
        rischio_spreco += min(25.0, (budget / 10000.0) * 5.0)

    rischio_spreco = max(0.0, min(100.0, rischio_spreco))

    if rischio_spreco < 30:
        livello = "Basso"
        sintesi = "Il modello rileva un livello di spreco contenuto."
    elif rischio_spreco < 70:
        livello = "Medio"
        sintesi = "Il modello rileva margini di ottimizzazione interessanti."
    else:
        livello = "Alto"
        sintesi = "Il modello rileva un potenziale spreco energetico significativo."

    risultato_html = f"""
        <div style='font-size:0.95rem; line-height:1.6;'>
            <strong>Analisi Dimostrativa RGandja</strong><br><br>
            <strong>Algoritmo:</strong> {algoritmo}<br>
            <strong>Budget indicativo:</strong> {budget:,.2f} €<br>
            <strong>Dipendenti:</strong> {num_dipendenti}<br>
            <strong>Volume/Superficie:</strong> {metri_quadri:,.0f} unità/m²<br>
            <strong>Ore di assenza:</strong> {ore_assenze:,.1f} h<br>
            <strong>Consumo standby:</strong> {standby_watt:,.0f} W<br>
            <strong>Intensità d'uso:</strong> {intensita_uso:,.1f} ind/100m²<br><br>
            <strong>Livello di spreco stimato:</strong> {livello} ({rischio_spreco:,.1f}%)<br>
            {sintesi}<br><br>
            <em>Nota: simulazione generata dal motore euristico RGandja.</em>
        </div>
    """
    return jsonify(
        {
            "risultato": risultato_html,
            "is_premium_locked": True,
            "score": rischio_spreco,
        }
    )


# ---------------------------------------------------------
# 4) ENDPOINT REPORT (LEAD GENERATION CON CONTROLLO PRIVACY)
# ---------------------------------------------------------
@app.route("/report", methods=["POST"])
def report():
    data = request.get_json() or {}
    email = data.get("email")
    privacy_accepted = data.get("privacy_accepted", False)

    if not email:
        return (
            jsonify({"status": "error", "message": "Email obbligatoria"}),
            400,
        )

    # Verifica conformità GDPR se inviato via API
    if not privacy_accepted and data.get("check_privacy", True):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "È necessario accettare la Privacy Policy per continuare.",
                }
            ),
            422,
        )

    ragione_sociale = data.get("ragione_sociale", "N/D - Professionista/PMI")
    piano = data.get("piano_suggerito", "N/D")

    print("--- NUOVA RICHIESTA REPORT/DEMO RICEVUTA ---")
    print(f"Email: {email}")
    print(f"Contatto/Azienda: {ragione_sociale}")
    print(f"Piano Suggerito: {piano}")
    print(f"Consenso Privacy Accettato: {privacy_accepted}")
    print("--------------------------------------------")

    return jsonify(
        {
            "status": "success",
            "message": "Report demo e autorizzazione registrati con successo.",
            "nota": "Dati elaborati dal nodo Athens-01.",
        }
    )


# ---------------------------------------------------------
# 5) AVVIO UNICO
# ---------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
