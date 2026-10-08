from datetime import datetime
import html

def build_html_report(df, analysis, ai_report):
    p = analysis["profile"]
    kpis = analysis["kpis"]
    a = analysis["anomalies"]
    rows = df.head(15).to_html(index=False, border=0, classes="table")
    stats = ""
    for col, vals in p["numeric_stats"].items():
        stats += f"<h3>{html.escape(col)}</h3><pre>{html.escape(str(vals))}</pre>"
    kpi_html = "".join(f"<li><b>{html.escape(str(k))}:</b> {html.escape(str(v))}</li>" for k,v in kpis.items())
    ai = ai_report or "AI insights were not generated."
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>AI Data Detective Report</title>
<style>
body{{font-family:Arial,sans-serif;max-width:1000px;margin:40px auto;padding:0 20px;color:#17202a}}
h1{{margin-bottom:4px}} .muted{{color:#667085}} .table{{border-collapse:collapse;width:100%}}
.table th,.table td{{border:1px solid #ddd;padding:7px}} .table th{{background:#f2f4f7}}
pre{{background:#f7f7f8;padding:12px;border-radius:8px;overflow:auto}}
</style></head><body>
<h1>AI DATA DETECTIVE</h1><p class="muted">Python-Powered Analytics + Generative AI Insights</p>
<p><b>Analysis time:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
<h2>Dataset Information</h2>
<ul><li>Rows: {p['rows']}</li><li>Columns: {p['columns']}</li>
<li>Missing values: {p['missing_total']}</li><li>Duplicate rows: {p['duplicate_rows']}</li></ul>
<h2>KPIs</h2><ul>{kpi_html}</ul>
<h2>Numerical Statistics</h2>{stats}
<h2>Anomaly Detection</h2><p>Detected {a['total_anomalies']} anomalous numerical cells across {len(a['affected_rows'])} affected rows using the IQR rule.</p>
<h2>Dataset Preview</h2>{rows}
<h2>AI Insights</h2>{ai.replace(chr(10), '<br>')}
</body></html>"""
