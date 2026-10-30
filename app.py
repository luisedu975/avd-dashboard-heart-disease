import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Heart Disease - Dashboards", layout="wide")

CP_MAP = {1: "Angina típica", 2: "Angina atípica", 3: "Dor não anginosa", 4: "Assintomática"}


@st.cache_data
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv("data/heart_disease.csv")
    except FileNotFoundError:
        from ucimlrepo import fetch_ucirepo
        ds = fetch_ucirepo(id=45)
        df = pd.concat([ds.data.features, ds.data.targets], axis=1)
    # Mesmo tratamento da EDA: binarização do alvo e remoção dos ausentes (ca, thal)
    df = df.dropna(subset=["ca", "thal"]).copy()
    df["doenca_cardiaca"] = df["num"].apply(lambda x: "Normal" if x == 0 else "Cardíaco")
    df["alvo"] = (df["num"] > 0).astype(int)
    df["sexo"] = df["sex"].map({1: "Masculino", 0: "Feminino"})
    df["tipo_dor"] = df["cp"].map(CP_MAP)
    df["faixa_etaria"] = pd.cut(df["age"], [0, 44, 54, 64, 120],
                                labels=["<45", "45-54", "55-64", "65+"])
    return df


df = load_data()
quant = ["age", "trestbps", "chol", "thalach", "oldpeak"]

# ---------------- Painel lateral ----------------
st.sidebar.header("Filtros")
vars_sel = st.sidebar.multiselect("Variáveis quantitativas", quant, default=quant)
age_r = st.sidebar.slider("Intervalo de idade", int(df.age.min()), int(df.age.max()),
                          (int(df.age.min()), int(df.age.max())))
chol_r = st.sidebar.slider("Intervalo de colesterol (exclui outliers)",
                           int(df.chol.min()), int(df.chol.max()),
                           (int(df.chol.min()), int(df.chol.max())))
dff = df[df.age.between(*age_r) & df.chol.between(*chol_r)]
st.sidebar.caption(f"{len(dff)} de {len(df)} pacientes")

if dff.empty:
    st.warning("Nenhum paciente no intervalo escolhido.")
    st.stop()

tab1, tab2 = st.tabs(["🔬 Laboratório", "🩺 KPIs Clínicos"])

# ---------------- Dashboard 1 ----------------
with tab1:
    st.header("Distribuição e correlação")
    if len(vars_sel) >= 1:
        corr = dff[vars_sel + ["alvo"]].corr()
        st.plotly_chart(
            px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                      zmin=-1, zmax=1, title="Mapa de calor de correlação (alvo = doença cardíaca)"),
            width="stretch")
        cols = st.columns(2)
        for i, v in enumerate(vars_sel):
            cols[i % 2].plotly_chart(
                px.histogram(dff, x=v, color="doenca_cardiaca", nbins=25,
                             barmode="overlay", opacity=0.7, title=f"Histograma de {v}"),
                width="stretch")
    else:
        st.info("Selecione ao menos 1 variável no painel lateral.")

# ---------------- Dashboard 2 ----------------
# Público-alvo: cardiologista na triagem de pacientes com suspeita de doença cardíaca
with tab2:
    st.header("Perfil de risco — visão do cardiologista")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Pacientes", len(dff))
    c2.metric("Prevalência de doença", f"{dff.alvo.mean():.1%}")
    c3.metric("Idade média", f"{dff.age.mean():.1f}")
    c4.metric("FC máx. média", f"{dff.thalach.mean():.0f} bpm")
    c5.metric("Colesterol médio", f"{dff.chol.mean():.0f} mg/dl")

    a, b = st.columns(2)
    dor = dff.groupby("tipo_dor")["alvo"].mean().reset_index()
    a.plotly_chart(px.bar(dor, x="tipo_dor", y="alvo", title="Taxa de doença por tipo de dor no peito",
                          labels={"alvo": "Taxa", "tipo_dor": "Tipo de dor"}),
                   width="stretch")
    b.plotly_chart(px.box(dff, x="doenca_cardiaca", y="thalach", color="doenca_cardiaca",
                          title="Frequência cardíaca máxima por diagnóstico"),
                   width="stretch")
    fx = dff.groupby(["faixa_etaria", "sexo"], observed=True)["alvo"].mean().reset_index()
    st.plotly_chart(px.bar(fx, x="faixa_etaria", y="alvo", color="sexo", barmode="group",
                           title="Taxa de doença por faixa etária e sexo", labels={"alvo": "Taxa"}),
                    width="stretch")