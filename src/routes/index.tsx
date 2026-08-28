import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";

import { WG_CSS, WG_MARKUP, WG_SCRIPT } from "@/lib/weathergpt-assets";
import { LANGUAGES, translateHtml, type LangCode } from "@/lib/weathergpt-i18n";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "MausamAI — Flood Intelligence Desk for Odisha" },
      {
        name: "description",
        content:
          "Grid-level rainfall and flood risk answers for Odisha in ten Indian languages, with causal reasoning and plain-language advisories.",
      },
      { property: "og:title", content: "MausamAI — Flood Intelligence Desk" },
      {
        property: "og:description",
        content:
          "Ask about flood risk, safe travel windows and advisories for any grid cell in Odisha, in your own language.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

const GATE_CSS = `
.lang-gate{
  position:fixed; inset:0; z-index:50;
  background:linear-gradient(180deg,#101a2e,#0b1220);
  color:#e9eef7;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:26px; padding:32px; text-align:center;
  font-family:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
.lang-gate .gate-mark{
  width:52px; height:52px; border-radius:14px;
  background:linear-gradient(140deg,#1cb5a4,#0f9b8e);
  display:flex; align-items:center; justify-content:center;
  box-shadow:0 6px 20px rgba(15,155,142,0.35);
}
.lang-gate h1{
  font-family:"Fraunces","Iowan Old Style",Georgia,serif;
  font-size:34px; font-weight:600; margin:0;
}
.lang-gate p.sub{ margin:0; color:#9fb0cc; font-size:14.5px; }
.lang-grid{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr));
  gap:12px; width:100%; max-width:760px;
}
.lang-btn{
  background:rgba(255,255,255,0.045);
  border:1px solid rgba(255,255,255,0.1);
  border-radius:14px; padding:16px 14px; color:#e9eef7;
  display:flex; flex-direction:column; gap:4px; align-items:center;
  transition:border-color .15s ease, background .15s ease, transform .15s ease;
}
.lang-btn:hover{ border-color:#1cb5a4; background:rgba(28,181,164,0.12); transform:translateY(-2px); }
.lang-btn .native{ font-size:19px; font-weight:600; }
.lang-btn .prompt{ font-size:11.5px; color:#9fb0cc; }
`;

function Index() {
  const [lang, setLang] = useState<LangCode | null>(null);
  const hostRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const saved = localStorage.getItem("wg-lang") as LangCode | null;
    if (saved && LANGUAGES.some((l) => l.code === saved)) setLang(saved);
  }, []);

  useEffect(() => {
  if (!lang || !hostRef.current) return;

  hostRef.current.innerHTML = translateHtml(WG_MARKUP, lang);

  // Keep the existing WeatherGPT script working
  // eslint-disable-next-line @typescript-eslint/no-implied-eval
  new Function(WG_SCRIPT)();

  // Language changer inside the WeatherGPT header
  const languageSwitcher =
    hostRef.current.querySelector<HTMLSelectElement>("#languageSwitcher");

  if (languageSwitcher) {
    languageSwitcher.value = lang;

    const handleLanguageChange = (event: Event) => {
      const target = event.target as HTMLSelectElement;
      choose(target.value as LangCode);
    };

    languageSwitcher.addEventListener("change", handleLanguageChange);
  }
}, [lang]);

  const choose = (code: LangCode) => {
    localStorage.setItem("wg-lang", code);
    setLang(code);
  };

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: WG_CSS + GATE_CSS }} />
      {lang ? (
        <div ref={hostRef} />
      ) : (
        <div className="lang-gate">
          <div className="gate-mark">
            <svg viewBox="0 0 24 24" fill="none" style={{ width: 26, height: 26 }}>
              <path
                d="M6 14a4 4 0 010-8 5 5 0 019.6-1.5A4.5 4.5 0 0118 14H6z"
                stroke="#06282a"
                strokeWidth="1.6"
                strokeLinejoin="round"
              />
              <path
                d="M8 17.5l-1 2M12 17.5l-1 2M16 17.5l-1 2"
                stroke="#06282a"
                strokeWidth="1.6"
                strokeLinecap="round"
              />
            </svg>
          </div>
          <div>
            <h1>WeatherGPT</h1>
            <p className="sub">भाषा · ଭାଷା · ভাষা · ભાષા · ಭಾಷೆ · மொழி · భాష · ਭਾਸ਼ਾ</p>
          </div>
          <div className="lang-grid">
            {LANGUAGES.map((l) => (
              <button key={l.code} className="lang-btn" onClick={() => choose(l.code)}>
                <span className="native">{l.native}</span>
                <span className="prompt">{l.prompt}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
