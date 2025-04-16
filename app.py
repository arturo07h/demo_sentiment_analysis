import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Inicializa la app
app = dash.Dash(__name__)
app.title = "Análisis de Sentimiento"
server = app.server

# Carga de datos
df_menciones     = pd.read_csv("data/menciones_por_empresa.csv")
df_hora          = pd.read_csv("data/sentimiento_por_hora.csv")
df_producto      = pd.read_csv("data/conteo_sentimientos.csv")
df_sent_empresa  = pd.read_csv("data/sentimiento_empresa.csv")

# Figuras
fig_menciones = px.bar(
    df_menciones.sort_values("total_menciones", ascending=True),
    x="total_menciones", y="empresa", orientation="h",
    labels={"total_menciones":"Menciones", "empresa":"Empresa"},
    color_discrete_sequence=["#00d4d8"]
)
fig_menciones.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

fig_tendencia = px.line(
    df_hora.sort_values("hora_redondeada"),
    x="hora_redondeada", y="sentimiento_promedio",
    labels={"hora_redondeada":"Hora", "sentimiento_promedio":"Sentimiento promedio"},
    color_discrete_sequence=["#00d4d8"]
)
fig_tendencia.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

fig_producto = px.bar(
    df_producto.sort_values("total_menciones", ascending=True),
    x="total_menciones", y="producto", orientation="h",
    labels={"total_menciones":"Menciones", "producto":"Producto"},
    color="sentimiento_promedio", color_continuous_scale="tealgrn"
)
fig_producto.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

fig_dist_sent = px.bar(
    df_sent_empresa,
    x="empresa", y="conteo", color="sentimiento",
    barmode="group",
    labels={"conteo":"Número de comentarios", "empresa":"Empresa"}
)
fig_dist_sent.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

# Layout
app.layout = html.Div(style={
    "fontFamily": "Arial, sans-serif",
    "backgroundColor": "#0f1117",
    "color": "white",
    "padding": "30px"
}, children=[

    html.H1("Dashboard", style={
        "textAlign": "left",
        "fontWeight": "bold",
        "fontSize": "36px",
        "marginBottom": "30px"
    }),

    dcc.Tabs([
        dcc.Tab(label="Análisis de Sentimientos", style={"backgroundColor": "#1e212d", "color": "white"},
                selected_style={"backgroundColor": "#2d2f3a", "color": "#00d4d8"}, children=[

            html.Div(style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px"
            }, children=[

                html.Div(style={
                    "backgroundColor": "#1e212d",
                    "padding": "20px",
                    "borderRadius": "15px"
                }, children=[
                    html.H3("Mentions by Company"),
                    dcc.Graph(figure=fig_menciones, config={"displayModeBar": False})
                ]),

                html.Div(style={
                    "backgroundColor": "#1e212d",
                    "padding": "20px",
                    "borderRadius": "15px"
                }, children=[
                    html.H3("Sentiment Over Time"),
                    dcc.Graph(figure=fig_tendencia, config={"displayModeBar": False})
                ]),

                html.Div(style={
                    "backgroundColor": "#1e212d",
                    "padding": "20px",
                    "borderRadius": "15px"
                }, children=[
                    html.H3("Sentiment by Product"),
                    dcc.Graph(figure=fig_producto, config={"displayModeBar": False})
                ]),

                html.Div(style={
                    "backgroundColor": "#1e212d",
                    "padding": "20px",
                    "borderRadius": "15px"
                }, children=[
                    html.H3("Distribution by Company"),
                    dcc.Graph(figure=fig_dist_sent, config={"displayModeBar": False})
                ]),
            ])
        ]),

        dcc.Tab(label="Criptos", style={"backgroundColor": "#1e212d", "color": "white"},
                selected_style={"backgroundColor": "#2d2f3a", "color": "#00d4d8"}, children=[
            html.Div("Sección próximamente disponible...", style={
                "backgroundColor": "#1e212d",
                "padding": "40px",
                "borderRadius": "15px",
                "textAlign": "center",
                "fontSize": "20px"
            })
        ])
    ])
])

# Servidor
if __name__ == "__main__":
    app.run(debug=True)
