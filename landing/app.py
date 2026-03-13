from flask import Flask, render_template_string
app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IntraCorp CTF</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@400;600;700;800&family=Syne+Mono&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#050508;--surf:#0a0b12;--border:#15182a;
  --c1:#00d4ff;--c2:#7c3aff;--c3:#ff3c6e;--c4:#a8ff00;
  --text:#b0bcd4;--dim:#3a4560;
  --mono:'Syne Mono',monospace;--sans:'Syne',sans-serif;--body:'Inter',sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:var(--body);min-height:100vh;display:flex;flex-direction:column;overflow-x:hidden}

/* BG */
.bg-glow{position:fixed;top:0;left:0;right:0;bottom:0;
  background:radial-gradient(ellipse at 50% -10%,rgba(124,58,255,.12) 0%,transparent 55%),
             radial-gradient(ellipse at 10% 90%,rgba(0,212,255,.05) 0%,transparent 45%);
  pointer-events:none;z-index:0}

/* HEADER */
header{
  border-bottom:1px solid var(--border);
  padding:0 60px;height:64px;
  display:flex;align-items:center;justify-content:space-between;
  position:relative;z-index:10;
  background:rgba(5,5,8,.96);backdrop-filter:blur(10px);
}
.logo{font-family:var(--mono);font-size:15px;color:var(--c1);letter-spacing:4px}
.logo span{color:var(--dim)}
.live-pill{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10px;
  letter-spacing:2px;color:var(--c4);padding:5px 14px;
  border:1px solid rgba(168,255,0,.25);background:rgba(168,255,0,.04)}
.dot{width:6px;height:6px;background:var(--c4);border-radius:50%;animation:blink 1.2s step-end infinite}
@keyframes blink{50%{opacity:0}}

/* HERO */
.hero{
  min-height:calc(100vh - 64px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;padding:80px 40px;
  position:relative;z-index:2;
}
.hero-tag{
  font-family:var(--mono);font-size:11px;color:var(--c2);
  letter-spacing:5px;text-transform:uppercase;margin-bottom:28px;
}
.hero h1{
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(100px,18vw,200px);
  line-height:.88;letter-spacing:4px;margin-bottom:40px;
  background:linear-gradient(160deg,#ffffff 30%,rgba(255,255,255,.35) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 60px rgba(124,58,255,.15));
}
.hero-desc{
  font-size:17px;font-weight:300;color:var(--dim);
  max-width:520px;margin:0 auto 60px;line-height:1.7;
}
.hero-desc strong{color:var(--text);font-weight:500}

/* STATS */
.stats-bar{
  display:flex;justify-content:center;gap:0;
  border:1px solid var(--border);background:var(--surf);
  max-width:520px;width:100%;margin:0 auto 80px;
}
.stat{flex:1;padding:22px 20px;text-align:center;border-right:1px solid var(--border)}
.stat:last-child{border-right:none}
.stat-val{font-family:var(--mono);font-size:26px;font-weight:700;color:#fff;display:block;margin-bottom:5px}
.stat-lbl{font-family:var(--mono);font-size:9px;letter-spacing:2px;color:var(--dim);text-transform:uppercase}
.scroll-hint{font-family:var(--mono);font-size:10px;color:var(--dim);letter-spacing:3px;text-transform:uppercase;animation:float 2s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(8px)}}

/* SECTION */
section{max-width:1100px;margin:0 auto;padding:80px 40px;position:relative;z-index:2;width:100%}
.section-hd{
  font-family:var(--mono);font-size:10px;letter-spacing:4px;
  text-transform:uppercase;color:var(--dim);
  margin-bottom:36px;display:flex;align-items:center;gap:16px;
}
.section-hd::after{content:'';flex:1;height:1px;background:var(--border)}

/* CARDS */
.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--border)}
@media(max-width:700px){.cards{grid-template-columns:1fr}}
.card{
  background:var(--surf);padding:36px 40px;
  position:relative;overflow:hidden;
  transition:background .25s;text-decoration:none;color:inherit;display:block;
}
.card:hover{background:#0d0f1a}
.card-accent{position:absolute;top:0;left:0;right:0;height:2px;opacity:0;transition:opacity .25s}
.card:hover .card-accent{opacity:1}
.ca1{background:linear-gradient(90deg,var(--c1),transparent)}
.ca2{background:linear-gradient(90deg,var(--c2),transparent)}
.ca3{background:linear-gradient(90deg,var(--c4),transparent)}
.ca4{background:linear-gradient(90deg,var(--c3),transparent)}
.card-top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:20px}
.card-num{font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:2px}
.card-port{font-family:var(--mono);font-size:10px;padding:3px 10px;border:1px solid var(--border);color:var(--dim)}
.card-title{font-family:var(--sans);font-size:24px;font-weight:700;color:#fff;margin-bottom:8px}
.vtag{display:inline-block;font-family:var(--mono);font-size:9px;letter-spacing:3px;text-transform:uppercase;padding:3px 10px;margin-bottom:18px;border-radius:2px}
.vt1{color:var(--c1);background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.2)}
.vt2{color:var(--c2);background:rgba(124,58,255,.07);border:1px solid rgba(124,58,255,.2)}
.vt3{color:var(--c4);background:rgba(168,255,0,.07);border:1px solid rgba(168,255,0,.2)}
.vt4{color:var(--c3);background:rgba(255,60,110,.07);border:1px solid rgba(255,60,110,.2)}
.card-desc{font-size:13px;color:var(--dim);line-height:1.75;margin-bottom:28px}
.card-foot{display:flex;align-items:center;justify-content:space-between;padding-top:20px;border-top:1px solid var(--border)}
.card-domain{font-family:var(--mono);font-size:10px;color:var(--dim)}
.card-btn{font-family:var(--mono);font-size:10px;letter-spacing:2px;padding:6px 16px;border:1px solid var(--border);color:var(--dim);text-decoration:none;transition:all .2s}
.card-btn:hover{color:#fff;border-color:#fff}
.c1 .card-btn:hover{border-color:var(--c1);color:var(--c1)}
.c2 .card-btn:hover{border-color:var(--c2);color:var(--c2)}
.c3 .card-btn:hover{border-color:var(--c4);color:var(--c4)}
.c4 .card-btn:hover{border-color:var(--c3);color:var(--c3)}

/* INFO */
.info-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border)}
@media(max-width:700px){.info-grid{grid-template-columns:1fr}}
.info-cell{background:var(--surf);padding:26px 30px}
.info-cell h3{font-family:var(--mono);font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--c1);margin-bottom:10px}
.info-cell p{font-size:13px;color:var(--dim);line-height:1.7}
.info-cell code{font-family:var(--mono);font-size:11px;color:var(--text);background:rgba(255,255,255,.04);padding:1px 5px}

