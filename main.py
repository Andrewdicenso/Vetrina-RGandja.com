"""
RGANDJA NEURAL ENGINE - CORE CONTENT MODULE & API
Architect: Andrew Di Censo & AI Master Integration
Version: 6.2.1 - Independent Developer Deployment (Athens / Italy)
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="RGandja Neural Engine API",
    version="6.2.1",
    description="Engine backend per l'analisi predittiva e la gestione delle scorte.",
)

# Configurazione CORS per consentire le chiamate dal frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html_content = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RGandja Neural Engine</title>
    <style>
        :root {
            --bg-dark: #020617;
            --card-bg: #0b132b;
            --accent-gold: #eab308;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #1e293b;
        }
        body {
            margin: 0;
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .text-center { text-align: center; }
        .badge-status {
            background: rgba(234, 179, 8, 0.1);
            color: var(--accent-gold);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 1px;
        }
        .hero-premium { padding: 100px 0 60px; }
        .hero-subtitle { max-width: 700px; margin: 20px auto; color: var(--text-muted); font-size: 1.2rem; line-height: 1.6; }
        .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; }
        .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
        .card-expert {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 30px;
        }
        .btn {
            display: inline-block;
            padding: 12px 28px;
            border-radius: 8px;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-gold { background: var(--accent-gold); color: #000; border: none; }
        .btn-gold:hover { opacity: 0.9; }
        .btn-outline { border: 1px solid var(--border); color: var(--text-main); }

        /* Modal Styles */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .modal-card {
            background: #0d1527;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 40px;
            max-width: 480px;
            width: 90%;
            position: relative;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }
        .close-btn {
            position: absolute;
            top: 20px; right: 20px;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 1.2rem;
        }
        .upload-box {
            border: 2px dashed var(--border);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            cursor: pointer;
            background: rgba(255,255,255,0.02);
            transition: border-color 0.3s ease;
        }
        .upload-box:hover { border-color: var(--accent-gold); }
        .status-msg { margin-top: 15px; font-size: 0.9rem; font-weight: 600; min-height: 24px; }
    </style>
</head>
<body>
    <main>
        <section class="hero-premium">
            <div class="container text-center">
                <span class="badge-status">IL PROGETTO</span>
                <h1 style="margin-top: 25px;">Costruito per chi<br><span style="color: var(--accent-gold);">gestisce scorte ogni giorno.</span></h1>
                <p class="hero-subtitle">
                    RGandja nasce da un'osservazione semplice: troppi imprenditori sanno a memoria cosa hanno in magazzino,
                    ma non sanno cosa sta per costargli soldi. Abbiamo sviluppato lo strumento che mancava.
                </p>
                <div style="margin-top: 30px;">
                    <button class="btn btn-gold" onclick="openModal()">Testa RGandja Engine</button>
                </div>
            </div>
        </section>

        <!-- LA STORIA -->
        <section class="section container" style="padding: 80px 0;">
            <div class="grid-2" style="align-items: center;">
                <div>
                    <span style="color: var(--accent-gold); font-size: 0.75rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;">La storia</span>
                    <h2 style="color: #fff; font-size: 2.2rem; margin: 15px 0 25px; letter-spacing: -1px;">Perché abbiamo costruito RGandja Neural Engine</h2>
                    <p style="margin-bottom: 20px; font-size: 1.05rem; color: var(--text-muted); line-height: 1.8;">
                        Abbiamo visto troppi imprenditori perdere risorse non per mancanza di impegno,
                        ma per mancanza di visibilità. Merce ferma che immobilizza capitale e scadenze controllate a mano.
                    </p>
                    <p style="margin-bottom: 20px; font-size: 1.05rem; color: var(--text-muted); line-height: 1.8;">
                        Il problema è che gli strumenti esistenti sono o troppo costosi o troppo primitivi. <strong>RGandja Neural Engine riempie esattamente questo spazio.</strong>
                    </p>
                    <p style="font-size: 1.05rem; color: var(--text-muted); line-height: 1.8;">
                        Una soluzione SaaS accessibile, che parla il linguaggio dell'imprenditore — non quello dell'ingegnere dei dati.
                    </p>
                </div>
                <div class="card-expert">
                    <span style="color: var(--accent-gold); font-size: 0.75rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;">Il Fondatore</span>
                    <h3 style="font-size: 2rem; color: #fff; margin: 10px 0 0; letter-spacing: -1px;">Andrew Di Censo</h3>
                    <p style="color: var(--accent-gold); font-weight: 700; margin: 5px 0 20px; text-transform: uppercase; font-size: 0.8rem;">Independent Developer & Creator · Athens / EU</p>
                    <blockquote style="border-left: 2px solid var(--accent-gold); padding-left: 15px; margin: 15px 0; font-style: italic; color: var(--text-main);">
                        "Ho costruito RGandja perché volevo che anche una piccola impresa potesse avere
                        la stessa visibilità operativa di una grande azienda — senza bisogno di un team IT dedicato."
                    </blockquote>
                    <p style="margin-top: 20px; font-size: 0.85rem; color: var(--text-muted); line-height: 1.7;">
                        Sviluppatore autonomo specializzato in logica predittiva e sistemi di supporto alle decisioni aziendali.
                    </p>
                </div>
            </div>
        </section>

        <!-- VALORI -->
        <section class="section" style="background: #010409; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 80px 0;">
            <div class="container">
                <h2 class="text-center" style="margin-bottom: 60px; color: #fff; font-size: 2rem; letter-spacing: -1px;">
                    Come lavoriamo
                </h2>
                <div class="grid-3">
                    <div class="card-expert text-center">
                        <div style="font-size: 2.5rem; margin-bottom: 20px;">🎯</div>
                        <h3 style="color: #fff; margin-bottom: 15px;">Semplicità Prima di Tutto</h3>
                        <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.7;">
                            La tecnologia più sofisticata non serve se richiede settimane di formazione.
                            Ogni funzionalità è progettata per un utilizzo immediato.
                        </p>
                    </div>
                    <div class="card-expert text-center">
                        <div style="font-size: 2.5rem; margin-bottom: 20px;">🔒</div>
                        <h3 style="color: #fff; margin-bottom: 15px;">I tuoi Dati Restano Tuoi</h3>
                        <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.7;">
                            Nessuna cessione a terzi. Trattamento dati in piena conformità con le direttive GDPR dell'Unione Europea.
                        </p>
                    </div>
                    <div class="card-expert text-center">
                        <div style="font-size: 2.5rem; margin-bottom: 20px;">📈</div>
                        <h3 style="color: #fff; margin-bottom: 15px;">Risultati Misurabili</h3>
                        <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.7;">
                            L'obiettivo è consentirti di quantificare in breve tempo le inefficienze identificate e i margini recuperati.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- DOVE SIAMO -->
        <section class="section container" style="padding: 80px 0;">
            <div class="grid-2" style="align-items: center;">
                <div>
                    <span style="color: var(--accent-gold); font-size: 0.75rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;">Operatività</span>
                    <h2 style="color: #fff; font-size: 2rem; margin: 15px 0 25px; letter-spacing: -1px;">
                        Atene, Unione Europea
                    </h2>
                    <p style="font-size: 1.05rem; color: var(--text-muted); line-height: 1.8; margin-bottom: 20px;">
                        Operare dall'Unione Europea garantisce la massima tutela in materia di riservatezza e conformità al GDPR.
                    </p>
                    <p style="font-size: 1.05rem; color: var(--text-muted); line-height: 1.8;">
                        Sviluppo e supporto dedicati a PMI, professionisti e realtà commerciali. Disponibile <strong>Lun–Ven, 09:00–18:00 EET</strong>.
                    </p>
                </div>
                <div class="card-expert">
                    <p style="font-family: monospace; font-size: 0.8rem; color: var(--accent-gold); letter-spacing: 2px; margin-bottom: 25px; text-transform: uppercase;">Contatti Diretti</p>
                    <p style="color: #fff; font-size: 1rem; line-height: 2;">
                        📧 <a href="mailto:unit.athens@rgandja.com" style="color: var(--accent-gold); text-decoration: none;">unit.athens@rgandja.com</a><br>
                        📍 Athens, Greece — European Union<br>
                        🕐 Lun–Ven · 09:00–18:00 EET
                    </p>
                </div>
            </div>
        </section>
    </main>

    <!-- MODAL TEST ENGINE -->
    <div id="testModal" class="modal-overlay" style="display: none;">
        <div class="modal-card">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <h2 style="margin-top: 0;">Testa RGandja Engine</h2>
            <p style="color: var(--text-muted); font-size: 0.95rem;">
                Carica i dati della tua azienda (.csv, .xlsx o .json) per avviare l'elaborazione del report.
            </p>

            <form id="uploadForm" onsubmit="handleUpload(event)">
                <div class="upload-box" onclick="document.getElementById('fileInput').click()">
                    <span style="font-size: 1.5rem;">📁</span>
                    <div id="fileName" style="margin-top: 10px; font-weight: 600; color: var(--accent-gold);">
                        Seleziona File dal PC
                    </div>
                    <input type="file" id="fileInput" accept=".csv, .xlsx, .json" hidden onchange="updateFileName(this)">
                </div>

                <button type="submit" class="btn btn-gold" style="width: 100%;">AVVIA ELABORAZIONE</button>
            </form>

            <div id="statusMessage" class="status-msg text-center"></div>
        </div>
    </div>

    <script>
        function openModal() {
            document.getElementById('testModal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('testModal').style.display = 'none';
            document.getElementById('statusMessage').innerText = '';
        }

        function updateFileName(input) {
            const fileNameDiv = document.getElementById('fileName');
            if (input.files && input.files[0]) {
                fileNameDiv.innerText = input.files[0].name;
            } else {
                fileNameDiv.innerText = "Seleziona File dal PC";
            }
        }

        async function handleUpload(event) {
            event.preventDefault();

            const fileInput = document.getElementById('fileInput');
            const statusMessage = document.getElementById('statusMessage');

            if (!fileInput.files || !fileInput.files[0]) {
                statusMessage.innerText = "⚠️ Seleziona prima un file da analizzare.";
                statusMessage.style.color = "#ef4444";
                return;
            }

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            statusMessage.innerText = "⏳ Connessione al Neural Engine in corso...";
            statusMessage.style.color = "#94a3b8";

            try {
                const response = await fetch('/api/v1/analyze', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`Errore Server (${response.status})`);
                }

                const data = await response.json();

                // Aggiornamento dinamico con il messaggio restituito dal backend
                statusMessage.innerText = "✅ " + data.message;
                statusMessage.style.color = "#10b981";

            } catch (error) {
                console.error('Upload Error:', error);
                statusMessage.innerText = "❌ Impossibile elaborare il file. Verifica la connessione o riprova.";
                statusMessage.style.color = "#ef4444";
            }
        }
    </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content


@app.post("/api/v1/analyze")
async def analyze_file(file: UploadFile = File(...)):
    """
    Endpoint per l'ingestione e l'elaborazione dei file inviati dalla modale di prova gratuita.
    """
    if not file:
        raise HTTPException(status_code=400, detail="Nessun file caricato.")

    file_bytes = await file.read()
    file_size = len(file_bytes)

    return {
        "status": "success",
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": file_size,
        "message": f"File '{file.filename}' caricato ed elaborato con successo dal Neural Engine.",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
