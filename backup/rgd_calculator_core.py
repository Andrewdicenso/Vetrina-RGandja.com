"""
RGD SIMULATION & ENERGY HEURISTIC CORE
Isolato dal monolite legacy per il riuso indipendente in architetture software esterne.
"""


def compute_heuristic_simulation(data: dict) -> dict:
    algoritmo = str(data.get("algoritmo", "RGD-ALPHA"))

    try:
        budget = float(data.get("budget", 0) or 0)
        ore_assenze = float(data.get("ore_assenze", 0) or 0)
        standby_watt = float(data.get("standby_watt", 0) or 0)

        metri_quadri = float(
            data.get("metri_quadri")
            or data.get("volume_dati")
            or data.get("volume-dati")
            or 0
        )
        num_dipendenti = int(data.get("num_dipendenti", 0) or 0)
    except (ValueError, TypeError) as e:
        raise ValueError(
            "Parametri di calcolo non validi o non convertibili in numerici."
        ) from e

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

    return {
        "risultato": risultato_html,
        "is_premium_locked": True,
        "score": rischio_spreco,
        "livello": livello,
    }
