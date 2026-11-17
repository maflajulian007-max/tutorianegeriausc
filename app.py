import streamlit as st
import json
import random
import re
from openai import OpenAI

# =====================================================
# 1. CONFIGURACIÓN GENERAL Y CREDENCIALES (NVIDIA NIM)
# =====================================================

st.set_page_config(
    page_title="TutorIA Ingeniería | USC Santiago de Cali",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_KEY = "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"
MODELO_NVIDIA = "nvidia/nemotron-3.5-lightning-30b-a3b"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=API_KEY
)

# =====================================================
# 2. ESTILOS DARK MODE OLED + TARJETAS DE OPCIONES A/B/C/D
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #09090b;
    color: #fafafa;
}

section[data-testid="stSidebar"] {
    display: none;
}

div[data-testid="stRadio"] > div[role="radiogroup"] {
    gap: 12px;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    background-color: #111114;
    border: 1px solid #27272a;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 0 !important;
    transition: all 0.15s ease;
    cursor: pointer;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    border-color: #fb7185;
    background-color: #16161a;
}

div[data-testid="stRadio"] label,
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p,
.stTextInput label,
.stMultiSelect label,
.stSelectbox label,
.stSlider label {
    color: #f4f4f5 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

.badge-ods {
    display: inline-block;
    background-color: rgba(244, 63, 94, 0.16);
    color: #fda4af;
    border: 1px solid rgba(244, 63, 94, 0.4);
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 600;
    margin-right: 10px;
}
.badge-topic {
    display: inline-block;
    background-color: rgba(99, 102, 241, 0.16);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 600;
}
.badge-diff {
    display: inline-block;
    background-color: #18181b;
    color: #d4d4d8;
    border: 1px solid #27272a;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 600;
}
.subtitle-top {
    color: #a1a1aa;
    font-size: 13px;
}

.uni-box {
    background-color: #111114;
    border: 1px solid #27272a;
    border-radius: 12px;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.uni-icon {
    background-color: rgba(244, 63, 94, 0.16);
    color: #fb7185;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.knowledge-card {
    background-color: #111114;
    border: 1px solid #27272a;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 12px;
}
.knowledge-card-done {
    background-color: #111114;
    border: 1px solid rgba(34, 197, 94, 0.45);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 12px;
}
.card-top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}
.card-icon-box-red {
    background-color: rgba(244, 63, 94, 0.15);
    border: 1px solid rgba(244, 63, 94, 0.35);
    color: #fb7185;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.card-pill {
    background-color: #18181b;
    border: 1px solid #27272a;
    color: #d4d4d8;
    font-size: 11.5px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 999px;
}
.card-pill-done {
    background-color: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #4ade80;
    font-size: 11.5px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
}
.card-title {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}
.card-desc {
    font-size: 13.5px;
    color: #a1a1aa;
    line-height: 1.5;
    min-height: 78px;
    margin-bottom: 14px;
}
.card-divider {
    border: 0;
    border-top: 1px solid #27272a;
    margin: 12px 0;
}
.card-meta-row {
    display: flex;
    justify-content: space-between;
    font-size: 12.5px;
    margin-bottom: 6px;
}
.meta-label { color: #71717a; }
.meta-val-white { color: #e4e4e7; font-weight: 600; }
.meta-val-red { color: #fb7185; font-weight: 600; }
.meta-val-green { color: #4ade80; font-weight: 600; }

.stButton > button[kind="primary"] {
    background-color: #e11d48;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 16px;
}
.stButton > button[kind="primary"]:hover {
    background-color: #be123c;
    color: #ffffff;
}
.stButton > button[kind="secondary"] {
    background-color: #111114 !important;
    color: #e4e4e7 !important;
    border: 1px solid #27272a !important;
    border-radius: 10px;
}
.stButton > button[kind="secondary"]:hover {
    background-color: #18181b !important;
    color: #ffffff !important;
    border-color: #fb7185 !important;
}
.stButton > button:disabled {
    background-color: #0f0f12 !important;
    color: #52525b !important;
    border: 1px solid #1f1f23 !important;
    cursor: not-allowed !important;
}

.dark-panel {
    background-color: #111114;
    border: 1px solid #27272a;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
}
.question-card {
    background-color: #111114;
    border: 1px solid #27272a;
    border-radius: 16px;
    padding: 26px 28px;
    margin-bottom: 16px;
}
.flashcard-box {
    background: linear-gradient(145deg, #111114 0%, #18181b 100%);
    border: 1px solid #3f3f46;
    border-radius: 16px;
    padding: 32px 28px;
    text-align: center;
    margin: 12px 0;
}
.nvidia-status-pill {
    color: #34d399;
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. FUNCIONES CON CLIENTE OPENAI (NVIDIA NIM)
# =====================================================

def extraer_json_seguro(raw_text, es_lista=True):
    raw_text = re.sub(r"^```json\s*", "", raw_text, flags=re.IGNORECASE)
    raw_text = re.sub(r"^```\s*", "", raw_text)
    raw_text = re.sub(r"\s*```$", "", raw_text).strip()
    
    patron = r'\[.*\]' if es_lista else r'\{.*\}'
    match = re.search(patron, raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError(f"No se pudo extraer un JSON válido de la respuesta de la IA: {raw_text[:120]}...")

def llamar_ia_profesor(titulo_evaluacion, descripcion_temas, cantidad):
    semilla = random.randint(100000, 999999)
    prompt = f"""
    Actúa como profesor titular de ingeniería en la Universidad Santiago de Cali (USC).
    Crea un examen formal de opción múltiple con exactamente {cantidad} preguntas sobre: {titulo_evaluacion}.
    Temas a evaluar: {descripcion_temas}.
    Usa la semilla aleatoria #{semilla} para garantizar que las preguntas sean completamente nuevas e inéditas.
    
    DEVUELVE ÚNICAMENTE UN JSON VÁLIDO en forma de lista de objetos, sin bloques de código Markdown ni texto adicional fuera del JSON:
    [
        {{
            "pregunta": "Enunciado formal del problema o concepto...",
            "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],
            "correcta": "El texto exacto de la opción correcta",
            "tema": "{titulo_evaluacion}",
            "explicacion": "Explicación teórica detallada de la solución"
        }}
    ]
    """
    
    completion = client.chat.completions.create(
        model=MODELO_NVIDIA,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        top_p=0.95,
        max_tokens=4096,
        seed=semilla,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": True},
            "reasoning_budget": 2048
        },
        stream=False
    )
    
    raw_text = completion.choices[0].message.content.strip()
    preguntas = extraer_json_seguro(raw_text, es_lista=True)
    
    for p in preguntas:
        random.shuffle(p["opciones"])
    return preguntas[:cantidad]

def generar_set_area(area):
    if area == "Matemáticas":
        return llamar_ia_profesor(
            "Matemáticas para Ingeniería",
            "Diagnóstico de precálculo, funciones, trigonometría, álgebra lineal elemental y límites para ingeniería.",
            6
        )
    elif area == "Ingeniería":
        return llamar_ia_profesor(
            "Fundamentos de Ingeniería",
            "Evaluación de pensamiento computacional, análisis dimensional, unidades del SI y balance de masa elemental.",
            6
        )
    else:
        return llamar_ia_profesor(
            "Algoritmos y Programación 1",
            "Estructuras de control condicionales, bucles while/for, arreglos y funciones en programación.",
            6
        )

def generar_set_integral():
    return llamar_ia_profesor(
        "Diagnóstico Integral de Ingeniería",
        "Evaluación global de matemáticas, fundamentos de ingeniería y programación de primer semestre.",
        20
    )

def generar_flashcard_ia():
    prompt = """
    Genera una flashcard académica para ingeniería de primer semestre en formato JSON puro con los campos 'tema', 'frente' y 'reverso':
    {
        "tema": "Tema de primer semestre",
        "frente": "Pregunta conceptual clave",
        "reverso": "Definición formal exacta"
    }
    """
    completion = client.chat.completions.create(
        model=MODELO_NVIDIA,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        top_p=0.95,
        max_tokens=1024,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": True},
            "reasoning_budget": 1024
        },
        stream=False
    )
    
    raw_text = completion.choices[0].message.content.strip()
    try:
        return extraer_json_seguro(raw_text, es_lista=False)
    except:
        return {
            "tema": "Fundamentos de Ingeniería",
            "frente": "¿Qué es un sistema?",
            "reverso": "Conjunto de elementos interrelacionados que buscan un objetivo común."
        }

def evaluar_set(lista_preguntas, respuestas_dict):
    resultados = []
    puntajes = {}
    for i, pregunta in enumerate(lista_preguntas):
        respuesta = respuestas_dict.get(i, None)
        correcta = (respuesta == pregunta["correcta"])
        tema = pregunta.get("tema", "General")

        if tema not in puntajes:
            puntajes[tema] = {"aciertos": 0, "total": 0}
        puntajes[tema]["total"] += 1
        if correcta:
            puntajes[tema]["aciertos"] += 1

        resultados.append({
            "pregunta": pregunta["pregunta"],
            "respuesta": respuesta,
            "correcta": pregunta["correcta"],
            "acierto": correcta,
            "tema": tema,
            "area": pregunta.get("area", "General"),
            "explicacion": pregunta["explicacion"]
        })
    return resultados, puntajes

def iniciar_prueba(nombre_prueba):
    st.session_state.prueba_activa = nombre_prueba
    try:
        with st.spinner("⚡ Generando examen con Nemotron 3.5 Lightning (30B A3B)..."):
            if nombre_prueba == "Integral":
                st.session_state.preguntas_actuales = generar_set_integral()
            else:
                st.session_state.preguntas_actuales = generar_set_area(nombre_prueba)
        st.session_state.indice_pregunta = 0
        st.session_state.respuestas_wizard = {}
        st.session_state.vista = "Ejecutar Prueba"
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error al conectar con la IA de NVIDIA: {str(e)}")

# =====================================================
# 4. ESTADO DE SESIÓN Y REINICIO TOTAL
# =====================================================

def reiniciar_todo():
    st.session_state.vista = "Inicio"
    st.session_state.prueba_activa = "Matemáticas"
    st.session_state.preguntas_actuales = []
    st.session_state.indice_pregunta = 0
    st.session_state.respuestas_wizard = {}
    st.session_state.evaluaciones_iniciales = {
        "Matemáticas": None,
        "Ingeniería": None,
        "Programación": None
    }
    st.session_state.resultado_integral = None
    st.session_state.ultimo_reporte_clave = None
    st.session_state.examen_generado = None
    st.session_state.resultado_examen_custom = None
    st.session_state.fc_aciertos_bloque = 0
    st.session_state.fc_total_bloque = 0
    st.session_state.mostrar_retro_bloque = False
    st.session_state.mostrar_respuesta_fc = False
    try:
        st.session_state.fc_actual = generar_flashcard_ia()
    except:
        st.session_state.fc_actual = {
            "tema": "Ingeniería",
            "frente": "¿Qué es un sistema?",
            "reverso": "Conjunto de elementos interrelacionados que buscan un objetivo común."
        }

if "vista" not in st.session_state:
    reiniciar_todo()
    st.session_state.nombre = ""

completadas_base = sum(1 for v in st.session_state.evaluaciones_iniciales.values() if v is not None)
integral_completado = (st.session_state.resultado_integral is not None)
total_oficiales_completadas = completadas_base + (1 if integral_completado else 0)
todo_completado = (total_oficiales_completadas == 4)

# =====================================================
# 5. ENCABEZADO INSTITUCIONAL USC (SOLO ODS 4)
# =====================================================

col_head_izq, col_head_der = st.columns([2.2, 1])

with col_head_izq:
    st.markdown("""
<div style="margin-bottom: 10px;">
<span class="badge-ods">ODS 4: Educación con Calidad</span>
<span class="subtitle-top">Primer Semestre • Ingeniería</span>
</div>
<h1 style="font-size: 38px; font-weight: 800; letter-spacing: -0.8px; margin: 0 0 8px 0; padding: 0; color: #ffffff;">TutorIA Ingeniería USC</h1>
<p style="color: #a1a1aa; font-size: 15px; margin: 0;">Plataforma de evaluación formal con IA generativa en tiempo real.</p>
""", unsafe_allow_html=True)

with col_head_der:
    st.markdown("""
<div class="uni-box">
<div class="uni-icon">
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
<path d="M6 12v5c3 3 9 3 12 0v-5"/>
</svg>
</div>
<div>
<div style="font-weight: 700; font-size: 14px; color: #fafafa;">Universidad Santiago de Cali</div>
<div style="font-size: 12px; color: #71717a;">Facultad de Ingeniería • Demostrador IA</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 0; border-top: 1px solid #27272a; margin: 22px 0 18px 0;'>", unsafe_allow_html=True)

# =====================================================
# 6. ENRUTAMIENTO DE VISTAS
# =====================================================

vista = st.session_state.vista

if vista == "Inicio":
    st.markdown("<h3 style='font-size: 20px; font-weight: 700; color: #ffffff; margin-bottom: 14px;'>Menú Principal de Opciones</h3>", unsafe_allow_html=True)

    b1, b2, b3, b4, b5 = st.columns(5)

    with b1:
        if st.button("Zona de Evaluaciones", type="primary", use_container_width=True):
            st.session_state.vista = "Menu Evaluaciones"
            st.rerun()
    with b2:
        if st.button("Resultados", type="secondary", use_container_width=True):
            st.session_state.vista = "Resultados"
            st.rerun()
    with b3:
        etiqueta_plan_menu = "Plan de Nivelación" if todo_completado else f"🔒 Plan de Nivelación ({total_oficiales_completadas}/4)"
        if st.button(etiqueta_plan_menu, type="secondary", disabled=not todo_completado, use_container_width=True):
            st.session_state.vista = "Plan de Nivelacion"
            st.rerun()
    with b4:
        if st.button("Examen con IA", type="secondary", use_container_width=True):
            st.session_state.vista = "Generar Examen Custom"
            st.rerun()
    with b5:
        if st.button("Flashcards Infinitas", type="secondary", use_container_width=True):
            st.session_state.vista = "Laboratorio Flashcards"
            st.rerun()

    st.write("")
    st.markdown("<hr style='border: 0; border-top: 1px solid #27272a; margin: 22px 0;'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dark-panel" style="text-align: center; padding: 32px;">
        <div class="nvidia-status-pill">
            <span style="width: 8px; height: 8px; background-color: #34d399; border-radius: 50%; display: inline-block;"></span>
            IA de NVIDIA Activa (Nemotron 3.5 Lightning 30B)
        </div>
        <h3 style="color: #ffffff; margin-top: 8px;">Ecosistema Académico USC</h3>
        <p style="color: #a1a1aa; max-width: 700px; margin: 0 auto 16px auto;">Cada examen y tarjeta de estudio se crea de forma completamente aleatoria e inédita mediante el SDK de OpenAI con NVIDIA NIM.</p>
        <p style="color: #fb7185; font-weight: 600;">Progreso Oficial: {total_oficiales_completadas} / 4 Evaluaciones completadas</p>
    </div>
    """, unsafe_allow_html=True)

elif vista == "Menu Evaluaciones":
    c_ret, c_res_tot = st.columns([1.5, 3])
    with c_ret:
        if st.button("←  Ir al Inicio", type="secondary", use_container_width=True):
            st.session_state.vista = "Inicio"
            st.rerun()
    with c_res_tot:
        if st.button("🔄 Reiniciar Todo el Progreso", type="secondary", use_container_width=True):
            reiniciar_todo()
            st.session_state.nombre = ""
            st.rerun()

    st.write("")
    st.markdown(f"""
    <div class="dark-panel" style="padding: 16px 20px; margin-bottom: 10px;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
    <span style="font-weight:700; font-size:15px; color:#ffffff;">Zona Unificada de Evaluaciones Oficiales USC</span>
    <span style="font-weight:700; font-size:14px; color:#fb7185;">Progreso Total: {total_oficiales_completadas} / 4</span>
    </div>
    <p style="font-size:13px; color:#a1a1aa; margin:0;">Apartados basados en los temas oficiales del curso (6 preguntas aleatorias c/u). Diagnóstico Integral (20 preguntas).</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(total_oficiales_completadas / 4)

    if todo_completado:
        st.success("🎉 ¡Has completado las 4 evaluaciones! Ya puedes ingresar a **Plan de Nivelación** desde el inicio.")

    st.markdown("<h3 style='font-size: 21px; font-weight: 700; margin: 18px 0; color: #ffffff;'>Selecciona un Apartado</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    # APARTADO 1: MATEMÁTICAS
    with col1:
        eval_mat = st.session_state.evaluaciones_iniciales["Matemáticas"]
        clase_card = "knowledge-card-done" if eval_mat else "knowledge-card"
        pill_html = f"<span class='card-pill-done'>✓ {eval_mat['porcentaje']:.0f}%</span>" if eval_mat else "<span class='card-pill'>6 preguntas</span>"
        btn_txt = "✓ Completado" if eval_mat else "Iniciar Evaluación  →"

        st.markdown(f"""
<div class="{clase_card}">
<div class="card-top-row">
<div class="card-icon-box-red">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
<path d="M18 4a3 3 0 0 0-3 3v10a3 3 0 0 1-3 3"/>
<path d="M6 12h12"/>
<path d="M9 8l3-4 3 4"/>
</svg>
</div>
{pill_html}
</div>
<div class="card-title">1. Matemáticas para Ingeniería</div>
<div class="card-desc">Diagnóstico de precálculo, funciones, trigonometría y límites.</div>
<hr class="card-divider">
<div class="card-meta-row"><span class="meta-label">Estructura:</span><span class="meta-val-white">6 Preguntas</span></div>
</div>
""", unsafe_allow_html=True)
        if st.button(btn_txt, key="btn_area_mat", type="primary", disabled=(eval_mat is not None), use_container_width=True):
            iniciar_prueba("Matemáticas")

    # APARTADO 2: INGENIERÍA
    with col2:
        eval_ing = st.session_state.evaluaciones_iniciales["Ingeniería"]
        clase_card = "knowledge-card-done" if eval_ing else "knowledge-card"
        pill_html = f"<span class='card-pill-done'>✓ {eval_ing['porcentaje']:.0f}%</span>" if eval_ing else "<span class='card-pill'>6 preguntas</span>"
        btn_txt = "✓ Completado" if eval_ing else "Iniciar Evaluación  →"

        st.markdown(f"""
<div class="{clase_card}">
<div class="card-top-row">
<div class="card-icon-box-red">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>
</svg>
</div>
{pill_html}
</div>
<div class="card-title">2. Fundamentos de Ingeniería</div>
<div class="card-desc">Pensamiento computacional, análisis dimensional y unidades del SI.</div>
<hr class="card-divider">
<div class="card-meta-row"><span class="meta-label">Estructura:</span><span class="meta-val-white">6 Preguntas</span></div>
</div>
""", unsafe_allow_html=True)
        if st.button(btn_txt, key="btn_area_ing", type="primary", disabled=(eval_ing is not None), use_container_width=True):
            iniciar_prueba("Ingeniería")

    # APARTADO 3: PROGRAMACIÓN
    with col3:
        eval_prog = st.session_state.evaluaciones_iniciales["Programación"]
        clase_card = "knowledge-card-done" if eval_prog else "knowledge-card"
        pill_html = f"<span class='card-pill-done'>✓ {eval_prog['porcentaje']:.0f}%</span>" if eval_prog else "<span class='card-pill'>6 preguntas</span>"
        btn_txt = "✓ Completado" if eval_prog else "Iniciar Evaluación  →"

        st.markdown(f"""
<div class="{clase_card}">
<div class="card-top-row">
<div class="card-icon-box-red">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
<polyline points="4 17 10 11 4 5"/>
</svg>
</div>
{pill_html}
</div>
<div class="card-title">3. Algoritmos y Programación 1</div>
<div class="card-desc">Estructuras de control condicionales, bucles while/for y arreglos.</div>
<hr class="card-divider">
<div class="card-meta-row"><span class="meta-label">Estructura:</span><span class="meta-val-white">6 Preguntas</span></div>
</div>
""", unsafe_allow_html=True)
        if st.button(btn_txt, key="btn_area_prog", type="primary", disabled=(eval_prog is not None), use_container_width=True):
            iniciar_prueba("Programación")

    # DIAGNÓSTICO INTEGRAL (20 PREGUNTAS)
    with col4:
        eval_int = st.session_state.resultado_integral
        clase_card = "knowledge-card-done" if eval_int else "knowledge-card"
        pill_html = f"<span class='card-pill-done'>✓ {eval_int['porcentaje']:.0f}%</span>" if eval_int else "<span class='card-pill' style='border-color:#fb7185; color:#fda4af;'>20 preguntas</span>"
        btn_txt = "✓ Completado" if eval_int else "Iniciar Integral  →"

        st.markdown(f"""
<div class="{clase_card}">
<div class="card-top-row">
<div class="card-icon-box-red">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
</svg>
</div>
{pill_html}
</div>
<div class="card-title">Diagnóstico Integral</div>
<div class="card-desc">Evaluación global avanzada con 20 reactivos aleatorios de todo el semestre.</div>
<hr class="card-divider">
<div class="card-meta-row"><span class="meta-label">Estructura:</span><span class="meta-val-red">20 Preguntas</span></div>
</div>
""", unsafe_allow_html=True)
        if st.button(btn_txt, key="btn_area_integral", type="primary", disabled=(eval_int is not None), use_container_width=True):
            iniciar_prueba("Integral")

elif vista == "Ejecutar Prueba":
    prueba = st.session_state.prueba_activa
    preguntas = st.session_state.preguntas_actuales
    total_q = len(preguntas)
    idx_q = st.session_state.indice_pregunta
    q_actual = preguntas[idx_q]

    c_top1, c_top2 = st.columns([3.2, 1])
    with c_top1:
        titulo_p = "Diagnóstico Integral (20 Preguntas)" if prueba == "Integral" else f"Evaluación Apartado: {prueba} (6 Preguntas)"
        st.markdown(f"<h3 style='font-size: 22px; font-weight: 700; color: #ffffff; margin:0;'>{titulo_p}</h3>", unsafe_allow_html=True)
    with c_top2:
        if st.button("← Volver a Zona de Evaluaciones", type="secondary", use_container_width=True):
            st.session_state.vista = "Menu Evaluaciones"
            st.rerun()

    st.write("")
    nombre = st.text_input("Nombre completo del estudiante:", value=st.session_state.nombre, placeholder="Ej. Camila Rodríguez")
    if nombre.strip():
        st.session_state.nombre = nombre.strip()

    st.markdown(f"""
<div class="question-card">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
<span class="badge-topic">{q_actual.get('tema', prueba)}</span>
<span class="badge-diff">Pregunta {idx_q + 1} de {total_q} • Examen Parcial USC</span>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"#### {q_actual['pregunta']}")

    letras = ["A", "B", "C", "D"]
    opciones_formateadas = [f"{letras[i]}   |   {op}" for i, op in enumerate(q_actual["opciones"])]

    respuesta_guardada = st.session_state.respuestas_wizard.get(idx_q, None)
    indice_preseleccionado = None
    if respuesta_guardada in q_actual["opciones"]:
        indice_preseleccionado = q_actual["opciones"].index(respuesta_guardada)

    seleccion_radio = st.radio(
        "Elige una respuesta para continuar:",
        opciones_formateadas,
        index=indice_preseleccionado,
        key=f"wizard_radio_{prueba}_{idx_q}",
        label_visibility="collapsed"
    )

    if seleccion_radio is not None:
        texto_limpio = seleccion_radio.split("   |   ", 1)[1]
        st.session_state.respuestas_wizard[idx_q] = texto_limpio

    ya_respondida = (idx_q in st.session_state.respuestas_wizard)

    st.markdown("<hr style='border: 0; border-top: 1px solid #27272a; margin: 22px 0 16px 0;'>", unsafe_allow_html=True)

    col_prev, col_nums, col_next = st.columns([1.2, 2.6, 1.4])

    with col_prev:
        if st.button("←  Anterior", disabled=(idx_q == 0), use_container_width=True):
            st.session_state.indice_pregunta -= 1
            st.rerun()

    with col_nums:
        cols_pildoras = st.columns(min(total_q, 10))
        for n_i in range(total_q):
            if total_q > 10 and abs(n_i - idx_q) > 4 and n_i != 0 and n_i != total_q - 1:
                continue
            with cols_pildoras[n_i % len(cols_pildoras)]:
                respondida_n = (n_i in st.session_state.respuestas_wizard)
                es_actual = (n_i == idx_q)
                puede_ir = respondida_n or es_actual or (n_i == idx_q + 1 and ya_respondida)
                if st.button(
                    f"{n_i + 1}",
                    key=f"pill_q_{n_i}",
                    type="primary" if es_actual else "secondary",
                    disabled=not puede_ir,
                    use_container_width=True
                ):
                    st.session_state.indice_pregunta = n_i
                    st.rerun()

    with col_next:
        es_ultima = (idx_q == total_q - 1)
        if not es_ultima:
            if st.button("Siguiente  →", type="primary", disabled=not ya_respondida, use_container_width=True):
                st.session_state.indice_pregunta += 1
                st.rerun()
        else:
            if st.button("Finalizar Prueba  →", type="primary", disabled=not ya_respondida, use_container_width=True):
                if not st.session_state.nombre.strip():
                    st.warning("⚠️ Escribe tu nombre arriba antes de finalizar.")
                else:
                    resultados, puntajes = evaluar_set(preguntas, st.session_state.respuestas_wizard)
                    total_ok = sum(1 for r in resultados if r["acierto"])
                    porc = (total_ok / len(resultados)) * 100

                    if prueba == "Integral":
                        st.session_state.resultado_integral = {
                            "titulo": "Diagnóstico Integral (20 Preguntas)",
                            "resultados": resultados,
                            "puntajes": puntajes,
                            "porcentaje": porc,
                            "aciertos": total_ok,
                            "total": len(resultados)
                        }
                        st.session_state.ultimo_reporte_clave = "Integral"
                    else:
                        st.session_state.evaluaciones_iniciales[prueba] = {
                            "titulo": f"Evaluación Apartado: {prueba}",
                            "resultados": resultados,
                            "puntajes": puntajes,
                            "porcentaje": porc,
                            "aciertos": total_ok,
                            "total": len(resultados)
                        }
                        st.session_state.ultimo_reporte_clave = prueba

                    st.session_state.vista = "Resultados"
                    st.rerun()

elif vista == "Resultados":
    col_r_eval, col_r_home, col_r_reset = st.columns([1.5, 1.3, 1.2])
    with col_r_eval:
        if st.button("← Zona de Evaluaciones", type="primary", use_container_width=True):
            st.session_state.vista = "Menu Evaluaciones"
            st.rerun()
    with col_r_home:
        if st.button("⌂ Ir al Inicio", type="secondary", use_container_width=True):
            st.session_state.vista = "Inicio"
            st.rerun()
    with col_r_reset:
        if st.button("🔄 Reiniciar Todo", key="reset_en_resultados", type="secondary", use_container_width=True):
            reiniciar_todo()
            st.session_state.nombre = ""
            st.rerun()

    st.write("")
    st.markdown("<h3 style='font-size: 22px; font-weight: 700; color: #ffffff; text-align:center;'>Informe de Desempeño USC</h3>", unsafe_allow_html=True)

    reportes_disponibles = {}
    for area_nombre, data in st.session_state.evaluaciones_iniciales.items():
        if data is not None:
            reportes_disponibles[area_nombre] = data
    if st.session_state.resultado_integral is not None:
        reportes_disponibles["Integral"] = st.session_state.resultado_integral

    if not reportes_disponibles:
        st.info("Aún no has presentado ninguna evaluación.")
    else:
        claves = list(reportes_disponibles.keys())
        idx_defecto = claves.index(st.session_state.ultimo_reporte_clave) if st.session_state.ultimo_reporte_clave in claves else 0
        seleccion = st.selectbox("Selecciona un apartado para revisar:", claves, index=idx_defecto)
        reporte = reportes_disponibles[seleccion]

        resultados = reporte["resultados"]
        puntajes = reporte["puntajes"]
        porcentaje = reporte["porcentaje"]
        total_correctas = reporte["aciertos"]
        total_reactivos = reporte["total"]
        nivel = "Óptimo" if porcentaje >= 80 else ("Nivelación" if porcentaje >= 40 else "Alerta")

        st.write(f"Estudiante: **{st.session_state.nombre}** • Apartado: **{reporte['titulo']}**")

        c1, c2, c3 = st.columns(3)
        c1.metric("Puntaje", f"{porcentaje:.1f}%")
        c2.metric("Correctas", f"{total_correctas} / {total_reactivos}")
        c3.metric("Nivel", nivel)

        st.progress(porcentaje / 100)

        for i, res in enumerate(resultados):
            with st.expander(f"Reactivo {i+1} [{res['tema']}]: {'✓ CORRECTO' if res['acierto'] else '✗ INCORRECTO'}"):
                st.write(res['pregunta'])
                st.write(f"Tu respuesta: {res['respuesta']}")
                st.info(f"Respuesta correcta: {res['correcta']}")
                st.markdown(f"**Explicación:** {res['explicacion']}")

elif vista == "Plan de Nivelacion":
    if st.button("← Ir al Inicio", type="primary"):
        st.session_state.vista = "Inicio"
        st.rerun()

    st.write("")
    if not todo_completado:
        st.warning(f"🔒 El Plan de Nivelación requiere completar los 3 apartados y el integral ({total_oficiales_completadas}/4).")
    else:
        st.markdown("<h3 style='font-size: 24px; font-weight: 700; color: #ffffff;'>Plan de Nivelación Organizado por Semanas (USC)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#a1a1aa;'>Ruta de estudio adaptativa y detallada basada en tu desempeño oficial.</p>", unsafe_allow_html=True)

        todos_resultados = []
        puntajes_globales = {}

        for area_nombre, data in st.session_state.evaluaciones_iniciales.items():
            todos_resultados.extend(data["resultados"])
            for tema, d in data["puntajes"].items():
                if tema not in puntajes_globales:
                    puntajes_globales[tema] = {"aciertos": 0, "total": 0}
                puntajes_globales[tema]["aciertos"] += d["aciertos"]
                puntajes_globales[tema]["total"] += d["total"]

        todos_resultados.extend(st.session_state.resultado_integral["resultados"])
        for tema, d in st.session_state.resultado_integral["puntajes"].items():
            if tema not in puntajes_globales:
                puntajes_globales[tema] = {"aciertos": 0, "total": 0}
            puntajes_globales[tema]["aciertos"] += d["aciertos"]
            puntajes_globales[tema]["total"] += d["total"]

        temas_con_falla = [tema for tema, d in puntajes_globales.items() if (d["aciertos"] / d["total"]) < 1]

        if not temas_con_falla:
            st.success("🌟 ¡Excelente trabajo! Tienes un rendimiento óptimo en todos los temas evaluados.")
        else:
            for idx, tema in enumerate(temas_con_falla):
                st.markdown(f"""
                <div class="dark-panel">
                    <h4 style="color:#fb7185; margin:0;">📅 Semana {idx + 1} — Plan de Repaso: {tema}</h4>
                    <p style="color:#e4e4e7; margin-top:8px;"><b>Objetivo:</b> Consolidar bases teóricas y resolver ejercicios prácticos guiados para superar las brechas detectadas en la evaluación.</p>
                    <ul style="color:#a1a1aa; font-size:13.5px; margin-bottom:0;">
                        <li>Sesión 1: Repaso conceptual y resolución de ejemplos clave.</li>
                        <li>Sesión 2: Práctica intensiva con ejercicios propuestos por la IA.</li>
                        <li>Sesión 3: Autoevaluación y comprobación de conceptos dominados.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

elif vista == "Generar Examen Custom":
    if st.button("← Ir al Inicio", type="primary"):
        st.session_state.vista = "Inicio"
        st.rerun()

    st.write("")
    st.markdown("<h3 style='font-size: 24px; font-weight: 700; color: #ffffff;'>Práctica Libre: Examen con IA</h3>", unsafe_allow_html=True)
    
    temas_sel = st.multiselect("Temas USC:", ["Matemáticas para Ingeniería", "Fundamentos de Ingeniería", "Algoritmos y Programación 1"], default=["Matemáticas para Ingeniería", "Algoritmos y Programación 1"])
    num_p = st.slider("Cantidad de preguntas:", 3, 10, 5)

    if st.button("Generar Examen con IA  →", type="primary"):
        try:
            with st.spinner("⚡ Conectando con IA de NVIDIA (Nemotron 3.5 Lightning)..."):
                st.session_state.examen_generado = llamar_ia_profesor("Práctica Libre", ", ".join(temas_sel), num_p)
                st.session_state.resultado_examen_custom = None
                st.success("¡Examen generado con éxito mediante IA!")
                st.rerun()
        except Exception as e:
            st.error(f"❌ Error al generar examen: {str(e)}")

    if st.session_state.examen_generado:
        st.markdown("<hr style='border: 0; border-top: 1px solid #27272a; margin: 20px 0;'>", unsafe_allow_html=True)
        respuestas_custom = {}
        for i, p in enumerate(st.session_state.examen_generado):
            st.markdown(f"**{i+1}. {p['pregunta']}**")
            sel = st.radio("Opciones:", p["opciones"], key=f"ex_custom_{i}")
            respuestas_custom[i] = sel

        if st.button("Calificar Examen Custom 📝", type="primary"):
            correctas_c = 0
            detalle_custom = []
            for i, p in enumerate(st.session_state.examen_generado):
                user_ans = respuestas_custom.get(i)
                es_ok = (user_ans == p["correcta"])
                if es_ok:
                    correctas_c += 1
                detalle_custom.append((p, user_ans, es_ok))
            
            st.session_state.resultado_examen_custom = {
                "correctas": correctas_c,
                "total": len(st.session_state.examen_generado),
                "detalle": detalle_custom
            }
            st.rerun()

    if st.session_state.get("resultado_examen_custom"):
        res_c = st.session_state.resultado_examen_custom
        st.markdown(f"""
        <div class="dark-panel" style="border: 1px solid #34d399; text-align: center; padding: 20px; margin-top: 20px;">
            <h3 style="color: #ffffff;">Resultados de Práctica Libre</h3>
            <p style="color: #4ade80; font-size: 18px; font-weight: 700;">Aciertos: {res_c['correctas']} / {res_c['total']} ({(res_c['correctas']/res_c['total'])*100:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)

        for i, (p, user_ans, es_ok) in enumerate(res_c["detalle"]):
            estado_txt = "✓ Correcto" if es_ok else "✗ Incorrecto"
            color_est = "#4ade80" if es_ok else "#fb7185"
            with st.expander(f"Pregunta {i+1}: {estado_txt}"):
                st.write(f"**Enunciado:** {p['pregunta']}")
                st.write(f"Tu respuesta: {user_ans}")
                st.markdown(f"<span style='color:{color_est};'>Respuesta correcta: {p['correcta']}</span>", unsafe_allow_html=True)
                st.info(f"**Explicación:** {p['explicacion']}")

elif vista == "Laboratorio Flashcards":
    if st.button("← Ir al Inicio", type="primary"):
        st.session_state.vista = "Inicio"
        st.rerun()

    st.write("")
    st.markdown("<h3 style='font-size: 24px; font-weight: 700; color: #ffffff;'>Tarjetas de Estudio Activo (Flashcards con IA)</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#a1a1aa;'>Tarjeta <b>{(st.session_state.fc_total_bloque % 10) + 1}</b> de 10</p>", unsafe_allow_html=True)

    if st.session_state.mostrar_retro_bloque:
        st.markdown(f"""
<div class="dark-panel" style="border: 2px solid #fb7185; text-align: center; padding: 24px;">
<h3 style="color: #ffffff;">📊 Retroalimentación del Bloque</h3>
<p style="color: #4ade80; font-size: 16px;">Aciertos: {st.session_state.fc_aciertos_bloque} / 10</p>
</div>
""", unsafe_allow_html=True)
        if st.button("Siguiente Bloque  →", type="primary"):
            st.session_state.fc_aciertos_bloque = 0
            st.session_state.fc_total_bloque = 0
            st.session_state.mostrar_retro_bloque = False
            st.rerun()
    else:
        tarjeta = st.session_state.fc_actual
        st.markdown(f"""
<div class="flashcard-box">
<span class="badge-ods">{tarjeta['tema']}</span>
<h3 style="margin-top: 16px; color: #ffffff;">{tarjeta['frente']}</h3>
</div>
""", unsafe_allow_html=True)

        if st.session_state.mostrar_respuesta_fc:
            st.success(f"**Solución:** {tarjeta['reverso']}")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✓ La dominé", type="primary", use_container_width=True):
                    st.session_state.fc_aciertos_bloque += 1
                    st.session_state.fc_total_bloque += 1
                    if st.session_state.fc_total_bloque % 10 == 0:
                        st.session_state.mostrar_retro_bloque = True
                    else:
                        try:
                            with st.spinner("⚡ Generando siguiente tarjeta con IA de NVIDIA..."):
                                st.session_state.fc_actual = generar_flashcard_ia()
                            st.session_state.mostrar_respuesta_fc = False
                        except Exception as e:
                            st.error(f"Error: {e}")
                    st.rerun()
            with c2:
                if st.button("✗ Fallé", type="secondary", use_container_width=True):
                    st.session_state.fc_total_bloque += 1
                    if st.session_state.fc_total_bloque % 10 == 0:
                        st.session_state.mostrar_retro_bloque = True
                    else:
                        try:
                            with st.spinner("⚡ Generando siguiente tarjeta con IA de NVIDIA..."):
                                st.session_state.fc_actual = generar_flashcard_ia()
                            st.session_state.mostrar_respuesta_fc = False
                        except Exception as e:
                            st.error(f"Error: {e}")
                    st.rerun()
        else:
            if st.button("Voltear Tarjeta  →", type="primary", use_container_width=True):
                st.session_state.mostrar_respuesta_fc = True
                st.rerun()
