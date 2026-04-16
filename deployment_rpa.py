import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Evaluador de Madurez de Automatización")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stAppViewContainer"] { background-color: #05080c; }
        .block-container {
            padding-top: 0rem; padding-bottom: 0rem;
            padding-left: 0rem; padding-right: 0rem;
            max-width: 100%;
        }
        .stDeployButton { display:none; }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
#  REEMPLAZA ESTA URL con la que Google Apps Script te dé
#  al hacer el deploy (ver instrucciones en apps_script.gs)
# ──────────────────────────────────────────────────────────
APPS_SCRIPT_URL = "https://script.google.com/a/macros/krugercorporation.com/s/AKfycby7LpzDbDtkzHLSShviKHm78bIMSqjX-gsQ7083goCPUCa52sc-Iqf0X_DCAHu1Tu7H6Q/exec"

codigo_html = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
  *{{box-sizing:border-box;margin:0;padding:0}}
  :root{{
    --k-bg:#05080c;--k-card:rgba(15,23,42,0.85);--k-cyan:#00e5ff;--k-orange:#ff5a00;
    --k-cyan-dim:rgba(0,229,255,0.12);--k-orange-dim:rgba(255,90,0,0.12);
    --k-border:rgba(255,255,255,0.07);--k-text:#e2e8f0;--k-muted:#64748b;
  }}
  #app{{font-family:'Outfit',sans-serif;background:#05080c;min-height:600px;color:#e2e8f0;overflow:hidden;position:relative}}
  canvas#particles{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}}
  .glow-orb{{position:absolute;border-radius:50%;pointer-events:none;z-index:0;transition:all 1.5s ease}}
  .g1{{width:500px;height:500px;top:-20%;left:-15%;background:radial-gradient(circle,rgba(0,229,255,0.07),transparent 70%);animation:drift1 8s ease-in-out infinite}}
  .g2{{width:400px;height:400px;bottom:-15%;right:-10%;background:radial-gradient(circle,rgba(255,90,0,0.06),transparent 70%);animation:drift2 10s ease-in-out infinite}}
  @keyframes drift1{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(30px,-30px)}}}}
  @keyframes drift2{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-20px,20px)}}}}
  .screen{{position:relative;z-index:1;padding:2rem;min-height:600px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
  .glass{{background:rgba(15,23,42,0.75);border:1px solid rgba(255,255,255,0.07);backdrop-filter:blur(16px);border-radius:20px}}
  /* ── INTRO ── */
  .logo-mark{{display:inline-flex;align-items:center;gap:8px;margin-bottom:1.5rem;font-size:13px;font-weight:600;color:var(--k-cyan);letter-spacing:2px;text-transform:uppercase;opacity:0.7}}
  .logo-mark::before,.logo-mark::after{{content:'';display:inline-block;width:6px;height:6px;background:var(--k-cyan);border-radius:50%}}
  h1.hero{{font-size:clamp(2rem,5vw,3rem);font-weight:800;line-height:1.1;margin-bottom:1rem}}
  .gradient-text{{background:linear-gradient(135deg,var(--k-cyan),#4f8eff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
  .orange-text{{background:linear-gradient(135deg,var(--k-orange),#ff9500);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
  .intro-desc{{color:var(--k-muted);font-size:1.05rem;line-height:1.6;margin-bottom:2rem}}
  .stats-row{{display:flex;justify-content:center;gap:2rem;margin-bottom:2.5rem;flex-wrap:wrap}}
  .stat-item{{text-align:center}}
  .stat-num{{font-size:1.6rem;font-weight:800;color:var(--k-cyan)}}
  .stat-lbl{{font-size:0.75rem;color:var(--k-muted);text-transform:uppercase;letter-spacing:1px;margin-top:2px}}
  .btn-primary{{background:linear-gradient(135deg,var(--k-orange),#ff2a00);color:#fff;font-family:'Outfit',sans-serif;font-weight:700;font-size:1rem;padding:14px 36px;border:none;border-radius:50px;cursor:pointer;letter-spacing:1px;text-transform:uppercase;transition:all 0.3s ease;display:inline-flex;align-items:center;gap:8px}}
  .btn-primary:hover{{box-shadow:0 0 30px rgba(255,90,0,0.5);transform:translateY(-2px) scale(1.03)}}
  .btn-primary svg{{transition:transform 0.3s}}
  .btn-primary:hover svg{{transform:translateX(4px)}}
  /* ── QUIZ ── */
  #quiz-screen{{display:none}}
  #quiz-screen .inner{{max-width:680px;width:100%}}
  .topbar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem}}
  .progress-wrap{{flex:1}}
  .progress-label{{display:flex;justify-content:space-between;font-size:0.8rem;color:var(--k-muted);margin-bottom:6px;font-weight:600}}
  .progress-label span:last-child{{color:var(--k-cyan)}}
  .progress-track{{width:100%;height:4px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden}}
  .progress-fill{{height:100%;background:linear-gradient(90deg,var(--k-cyan),#4f8eff);border-radius:4px;transition:width 0.6s cubic-bezier(0.4,0,0.2,1);width:0%}}
  .dim-chips{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:1.2rem}}
  .dim-chip{{font-size:0.7rem;padding:4px 10px;border-radius:20px;font-weight:600;letter-spacing:0.5px;border:1px solid;transition:all 0.3s}}
  .dim-chip.inactive{{border-color:rgba(255,255,255,0.1);color:var(--k-muted);background:transparent}}
  .dim-chip.active{{border-color:var(--k-cyan);color:var(--k-cyan);background:var(--k-cyan-dim);box-shadow:0 0 10px rgba(0,229,255,0.2)}}
  .dim-chip.done{{border-color:rgba(0,229,255,0.3);color:rgba(0,229,255,0.4);background:rgba(0,229,255,0.05)}}
  .q-card{{padding:2.5rem;transition:opacity 0.3s,transform 0.3s}}
  .q-cat{{font-size:0.72rem;font-weight:700;color:var(--k-orange);text-transform:uppercase;letter-spacing:2px;margin-bottom:0.8rem;display:flex;align-items:center;gap:6px}}
  .q-cat::before{{content:'';width:16px;height:2px;background:var(--k-orange);border-radius:2px}}
  .q-text{{font-size:1.35rem;font-weight:700;line-height:1.4;margin-bottom:2rem;color:#f1f5f9}}
  .options-grid{{display:flex;flex-direction:column;gap:10px}}
  .opt-btn{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px 18px;text-align:left;color:var(--k-text);font-family:'Outfit',sans-serif;font-size:1rem;font-weight:500;cursor:pointer;transition:all 0.25s ease;display:flex;align-items:center;gap:12px;position:relative;overflow:hidden}}
  .opt-btn::before{{content:'';position:absolute;left:0;top:0;height:100%;width:3px;background:var(--k-cyan);transform:scaleY(0);transition:transform 0.2s}}
  .opt-btn:hover{{border-color:rgba(0,229,255,0.4);background:var(--k-cyan-dim);transform:translateX(4px)}}
  .opt-btn:hover::before{{transform:scaleY(1)}}
  .opt-btn.selected{{border-color:var(--k-cyan);background:rgba(0,229,255,0.1);transform:translateX(4px)}}
  .opt-btn.selected::before{{transform:scaleY(1)}}
  .opt-indicator{{width:28px;height:28px;border:1.5px solid rgba(255,255,255,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:0.8rem;font-weight:700;color:var(--k-muted);transition:all 0.2s}}
  .opt-btn:hover .opt-indicator,.opt-btn.selected .opt-indicator{{border-color:var(--k-cyan);color:var(--k-cyan);background:rgba(0,229,255,0.15)}}
  /* ── FORMULARIO ── */
  #form-screen{{display:none}}
  .form-input{{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:13px 16px;color:#e2e8f0;font-family:'Outfit',sans-serif;font-size:0.95rem;width:100%;outline:none;transition:all 0.25s}}
  .form-input:focus{{border-color:rgba(0,229,255,0.45);background:rgba(0,229,255,0.05);box-shadow:0 0 0 3px rgba(0,229,255,0.08)}}
  .form-input::placeholder{{color:var(--k-muted)}}
  .form-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
  @media(max-width:480px){{.form-grid{{grid-template-columns:1fr}}}}
  .form-label{{font-size:0.75rem;font-weight:600;color:var(--k-muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:5px;display:block}}
  .field{{display:flex;flex-direction:column}}
  .step-badge{{display:inline-flex;align-items:center;gap:8px;font-size:0.78rem;font-weight:700;color:var(--k-cyan);letter-spacing:1px;text-transform:uppercase;margin-bottom:1rem;background:rgba(0,229,255,0.08);padding:6px 14px;border-radius:50px;border:1px solid rgba(0,229,255,0.2)}}
  /* ── RESULTADOS ── */
  #results-screen{{display:none}}
  #results-screen .inner{{max-width:720px;width:100%}}
  .results-hero{{padding:2.5rem;text-align:center;margin-bottom:1rem;position:relative;overflow:hidden}}
  .results-label{{font-size:0.75rem;font-weight:700;color:var(--k-muted);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.5rem}}
  .score-big{{font-size:clamp(5rem,15vw,9rem);font-weight:800;line-height:1;background:linear-gradient(135deg,var(--k-cyan),#4f8eff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0.5rem 0}}
  .score-max{{font-size:1.1rem;color:var(--k-muted);margin-bottom:1rem}}
  .level-badge{{display:inline-block;padding:8px 24px;border-radius:50px;font-weight:700;font-size:0.95rem;margin-bottom:1.2rem}}
  .level-0{{background:rgba(99,215,17,0.1);border:1px solid rgba(99,215,17,0.3);color:#63d711}}
  .level-1{{background:rgba(255,165,0,0.1);border:1px solid rgba(255,165,0,0.35);color:#ffa500}}
  .level-2{{background:rgba(255,90,0,0.12);border:1px solid rgba(255,90,0,0.4);color:var(--k-orange)}}
  .result-msg{{font-size:1.05rem;color:var(--k-muted);line-height:1.7;max-width:520px;margin:0 auto}}
  .result-msg strong{{color:#e2e8f0}}
  .dim-results{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:1rem 0}}
  @media(max-width:480px){{.dim-results{{grid-template-columns:1fr}}}}
  .dim-result-card{{padding:1rem 1.2rem;border-radius:12px;background:rgba(15,23,42,0.6);border:1px solid rgba(255,255,255,0.07)}}
  .dr-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}}
  .dr-name{{font-size:0.78rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--k-muted)}}
  .dr-pct{{font-size:0.85rem;font-weight:700}}
  .dr-bar-track{{height:3px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden}}
  .dr-bar-fill{{height:100%;border-radius:3px;transition:width 1.2s cubic-bezier(0.4,0,0.2,1)}}
  .btn-cta-big{{display:block;text-align:center;background:linear-gradient(135deg,var(--k-orange),#ff2a00);color:#fff;font-family:'Outfit',sans-serif;font-weight:700;font-size:1.05rem;padding:16px 40px;border-radius:50px;text-decoration:none;letter-spacing:1px;text-transform:uppercase;cursor:pointer;margin-top:1.5rem;transition:all 0.3s;border:none;width:100%}}
  .btn-cta-big:hover{{box-shadow:0 0 35px rgba(255,90,0,0.5);transform:translateY(-2px)}}
  .restart-btn{{background:none;border:1px solid rgba(255,255,255,0.1);color:var(--k-muted);font-family:'Outfit',sans-serif;font-size:0.85rem;padding:10px 24px;border-radius:50px;cursor:pointer;margin-top:10px;width:100%;transition:all 0.2s}}
  .restart-btn:hover{{border-color:rgba(255,255,255,0.25);color:#e2e8f0}}
  .error-msg{{color:#ff6b6b;font-size:0.82rem;margin-top:8px;padding:8px 12px;background:rgba(255,90,0,0.08);border-radius:8px;border:1px solid rgba(255,90,0,0.2);display:none}}
  .saving-indicator{{display:flex;align-items:center;gap:8px;font-size:0.8rem;color:var(--k-muted);justify-content:center;margin-top:12px}}
  .dot-pulse{{width:6px;height:6px;background:var(--k-cyan);border-radius:50%;animation:pulse 1.2s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:0.3;transform:scale(0.8)}}50%{{opacity:1;transform:scale(1.2)}}}}
  .fade-in{{animation:fadeIn 0.5s cubic-bezier(0.4,0,0.2,1) forwards}}
  @keyframes fadeIn{{from{{opacity:0;transform:translateY(12px) scale(0.98)}}to{{opacity:1;transform:translateY(0) scale(1)}}}}
  .sr-only{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}}
  .user-greeting{{font-size:0.9rem;color:var(--k-cyan);font-weight:600;margin-bottom:0.5rem;opacity:0.85}}
</style>

<div id="app">
  <h2 class="sr-only">Índice de Madurez de Automatización — KrugerTech</h2>
  <div class="glow-orb g1"></div>
  <div class="glow-orb g2"></div>
  <canvas id="particles"></canvas>

  <!-- ═══════════════════════════════ INTRO ═══════════════════════════════ -->
  <div class="screen" id="intro-screen">
    <div class="glass" style="max-width:600px;width:100%;padding:3rem 2.5rem;text-align:center">
      <div class="logo-mark">KrugerTech &nbsp; RPA Intelligence</div>
      <div style="margin:1.5rem 0;position:relative;display:inline-block">
        <svg width="72" height="72" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="36" cy="36" r="35" stroke="rgba(0,229,255,0.2)" stroke-width="1"/>
          <circle cx="36" cy="36" r="27" stroke="rgba(0,229,255,0.1)" stroke-width="1" stroke-dasharray="4 3"/>
          <rect x="22" y="22" width="28" height="28" rx="4" stroke="#00e5ff" stroke-width="1.5"/>
          <rect x="28" y="28" width="16" height="16" rx="2" fill="rgba(0,229,255,0.15)" stroke="#00e5ff" stroke-width="1"/>
          <line x1="36" y1="14" x2="36" y2="20" stroke="#00e5ff" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="36" y1="52" x2="36" y2="58" stroke="#00e5ff" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="14" y1="36" x2="20" y2="36" stroke="#00e5ff" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="52" y1="36" x2="58" y2="36" stroke="#00e5ff" stroke-width="1.5" stroke-linecap="round"/>
          <circle cx="36" cy="36" r="3" fill="#00e5ff"/>
        </svg>
        <div style="position:absolute;top:-4px;right:-4px;width:12px;height:12px;background:#ff5a00;border-radius:50%;box-shadow:0 0 8px rgba(255,90,0,0.8)"></div>
      </div>
      <h1 class="hero">Índice de <span class="gradient-text">Madurez</span><br>de <span class="orange-text">Automatización</span></h1>
      <p class="intro-desc" style="margin-top:1rem">Descubre en menos de 2 minutos qué tan automatizables son tus procesos y dónde está el mayor potencial de ROI.</p>
      <div class="stats-row">
        <div class="stat-item"><div class="stat-num">13</div><div class="stat-lbl">Preguntas</div></div>
        <div class="stat-item" style="border-left:1px solid rgba(255,255,255,0.07);border-right:1px solid rgba(255,255,255,0.07);padding:0 2rem"><div class="stat-num">~2</div><div class="stat-lbl">Minutos</div></div>
        <div class="stat-item"><div class="stat-num">5</div><div class="stat-lbl">Dimensiones</div></div>
      </div>
      <button class="btn-primary" onclick="startAssessment()">
        Iniciar Diagnóstico
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <p style="margin-top:1.5rem;font-size:0.78rem;color:var(--k-muted)">Sin registro previo requerido · Resultados inmediatos</p>
    </div>
  </div>

  <!-- ═══════════════════════════════ QUIZ ═══════════════════════════════ -->
  <div class="screen" id="quiz-screen">
    <div class="inner">
      <div class="topbar">
        <div class="progress-wrap">
          <div class="progress-label"><span>Progreso del diagnóstico</span><span id="prog-text">1 / 13</span></div>
          <div class="progress-track"><div class="progress-fill" id="prog-bar"></div></div>
        </div>
      </div>
      <div class="dim-chips" id="dim-chips"></div>
      <div class="glass q-card" id="q-card">
        <div class="q-cat" id="q-cat"></div>
        <div class="q-text" id="q-text"></div>
        <div class="options-grid" id="q-opts"></div>
      </div>
    </div>
  </div>

  <!-- ═══════════════════════════════ FORMULARIO ═══════════════════════════════ -->
  <div class="screen" id="form-screen">
    <div class="glass" style="max-width:560px;width:100%;padding:2.5rem 2.5rem 2rem">

      <div style="text-align:center;margin-bottom:1.8rem">
        <div class="step-badge">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M8 1l2 5h5l-4 3 1.5 5L8 11.5 3.5 14 5 9 1 6h5z" stroke="#00e5ff" stroke-width="1.5" stroke-linejoin="round"/></svg>
          Diagnóstico completado
        </div>
        <h2 style="font-size:1.7rem;font-weight:800;line-height:1.2;margin-bottom:0.6rem">
          ¿A quién enviamos<br>tu <span class="gradient-text">Score de Madurez</span>?
        </h2>
        <p style="color:var(--k-muted);font-size:0.9rem;line-height:1.5">Completa tus datos para ver el análisis completo por dimensión y recomendaciones personalizadas.</p>
      </div>

      <div style="display:flex;flex-direction:column;gap:14px">

        <div class="field">
          <label class="form-label" for="f-nombre">Nombre completo</label>
          <input class="form-input" id="f-nombre" type="text" placeholder="Ej. María González" autocomplete="name">
        </div>

        <div class="form-grid">
          <div class="field">
            <label class="form-label" for="f-celular">Celular / WhatsApp</label>
            <input class="form-input" id="f-celular" type="tel" placeholder="+593 99 999 9999" autocomplete="tel">
          </div>
          <div class="field">
            <label class="form-label" for="f-correo">Correo electrónico</label>
            <input class="form-input" id="f-correo" type="email" placeholder="maria@empresa.com" autocomplete="email">
          </div>
        </div>

        <div class="form-grid">
          <div class="field">
            <label class="form-label" for="f-empresa">Empresa</label>
            <input class="form-input" id="f-empresa" type="text" placeholder="Nombre de tu empresa" autocomplete="organization">
          </div>
          <div class="field">
            <label class="form-label" for="f-cargo">Cargo</label>
            <input class="form-input" id="f-cargo" type="text" placeholder="Ej. Gerente de Operaciones" autocomplete="organization-title">
          </div>
        </div>

      </div>

      <div class="error-msg" id="form-error">Por favor completa todos los campos correctamente.</div>

      <button class="btn-primary" id="submit-btn" style="width:100%;justify-content:center;margin-top:1.5rem;font-size:1rem" onclick="submitForm()">
        Ver mi Score de Madurez
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <div class="saving-indicator" id="saving-ind" style="display:none">
        <div class="dot-pulse"></div>
        Guardando tu diagnóstico...
      </div>
      <p style="margin-top:1rem;font-size:0.75rem;color:var(--k-muted);text-align:center">
        🔒 Tus datos están seguros y no serán compartidos con terceros
      </p>
    </div>
  </div>

  <!-- ═══════════════════════════════ RESULTADOS ═══════════════════════════════ -->
  <div class="screen" id="results-screen">
    <div class="inner">
      <div class="glass results-hero">
        <div class="user-greeting" id="user-greeting"></div>
        <div class="results-label">Score de madurez RPA</div>
        <div class="score-big" id="score-display">0</div>
        <div class="score-max">de 65 puntos posibles</div>
        <div class="level-badge" id="level-badge"></div>
        <p class="result-msg" id="result-msg"></p>
      </div>
      <div class="dim-results" id="dim-results"></div>
      <div style="margin-top:1.5rem;padding:1.2rem 1.4rem;border-radius:14px;background:rgba(0,229,255,0.05);border:1px solid rgba(0,229,255,0.15)">
        <p style="font-size:0.82rem;color:var(--k-muted);text-align:center;line-height:1.6">
          ✅ Tu diagnóstico fue guardado. Un especialista de KrugerTech se pondrá en contacto contigo para presentarte las oportunidades de automatización identificadas.
        </p>
      </div>
      <button class="btn-cta-big" onclick="openContact()">
        Hablar con un Especialista AI →
      </button>
      <button class="restart-btn" onclick="restart()">↩ Reiniciar diagnóstico</button>
    </div>
  </div>
</div>

<script>
const APPS_SCRIPT_URL = "{APPS_SCRIPT_URL}";

const DIMS = [
  {{name:"Dependencia manual",  color:"#00e5ff", qs:[0,1],   max:10}},
  {{name:"Conocimiento crítico", color:"#4f8eff", qs:[2,3],   max:10}},
  {{name:"Complejidad y volumen",color:"#a78bfa", qs:[4,5,6], max:15}},
  {{name:"Calidad y errores",   color:"#ff9500", qs:[7,8,9], max:15}},
  {{name:"Datos y gobernanza",  color:"#ff5a00", qs:[10,11,12],max:15}}
];

const QUESTIONS=[
  {{dim:0,cat:"Dependencia manual",   q:"¿Cuánto del proceso depende de copiar y pegar datos entre sistemas?",opts:["Casi nada","Solo en un paso puntual","En varios momentos","La mayor parte del proceso","Proceso completo es puente manual"]}},
  {{dim:0,cat:"Dependencia manual",   q:"¿El proceso funciona porque las personas conectan información que los sistemas no conectan solos?",opts:["No","Muy poco","Ocasional","Con alta frecuencia","Totalmente dependiente"]}},
  {{dim:1,cat:"Conocimiento crítico", q:"Si mañana no está la persona que lo domina, ¿qué ocurre?",opts:["Nada cambia","Avanza con lentitud","Avanza con apoyo parcial","Se vuelve muy difícil","El proceso se detiene"]}},
  {{dim:1,cat:"Conocimiento crítico", q:"¿Qué tan claras y repetibles son las reglas del proceso?",opts:["Totalmente definidas y estables","Documentadas","Medianamente definidas","Reglas informales","No hay reglas"]}},
  {{dim:2,cat:"Complejidad y volumen",q:"¿Cuántas aplicaciones intervienen desde que inicia hasta que termina?",opts:["Una","Dos","Tres","Cuatro","Cinco o más"]}},
  {{dim:2,cat:"Complejidad y volumen",q:"¿Qué volumen mensual maneja esta tarea?",opts:["< 50","50–200","200–500","500–1,000","> 1,000"]}},
  {{dim:2,cat:"Complejidad y volumen",q:"¿Cuántas horas al mes consume hoy tu equipo en este trabajo?",opts:["< 20 h","20–50 h","50–100 h","100–200 h","> 200 h"]}},
  {{dim:3,cat:"Calidad y errores",    q:"¿Con qué frecuencia aparecen errores de digitación o formatos mal cargados?",opts:["< 5/mes","5–15/mes","15–30/mes","30–60/mes","> 60/mes"]}},
  {{dim:3,cat:"Calidad y errores",    q:"¿Cuánto re-trabajo se genera porque los datos no cuadran solos?",opts:["< 5%","5–10%","10–20%","20–35%","> 35%"]}},
  {{dim:3,cat:"Calidad y errores",    q:"¿El atraso en este proceso afecta servicio, ingresos o cumplimiento?",opts:["No","Bajo","Medio","Alto","Impacto muy alto"]}},
  {{dim:4,cat:"Datos y gobernanza",   q:"¿Qué tan estandarizados están los datos de entrada?",opts:["Totalmente estandarizados","Mayormente estables","Media","Heterogéneos","Muy heterogéneos"]}},
  {{dim:4,cat:"Datos y gobernanza",   q:"¿Todo empieza y termina en el ERP o quedan bordes fuera?",opts:["100% dentro del ERP","Casi todo","Parcial","Muy poco dentro","No — los bordes quedan fuera"]}},
  {{dim:4,cat:"Datos y gobernanza",   q:"¿Cuántos pasos fuera del core nadie gobierna hoy?",opts:["Ninguno","Muy pocos","Media","Muchos","La mayoría del proceso"]}}
];

let idx=0, total=0, scores=[];
let userData = {{}};

// ── INTRO → QUIZ ──────────────────────────────────────────────────────────────
function startAssessment(){{
  const i=document.getElementById('intro-screen');
  i.style.opacity=0; i.style.transform='scale(0.96)'; i.style.transition='all 0.4s';
  setTimeout(()=>{{
    i.style.display='none';
    const q=document.getElementById('quiz-screen');
    q.style.display='flex';
    buildChips(); renderQ();
  }},400);
}}

function buildChips(){{
  const el=document.getElementById('dim-chips');
  el.innerHTML=DIMS.map((d,i)=>`<span class="dim-chip inactive" id="chip-${{i}}">${{d.name}}</span>`).join('');
}}

function renderQ(){{
  const cur=QUESTIONS[idx];
  document.getElementById('prog-text').textContent=`${{idx+1}} / ${{QUESTIONS.length}}`;
  document.getElementById('prog-bar').style.width=`${{(idx/QUESTIONS.length)*100}}%`;
  DIMS.forEach((d,di)=>{{
    const chip=document.getElementById('chip-'+di);
    const qs=d.qs;
    if(qs.includes(idx)){{chip.className='dim-chip active';chip.style.borderColor=d.color;chip.style.color=d.color;chip.style.background=d.color+'18'}}
    else if(qs.every(q=>q<idx)){{chip.className='dim-chip done';chip.style.cssText=''}}
    else{{chip.className='dim-chip inactive';chip.style.cssText=''}}
  }});
  const card=document.getElementById('q-card');
  card.style.opacity=0; card.style.transform='translateY(8px)';
  setTimeout(()=>{{
    document.getElementById('q-cat').textContent=cur.cat;
    document.getElementById('q-text').textContent=cur.q;
    const opts=document.getElementById('q-opts');
    opts.innerHTML='';
    cur.opts.forEach((o,oi)=>{{
      const b=document.createElement('button');
      b.className='opt-btn';
      const letters=['A','B','C','D','E'];
      b.innerHTML=`<span class="opt-indicator">${{letters[oi]}}</span><span>${{o}}</span>`;
      b.onclick=()=>pick(oi+1);
      opts.appendChild(b);
    }});
    card.style.transition='all 0.4s cubic-bezier(0.4,0,0.2,1)';
    card.style.opacity=1; card.style.transform='translateY(0)';
  }},200);
}}

function pick(pts){{
  scores.push({{dim:QUESTIONS[idx].dim, pts}});
  total+=pts; idx++;
  if(idx<QUESTIONS.length){{
    const card=document.getElementById('q-card');
    card.style.opacity=0; card.style.transform='translateY(-8px)';
    setTimeout(renderQ,200);
  }}else goToForm();
}}

// ── QUIZ → FORMULARIO ─────────────────────────────────────────────────────────
function goToForm(){{
  const q=document.getElementById('quiz-screen');
  q.style.opacity=0; q.style.transition='opacity 0.4s';
  setTimeout(()=>{{
    q.style.display='none';
    const f=document.getElementById('form-screen');
    f.style.display='flex'; f.classList.add('fade-in');
  }},400);
}}

// ── FORMULARIO → GUARDAR → RESULTADOS ─────────────────────────────────────────
function submitForm(){{
  const nombre  = document.getElementById('f-nombre').value.trim();
  const celular = document.getElementById('f-celular').value.trim();
  const correo  = document.getElementById('f-correo').value.trim();
  const empresa = document.getElementById('f-empresa').value.trim();
  const cargo   = document.getElementById('f-cargo').value.trim();

  const errEl = document.getElementById('form-error');

  if(!nombre||!celular||!correo||!empresa||!cargo){{
    errEl.textContent='Por favor completa todos los campos.';
    errEl.style.display='block'; return;
  }}
  if(!/\S+@\S+\.\S+/.test(correo)){{
    errEl.textContent='Ingresa un correo electrónico válido.';
    errEl.style.display='block'; return;
  }}
  errEl.style.display='none';

  userData = {{nombre, celular, correo, empresa, cargo}};

  // Calcular scores por dimensión
  const dimScores={{}};
  DIMS.forEach((_,di)=>{{dimScores[di]=0}});
  scores.forEach(s=>{{dimScores[s.dim]+=s.pts}});

  const payload = {{
    timestamp:  new Date().toISOString(),
    nombre, celular, correo, empresa, cargo,
    score_total:        total,
    score_max:          65,
    score_pct:          Math.round((total/65)*100),
    nivel:              total>=50 ? 'Alta dependencia manual' : total>=30 ? 'Punto de inflexión' : 'Procesos estructurados',
    dim_dependencia_manual:   dimScores[0],
    dim_conocimiento_critico: dimScores[1],
    dim_complejidad_volumen:  dimScores[2],
    dim_calidad_errores:      dimScores[3],
    dim_datos_gobernanza:     dimScores[4],
    pct_dependencia:  Math.round((dimScores[0]/DIMS[0].max)*100),
    pct_conocimiento: Math.round((dimScores[1]/DIMS[1].max)*100),
    pct_complejidad:  Math.round((dimScores[2]/DIMS[2].max)*100),
    pct_calidad:      Math.round((dimScores[3]/DIMS[3].max)*100),
    pct_datos:        Math.round((dimScores[4]/DIMS[4].max)*100),
  }};

  // UI de carga
  const btn = document.getElementById('submit-btn');
  btn.disabled=true; btn.style.opacity='0.6';
  btn.innerHTML='Procesando... <span style="font-size:1.2rem">⏳</span>';
  document.getElementById('saving-ind').style.display='flex';

  // Enviar a Google Sheets (no-cors: no importa la respuesta, el dato llega igual)
  fetch(APPS_SCRIPT_URL, {{
    method:'POST',
    mode:'no-cors',
    headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify(payload)
  }}).catch(()=>{{}}).finally(()=>{{
    showResults();
  }});
}}

// ── MOSTRAR RESULTADOS ─────────────────────────────────────────────────────────
function showResults(){{
  const f=document.getElementById('form-screen');
  f.style.opacity=0; f.style.transition='opacity 0.4s';
  setTimeout(()=>{{
    f.style.display='none';
    const r=document.getElementById('results-screen');
    r.style.display='flex'; r.classList.add('fade-in');

    const nombre = userData.nombre || '';
    if(nombre){{
      const firstName = nombre.split(' ')[0];
      document.getElementById('user-greeting').textContent = `Hola ${{firstName}}, aquí está tu diagnóstico 👋`;
    }}

    animScore(total);

    const badge=document.getElementById('level-badge');
    const msg=document.getElementById('result-msg');
    if(total>=50){{
      badge.className='level-badge level-2'; badge.textContent='Alta dependencia manual';
      msg.innerHTML='Tus procesos tienen una <strong>oportunidad masiva de automatización</strong>. Reducir la carga manual liberará capacidad operativa y minimizará riesgos inmediatos de forma significativa.';
    }}else if(total>=30){{
      badge.className='level-badge level-1'; badge.textContent='Punto de inflexión';
      msg.innerHTML='Estás en un <strong>momento clave</strong>. Hay cuellos de botella claros donde la automatización e integración de sistemas generará un ROI alto y rápido.';
    }}else{{
      badge.className='level-badge level-0'; badge.textContent='Procesos estructurados';
      msg.innerHTML='Tienes buenas bases. La <strong>optimización con IA y automatización avanzada</strong> te llevará al siguiente nivel de escalabilidad y eficiencia operativa.';
    }}
    buildDimResults();
  }},400);
}}

function buildDimResults(){{
  const dimScores={{}};
  DIMS.forEach((_,di)=>{{dimScores[di]=0}});
  scores.forEach(s=>{{dimScores[s.dim]+=s.pts}});
  const el=document.getElementById('dim-results');
  el.innerHTML=DIMS.map((d,di)=>{{
    const pct=Math.round((dimScores[di]/d.max)*100);
    const barColor=pct>=75?'#ff5a00':pct>=50?'#ffa500':'#00e5ff';
    return `<div class="dim-result-card">
      <div class="dr-head">
        <span class="dr-name">${{d.name}}</span>
        <span class="dr-pct" style="color:${{barColor}}">${{pct}}%</span>
      </div>
      <div class="dr-bar-track"><div class="dr-bar-fill" style="width:0%;background:${{barColor}}" data-target="${{pct}}"></div></div>
    </div>`;
  }}).join('');
  setTimeout(()=>{{
    document.querySelectorAll('.dr-bar-fill').forEach(b=>{{b.style.width=b.dataset.target+'%'}});
  }},100);
}}

function animScore(target){{
  let cur=0; const dur=1800; const step=target/(dur/16);
  const el=document.getElementById('score-display');
  const t=setInterval(()=>{{cur+=step;if(cur>=target){{el.textContent=target;clearInterval(t)}}else el.textContent=Math.floor(cur)}},16);
}}

function openContact(){{
  window.open('mailto:contacto@krugertech.com?subject=Solicito%20asesoría%20RPA%20-%20Score%20'+total, '_blank');
}}

function restart(){{
  idx=0; total=0; scores=[]; userData={{}};
  document.getElementById('results-screen').style.display='none';
  document.getElementById('results-screen').classList.remove('fade-in');
  document.getElementById('form-screen').style.display='none';
  document.getElementById('form-screen').classList.remove('fade-in');
  // Reset form
  ['f-nombre','f-celular','f-correo','f-empresa','f-cargo'].forEach(id=>{{
    document.getElementById(id).value='';
  }});
  const btn=document.getElementById('submit-btn');
  btn.disabled=false; btn.style.opacity='1';
  btn.innerHTML='Ver mi Score de Madurez <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  document.getElementById('saving-ind').style.display='none';
  document.getElementById('form-error').style.display='none';
  document.getElementById('prog-bar').style.width='0%';
  document.getElementById('intro-screen').style.cssText='';
  document.getElementById('quiz-screen').style.cssText='display:none';
}}

// ── PARTÍCULAS ─────────────────────────────────────────────────────────────────
(function(){{
  const c=document.getElementById('particles');
  const ctx=c.getContext('2d');
  const app=document.getElementById('app');
  function resize(){{c.width=app.offsetWidth;c.height=app.offsetHeight}}
  resize(); window.addEventListener('resize',resize);
  const dots=Array.from({{length:50}},()=>(({{
    x:Math.random()*c.width, y:Math.random()*c.height,
    r:Math.random()*1.5+0.3,
    vx:(Math.random()-0.5)*0.3, vy:(Math.random()-0.5)*0.3,
    a:Math.random()*0.4+0.1
  }})));
  function draw(){{
    ctx.clearRect(0,0,c.width,c.height);
    dots.forEach(d=>{{
      d.x+=d.vx; d.y+=d.vy;
      if(d.x<0||d.x>c.width)d.vx*=-1;
      if(d.y<0||d.y>c.height)d.vy*=-1;
      ctx.beginPath(); ctx.arc(d.x,d.y,d.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(0,229,255,${{d.a}})`; ctx.fill();
    }});
    for(let i=0;i<dots.length;i++)for(let j=i+1;j<dots.length;j++){{
      const dx=dots[i].x-dots[j].x, dy=dots[i].y-dots[j].y;
      const dist=Math.sqrt(dx*dx+dy*dy);
      if(dist<90){{
        ctx.beginPath(); ctx.moveTo(dots[i].x,dots[i].y); ctx.lineTo(dots[j].x,dots[j].y);
        ctx.strokeStyle=`rgba(0,229,255,${{0.06*(1-dist/90)}})`; ctx.lineWidth=0.5; ctx.stroke();
      }}
    }}
    requestAnimationFrame(draw);
  }}
  draw();
}})();
</script>
""".replace("{APPS_SCRIPT_URL}", APPS_SCRIPT_URL)

components.html(codigo_html, height=880, scrolling=False)
