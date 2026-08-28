// Generated from the WeatherGPT design file. Markup, styles and behaviour of the app shell.
export const WG_CSS = `
  :root{
    --navy-950:#0b1220;
    --navy-900:#101a2e;
    --navy-800:#16233b;
    --navy-700:#20304c;
    --teal-500:#0f9b8e;
    --teal-400:#1cb5a4;
    --teal-050:#e6f5f2;
    --amber-500:#e8a13a;
    --ink-900:#101828;
    --ink-600:#475467;
    --ink-400:#94a3b8;
    --line:#e6e9ef;
    --bg:#f5f6f9;
    --card:#ffffff;
    --danger:#d0453a;
    --danger-bg:#fdeceb;
    --warn:#b8791f;
    --warn-bg:#fdf3e2;
    --ok:#1a8f5a;
    --ok-bg:#e9f8f0;
    --radius:14px;
    --font-display: "Fraunces", "Iowan Old Style", Georgia, serif;
    --font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    --font-mono: "IBM Plex Mono", "SFMono-Regular", Menlo, monospace;
  }

  *{ box-sizing:border-box; }
  html,body{ height:100%; }
  body{
    margin:0;
    font-family:var(--font-body);
    background:var(--bg);
    color:var(--ink-900);
    -webkit-font-smoothing:antialiased;
  }
  @media (prefers-reduced-motion: reduce){
    *{ animation-duration:0.01ms !important; transition-duration:0.01ms !important; }
  }

  a{ color:inherit; }
  button{ font-family:inherit; cursor:pointer; }

  .app{
    display:grid;
    grid-template-columns:272px 1fr;
    min-height:100vh;
  }

  /* ===== Sidebar ===== */
  .sidebar{
    background:linear-gradient(180deg,var(--navy-900),var(--navy-950));
    color:#dbe4f0;
    padding:22px 18px 18px;
    display:flex;
    flex-direction:column;
    gap:22px;
    position:sticky;
    top:0;
    height:100vh;
  }
  .brand{
    display:flex;
    align-items:center;
    gap:12px;
  }
  .brand-mark{
    width:40px; height:40px;
    border-radius:11px;
    background:linear-gradient(140deg,var(--teal-400),var(--teal-500));
    display:flex; align-items:center; justify-content:center;
    flex-shrink:0;
    box-shadow:0 4px 14px rgba(15,155,142,0.35);
  }
  .brand-mark svg{ width:22px; height:22px; }
  .brand-eyebrow{
    font-family:var(--font-mono);
    font-size:10px;
    letter-spacing:0.16em;
    text-transform:uppercase;
    color:var(--teal-400);
    margin:0 0 2px;
  }
  .brand-title{
    font-family:var(--font-display);
    font-size:17px;
    font-weight:600;
    margin:0;
    color:#f2f5f9;
  }

  .loc-card{
    background:rgba(255,255,255,0.045);
    border:1px solid rgba(255,255,255,0.07);
    border-radius:var(--radius);
    padding:14px 15px;
  }
  .loc-label{
    font-family:var(--font-mono);
    font-size:10px;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color:#7b8bab;
    margin:0 0 6px;
  }
  .loc-name{
    font-size:15px;
    font-weight:600;
    color:#f2f5f9;
    margin:0 0 8px;
  }
  .loc-action{
    display:flex; align-items:center; gap:6px;
    background:none; border:none; padding:0;
    color:var(--teal-400);
    font-size:12.5px;
    font-weight:500;
  }
  .loc-action svg{ width:13px; height:13px; }

  .nav-label{
    font-family:var(--font-mono);
    font-size:10px;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color:#5f7092;
    margin:2px 4px 2px;
  }
  .nav{
    display:flex; flex-direction:column; gap:3px;
  }
  .nav-item{
    display:flex; align-items:center; gap:11px;
    padding:10px 12px;
    border-radius:10px;
    background:none; border:none;
    color:#aab8cf;
    font-size:14px;
    text-align:left;
    width:100%;
    transition:background 0.15s ease, color 0.15s ease;
  }
  .nav-item svg{ width:17px; height:17px; flex-shrink:0; opacity:0.85; }
  .nav-item:hover{ background:rgba(255,255,255,0.05); color:#f0f4f9; }
  .nav-item.active{
    background:linear-gradient(120deg, rgba(28,181,164,0.22), rgba(28,181,164,0.08));
    color:#f0fbf9;
    box-shadow:inset 0 0 0 1px rgba(28,181,164,0.35);
  }
  .nav-item.active svg{ opacity:1; color:var(--teal-400); }
  .nav-badge{
    margin-left:auto;
    background:var(--amber-500);
    color:#1a1204;
    font-size:11px;
    font-weight:700;
    border-radius:20px;
    padding:1px 7px;
  }

  .sidebar-spacer{ flex:1; }

  .new-question{
    display:flex; align-items:center; gap:9px;
    border:1px dashed rgba(255,255,255,0.18);
    border-radius:10px;
    padding:10px 12px;
    background:none;
    color:#c6d1e5;
    font-size:13px;
    width:100%;
  }
  .new-question:hover{ border-color:var(--teal-400); color:#f0fbf9; }

  .thread-pill{
    display:flex; align-items:center; gap:8px;
    font-size:12px;
    color:#8fa0bd;
    padding:9px 4px 0;
    border-top:1px solid rgba(255,255,255,0.07);
    margin-top:6px;
  }
  .dot{ width:6px; height:6px; border-radius:50%; background:var(--teal-400); flex-shrink:0; }

  /* ===== Main ===== */
  .main{ display:flex; flex-direction:column; min-height:100vh; }

  .topbar{
    display:flex; align-items:center; justify-content:space-between;
    padding:20px 32px 14px;
    background:var(--bg);
  }
  .topbar-left .eyebrow{
    font-family:var(--font-mono);
    font-size:10.5px;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color:var(--ink-400);
    margin:0 0 4px;
  }
  .topbar-left .title-row{
    display:flex; align-items:center; gap:10px;
  }
  .topbar-left h1{
    font-family:var(--font-display);
    font-size:19px;
    font-weight:600;
    margin:0;
  }
  .live-pill{
    display:flex; align-items:center; gap:5px;
    background:var(--ok-bg);
    color:var(--ok);
    font-size:11px;
    font-weight:700;
    letter-spacing:0.04em;
    padding:3px 10px;
    border-radius:20px;
  }
  .live-dot{
    width:6px; height:6px; border-radius:50%;
    background:var(--ok);
    animation:pulse 1.8s infinite;
  }
  @keyframes pulse{
    0%,100%{ opacity:1; } 50%{ opacity:0.35; }
  }

  .topbar-right{ display:flex; align-items:center; gap:10px; }
  
  .icon-btn{
    width:36px; height:36px; border-radius:9px;
    border:1px solid var(--line); background:var(--card);
    display:flex; align-items:center; justify-content:center;
    position:relative;
  }
  .icon-btn svg{ width:17px; height:17px; color:var(--ink-600); }
  .ping{
    position:absolute; top:-2px; right:-2px;
    width:8px; height:8px; border-radius:50%;
    background:var(--amber-500); border:2px solid var(--bg);
  }
.language-switcher{
  height:36px;
  min-width:110px;
  border-radius:9px;
  border:1px solid var(--line);
  background:var(--card);
  color:var(--ink-900);
  padding:0 10px;
  font-family:inherit;
  font-size:12px;
  font-weight:700;
  outline:none;
  cursor:pointer;
}

.language-switcher:focus{
  border-color:var(--teal-500);
}
  .loc-picker{
    display:flex; align-items:center; gap:8px;
    background:var(--card); border:1px solid var(--line);
    border-radius:11px; padding:9px 14px;
    font-size:13.5px; font-weight:600;
  }
  .loc-picker svg{ width:15px; height:15px; color:var(--teal-500); }
  .loc-picker .chev{ width:12px; height:12px; color:var(--ink-400); margin-left:2px; }

  .content{ padding:6px 32px 28px; flex:1; }

  /* ---- page: current weather ---- */
  .page{ display:none; }
  .page.active{ display:block; animation:fadein 0.25s ease; }
  @keyframes fadein{ from{opacity:0; transform:translateY(4px);} to{opacity:1; transform:translateY(0);} }

  .hero-row{ display:flex; justify-content:space-between; align-items:flex-start; gap:24px; margin-top:6px; }
  .hero-eyebrow{
    display:flex; align-items:center; gap:8px;
    font-family:var(--font-mono); font-size:10.5px; letter-spacing:0.16em;
    text-transform:uppercase; color:var(--teal-500); font-weight:700; margin-bottom:14px;
  }
  .hero-eyebrow::before{ content:""; width:22px; height:1.5px; background:var(--teal-500); display:inline-block; }
  .hero-title{
    font-family:var(--font-display);
    font-weight:600;
    font-size:44px;
    line-height:1.12;
    max-width:760px;
    margin:0 0 16px;
    letter-spacing:-0.01em;
  }
  .hero-meta{
    display:flex; align-items:center; gap:10px; flex-wrap:wrap;
    color:var(--ink-600); font-size:13.5px; margin-bottom:26px;
  }
  .hero-meta .chip{
    display:flex; align-items:center; gap:6px;
    background:var(--card); border:1px solid var(--line);
    padding:5px 11px; border-radius:20px;
  }
  .hero-meta .chip svg{ width:13px; height:13px; color:var(--amber-500); }
  .hero-meta .sep{ color:var(--ink-400); }

  .section-label{
    font-family:var(--font-mono); font-size:10.5px; letter-spacing:0.14em;
    text-transform:uppercase; color:var(--ink-400); font-weight:600;
    display:flex; align-items:center; gap:10px; margin:0 0 14px;
  }
  .section-label::after{ content:""; flex:1; height:1px; background:var(--line); }

  .suggest-grid{
    display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:22px;
  }
  .suggest-card{
    display:flex; align-items:center; justify-content:space-between; gap:12px;
    background:var(--card); border:1px solid var(--line); border-radius:var(--radius);
    padding:16px 18px; text-align:left; border-width:1px;
    transition:transform 0.14s ease, box-shadow 0.14s ease, border-color 0.14s ease;
  }
  .suggest-card:hover{ transform:translateY(-2px); box-shadow:0 10px 24px rgba(16,26,46,0.07); border-color:#c9e9e4; }
  .suggest-left{ display:flex; align-items:center; gap:13px; }
  .suggest-icon{
    width:38px; height:38px; border-radius:10px; background:var(--teal-050);
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
  }
  .suggest-icon svg{ width:18px; height:18px; color:var(--teal-500); }
  .suggest-text .k{
    font-family:var(--font-mono); font-size:10px; letter-spacing:0.1em;
    text-transform:uppercase; color:var(--ink-400); font-weight:700; margin:0 0 3px;
  }
  .suggest-text .q{ font-size:14.5px; font-weight:600; margin:0; }
  .suggest-card .arrow{ width:15px; height:15px; color:var(--ink-400); flex-shrink:0; }

  .quote-strip{
    display:flex; align-items:center; gap:12px;
    background:var(--card); border:1px solid var(--line); border-radius:var(--radius);
    padding:14px 18px; margin-bottom:20px; font-size:13.5px; color:var(--ink-600);
  }
  .quote-strip .stack{ width:17px; height:17px; color:var(--amber-500); flex-shrink:0; }
  .quote-strip .chev{ width:14px; height:14px; color:var(--ink-400); margin-left:auto; }

  /* chat transcript */
  .transcript{ display:flex; flex-direction:column; gap:14px; margin-bottom:16px; }
  .msg{ display:flex; gap:12px; max-width:780px; }
  .msg.user{ align-self:flex-end; flex-direction:row-reverse; }
  .msg-avatar{
    width:30px; height:30px; border-radius:9px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700;
  }
  .msg.assistant .msg-avatar{ background:var(--teal-050); color:var(--teal-500); }
  .msg.user .msg-avatar{ background:var(--amber-500); color:#1a1204; }
  .msg-bubble{
    background:var(--card); border:1px solid var(--line); border-radius:14px;
    padding:13px 16px; font-size:14px; line-height:1.55;
  }
  .msg.user .msg-bubble{ background:var(--navy-900); color:#e9eef7; border-color:var(--navy-900); }

  .causal-chain{
    display:flex; align-items:center; flex-wrap:wrap; gap:6px;
    margin:10px 0 12px; font-family:var(--font-mono); font-size:11.5px;
  }
  .causal-node{
    background:var(--teal-050); color:#0b6a60; padding:4px 10px; border-radius:20px; font-weight:600;
  }
  .causal-arrow{ color:var(--ink-400); }
  .prob-readout{
    display:flex; align-items:center; gap:14px;
    background:var(--warn-bg); border:1px solid #f3ddac; border-radius:12px;
    padding:12px 16px; margin-top:6px;
  }
  .prob-readout .num{ font-family:var(--font-display); font-size:26px; font-weight:600; color:var(--warn); }
  .prob-readout .lbl{ font-size:12.5px; color:#8a6015; line-height:1.4; }

  /* input dock */
  .dock{
    background:var(--card); border:1px solid var(--line); border-radius:18px;
    padding:16px 18px 12px; box-shadow:0 12px 30px rgba(16,26,46,0.05);
  }
  .dock textarea{
    width:100%; border:none; outline:none; resize:none;
    font-family:inherit; font-size:14.5px; color:var(--ink-900);
    min-height:24px; max-height:120px; background:none;
  }
  .dock textarea::placeholder{ color:var(--ink-400); }
  .dock-footer{ display:flex; align-items:center; justify-content:space-between; margin-top:10px; }
  .voice-btn{
    display:flex; align-items:center; gap:7px; background:none; border:none;
    color:var(--ink-600); font-size:13px; font-weight:500;
  }
  .voice-btn svg{ width:15px; height:15px; color:var(--teal-500); }
  .dock-right{ display:flex; align-items:center; gap:12px; }
  .kbd-hint{ font-family:var(--font-mono); font-size:10.5px; color:var(--ink-400); letter-spacing:0.04em; }
  .send-btn{
    width:38px; height:38px; border-radius:11px; border:none;
    background:var(--teal-500); color:#fff;
    display:flex; align-items:center; justify-content:center;
    transition:background 0.15s ease, transform 0.1s ease;
  }
  .send-btn:hover{ background:var(--teal-400); }
  .send-btn:active{ transform:scale(0.94); }
  .send-btn svg{ width:16px; height:16px; }
  .dock-tagline{ text-align:center; font-size:11.5px; color:var(--ink-400); margin:12px 0 0; }

  /* ---- forecast page ---- */
  .forecast-strip{ display:flex; gap:12px; overflow-x:auto; padding-bottom:6px; margin-bottom:26px; }
  .fc-card{
    flex:0 0 128px; background:var(--card); border:1px solid var(--line); border-radius:var(--radius);
    padding:16px 14px; text-align:center;
  }
  .fc-card.today{ border-color:var(--teal-400); box-shadow:0 0 0 1px var(--teal-400); }
  .fc-day{ font-size:12px; font-weight:700; color:var(--ink-600); margin:0 0 10px; }
  .fc-icon{ font-size:22px; margin-bottom:8px; }
  .fc-temp{ font-family:var(--font-display); font-size:19px; font-weight:600; margin:0 0 6px; }
  .fc-rain{ font-size:11.5px; color:var(--teal-500); font-weight:600; }

  .panel-grid{ display:grid; grid-template-columns:1.4fr 1fr; gap:18px; }
  .panel{
    background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:22px;
  }
  .panel h3{ font-family:var(--font-display); font-size:16px; margin:0 0 16px; }

  .flux-row{ display:flex; align-items:center; gap:14px; padding:11px 0; border-bottom:1px solid var(--line); }
  .flux-row:last-child{ border-bottom:none; }
  .flux-label{ width:110px; font-size:12.5px; color:var(--ink-600); font-weight:600; }
  .flux-bar-track{ flex:1; height:8px; background:var(--bg); border-radius:6px; overflow:hidden; }
  .flux-bar-fill{ height:100%; border-radius:6px; background:linear-gradient(90deg,var(--teal-400),var(--teal-500)); }
  .flux-val{ width:44px; text-align:right; font-family:var(--font-mono); font-size:12px; font-weight:600; }

  .advisory-item{ display:flex; gap:12px; padding:12px 0; border-bottom:1px solid var(--line); }
  .advisory-item:last-child{ border-bottom:none; }
  .advisory-dot{ width:8px; height:8px; border-radius:50%; margin-top:5px; flex-shrink:0; }
  .advisory-dot.ok{ background:var(--ok); }
  .advisory-dot.warn{ background:var(--warn); }
  .advisory-item .t{ font-size:13.5px; font-weight:600; margin:0 0 2px; }
  .advisory-item .d{ font-size:12.5px; color:var(--ink-600); margin:0; }

  /* ---- flood map page (signature element) ---- */
  .map-wrap{ display:grid; grid-template-columns:1fr 260px; gap:18px; }
  .grid-map{
    background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:20px;
  }
  .grid-map-head{ display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; }
  .grid-map-head h3{ font-family:var(--font-display); font-size:16px; margin:0; }
  .grid-map-head .sub{ font-family:var(--font-mono); font-size:11px; color:var(--ink-400); }
  .cellgrid{
    display:grid; grid-template-columns:repeat(14,1fr); gap:3px; aspect-ratio:14/9;
  }
  .cell{ border-radius:3px; position:relative; }
  .cell:hover::after{
    content:attr(data-p);
    position:absolute; bottom:110%; left:50%; transform:translateX(-50%);
    background:var(--navy-950); color:#fff; font-family:var(--font-mono);
    font-size:10px; padding:3px 6px; border-radius:5px; white-space:nowrap; z-index:2;
  }
  .map-legend{ display:flex; align-items:center; gap:14px; margin-top:14px; font-size:11.5px; color:var(--ink-600); }
  .legend-scale{ display:flex; align-items:center; gap:2px; }
  .legend-scale span{ width:16px; height:8px; border-radius:2px; }

  .side-panel{ display:flex; flex-direction:column; gap:14px; }
  .risk-card{ background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:18px; }
  .risk-card .k{ font-family:var(--font-mono); font-size:10.5px; letter-spacing:0.1em; text-transform:uppercase; color:var(--ink-400); margin:0 0 8px; }
  .risk-card .v{ font-family:var(--font-display); font-size:24px; font-weight:600; margin:0 0 4px; }
  .risk-card .d{ font-size:12px; color:var(--ink-600); margin:0; }

  /* ---- alerts page ---- */
  .alert-card{
    display:flex; gap:14px; background:var(--card); border:1px solid var(--line);
    border-left:4px solid var(--warn); border-radius:12px; padding:16px 18px; margin-bottom:12px;
  }
  .alert-card.high{ border-left-color:var(--danger); }
  .alert-card .a-icon{ font-size:19px; }
  .alert-card .a-title{ font-size:14.5px; font-weight:700; margin:0 0 4px; }
  .alert-card .a-body{ font-size:13px; color:var(--ink-600); margin:0 0 8px; }
  .alert-card .a-meta{ font-family:var(--font-mono); font-size:10.5px; color:var(--ink-400); }
  .sev-badge{
    font-size:10.5px; font-weight:700; padding:2px 9px; border-radius:20px; margin-left:auto; align-self:flex-start;
  }
  .sev-badge.moderate{ background:var(--warn-bg); color:var(--warn); }
  .sev-badge.high{ background:var(--danger-bg); color:var(--danger); }

  /* ---- climate insights page ---- */
  .trend-card{ background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:22px; margin-bottom:18px; }
  .trend-card h3{ font-family:var(--font-display); font-size:16px; margin:0 0 4px; }
  .trend-card .sub{ font-size:12.5px; color:var(--ink-600); margin:0 0 18px; }

  .kpi-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:20px; }
  .kpi{ background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:18px; }
  .kpi .v{ font-family:var(--font-display); font-size:26px; font-weight:600; margin:0 0 4px; }
  .kpi .l{ font-size:12px; color:var(--ink-600); margin:0; }
  .kpi .delta{ font-size:11.5px; font-weight:700; margin-left:6px; }
  .kpi .delta.up{ color:var(--danger); }
  .kpi .delta.down{ color:var(--ok); }

  ::-webkit-scrollbar{ height:8px; width:8px; }
  ::-webkit-scrollbar-thumb{ background:#d7dce4; border-radius:8px; }

  @media (max-width: 880px){
    .app{ grid-template-columns:1fr; }
    .sidebar{ display:none; }
    .hero-title{ font-size:30px; }
    .suggest-grid{ grid-template-columns:1fr; }
    .panel-grid, .map-wrap{ grid-template-columns:1fr; }
    .kpi-grid{ grid-template-columns:1fr; }
  }


/* --- fixed, always-visible ask dock --- */
.main{ height:100vh; overflow:hidden; }
.content{ overflow-y:auto; padding-bottom:16px; }
#page-home.page.active{ display:flex; flex-direction:column; height:100%; }
#page-home .transcript{ flex:1; overflow-y:auto; min-height:0; }
#page-home .dock{ position:sticky; bottom:0; z-index:5; }
#page-home .dock-tagline{ margin-bottom:0; }
`;

