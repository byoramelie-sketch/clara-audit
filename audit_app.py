import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="AuditMatch",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# ---------------------------------------------------------------------------
# STYLE
# ---------------------------------------------------------------------------
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #f3f4f6; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #1f2937; }
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: visible; }
    .block-container { padding-top: 1.5rem; max-width: 1200px; }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #ffffff; border-right: 1px solid #e5e7eb;
    }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }

    .sb-logo { display:flex; align-items:center; gap:0.7rem; padding: 0 0.2rem 1.4rem 0.2rem; }
    .sb-logo-badge {
        width: 36px; height: 36px; border-radius: 11px; background: #000000; color: white;
        display:flex; align-items:center; justify-content:center; font-size: 0.95rem; flex-shrink:0;
    }
    .sb-logo-text { font-weight: 800; font-size: 1.05rem; letter-spacing: -0.01em; }

    .sb-nav-item {
        display:flex; align-items:center; gap: 0.7rem; padding: 0.65rem 0.8rem;
        border-radius: 11px; font-size: 0.85rem; font-weight: 600; color: #6b7280;
        margin-bottom: 0.15rem;
    }
    .sb-nav-item i { width: 16px; text-align:center; font-size: 0.85rem; }
    .sb-nav-item.active { background: #f3f4f6; color: #111827; }

    .sb-feedback {
        margin-top: 1.6rem; padding: 0.9rem; background: #f9fafb; border: 1px solid #eef0f4;
        border-radius: 12px; font-size: 0.78rem; color: #6b7280; line-height: 1.4;
    }
    .sb-feedback i { color: #4f46e5; margin-right: 0.35rem; }

    /* sidebar nav buttons (real st.button, styled to look like the nav rows) */
    section[data-testid="stSidebar"] .stButton { margin-bottom: 0.15rem; }
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important; color: #6b7280 !important; border: none !important;
        text-align: left !important; justify-content: flex-start !important;
        font-weight: 600 !important; font-size: 0.85rem !important;
        padding: 0.65rem 0.8rem !important; border-radius: 11px !important; box-shadow: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #f9fafb !important; color: #111827 !important;
    }
    section[data-testid="stSidebar"] .stButton > button:disabled {
        background: #f3f4f6 !important; color: #111827 !important; opacity: 1 !important;
    }

    /* ---------- Top header ---------- */
    .topheader { display:flex; align-items:center; justify-content:space-between; margin-bottom: 1.4rem; }
    .breadcrumb { font-size: 0.85rem; color: #9ca3af; font-weight: 500; }
    .breadcrumb b { color: #1f2937; font-weight: 700; }
    .status-pill {
        display:inline-flex; align-items:center; gap: 0.5rem; background: white; border: 1px solid #e5e7eb;
        padding: 0.45rem 0.9rem; border-radius: 11px; font-size: 0.78rem; font-weight: 600; color: #4b5563;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .status-pill i { color: #9ca3af; }
    .status-pill.warning { border-color: #fde68a; background: #fffbeb; color: #b45309; }
    .status-pill.warning i { color: #d97706; }
    .status-pill.ready { border-color: #a7f3d0; background: #ecfdf5; color: #047857; }
    .status-pill.ready i { color: #059669; }

    /* ---------- Section headers ---------- */
    .sec-title { font-weight: 700; font-size: 0.92rem; display:flex; align-items:center; gap:0.5rem;
        margin: 0.2rem 0 0.8rem 0; color: #1f2937; }
    .sec-title i { color: #9ca3af; font-size: 0.8rem; }

    /* ---------- Cards ---------- */
    .card {
        background: white; border: 1px solid #f3f4f6; border-radius: 16px; padding: 1.3rem 1.4rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .kpi-top { display:flex; align-items:center; gap: 0.5rem; color:#6b7280; font-size: 0.78rem; font-weight: 600; }
    .kpi-top i { color: #9ca3af; }
    .kpi-value { font-size: 1.85rem; font-weight: 800; margin-top: 0.6rem; letter-spacing: -0.02em; }
    .kpi-sub { font-size: 0.75rem; color: #9ca3af; margin-top: 0.15rem; }
    .pill-mini { display:inline-block; padding: 0.32rem 0.7rem; border-radius: 9px; font-size: 0.72rem; font-weight: 700; }
    .pill-red { background: #fef2f2; color: #dc2626; border: 1px solid #fee2e2; }
    .pill-amber { background: #fffbeb; color: #b45309; border: 1px solid #fef3c7; }
    .pill-blue { background: #eff6ff; color: #1d4ed8; border: 1px solid #dbeafe; }
    .pill-green { background: #ecfdf5; color: #059669; border: 1px solid #d1fae5; }

    /* ---------- Insight banner ---------- */
    .insight-banner {
        background: #1f2126; color: white; border-radius: 16px; padding: 1.15rem 1.4rem;
        display:flex; align-items:center; justify-content:space-between; gap: 1rem;
    }
    .insight-left { display:flex; align-items:center; gap: 0.9rem; }
    .insight-icon {
        width: 38px; height: 38px; border-radius: 11px; background: rgba(255,255,255,0.08);
        display:flex; align-items:center; justify-content:center; flex-shrink:0;
    }
    .insight-title { font-weight: 700; font-size: 0.88rem; margin: 0; }
    .insight-desc { font-size: 0.78rem; color: #9ca3af; margin: 0.15rem 0 0 0; }

    /* ---------- Legend list (donut) ---------- */
    .legend-row { display:flex; align-items:center; justify-content:space-between; font-size: 0.8rem; padding: 0.25rem 0; }
    .legend-left { display:flex; align-items:center; gap: 0.5rem; color: #4b5563; }
    .legend-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink:0; }
    .legend-val { font-weight: 700; color: #1f2937; }

    /* ---------- Table ---------- */
    .flag-table { width: 100%; border-collapse: collapse; font-size: 0.83rem; }
    .flag-table th { text-align: left; color: #9ca3af; font-size: 0.7rem; text-transform: uppercase;
        letter-spacing: 0.03em; font-weight: 700; padding: 0.85rem 1rem; background: #f9fafb; }
    .flag-table td { padding: 0.85rem 1rem; border-top: 1px solid #f3f4f6; color: #374151; font-weight: 500; }
    .flag-table tr:hover td { background: #fafbff; }
    .table-header-row { display:flex; align-items:center; gap: 0.5rem; padding: 1.1rem 1.4rem;
        border-bottom: 1px solid #f3f4f6; color: #dc2626; }
    .table-header-row span { color: #1f2937; font-weight: 700; font-size: 0.88rem; }

    /* ---------- Upload / buttons ---------- */
    div[data-testid="stFileUploader"] {
        background: white; border: 1.5px dashed #d1d5db; border-radius: 13px; padding: 0.7rem;
    }
    .stButton > button {
        background: #111827; color: white; border-radius: 11px; border: none;
        padding: 0.6rem 1.6rem; font-weight: 600; font-size: 0.85rem;
    }
    .stButton > button:hover { background: #000000; }
    .stDownloadButton > button {
        background: white; color: #111827; border: 1px solid #e5e7eb; border-radius: 11px; font-weight: 600;
    }
    .stDownloadButton > button:hover { border-color: #111827; }

    .stDataFrame { border-radius: 12px; overflow: hidden; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    div[data-testid="stExpander"] { border-radius: 13px; border: 1px solid #eef0f4; background: white; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-badge"><i class="fa-solid fa-diamond"></i></div>
        <span class="sb-logo-text">AuditMatch</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Tableau de bord", use_container_width=True, disabled=(st.session_state.page == "dashboard")):
        st.session_state.page = "dashboard"
    if st.button("Guide d'utilisation", use_container_width=True, disabled=(st.session_state.page == "guide")):
        st.session_state.page = "guide"
    if st.button("Aide", use_container_width=True, disabled=(st.session_state.page == "aide")):
        st.session_state.page = "aide"

    st.markdown("""
    <div class="sb-feedback">
        <i class="fa-solid fa-comment-dots"></i>Version de test (v0). Toute remarque sur ce qui manque
        ou ce qui gêne est utile — note-la pour en discuter.
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TOP HEADER
# ---------------------------------------------------------------------------
today_str = datetime.now().strftime("%d %B %Y")

# ---------------------------------------------------------------------------
# PAGE: TABLEAU DE BORD
# ---------------------------------------------------------------------------
if st.session_state.page == "dashboard":

    st.markdown("""
    <div class="card" style="margin-bottom:1.4rem; display:flex; align-items:center; justify-content:space-between; gap:1rem;">
        <div style="display:flex; align-items:center; gap:0.8rem;">
            <div class="insight-icon" style="background:#eef2ff;"><i class="fa-solid fa-book-open" style="color:#4f46e5;"></i></div>
            <div>
                <p style="font-weight:700; font-size:0.85rem; margin:0;">Première visite ?</p>
                <p style="font-size:0.78rem; color:#9ca3af; margin:0.1rem 0 0 0;">Importe deux fichiers, choisis les colonnes, lance le rapprochement — le détail est dans "Guide d'utilisation", dans le menu à gauche.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------------------------
    # STEP 1 — UPLOAD
    # ---------------------------------------------------------------------------
    st.markdown('<div class="sec-title"><i class="fa-solid fa-file-import"></i>Importer les fichiers</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.caption("Fichier de référence (ex : grand livre)")
        file1 = st.file_uploader("Fichier 1", type=["xlsx", "xls", "csv"], key="f1", label_visibility="collapsed")
    with col2:
        st.caption("Fichier à comparer (ex : relevé bancaire)")
        file2 = st.file_uploader("Fichier 2", type=["xlsx", "xls", "csv"], key="f2", label_visibility="collapsed")


    def load_file(f):
        if f is None:
            return None
        if f.name.endswith(".csv"):
            return pd.read_csv(f)
        return pd.read_excel(f)


    df1 = load_file(file1)
    df2 = load_file(file2)

    n_uploaded = sum(x is not None for x in [df1, df2])
    if n_uploaded == 0:
        status_label = "Aucun fichier importé"
        status_icon = "fa-regular fa-circle"
        status_class = ""
    elif n_uploaded == 1:
        missing = "à comparer (à droite)" if df1 is not None else "de référence (à gauche)"
        status_label = f"1 fichier sur 2 — il manque le fichier {missing}"
        status_icon = "fa-solid fa-triangle-exclamation"
        status_class = "warning"
    else:
        status_label = "2 fichiers importés"
        status_icon = "fa-solid fa-circle-check"
        status_class = "ready"

    st.markdown(f"""
    <div style="margin-top:0.9rem; margin-bottom:1.6rem;">
        <span class="status-pill {status_class}"><i class="{status_icon}"></i>{status_label}</span>
    </div>
    """, unsafe_allow_html=True)

    if df1 is not None and df2 is not None:
        with st.expander("Aperçu des données importées", expanded=False):
            c1, c2 = st.columns(2)
            c1.write(f"**Fichier 1** — {len(df1)} lignes")
            c1.dataframe(df1.head(5), use_container_width=True)
            c2.write(f"**Fichier 2** — {len(df2)} lignes")
            c2.dataframe(df2.head(5), use_container_width=True)

        # -----------------------------------------------------------------
        # STEP 2 — CONFIGURATION
        # -----------------------------------------------------------------
        st.markdown('<div class="sec-title"><i class="fa-solid fa-sliders"></i>Configurer le rapprochement</div>', unsafe_allow_html=True)

        common_cols = [c for c in df1.columns if c in df2.columns]

        c1, c2, c3 = st.columns(3)
        with c1:
            key_cols = st.multiselect(
                "Colonne(s) clé (identifiant unique)",
                options=common_cols,
                default=[common_cols[0]] if common_cols else [],
                help="Colonne(s) permettant d'identifier une même ligne dans les deux fichiers (ex : n° de facture, référence)."
            )
        with c2:
            value_col = st.selectbox(
                "Colonne montant à comparer",
                options=[c for c in common_cols if c not in key_cols] or common_cols,
                help="Colonne numérique dont on va comparer les valeurs entre les deux fichiers."
            )
        with c3:
            tolerance = st.number_input("Tolérance d'écart (€)", min_value=0.0, value=0.01, step=0.01,
                                         help="En dessous de ce seuil, un écart n'est pas considéré comme une anomalie.")

        run = st.button("Lancer le rapprochement", type="primary", disabled=not key_cols)

        # -----------------------------------------------------------------
        # STEP 3 — RESULTS
        # -----------------------------------------------------------------
        if run and key_cols:
            d1 = df1.copy()
            d2 = df2.copy()
            d1["_key"] = d1[key_cols].astype(str).agg("|".join, axis=1)
            d2["_key"] = d2[key_cols].astype(str).agg("|".join, axis=1)

            merged = d1.merge(d2, on="_key", how="outer", suffixes=("_f1", "_f2"), indicator=True)

            only_1 = merged[merged["_merge"] == "left_only"]
            only_2 = merged[merged["_merge"] == "right_only"]
            both = merged[merged["_merge"] == "both"].copy()

            val1_col = f"{value_col}_f1" if f"{value_col}_f1" in both.columns else value_col
            val2_col = f"{value_col}_f2" if f"{value_col}_f2" in both.columns else value_col

            both["_ecart"] = pd.to_numeric(both[val1_col], errors="coerce") - pd.to_numeric(both[val2_col], errors="coerce")
            anomalies = both[both["_ecart"].abs() > tolerance].copy()
            matched_ok = both[both["_ecart"].abs() <= tolerance]

            def classify(ecart):
                a = abs(ecart)
                if a > 500:
                    return ("Majeur", "pill-red")
                elif a > 100:
                    return ("Modéré", "pill-amber")
                else:
                    return ("Mineur", "pill-blue")

            if len(anomalies) > 0:
                anomalies[["_sev_label", "_sev_class"]] = anomalies["_ecart"].apply(lambda e: pd.Series(classify(e)))
                n_major = (anomalies["_sev_label"] == "Majeur").sum()
                n_other = len(anomalies) - n_major
            else:
                n_major, n_other = 0, 0

            total = len(matched_ok) + len(anomalies) + len(only_1) + len(only_2)
            score = round(100 * len(matched_ok) / total, 1) if total else 0

            st.write("")
            st.markdown('<div class="sec-title"><i class="fa-solid fa-chart-simple"></i>Résultats</div>', unsafe_allow_html=True)

            # KPI cards
            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown(f"""
                <div class="card">
                    <div class="kpi-top"><i class="fa-regular fa-circle-check"></i>Lignes rapprochées</div>
                    <div class="kpi-value">{len(matched_ok)}</div>
                    <div class="kpi-sub">sur {total} lignes traitées</div>
                </div>""", unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div class="card">
                    <div class="kpi-top"><i class="fa-solid fa-triangle-exclamation"></i>Écarts détectés</div>
                    <div style="margin-top:0.7rem; display:flex; gap:0.5rem;">
                        <span class="pill-mini pill-red">{n_major} Majeurs</span>
                        <span class="pill-mini pill-amber">{n_other} Modérés/Mineurs</span>
                    </div>
                    <div class="kpi-sub" style="margin-top:0.5rem;">anomalies repérées</div>
                </div>""", unsafe_allow_html=True)
            with k3:
                score_color = "#059669" if score >= 90 else ("#b45309" if score >= 70 else "#dc2626")
                st.markdown(f"""
                <div class="card">
                    <div class="kpi-top"><i class="fa-solid fa-gauge-high"></i>Score de cohérence</div>
                    <div class="kpi-value" style="color:{score_color};">{score}<span style="font-size:1.1rem; color:#9ca3af; font-weight:600;">/100</span></div>
                    <div class="kpi-sub">fiabilité du rapprochement</div>
                </div>""", unsafe_allow_html=True)

            st.write("")

            # Insight banner
            top_ref = ""
            if len(anomalies) > 0:
                worst = anomalies.reindex(anomalies["_ecart"].abs().sort_values(ascending=False).index).iloc[0]
                top_ref = f" Le plus important concerne {worst['_key']} ({worst['_ecart']:+,.2f} €)."
            insight_text = (
                f"{len(anomalies)} écart(s) détecté(s) dont {n_major} au-delà de 500 €, "
                f"{len(only_1)} ligne(s) présente(s) uniquement dans le fichier 1 et {len(only_2)} uniquement dans le fichier 2."
                f"{top_ref}"
            ) if len(anomalies) > 0 or len(only_1) or len(only_2) else "Aucun écart détecté au-delà de la tolérance définie — les deux fichiers concordent."

            st.markdown(f"""
            <div class="insight-banner">
                <div class="insight-left">
                    <div class="insight-icon"><i class="fa-solid fa-list-check"></i></div>
                    <div>
                        <p class="insight-title">Résumé du rapprochement</p>
                        <p class="insight-desc">{insight_text}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            chart_col1, chart_col2 = st.columns([2, 1])

            with chart_col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="sec-title" style="margin-bottom:0.4rem;"><i class="fa-solid fa-chart-column"></i>Top écarts par référence</div>', unsafe_allow_html=True)
                if len(anomalies) > 0:
                    top_anom = anomalies.reindex(anomalies["_ecart"].abs().sort_values(ascending=False).index).head(10)
                    fig2 = px.bar(
                        top_anom, x="_key", y="_ecart",
                        color=top_anom["_ecart"].apply(lambda v: "Positif" if v > 0 else "Négatif"),
                        color_discrete_map={"Positif": "#059669", "Négatif": "#dc2626"},
                        labels={"_key": "Référence", "_ecart": "Écart (€)"},
                    )
                    fig2.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#374151", showlegend=False,
                        margin=dict(t=10, b=10, l=10, r=10), height=280,
                        xaxis=dict(gridcolor="#f3f4f6"), yaxis=dict(gridcolor="#f3f4f6"),
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.markdown('<p style="color:#9ca3af; font-size:0.85rem; padding:2rem 0; text-align:center;">Aucun écart à afficher.</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with chart_col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="sec-title" style="margin-bottom:0.4rem;"><i class="fa-solid fa-chart-pie"></i>Répartition</div>', unsafe_allow_html=True)
                fig = go.Figure(data=[go.Pie(
                    labels=["OK", "Écarts", "Fichier 1 seul", "Fichier 2 seul"],
                    values=[len(matched_ok), len(anomalies), len(only_1), len(only_2)],
                    hole=0.62,
                    marker=dict(colors=["#059669", "#dc2626", "#d97706", "#4f46e5"]),
                    textinfo="none",
                )])
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=170,
                )
                st.plotly_chart(fig, use_container_width=True)

                legend_items = [
                    ("OK", "#059669", len(matched_ok)),
                    ("Écarts", "#dc2626", len(anomalies)),
                    ("Fichier 1 seul", "#d97706", len(only_1)),
                    ("Fichier 2 seul", "#4f46e5", len(only_2)),
                ]
                legend_html = ""
                for label, color, val in legend_items:
                    pct = round(100 * val / total, 0) if total else 0
                    legend_html += f"""
                    <div class="legend-row">
                        <div class="legend-left"><span class="legend-dot" style="background:{color};"></span>{label}</div>
                        <div class="legend-val">{val} ({pct:.0f}%)</div>
                    </div>"""
                st.markdown(legend_html, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.write("")

            # Flagged table
            st.markdown('<div class="card" style="padding:0;">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="table-header-row"><i class="fa-solid fa-flag"></i><span>Lignes en écart</span></div>
            """, unsafe_allow_html=True)
            if len(anomalies) > 0:
                rows_html = ""
                for _, r in anomalies.iterrows():
                    ecart_color = "#dc2626" if r["_ecart"] < 0 else "#059669"
                    rows_html += f"""
                    <tr>
                        <td>{r['_key']}</td>
                        <td>{r[val1_col]:,.2f} €</td>
                        <td>{r[val2_col]:,.2f} €</td>
                        <td style="color:{ecart_color}; font-weight:700;">{r['_ecart']:+,.2f} €</td>
                        <td><span class="pill-mini {r['_sev_class']}">{r['_sev_label']}</span></td>
                    </tr>"""
                st.markdown(f"""
                <table class="flag-table">
                    <tr><th>Référence</th><th>Valeur F1</th><th>Valeur F2</th><th>Écart</th><th>Sévérité</th></tr>
                    {rows_html}
                </table>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#9ca3af; font-size:0.85rem; padding:1.5rem;">Aucune ligne en écart.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if len(only_1) > 0 or len(only_2) > 0:
                st.write("")
                tab1, tab2 = st.tabs([f"Uniquement fichier 1 ({len(only_1)})", f"Uniquement fichier 2 ({len(only_2)})"])
                with tab1:
                    st.dataframe(only_1[[c for c in only_1.columns if c.endswith("_f1") or c == "_key"]], use_container_width=True) if len(only_1) else st.info("Rien à afficher.")
                with tab2:
                    st.dataframe(only_2[[c for c in only_2.columns if c.endswith("_f2") or c == "_key"]], use_container_width=True) if len(only_2) else st.info("Rien à afficher.")

            # Export
            st.write("")
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                anomalies.to_excel(writer, sheet_name="Ecarts", index=False)
                only_1.to_excel(writer, sheet_name="Fichier1_seul", index=False)
                only_2.to_excel(writer, sheet_name="Fichier2_seul", index=False)
                matched_ok.to_excel(writer, sheet_name="OK", index=False)
            st.download_button(
                "Télécharger le rapport complet (Excel)",
                data=buffer.getvalue(),
                file_name="rapport_rapprochement.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 2.5rem 1rem; color:#9ca3af;">
            <i class="fa-regular fa-folder-open" style="font-size:1.6rem; margin-bottom:0.6rem; display:block;"></i>
            Importe deux fichiers Excel (ou CSV) pour commencer — ou utilise les fichiers d'exemple fournis.
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# PAGE: GUIDE D'UTILISATION — reads GUIDE.md from disk and displays it
# ---------------------------------------------------------------------------
elif st.session_state.page == "guide":
    import os

    st.markdown('<div class="sec-title"><i class="fa-solid fa-book-open"></i>Guide d\'utilisation</div>', unsafe_allow_html=True)

    guide_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GUIDE.md")
    try:
        with open(guide_path, "r", encoding="utf-8") as f:
            guide_content = f.read()
    except FileNotFoundError:
        guide_content = None

    with st.container(border=True):
        if guide_content:
            st.markdown(guide_content)
        else:
            st.markdown("""
            <div style="text-align:center; padding: 1.5rem; color:#9ca3af;">
                <i class="fa-regular fa-file-excel" style="font-size:1.4rem; display:block; margin-bottom:0.6rem;"></i>
                Le fichier <b>GUIDE.md</b> est introuvable. Vérifie qu'il est bien placé dans le même
                dossier que <code>audit_app.py</code>.
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# PAGE: AIDE — short contextual help
# ---------------------------------------------------------------------------
elif st.session_state.page == "aide":
    st.markdown('<div class="sec-title"><i class="fa-solid fa-circle-question"></i>Aide</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("""
**Un problème d'affichage, la page ne répond plus ?**

1. Ferme complètement l'onglet du navigateur
2. Dans le terminal, arrête le serveur (`Ctrl + C`)
3. Relance `streamlit run audit_app.py`
4. Rouvre un nouvel onglet

**Une question sur comment utiliser l'outil ?**

Va voir "Guide d'utilisation" dans le menu à gauche — il détaille chaque étape,
de l'import des fichiers jusqu'au téléchargement du rapport.

**Une idée ou une remarque à transmettre ?**

Note-la simplement quelque part (capture d'écran si utile) pour en discuter — c'est
une version de test, tout retour sert à l'améliorer.
        """)