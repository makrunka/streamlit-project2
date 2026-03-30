import streamlit as st
import pandas as pd
import plotly.express as px

# Налаштування сторінки
st.set_page_config(page_title="Кіберзагрози", layout="wide")

# Заголовок
st.title("🌐 Система моніторингу кіберзагроз")

# Завантаження даних
try:
    df = pd.read_csv("cyber_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
except:
    st.error("❌ Файл cyber_data.csv не знайдено")
    st.stop()

# --- Вхідні дані ---
st.subheader("📄 Дані про атаки")
st.dataframe(df, use_container_width=True)

# --- Бокова панель ---
st.sidebar.header("🔎 Фільтри")

countries = ["Всі"] + sorted(df["Country"].dropna().unique())

selected_country = st.sidebar.selectbox(
    "Оберіть країну",
    countries
)

# Фільтрація
if selected_country != "Всі":
    df_filtered = df[df["Country"] == selected_country]
else:
    df_filtered = df

# --- Карта атак ---
st.subheader("🗺️ Геолокація атак")

fig_map = px.scatter_geo(
    df_filtered,
    lat="Latitude",
    lon="Longitude",
    color="Country",
    hover_name="IP",
    title="Карта кібер-атак"
)

st.plotly_chart(fig_map, use_container_width=True)

# --- ТОП країни ---
st.subheader("🌍 Активність по країнах")

country_counts = df["Country"].value_counts().reset_index()
country_counts.columns = ["Country", "Count"]

fig_bar = px.bar(
    country_counts,
    x="Country",
    y="Count",
    color="Country",
    title="Кількість атак по країнах"
)

st.plotly_chart(fig_bar, use_container_width=True)

# --- Тренд ---
st.subheader("📈 Тренд атак по днях")

trend = df.groupby("Date").size().reset_index(name="Attacks")

fig_line = px.line(
    trend,
    x="Date",
    y="Attacks",
    markers=True,
    title="Динаміка атак"
)

st.plotly_chart(fig_line, use_container_width=True)

# --- Метрики ---
st.subheader("📊 Загальна статистика")

col1, col2 = st.columns(2)

with col1:
    st.metric("🔢 Загальна кількість атак", len(df))

with col2:
    st.metric("🌍 Кількість країн", df["Country"].nunique())

# --- Додатково ---
st.subheader("📌 Відфільтровані дані")

if df_filtered.empty:
    st.warning("Немає даних для вибраної країни")
else:
    st.dataframe(df_filtered, use_container_width=True)