export const WG_MARKUP = `

<div class="app">
  <!-- ================= SIDEBAR ================= -->
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-mark">
        <svg viewBox="0 0 24 24" fill="none"><path d="M6 14a4 4 0 010-8 5 5 0 019.6-1.5A4.5 4.5 0 0118 14H6z" stroke="#06282a" stroke-width="1.6" stroke-linejoin="round"/><path d="M8 17.5l-1 2M12 17.5l-1 2M16 17.5l-1 2" stroke="#06282a" stroke-width="1.6" stroke-linecap="round"/></svg>
      </div>
      <div>
        <p class="brand-eyebrow">MausamAI </p>
        <p class="brand-title">Flood Intelligence</p>
      </div>
    </div>

    <div class="loc-card">
      <p class="loc-label">Your location</p>
      <p class="loc-name">Bhubaneswar, Odisha</p>
      <button class="loc-action">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 2v3M12 19v3M2 12h3M19 12h3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="12" r="4.5" stroke="currentColor" stroke-width="1.8"/></svg>
        Use current location
      </button>
    </div>

    <div>
      <p class="nav-label">Workspace</p>
      <nav class="nav" id="mainNav">
        <button class="nav-item active" data-page="home">
          <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.7"/><path d="M12 2v2M12 20v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2 12h2M20 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
          Current weather
        </button>
        <button class="nav-item" data-page="forecast">
          <svg viewBox="0 0 24 24" fill="none"><rect x="3.5" y="4.5" width="17" height="16" rx="2.5" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 9.5h17M8 3v3M16 3v3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          Forecasts
        </button>
        <button class="nav-item" data-page="map">
          <svg viewBox="0 0 24 24" fill="none"><path d="M9 4L3.5 6.2v13.3L9 17.3l6 2.5 5.5-2.2V4.3L15 6.8 9 4z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M9 4v13.3M15 6.8v13" stroke="currentColor" stroke-width="1.5"/></svg>
          Flood map
        </button>
        <button class="nav-item" data-page="alerts">
          <svg viewBox="0 0 24 24" fill="none"><path d="M12 3L2 20h20L12 3z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 10v4.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="17" r="0.9" fill="currentColor"/></svg>
          Alerts
          <span class="nav-badge">3</span>
        </button>
        <button class="nav-item" data-page="climate">
          <svg viewBox="0 0 24 24" fill="none"><path d="M3 17c2 0 2-2 4-2s2 2 4 2 2-2 4-2 2 2 4 2M3 12c2 0 2-2 4-2s2 2 4 2 2-2 4-2 2 2 4 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          Climate insights
        </button>
      </nav>
    </div>

    <div class="sidebar-spacer"></div>

    <button class="new-question">
      <svg viewBox="0 0 24 24" fill="none" style="width:14px;height:14px;"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      New question
    </button>
    <div class="thread-pill">
      <span class="dot"></span>
      Grid-based, causal, built for Odisha
    </div>
  </aside>

  <!-- ================= MAIN ================= -->
  <main class="main">
    <header class="topbar">
      <div class="topbar-left">
        <p class="eyebrow" id="pageEyebrow">Current weather</p>
        <div class="title-row">
          <h1 id="pageTitle">Bhubaneswar, Odisha</h1>
          <span class="live-pill"><span class="live-dot"></span>LIVE</span>
        </div>
      </div>
      <div class="topbar-right">
        
        <button class="icon-btn" aria-label="Notifications">
          <svg viewBox="0 0 24 24" fill="none"><path d="M12 3a5.5 5.5 0 00-5.5 5.5v3.2L4.8 15h14.4l-1.7-3.3V8.5A5.5 5.5 0 0012 3z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M9.7 18a2.3 2.3 0 004.6 0" stroke="currentColor" stroke-width="1.5"/></svg>
          <span class="ping"></span>
        </button>
        <select class="language-switcher" id="languageSwitcher" aria-label="Change language">
  <option value="en">English</option>
  <option value="hi">हिन्दी</option>
  <option value="or">ଓଡ଼ିଆ</option>
  <option value="bn">বাংলা</option>
  <option value="gu">ગુજરાતી</option>
  <option value="mr">मराठी</option>
  <option value="kn">ಕನ್ನಡ</option>
  <option value="ta">தமிழ்</option>
  <option value="te">తెలుగు</option>
  <option value="pa">ਪੰਜਾਬੀ</option>
</select>
      </div>
    </header>

    <section class="content">

      <!-- ============ PAGE: HOME / CURRENT WEATHER ============ -->
      <div class="page active" id="page-home">
        <div class="hero-row">
          <div style="flex:1;">
            <p class="hero-eyebrow">Today</p>
            <h2 class="hero-title" id="heroTitle">Want to know your flood risk before it matters? Ask here.</h2>
            <div class="hero-meta">
              <span class="chip">
                <svg viewBox="0 0 24 24" fill="none"><path d="M12 2v11M12 13a4 4 0 104 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                Rainfall intensifying after 4 PM
              </span>
              <span class="sep">/</span>
              <span>Updated 6 min ago </span>
            </div>
          </div>
          <div class="loc-picker">
            <svg viewBox="0 0 24 24" fill="none"><path d="M12 21s7-6.1 7-11.5A7 7 0 005 9.5C5 14.9 12 21 12 21z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="9.5" r="2.3" stroke="currentColor" stroke-width="1.6"/></svg>
            Bhubaneswar, Odisha
            <svg class="chev" viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          </div>
        </div>

       

        <p class="section-label">Conversation</p>
        <div class="transcript" id="transcript">
          <div class="msg assistant">
            <div class="msg-avatar">W</div>
            <div class="msg-bubble">
              Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.
            </div>
          </div>
        </div>

        <div class="dock">
          <textarea id="chatInput" rows="1" placeholder="Ask MausamAI anything about weather and flood risk…"></textarea>
          <div class="dock-footer">
            <button class="voice-btn">
              <svg viewBox="0 0 24 24" fill="none"><rect x="9" y="3" width="6" height="11" rx="3" stroke="currentColor" stroke-width="1.6"/><path d="M5 11a7 7 0 0014 0M12 18v3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
              Voice
            </button>
            <div class="dock-right">
              <span class="kbd-hint">SHIFT + ENTER FOR NEW LINE</span>
              <button class="send-btn" id="sendBtn" aria-label="Send">
                <svg viewBox="0 0 24 24" fill="none"><path d="M3 12l18-8-8 18-2.5-7.5L3 12z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>
              </button>
            </div>
          </div>
        </div>
        <p class="dock-tagline">Grid-level forecasts · causal reasoning · plain-language advisories</p>
      </div>

      <!-- ============ PAGE: FORECASTS ============ -->
      <div class="page" id="page-forecast">
        <p class="section-label">Next 6 days · Bhubaneswar grid cluster</p>
        <div class="forecast-strip">
          <div class="fc-card today"><p class="fc-day">Today</p><div class="fc-icon">🌦️</div><p class="fc-temp">29°</p><p class="fc-rain">62% rain</p></div>
          <div class="fc-card"><p class="fc-day">Thu</p><div class="fc-icon">⛈️</div><p class="fc-temp">27°</p><p class="fc-rain">81% rain</p></div>
          <div class="fc-card"><p class="fc-day">Fri</p><div class="fc-icon">⛈️</div><p class="fc-temp">26°</p><p class="fc-rain">88% rain</p></div>
          <div class="fc-card"><p class="fc-day">Sat</p><div class="fc-icon">🌥️</div><p class="fc-temp">28°</p><p class="fc-rain">34% rain</p></div>
          <div class="fc-card"><p class="fc-day">Sun</p><div class="fc-icon">⛅</div><p class="fc-temp">30°</p><p class="fc-rain">18% rain</p></div>
          <div class="fc-card"><p class="fc-day">Mon</p><div class="fc-icon">☀️</div><p class="fc-temp">31°</p><p class="fc-rain">6% rain</p></div>
        </div>

        <div class="panel-grid">
          <div class="panel">
            <h3>Prediction layer — model signals</h3>
            <div class="flux-row"><div class="flux-label">Rainfall</div><div class="flux-bar-track"><div class="flux-bar-fill" style="width:82%;"></div></div><div class="flux-val">82%</div></div>
            <div class="flux-row"><div class="flux-label">Soil saturation</div><div class="flux-bar-track"><div class="flux-bar-fill" style="width:67%;"></div></div><div class="flux-val">67%</div></div>
            <div class="flux-row"><div class="flux-label">Runoff index</div><div class="flux-bar-track"><div class="flux-bar-fill" style="width:54%;"></div></div><div class="flux-val">54%</div></div>
            <div class="flux-row"><div class="flux-label">Terrain drainage</div><div class="flux-bar-track"><div class="flux-bar-fill" style="width:31%;"></div></div><div class="flux-val">31%</div></div>
            <div class="flux-row"><div class="flux-label">P(flood), 6h</div><div class="flux-bar-track"><div class="flux-bar-fill" style="width:38%; background:linear-gradient(90deg,#e8a13a,#d0453a);"></div></div><div class="flux-val">38%</div></div>
          </div>
          <div class="panel">
            <h3>Reasoning &amp; decision layer</h3>
            <div class="advisory-item"><span class="advisory-dot warn"></span><div><p class="t">Moderate flood risk after 4 PM</p><p class="d">Saturated soil + sustained rainfall raises runoff in low-lying wards.</p></div></div>
            <div class="advisory-item"><span class="advisory-dot ok"></span><div><p class="t">Morning commute unaffected</p><p class="d">Roads stay dry until early afternoon — safe travel window before 1 PM.</p></div></div>
            <div class="advisory-item"><span class="advisory-dot warn"></span><div><p class="t">Delay crop spraying</p><p class="d">Rain likely to wash off treatment before it takes effect.</p></div></div>
          </div>
        </div>
      </div>

      <!-- ============ PAGE: FLOOD MAP ============ -->
      <div class="page" id="page-map">
        <p class="section-label">Grid cell risk — P(flood) by cell</p>
        <div class="map-wrap">
          <div class="grid-map">
            <div class="grid-map-head">
              <h3>Odisha coastal grid, next 24h</h3>
              <span class="sub">grid_id · calibrated probability</span>
            </div>
            <div class="cellgrid" id="cellGrid"></div>
            <div class="map-legend">
              <span>Low</span>
              <div class="legend-scale">
                <span style="background:#e6f5f2;"></span>
                <span style="background:#9fded2;"></span>
                <span style="background:#3fbfab;"></span>
                <span style="background:#e8a13a;"></span>
                <span style="background:#d0453a;"></span>
              </div>
              <span>High</span>
            </div>
          </div>
          <div class="side-panel">
            <div class="risk-card">
              <p class="k">Highest-risk cell</p>
              <p class="v">B-114</p>
              <p class="d">P(flood) 0.71 · near Kuakhai river bend</p>
            </div>
            <div class="risk-card">
              <p class="k">Cells above threshold</p>
              <p class="v">9 / 168</p>
              <p class="d">Threshold set at P ≥ 0.35 for advisory trigger</p>
            </div>
            <div class="risk-card">
              <p class="k">Model</p>
              <p class="v">XGBoost v3</p>
              <p class="d">Rainfall + soil + DEM + causal interactions, isotonic-calibrated</p>
            </div>
          </div>
        </div>
      </div>

      <!-- ============ PAGE: ALERTS ============ -->
      <div class="page" id="page-alerts">
        <p class="section-label">Active alerts</p>

        <div class="alert-card high">
          <div class="a-icon">⛔</div>
          <div style="flex:1;">
            <p class="a-title">Flash flood watch — low-lying wards, Bhubaneswar East</p>
            <p class="a-body">Runoff modeling shows a sharp rise in cell-level flood probability after 4 PM as rainfall compounds with already-saturated soil.</p>
            <p class="a-meta">ISSUED 09:20 · VALID UNTIL TOMORROW 06:00</p>
          </div>
          <span class="sev-badge high">High</span>
        </div>

        <div class="alert-card">
          <div class="a-icon">🌧️</div>
          <div style="flex:1;">
            <p class="a-title">Sustained heavy rainfall expected, coastal belt</p>
            <p class="a-body">Rainfall intensity likely to stay above the 24h threshold used in the prediction pipeline — monitor cell B-114 and neighbors.</p>
            <p class="a-meta">ISSUED YESTERDAY 21:40 · VALID UNTIL TODAY 20:00</p>
          </div>
          <span class="sev-badge moderate">Moderate</span>
        </div>

        <div class="alert-card">
          <div class="a-icon">🚜</div>
          <div style="flex:1;">
            <p class="a-title">Farm advisory — delay spraying and low-field work</p>
            <p class="a-body">Soil saturation trend suggests standing water risk in low fields near Daya river cells over the next 12 hours.</p>
            <p class="a-meta">ISSUED TODAY 07:05 · VALID UNTIL TOMORROW 12:00</p>
          </div>
          <span class="sev-badge moderate">Moderate</span>
        </div>
      </div>

      <!-- ============ PAGE: CLIMATE INSIGHTS ============ -->
      <div class="page" id="page-climate">
        <p class="section-label">Seasonal trends</p>
        <div class="kpi-grid">
          <div class="kpi"><p class="v">+18%<span class="delta up">▲</span></p><p class="l">Monsoon rainfall vs. 10yr avg</p></div>
          <div class="kpi"><p class="v">0.185%<span class="delta up">▲</span></p><p class="l">Flood-day prevalence, all grid cells</p></div>
          <div class="kpi"><p class="v">73.2%<span class="delta down">▼</span></p><p class="l">Event-level detection rate, current model</p></div>
        </div>

        <div class="trend-card">
          <h3>Rainfall vs. soil saturation, last 14 days</h3>
          <p class="sub">Rising soil saturation ahead of rainfall spikes is the leading causal signal the model tracks.</p>
          <svg viewBox="0 0 600 180" width="100%" height="180" preserveAspectRatio="none">
            <polyline fill="none" stroke="#1cb5a4" stroke-width="2.5" points="0,140 40,132 80,120 120,128 160,90 200,70 240,95 280,60 320,50 360,75 400,40 440,55 480,30 520,45 560,20 600,35"/>
            <polyline fill="none" stroke="#e8a13a" stroke-width="2.5" stroke-dasharray="5,4" points="0,160 40,158 80,150 120,152 160,138 200,128 240,135 280,112 320,105 360,118 400,95 440,102 480,85 520,92 560,78 600,84"/>
          </svg>
        </div>

        <div class="panel-grid">
          <div class="panel">
            <h3>Where the model still struggles</h3>
            <div class="advisory-item"><span class="advisory-dot warn"></span><div><p class="t">Cell-level precision ~1.3%</p><p class="d">Rare-event imbalance makes exact-cell prediction hard; event-level detection is far stronger.</p></div></div>
            <div class="advisory-item"><span class="advisory-dot warn"></span><div><p class="t">Spatial IoU ~0.014</p><p class="d">Predicted flood extent often misaligns with true extent — informs the move toward GNN-based spatial modeling.</p></div></div>
          </div>
          <div class="panel">
            <h3>Roadmap</h3>
            <div class="advisory-item"><span class="advisory-dot ok"></span><div><p class="t">Hard-negative + spatial sampling</p><p class="d">Training-only rebalancing, val/test left untouched.</p></div></div>
            <div class="advisory-item"><span class="advisory-dot ok"></span><div><p class="t">Temporal + spatial models → causal Bayesian net</p><p class="d">TCN/LSTM and GNN feeding a rainfall → soil → runoff → flood reasoning chain.</p></div></div>
          </div>
        </div>
      </div>

    </section>
  </main>
</div>

`;

