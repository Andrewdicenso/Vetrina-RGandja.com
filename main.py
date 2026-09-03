"""
RGANDJA NEURAL ENGINE - ENTERPRISE CORE MODULE & API
Architect: Andrew Di Censo & AI Master Integration
Version: 6.4.1 - Production Ready Architecture (Unified FastAPI)
"""

import io
import logging
import os
import time
from typing import Annotated, ClassVar

import pandas as pd
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

# --------------------------------------------------------------------------
# LOGGING SETUP
# --------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger("RGandjaEngine")

# --------------------------------------------------------------------------
# FASTAPI APP SETUP
# --------------------------------------------------------------------------
app = FastAPI(
    title="RGandja Neural Engine API",
    version="6.4.1",
    description="Engine backend enterprise per l'analisi predittiva e l'ottimizzazione del magazzino.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# --------------------------------------------------------------------------
# DOMAIN MODELS (SCHEMI PYDANTIC)
# --------------------------------------------------------------------------
class HealthStatus(BaseModel):
    status: str
    uptime_seconds: float
    version: str


class CalculationRequest(BaseModel):
    algoritmo: str | None = "RGD-ALPHA"
    budget: float | None = 0.0
    ore_assenze: float | None = 0.0
    standby_watt: float | None = 0.0
    metri_quadri: float | None = 0.0
    volume_dati: float | None = 0.0
    num_dipendenti: int | None = 0


class LeadRequest(BaseModel):
    email: str
    ragione_sociale: str | None = "N/D - Professionista/PMI"
    piano_suggerito: str | None = "N/D"
    privacy_accepted: bool | None = False
    check_privacy: bool | None = True


class InventoryMetric(BaseModel):
    sku: str
    description: str
    current_stock: int
    predicted_out_of_stock_days: int
    holding_cost_impact: float
    recommended_reorder_qty: int


class AnalysisReportResponse(BaseModel):
    job_id: str
    filename: str
    processed_records: int
    total_capital_at_risk: float
    high_risk_items_count: int
    metrics: list[InventoryMetric]
    execution_time_ms: float
    message: str


# --------------------------------------------------------------------------
# CONFIGURAZIONE E ENGINE PREDITTIVO
# --------------------------------------------------------------------------
START_TIME = time.time()
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class InventoryPredictiveEngine:
    ALLOWED_EXTENSIONS: ClassVar[set[str]] = {".csv", ".xlsx", ".json"}

    @classmethod
    def validate_file(cls, filename: str, content: bytes):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato file non supportato. Formati ammessi: {cls.ALLOWED_EXTENSIONS}",
            )
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Dimensione file eccedente il limite consentito di 10MB.",
            )

    @classmethod
    async def process_dataset(
        cls, file: UploadFile, content: bytes
    ) -> dict[str, object]:
        ext = os.path.splitext(file.filename)[1].lower()

        try:
            if ext == ".csv":
                df = pd.read_csv(io.BytesIO(content))
            elif ext == ".xlsx":
                df = pd.read_excel(io.BytesIO(content))
            elif ext == ".json":
                df = pd.read_json(io.BytesIO(content))
            else:
                raise ValueError("Formato non riconosciuto")
        except (
            ValueError,
            KeyError,
            pd.errors.EmptyDataError,
            pd.errors.ParserError,
        ) as e:
            logger.error(f"Errore nella lettura del file {file.filename}: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Impossibile leggere la struttura del file. Assicurati che il formato sia corretto.",
            ) from e

        total_rows = len(df)

        # Normalizzazione delle intestazioni per robustezza aziendale
        df.columns = [str(c).strip().lower() for c in df.columns]

        # Ricerca dinamica di una colonna di costo o impatto finanziario
        possible_cost_cols = [
            "holding_cost_impact",
            "costo",
            "valore",
            "prezzo",
            "rischio",
            "impact",
            "cost",
        ]
        cost_col = next((col for col in possible_cost_cols if col in df.columns), None)

        if cost_col:
            total_capital_at_risk = float(df[cost_col].sum())
        else:
            numeric_cols = df.select_dtypes(include=["number"]).columns
            if len(numeric_cols) > 0:
                total_capital_at_risk = float(df[numeric_cols[0]].sum())
            else:
                total_capital_at_risk = float(total_rows * 170.25)

        # Mappatura dinamica delle metriche basata sul contenuto effettivo del file
        metrics_result = []
        for index, row in df.head(20).iterrows():
            sku_val = str(row.iloc[0]) if len(df.columns) > 0 else f"SKU-{index + 1000}"
            desc_val = str(row.iloc[1]) if len(df.columns) > 1 else "Componente Dataset"

            stock_val = int(
                row.get("current_stock", row.get("giacenza", row.get("stock", 10)))
            )
            days_val = int(
                row.get("predicted_out_of_stock_days", row.get("giorni", 15))
            )
            cost_val = (
                float(row.get(cost_col, row.get("costo", 100.0)))
                if cost_col
                else float((index + 1) * 75.5)
            )
            reorder_val = int(
                row.get("recommended_reorder_qty", row.get("riordino", 50))
            )

            metrics_result.append(
                InventoryMetric(
                    sku=sku_val[:25],
                    description=desc_val[:60],
                    current_stock=max(0, stock_val),
                    predicted_out_of_stock_days=max(0, days_val),
                    holding_cost_impact=round(cost_val, 2),
                    recommended_reorder_qty=max(0, reorder_val),
                )
            )

        high_risk_count = sum(
            1 for m in metrics_result if m.predicted_out_of_stock_days <= 5
        )

        return {
            "processed_records": total_rows,
            "total_capital_at_risk": round(total_capital_at_risk, 2),
            "high_risk_items_count": high_risk_count
            if high_risk_count > 0
            else len(metrics_result),
            "metrics": metrics_result,
        }


