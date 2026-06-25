from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # permette alla demo locale e al sito ufficiale di chiamare l'API


# ---------------------------------------------------------
# 1) ENDPOINT DI STATO (homepage API)
# ---------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    """
    Endpoint pubblico di stato.
    Non contiene logica commerciale.
    Serve solo a mostrare che l'API è attiva.
    """
    return jsonify({
        "status": "online",
        "version": "6.2.0",
        "node": "Athens-01",
        "timestamp": datetime.utcnow().isoformat()
    })


# ---------------------------------------------------------
# 2) ENDPOINT DI ANALISI DIMOSTRATIVA
# ---------------------------------------------------------
@app.route("/calcola", methods=["POST"])
def calcola():
    """
    Questo endpoint viene chiamato dalla tua demo.
    Restituisce una simulazione parziale, NON una consulenza.
    Nessun prezzo, nessuna vendita, nessuna proposta commerciale.
    """
    data = request.get_json() or {}

    algoritmo = data.get("algoritmo", "RGD-ALPHA")
    budget = float(data.get("budget", 0) or 0)
    ore_assenze = float(data.get("ore_assenze", 0) or 0)
    standby_watt = float(data.get("standby_watt", 0) or 0)
    metri_quadri = float(data.get("metri_quadri", 0) or 0)
    num_dipendenti = int(data.get("num_dipendenti", 0) or 0)

    # ---------------------------------------------------------
    # MINI MODELLO DIMOSTRATIVO (SEMPLIFICATO)
    # ---------------------------------------------------------
    intensita_uso = 0
    if num_dipendenti > 0 and metri_quadri > 0:
        intensita_uso = (num_dipendenti / metri_quadri) * 100

    rischio_spreco = 0
    rischio_spreco += standby_watt * 0.02
    rischio_spreco += ore_assenze * 0.5
    if budget > 0:
        rischio_spreco += min(25, (budget / 10000) * 5)

    rischio_spreco = max(0, min(100, rischio_spreco))

    if rischio_spreco < 30:
        livello = "Basso"
        sintesi = "Il modello rileva un livello di spreco contenuto."
    elif rischio_spreco < 70:
        livello = "Medio"
        sintesi = "Il modello rileva margini di ottimizzazione interessanti."
    else:
        livello = "Alto"
        sintesi = "Il modello rileva un potenziale spreco energetico significativo."

    # ---------------------------------------------------------
    # RISULTATO PARZIALE (VETRINA)
    # ---------------------------------------------------------
    risultato_html = f"""
        <div style='font-size:0.95rem; line-height:1.6;'>
            <strong>Analisi dimostrativa RGandja</strong><br><br>

            <strong>Algoritmo:</strong> {algoritmo}<br>
            <strong>Budget indicativo:</strong> {budget:,.2f} €<br>
            <strong>Dipendenti:</strong> {num_dipendenti}<br>
            <strong>Superficie:</strong> {metri_quadri:,.0f} m²<br>
            <strong>Ore di assenza:</strong> {ore_assenze:,.1f} h<br>
            <strong>Consumo standby:</strong> {standby_watt:,.0f} W<br><br>

            <strong>Livello di spreco stimato:</strong> {livello} ({rischio_spreco:,.1f}%)<br>
            {sintesi}<br><br>

            <em>
                Nota: questa è una simulazione dimostrativa e non costituisce
                consulenza tecnica o proposta commerciale. Il sistema completo
                utilizza parametri aggiuntivi e modelli avanzati non inclusi
                nella versione di anteprima.
            </em>
        </div>
    """

    # ---------------------------------------------------------
    # PAYWALL (ATTIVA LA PARTE OSCURATA DELLA DEMO)
    # ---------------------------------------------------------
    return jsonify({
        "risultato": risultato_html,
        "is_premium_locked": True
    })


# ---------------------------------------------------------
# 3) AVVIO LOCALE (non usato su Render)
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

    @app.route("/report", methods=["POST"])
    def report():
        data = request.get_json() or {}
        email = data.get("email")
        messaggio = data.get("messaggio")

    # Qui puoi integrare un servizio email (es. SendGrid, SMTP)
    print(f"Richiesta report da: {email} - Messaggio: {messaggio}")

    return jsonify({
        "status": "ricevuto",
        "nota": "Il tuo messaggio è stato registrato. Il team RGandja ti contatterà per approfondire."
    })