export const WG_SCRIPT = `
  // ---- Nav switching ----
  const navItems = document.querySelectorAll('.nav-item');
  const pages = document.querySelectorAll('.page');
  const pageMeta = {
    home:     { eyebrow: 'Current weather', title: 'Bhubaneswar, Odisha' },
    forecast: { eyebrow: 'Forecasts',        title: '6-day flood-aware outlook' },
    map:      { eyebrow: 'Flood map',        title: 'Grid risk — Odisha coast' },
    alerts:   { eyebrow: 'Alerts',           title: '3 active advisories' },
    climate:  { eyebrow: 'Climate insights', title: 'Seasonal &amp; model trends' },
  };

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');
      const key = item.dataset.page;
      pages.forEach(p => p.classList.remove('active'));
      document.getElementById('page-' + key).classList.add('active');
      document.getElementById('pageEyebrow').textContent = pageMeta[key].eyebrow;
      document.getElementById('pageTitle').innerHTML = pageMeta[key].title;
    });
  });

  // ---- Language toggle (display-only demo) ----
  const langButtons = document.querySelectorAll('.lang-toggle button');
  const strings = {
    en: { hero: "Want to know your flood risk before it matters? Ask here.", placeholder: "Ask MausamAI anything about weather and flood risk…" },
    or: { hero: "ବନ୍ୟା ବିପଦ ଆସିବା ପୂର୍ବରୁ ଜାଣିବାକୁ ଚାହୁଁଛନ୍ତି? ଏଠାରେ ପଚାରନ୍ତୁ।", placeholder: "ପାଣିପାଗ ଓ ବନ୍ୟା ବିଷୟରେ MausamAI କୁ ପଚାରନ୍ତୁ…" }
  };
  langButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      langButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const lang = btn.dataset.lang;
      document.getElementById('heroTitle').textContent = strings[lang].hero;
      document.getElementById('chatInput').placeholder = strings[lang].placeholder;
    });
  });


  // ---- Chat: send behavior with mock causal-chain reply ----
  const transcript = document.getElementById('transcript');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');

  function addMessage(role, html){
    const wrap = document.createElement('div');
    wrap.className = 'msg ' + role;
    wrap.innerHTML = \`
      <div class="msg-avatar">\${role === 'user' ? 'RS' : 'W'}</div>
      <div class="msg-bubble">\${html}</div>
    \`;
    transcript.appendChild(wrap);
    wrap.scrollIntoView({ behavior:'smooth', block:'end' });
  }

  function mockAnswer(q){
    return \`Based on the current pipeline for this grid cluster:
      <div class="causal-chain">
        <span class="causal-node">Heavy rainfall</span><span class="causal-arrow">→</span>
        <span class="causal-node">Soil saturation ↑</span><span class="causal-arrow">→</span>
        <span class="causal-node">Runoff ↑</span><span class="causal-arrow">→</span>
        <span class="causal-node">Flood risk</span>
      </div>
      <div class="prob-readout">
        <div class="num">38%</div>
        <div class="lbl">Calibrated P(flood) over the next 6 hours — <strong>moderate</strong>. Avoid low-lying routes after 4 PM.</div>
      </div>\`;
  }

  function handleSend(){
    const val = chatInput.value.trim();
    if(!val) return;
    addMessage('user', val);
    chatInput.value = '';
    setTimeout(() => addMessage('assistant', mockAnswer(val)), 380);
  }

  sendBtn.addEventListener('click', handleSend);
  chatInput.addEventListener('keydown', e => {
    if(e.key === 'Enter' && !e.shiftKey){
      e.preventDefault();
      handleSend();
    }
  });
  chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
  });

  // ---- Build the flood-risk grid heatmap ----
  const cellGrid = document.getElementById('cellGrid');
  const palette = ['#e6f5f2','#c9ece4','#9fded2','#3fbfab','#e8a13a','#d0453a'];
  const TOTAL_CELLS = 14 * 9;
  // seeded pseudo-random so the map looks the same every load
  let seed = 42;
  function rand(){ seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }

  for(let i = 0; i < TOTAL_CELLS; i++){
    const r = rand();
    // skew distribution toward low risk, occasional hot cells (mirrors the ~0.185% flood prevalence)
    let p;
    if(r > 0.94) p = 0.55 + rand()*0.35;
    else if(r > 0.8) p = 0.25 + rand()*0.25;
    else p = rand()*0.2;

    let color;
    if(p < 0.12) color = palette[0];
    else if(p < 0.22) color = palette[1];
    else if(p < 0.35) color = palette[2];
    else if(p < 0.5) color = palette[3];
    else color = palette[5];

    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.style.background = color;
    cell.dataset.p = 'P(flood) ' + p.toFixed(2);
    cellGrid.appendChild(cell);
  }
`;