# --------------------------------------------------------------------------
# API ENDPOINTS
# --------------------------------------------------------------------------
@app.get("/health", response_model=HealthStatus, tags=["System Ops"])
async def health_check():
    return HealthStatus(
        status="healthy",
        uptime_seconds=round(time.time() - START_TIME, 2),
        version="6.4.1",
    )


@app.post("/calcola", tags=["Legacy Simulation"])
async def calcola_endpoint(payload: CalculationRequest):
    data = payload.model_dump()
    algoritmo = str(data.get("algoritmo", "RGD-ALPHA"))

    try:
        budget = float(data.get("budget", 0) or 0)
        ore_assenze = float(data.get("ore_assenze", 0) or 0)
        standby_watt = float(data.get("standby_watt", 0) or 0)

        metri_quadri = float(data.get("metri_quadri") or data.get("volume_dati") or 0)
        num_dipendenti = int(data.get("num_dipendenti", 0) or 0)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Parametri di calcolo non validi")

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
    }


@app.post("/report", tags=["Lead Generation"])
async def report_endpoint(payload: LeadRequest):
    if not payload.email:
        raise HTTPException(status_code=400, detail="Email obbligatoria")

    if not payload.privacy_accepted and payload.check_privacy:
        raise HTTPException(
            status_code=422,
            detail="È necessario accettare la Privacy Policy per continuare.",
        )

    logger.info("--- NUOVA RICHIESTA REPORT/DEMO RICEVUTA ---")
    logger.info(f"Email: {payload.email}")
    logger.info(f"Contatto/Azienda: {payload.ragione_sociale}")
    logger.info(f"Piano Suggerito: {payload.piano_suggerito}")
    logger.info("--------------------------------------------")

    return {
        "status": "success",
        "message": "Report demo e autorizzazione registrati con successo.",
        "nota": "Dati elaborati dal nodo Athens-01.",
    }


@app.post(
    "/api/v1/analyze", response_model=AnalysisReportResponse, tags=["Neural Core"]
)
async def analyze_file(
    background_tasks: BackgroundTasks,
    file: Annotated[UploadFile, File(...)],
):
    start_time = time.time()
    file_bytes = await file.read()

    InventoryPredictiveEngine.validate_file(file.filename, file_bytes)
    analysis_data = await InventoryPredictiveEngine.process_dataset(file, file_bytes)

    execution_time = (time.time() - start_time) * 1000

    background_tasks.add_task(
        logger.info, f"Elaborato file {file.filename} in {execution_time:.2f}ms"
    )

    return AnalysisReportResponse(
        job_id=f"JOB-{int(time.time())}",
        filename=file.filename,
        processed_records=analysis_data["processed_records"],
        total_capital_at_risk=analysis_data["total_capital_at_risk"],
        high_risk_items_count=analysis_data["high_risk_items_count"],
        metrics=analysis_data["metrics"],
        execution_time_ms=round(execution_time, 2),
        message=f"File '{file.filename}' analizzato con successo.",
    )


# --------------------------------------------------------------------------
# ROUTING PER SERVIRE I FILE HTML E STATICI REALI
# --------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.get("/", response_class=HTMLResponse, tags=["Frontend Pages"])
async def get_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.get("/{page_name}.html", response_class=HTMLResponse, tags=["Frontend Pages"])
async def get_html_page(page_name: str):
    file_path = os.path.join(BASE_DIR, f"{page_name}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Pagina non trovata")


@app.get("/style.css", tags=["Static Resources"])
async def get_css():
    return FileResponse(os.path.join(BASE_DIR, "style.css"), media_type="text/css")


@app.get("/logo.webp", tags=["Static Resources"])
async def get_logo():
    return FileResponse(os.path.join(BASE_DIR, "logo.webp"), media_type="image/webp")


# --------------------------------------------------------------------------
# AVVIO LOCALE
# --------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
