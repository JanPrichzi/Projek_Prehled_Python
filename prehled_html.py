import json
from IPython.display import HTML, display


def vykresli_html_prehled(skore_zprav, detaily_clanku, index_duvery, obdobi_duvery, kurzy_dict, vychozi_mena="EUR"):
    data_payload = {
        "skoreZprav": round(float(skore_zprav), 2),
        "clanky": detaily_clanku,
        "indexDuvery": index_duvery,
        "obdobiDuvery": obdobi_duvery or "",
        "kurzy": kurzy_dict,
        "vychoziMena": vychozi_mena if vychozi_mena in kurzy_dict else (next(iter(kurzy_dict), "EUR")),
    }
    json_data = json.dumps(data_payload, ensure_ascii=False)

    html_code = f"""
    <div id="app-root-6" style="font-family: Inter, system-ui, -apple-system, sans-serif; margin: 16px 0;">
      <style>
        .btn-spustit {{
          background: linear-gradient(135deg, #1e293b, #0f172a);
          color: #ffffff;
          border: none;
          padding: 12px 22px;
          font-size: 15px;
          font-weight: 600;
          border-radius: 10px;
          cursor: pointer;
          box-shadow: 0 4px 12px rgba(15, 23, 42, 0.18);
          transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.2s ease;
        }}
        .btn-spustit:hover {{
          transform: translateY(-1px);
          box-shadow: 0 6px 16px rgba(15, 23, 42, 0.25);
        }}
        .btn-spustit:active {{
          transform: translateY(0);
        }}

        .dashboard-card {{
          display: none;
          margin-top: 14px;
          background: #ffffff;
          border: 2px solid #0f172a;
          border-radius: 16px;
          padding: 24px;
          box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
          color: #000000;
        }}
        .dashboard-card.visible {{
          display: block;
          animation: fadeInCard 0.25s ease-out;
        }}
        @keyframes fadeInCard {{
          from {{ opacity: 0; transform: translateY(6px); }}
          to {{ opacity: 1; transform: translateY(0); }}
        }}

        .top-row {{
          display: flex;
          justify-content: center;
          align-items: stretch;
          gap: 20px;
          margin-bottom: 28px;
          transition: all 0.3s ease;
        }}
        .top-row.expanded {{
          justify-content: space-between;
        }}

        .score-box {{
          flex: 0 1 420px;
          background: #f8fafc;
          border: 1.5px solid #cbd5e1;
          border-radius: 14px;
          padding: 18px 22px;
          text-align: center;
          cursor: pointer;
          user-select: none;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          transition: all 0.3s ease;
        }}
        .score-box:hover {{
          border-color: #0f172a;
          background: #f1f5f9;
        }}
        .top-row.expanded .score-box {{
          flex: 0 0 320px;
        }}

        .box-title {{
          font-size: 32px;
          font-weight: 800;
          line-height: 1.2;
          letter-spacing: -0.01em;
          color: #000000;
          margin-bottom: 8px;
        }}
        .big-metric {{
          font-size: 32px;
          font-weight: 800;
          line-height: 1.2;
          color: #000000;
          margin: 4px 0;
        }}
        .period-label {{
          font-size: 15px;
          font-weight: 600;
          color: #334155;
          margin-top: 2px;
        }}
        .hint-text {{
          font-size: 12px;
          color: #475569;
          margin-top: 6px;
        }}

        .articles-panel {{
          display: none;
          flex: 1;
          background: #f8fafc;
          border: 1.5px solid #cbd5e1;
          border-radius: 14px;
          padding: 16px 20px;
          max-height: 310px;
          overflow-y: auto;
        }}
        .top-row.expanded .articles-panel {{
          display: block;
        }}
        .articles-header-title {{
          font-size: 18px;
          font-weight: 800;
          color: #000000;
          margin-bottom: 10px;
        }}
        .article-item {{
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          gap: 12px;
          padding: 8px 0;
          border-bottom: 1px solid #e2e8f0;
          font-size: 13.5px;
          color: #000000;
        }}
        .article-score {{
          white-space: nowrap;
          font-weight: 700;
          background: #e2e8f0;
          color: #000000;
          padding: 2px 8px;
          border-radius: 999px;
          font-size: 12px;
        }}
        .articles-source-row {{
          margin-top: 12px;
          padding-top: 10px;
          border-top: 1px solid #cbd5e1;
          font-size: 12px;
        }}

        .bottom-row {{
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 24px;
          align-items: stretch;
        }}
        @media (max-width: 780px) {{
          .bottom-row {{
            grid-template-columns: 1fr;
          }}
          .top-row.expanded {{
            flex-direction: column;
          }}
          .top-row.expanded .score-box {{
            flex: 1 1 auto;
          }}
        }}

        .info-panel {{
          background: #f8fafc;
          border: 1.5px solid #e2e8f0;
          border-radius: 14px;
          padding: 20px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          height: 100%;
          box-sizing: border-box;
        }}
        .info-panel.center-text {{
          text-align: center;
        }}
        .comment-text {{
          margin-top: 8px;
          font-size: 15px;
          font-weight: 600;
          color: #0f172a;
        }}
        .source-note {{
          margin-top: 12px;
          padding-top: 8px;
          border-top: 1px solid #e2e8f0;
          font-size: 11.5px;
          color: #475569;
          word-break: break-all;
        }}
        .source-note a,
        .articles-source-row a {{
          color: #1d4ed8;
          text-decoration: underline;
          cursor: pointer;
        }}

        .currency-header {{
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          justify-content: center;
          gap: 8px;
          margin-bottom: 12px;
        }}
        .currency-select {{
          padding: 6px 10px;
          font-size: 18px;
          font-weight: 700;
          border-radius: 8px;
          border: 1.5px solid #000000;
          background: #ffffff;
          color: #000000;
          cursor: pointer;
        }}
        .kurz-grid {{
          display: grid;
          grid-template-columns: auto auto;
          justify-content: center;
          column-gap: 18px;
          row-gap: 8px;
          font-size: 15px;
          margin-top: 10px;
        }}
        .kurz-label {{
          font-weight: 700;
          text-align: left;
          color: #000000;
        }}
        .kurz-val {{
          font-weight: 600;
          text-align: left;
          color: #000000;
        }}
      </style>

      <button id="btn-spustit-6" class="btn-spustit" onclick="spustitDashboard6()">
        ▶ Spustit přehled
      </button>

      <div id="dashboard-card-6" class="dashboard-card">
        <div id="top-row-6" class="top-row">
          <div id="score-box-6" class="score-box" onclick="prepniDetailyZprav6()" title="Kliknutím rozbalíte/sbalíte detail článků">
            <div class="box-title">SKÓRE ZPRÁV</div>
            <div id="score-value-6" class="big-metric">0</div>
            <div id="score-emoji-6" style="font-size: 24px;">😐</div>
            <div id="score-hint-6" class="hint-text">Kliknutím zobrazíte detail článků</div>
          </div>

          <div id="articles-panel-6" class="articles-panel">
            <div class="articles-header-title">DETAILNÍ ROZEPSÁNÍ ČLÁNKŮ</div>
            <div id="articles-list-6"></div>
            <div class="articles-source-row">
              Zdroj: <a href="https://ct24.ceskatelevize.cz" target="_blank" rel="noopener noreferrer">https://ct24.ceskatelevize.cz</a>
            </div>
          </div>
        </div>

        <div class="bottom-row">
          <div class="info-panel center-text">
            <div>
              <div class="box-title">SOUHRNNÝ INDIKÁTOR DŮVĚRY</div>
              <div id="csu-value-6" class="big-metric">–</div>
              <div id="csu-period-6" class="period-label"></div>
              <div id="csu-comment-6" class="comment-text">Načítání...</div>
            </div>
            <div class="source-note">
              Zdroj: <a href="https://csu.gov.cz/konjunkturalni-pruzkumy" target="_blank" rel="noopener noreferrer">https://csu.gov.cz/konjunkturalni-pruzkumy</a>
            </div>
          </div>

          <div class="info-panel center-text">
            <div>
              <div class="currency-header">
                <span class="box-title" style="margin: 0;">KURZ</span>
                <select id="currency-select-6" class="currency-select" onchange="aktualizujKurz6()"></select>
                <span class="box-title" style="margin: 0;">/CZK</span>
              </div>

              <div class="kurz-grid">
                <div class="kurz-label">Aktuální kurz:</div>
                <div id="kurz-aktualni-6" class="kurz-val">–</div>

                <div class="kurz-label">90denní průměr:</div>
                <div id="kurz-ma90-6" class="kurz-val">–</div>

                <div class="kurz-label">Odchylka:</div>
                <div id="kurz-odchylka-6" class="kurz-val">–</div>

                <div class="kurz-label">EXPORTÉR:</div>
                <div id="kurz-export-6" class="kurz-val">–</div>

                <div class="kurz-label">IMPORTÉR:</div>
                <div id="kurz-import-6" class="kurz-val">–</div>
              </div>
            </div>

            <div class="source-note">
              Zdroj: <a href="https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/" target="_blank" rel="noopener noreferrer">https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/</a>
            </div>
          </div>
        </div>
      </div>

      <script>
        const PAYLOAD_6 = {json_data};

        function formatCzNumber(num, decimals = 2) {{
          return Number(num).toLocaleString("cs-CZ", {{
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
          }});
        }}

        function spustitDashboard6() {{
          const card = document.getElementById("dashboard-card-6");
          const btn = document.getElementById("btn-spustit-6");
          card.classList.add("visible");
          btn.textContent = "↻ Obnovit zobrazení přehledu";
          naplnData6();
        }}

        function prepniDetailyZprav6() {{
          const topRow = document.getElementById("top-row-6");
          const hint = document.getElementById("score-hint-6");
          topRow.classList.toggle("expanded");
          if (topRow.classList.contains("expanded")) {{
            hint.textContent = "Kliknutím skryjete detail článků";
          }} else {{
            hint.textContent = "Kliknutím zobrazíte detail článků";
          }}
        }}

        function komentarDuvery6(val) {{
          if (val === null || val === undefined || Number.isNaN(Number(val))) {{
            return "Data z ČSÚ nejsou aktuálně k dispozici.";
          }}
          const n = Number(val);
          if (n < 99) {{
            return "Ekonomická důvěra je podprůměrná.";
          }}
          if (n >= 99 && n < 100) {{
            return "Ekonomická důvěra je lehce podprůměrná.";
          }}
          if (n === 100) {{
            return "Ekonomická důvěra je na historickém průměru.";
          }}
          if (n > 100 && n <= 101) {{
            return "Ekonomická důvěra je lehce nadprůměrná.";
          }}
          return "Ekonomická důvěra je nadprůměrná.";
        }}

        function naplnData6() {{
          const s = PAYLOAD_6.skoreZprav;
          const scoreEl = document.getElementById("score-value-6");
          const emojiEl = document.getElementById("score-emoji-6");
          scoreEl.textContent = formatCzNumber(s, 2).replace(/,?00$/, "");

          if (s > 0) {{
            emojiEl.textContent = "😊";
          }} else if (s < 0) {{
            emojiEl.textContent = "😞";
          }} else {{
            emojiEl.textContent = "😐";
          }}

          const listEl = document.getElementById("articles-list-6");
          listEl.innerHTML = "";
          (PAYLOAD_6.clanky || []).forEach((cl) => {{
            const row = document.createElement("div");
            row.className = "article-item";
            const scFormatted = Number(cl.skore).toLocaleString("cs-CZ", {{ maximumFractionDigits: 2 }});
            row.innerHTML = `
              <div>${{cl.oznaceni}} ${{cl.titulek}}</div>
              <span class="article-score">Skóre: ${{scFormatted}}</span>
            `;
            listEl.appendChild(row);
          }});

          const csuVal = PAYLOAD_6.indexDuvery;
          const csuPeriod = PAYLOAD_6.obdobiDuvery;
          const csuPeriodEl = document.getElementById("csu-period-6");
          const csuEl = document.getElementById("csu-value-6");
          const csuCommentEl = document.getElementById("csu-comment-6");

          if (csuVal !== null && csuVal !== undefined) {{
            csuEl.textContent = `${{formatCzNumber(csuVal, 1)}} %`;
          }} else {{
            csuEl.textContent = "N/A";
          }}
          csuCommentEl.textContent = komentarDuvery6(csuVal);

          csuPeriodEl.textContent = csuPeriod ? `${{csuPeriod}}` : "";

          const selectEl = document.getElementById("currency-select-6");
          const kody = Object.keys(PAYLOAD_6.kurzy || {{}}).sort();
          if (selectEl.options.length === 0 && kody.length > 0) {{
            kody.forEach((kod) => {{
              const opt = document.createElement("option");
              const m = PAYLOAD_6.kurzy[kod];
              opt.value = kod;
              opt.textContent = `${{kod}} – ${{m.nazev}}`;
              if (kod === PAYLOAD_6.vychoziMena) {{
                opt.selected = true;
              }}
              selectEl.appendChild(opt);
            }});
          }}
          aktualizujKurz6();
        }}

        function aktualizujKurz6() {{
          const selectEl = document.getElementById("currency-select-6");
          const kod = selectEl.value;
          const info = (PAYLOAD_6.kurzy || {{}})[kod];

          if (!info) {{
            document.getElementById("kurz-aktualni-6").textContent = "–";
            document.getElementById("kurz-ma90-6").textContent = "–";
            document.getElementById("kurz-odchylka-6").textContent = "–";
            document.getElementById("kurz-export-6").textContent = "–";
            document.getElementById("kurz-import-6").textContent = "–";
            return;
          }}

          document.getElementById("kurz-aktualni-6").textContent = `${{formatCzNumber(info.aktualni_kurz, 3)}} Kč (${{info.datum}})`;
          document.getElementById("kurz-ma90-6").textContent = `${{formatCzNumber(info.ma90, 3)}} Kč`;
          const sign = info.odchylka_pct > 0 ? "+" : "";
          document.getElementById("kurz-odchylka-6").textContent = `${{sign}}${{formatCzNumber(info.odchylka_pct, 2)}} %`;
          document.getElementById("kurz-export-6").textContent = info.export_stav;
          document.getElementById("kurz-import-6").textContent = info.import_stav;
        }}
      </script>
    </div>
    """
    display(HTML(html_code))