/* TABLE */
.flag-table{width:100%;border-collapse:collapse}
.flag-table th{font-family:var(--mono);font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--dim);padding:10px 16px;text-align:left;border-bottom:1px solid var(--border)}
.flag-table td{padding:14px 16px;border-bottom:1px solid var(--border);font-size:13px;color:var(--dim)}
.flag-table td:first-child{font-family:var(--mono);color:var(--text)}
.flag-table td code{font-family:var(--mono);font-size:12px;color:var(--c4)}

footer{margin-top:auto;border-top:1px solid var(--border);padding:20px 60px;display:flex;justify-content:space-between;font-family:var(--mono);font-size:10px;color:var(--dim);position:relative;z-index:2;background:rgba(5,5,8,.8)}
@media(max-width:600px){footer,header{padding:0 20px}section{padding:60px 20px}.hero{padding:60px 20px}}
</style>
</head>
<body>
<div class="bg-glow"></div>

<header>
  <div class="logo">INTRA<span>CORP</span> &middot; CTF</div>
  <div class="live-pill"><div class="dot"></div>4 CHALLENGES ACTIVOS</div>
</header>

<div class="hero">
  <div class="hero-tag">// Web Hacking Workshop &mdash; IntraCorp Simulated Environment</div>
  <h1>HACK<br>THE<br>CORP</h1>
  <p class="hero-desc">
    <strong>IntraCorp</strong> es una empresa ficticia con 4 servicios internos vulnerables.
    Tu misión: identificar y explotar cada vulnerabilidad, capturar la flag y demostrar que el sistema está comprometido.
  </p>
  <div class="stats-bar">
    <div class="stat"><span class="stat-val">04</span><span class="stat-lbl">Challenges</span></div>
    <div class="stat"><span class="stat-val" style="color:var(--c4)">04</span><span class="stat-lbl">Flags</span></div>
    <div class="stat"><span class="stat-val" style="color:var(--c2)">MED</span><span class="stat-lbl">Dificultad</span></div>
  </div>
  <div class="scroll-hint">&#x2193; ver challenges &#x2193;</div>
</div>

