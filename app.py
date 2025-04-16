# app.py

import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Inicializa la app
app = dash.Dash(__name__)
app.title = "Análisis de Sentimiento"

# Carga de datos
df_menciones     = pd.read_csv("data/menciones_por_empresa.csv")
df_hora          = pd.read_csv("data/sentimiento_por_hora.csv")
df_producto      = pd.read_csv("data/conteo_sentimientos.csv")
df_sent_empresa  = pd.read_csv("data/sentimiento_empresa.csv")

# Figuras
fig_menciones = px.bar(
    df_menciones.sort_values("total_menciones", ascending=True),
    x="total_menciones", y="empresa", orientation="h",
    title="Total de menciones por empresa",
    labels={"total_menciones":"Menciones", "empresa":"Empresa"},
    color="total_menciones", color_continuous_scale="plasma"
)

fig_tendencia = px.line(
    df_hora.sort_values("hora_redondeada"),
    x="hora_redondeada", y="sentimiento_promedio",
    title="Sentimiento promedio por hora",
    labels={"hora_redondeada":"Hora", "sentimiento_promedio":"Sentimiento promedio"}
)

fig_producto = px.bar(
    df_producto.sort_values("total_menciones", ascending=True),
    x="total_menciones", y="producto", orientation="h",
    title="Menciones por producto",
    labels={"total_menciones":"Menciones", "producto":"Producto"},
    color="sentimiento_promedio", color_continuous_scale="viridis"
)

fig_dist_sent = px.bar(
    df_sent_empresa,
    x="empresa", y="conteo", color="sentimiento",
    barmode="group",
    title="Conteo de sentimientos por empresa",
    labels={"conteo":"Número de comentarios", "empresa":"Empresa"}
)

# Layout
app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px"}, children=[

    html.H1("Demo Dash: Análisis de Sentimiento", style={"textAlign": "center"}),

    # Fila 1: Menciones & Sentimiento promedio
    html.Div(style={"display": "flex", "gap": "20px"}, children=[
        html.Div(style={"flex": "1"}, children=[
            html.H3("1. Ranking de menciones"),
            dcc.Graph(figure=fig_menciones)
        ]),
        html.Div(style={"flex": "1"}, children=[
            html.H3("2. Evolución de sentimiento"),
            dcc.Graph(figure=fig_tendencia)
        ]),
    ]),

    # Fila 2: Producto & Distribución de sentimientos
    html.Div(style={"display": "flex", "gap": "20px", "marginTop": "40px"}, children=[
        html.Div(style={"flex": "1"}, children=[
            html.H3("3. Menciones por producto"),
            dcc.Graph(figure=fig_producto)
        ]),
        html.Div(style={"flex": "1"}, children=[
            html.H3("4. Distribución de sentimiento"),
            dcc.Graph(figure=fig_dist_sent)
        ]),
    ]),

])

# Arranca el servidor
if __name__ == "__main__":
    app.run(debug=True)