<section>
  <div class="section-hd">Challenges</div>
  <div class="cards">
    <a href="http://localhost:8001" target="_blank" class="card c1">
      <div class="card-accent ca1"></div>
      <div class="card-top"><span class="card-num">01 / 04</span><span class="card-port">:8001</span></div>
      <div class="card-title">SQL Injection</div>
      <span class="vtag vt1">SQLi</span>
      <p class="card-desc">La inyección SQL ocurre cuando datos del usuario se incorporan sin sanitizar en consultas a la base de datos, permitiendo manipular la lógica de la query para leer, modificar o eliminar datos arbitrarios del sistema.</p>
      <div class="card-foot"><span class="card-domain">portal.intracorp.local</span><span class="card-btn">ACCEDER &rarr;</span></div>
    </a>
    <a href="http://localhost:8002" target="_blank" class="card c2">
      <div class="card-accent ca2"></div>
      <div class="card-top"><span class="card-num">02 / 04</span><span class="card-port">:8002</span></div>
      <div class="card-title">IDOR</div>
      <span class="vtag vt2">Insecure Direct Object Reference</span>
      <p class="card-desc">IDOR ocurre cuando una aplicación expone referencias directas a objetos internos sin verificar autorización, permitiendo acceder a recursos de otros usuarios simplemente manipulando el identificador en la solicitud.</p>
      <div class="card-foot"><span class="card-domain">api.intracorp.local</span><span class="card-btn">ACCEDER &rarr;</span></div>
    </a>
    <a href="http://localhost:8003" target="_blank" class="card c3">
      <div class="card-accent ca3"></div>
      <div class="card-top"><span class="card-num">03 / 04</span><span class="card-port">:8003</span></div>
      <div class="card-title">Command Injection</div>
      <span class="vtag vt3">OS Command Injection</span>
      <p class="card-desc">La inyección de comandos ocurre cuando datos del usuario se pasan a un intérprete del sistema operativo sin sanitizar, permitiendo ejecutar comandos arbitrarios en el servidor y comprometer el host vulnerado.</p>
      <div class="card-foot"><span class="card-domain">tools.intracorp.local</span><span class="card-btn">ACCEDER &rarr;</span></div>
    </a>
    <a href="http://localhost:8004" target="_blank" class="card c4">
      <div class="card-accent ca4"></div>
      <div class="card-top"><span class="card-num">04 / 04</span><span class="card-port">:8004</span></div>
      <div class="card-title">SSTI &mdash; Jinja2</div>
      <span class="vtag vt4">Server-Side Template Injection</span>
      <p class="card-desc">SSTI ocurre cuando datos del usuario se renderizan dentro de un motor de plantillas sin sanitizar, permitiendo inyectar expresiones que el servidor evalúa y derivando en lectura de archivos o ejecución de código remoto.</p>
      <div class="card-foot"><span class="card-domain">billing.intracorp.local</span><span class="card-btn">ACCEDER &rarr;</span></div>
    </a>
  </div>
</section>

<section style="padding-top:0">
  <div class="section-hd">Info del Lab</div>
  <div class="info-grid">
    <div class="info-cell">
      <h3>// Formato de Flags</h3>
      <p>Todas las flags siguen el formato <code>flag{nombre}</code>. Regístralas con el instructor una vez capturadas.</p>
    </div>
    <div class="info-cell">
      <h3>// Arquitectura</h3>
      <p>Cada reto corre en Docker aislado. Sin comunicación entre contenedores. Puertos <code>8001&ndash;8004</code>.</p>
    </div>
    <div class="info-cell">
      <h3>// Herramientas</h3>
      <p>Burp Suite, navegador + DevTools, <code>curl</code>, Python <code>requests</code>. Sin restricciones.</p>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="section-hd">Registro de Retos</div>
  <table class="flag-table">
    <thead><tr><th>#</th><th>Reto</th><th>Servicio</th><th>Flag(Haz tu diligencia)</th></tr></thead>
    <tbody>
      <tr><td>01</td><td>SQL Injection</td><td>portal.intracorp.local</td><code>flag{s****_****_****s}</code></td></tr>
      <tr><td>02</td><td>IDOR Encoded</td><td>api.intracorp.local</td><code>flag{****r_****d_****}</code></td></tr>
      <tr><td>03</td><td>Command Injection</td><td>tools.intracorp.local</td><code>flag{c****_**n**_****}</code></td></tr>
      <tr><td>04</td><td>SSTI Jinja2</td><td>billing.intracorp.local</td><code>flag{****_wit****_****}</code></td></tr>
    </tbody>
  </table>
</section>

<footer>
  <span>IntraCorp Internal Systems &mdash; CTF Environment</span>
  <span>Web Hacking Workshop &middot; 4 Challenges &middot; Difficulty: Medium</span>
</footer>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
