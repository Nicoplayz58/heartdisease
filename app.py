import dash
from dash import html, dcc
import plotly.io as pio
import json
import os
from dash.dependencies import Input, Output
from dash import dash_table



# Funciones
def cargar_figura(path):
    with open(path, 'r') as f:
        return json.load(f)

# Estilos visuales oscuros
estilo_general = {
    'backgroundColor': '#121212',
    'fontFamily': 'Arial, sans-serif',
    'padding': '20px 10px',
    'color': '#f5f5f5'
}

estilo_titulo = {
    'fontSize': '42px',
    'fontWeight': 'bold',
    'marginBottom': '2px',
    'color': '#90caf9',
    'textAlign': 'center',
    'backgroundColor': '#1e1e1e',
    'padding': '20px',
    'borderRadius': '10px'
}

estilo_subtitulo = {
    'fontSize': '26px',
    'fontWeight': 'bold',
    'color': '#bbdefb',
    'marginTop': '25px',
    'backgroundColor': '#1e1e1e',
    'padding': '12px',
    'borderRadius': '8px'
}

estilo_parrafo = {
    'fontSize': '16px',
    'color': '#e0e0e0',
    'lineHeight': '1.6'
}

estilo_grafico = {
    'width': '28%',
    'height': '200px',
    'marginTop': '20px',
    'marginBottom': '160px',
    'marginLeft': '15px',
    'marginRight': '15px',
    'display': 'inline-block',
    'verticalAlign': 'top',
    'minWidth': '200px',
    'boxSizing': 'border-box'
}

estilo_tabs = {
    'backgroundColor': '#1e1e1e',
    'color': 'white',
    'borderBottom': '1px solid #303f9f'
}

estilo_tab = {
    'backgroundColor': '#303f9f',
    'color': 'white',
    'padding': '10px'
}

# Inicializar Dash
app = dash.Dash(__name__, title="Heart Disease Dashboard")
server = app.server

# Gráficos disponibles
carpeta_graficos = "./eda_heart_json"
lista_graficos = [archivo for archivo in os.listdir(carpeta_graficos) if archivo.endswith(".json")]

# Solo incluir variables importantes en gráficos
variables_bar = ["thal", "cp", "ca", "sex", "slope"]
variables_hist = ["thalach", "oldpeak", "age"]
variables_box = ["thalach", "oldpeak", "age"]

barras = [f for f in lista_graficos if any(var in f for var in variables_bar) and f.endswith("_bar.json")]
primeras_barras = barras[:3]
resto_barras = barras[3:]
histogramas = [f for f in lista_graficos if any(var in f for var in variables_hist) and f.endswith("_hist.json")]
boxplots = [f for f in lista_graficos if any(var in f for var in variables_box) and f.endswith("_box.json")]

pie = ["fig_pie_target.json"]
correlaciones = ["fig_corr_spearman.json", "fig_corr_cramers.json"]
importancias = ["fig_importance_total.json", "fig_importance_numericas.json"]

def graficos_como_componentes(filtrados):
    componentes = []
    for archivo in filtrados:
        try:
            fig = pio.read_json(os.path.join(carpeta_graficos, archivo))
            componentes.append(html.Div(dcc.Graph(figure=fig), style=estilo_grafico))
        except:
            continue
    return componentes

app.layout = html.Div(style=estilo_general, children=[
    html.H1("Heart Disease Risk Analysis Dashboard", style=estilo_titulo),

    dcc.Tabs(id="tabs", value="contexto", children=[

        dcc.Tab(label='Contexto del Problema', value="contexto", children=[
            html.Div([
                html.H2("Contexto Social del Problema", style={
                    'color': '#90caf9',
                    'textAlign': 'center',
                    'marginTop': '30px',
                    'marginBottom': '30px',
                    'fontWeight': 'bold'
                }),

                html.Div([
                    html.Div([
                        html.P("""
                            Las enfermedades cardiovasculares representan la principal causa de muerte a nivel mundial. 
                            Afectan tanto a hombres como mujeres de todas las edades, y su prevalencia ha aumentado 
                            debido a factores como el sedentarismo, la mala alimentación, el estrés y la falta de diagnóstico temprano.
                        """, style={
                            'color': '#f5f5f5',
                            'padding': '20px',
                            'backgroundColor': '#1e1e1e',
                            'borderRadius': '12px',
                            'boxShadow': '0 0 10px rgba(144,202,249,0.3)',
                            'fontSize': '20px',
                            'lineHeight': '1.8',
                            'textAlign': 'justify'
                        }),

                        html.P("""
                            Este dashboard busca analizar patrones en los datos relacionados con enfermedades cardíacas
                            y apoyar el diagnóstico preventivo mediante técnicas de ciencia de datos.
                            El objetivo es empoderar a profesionales de salud y pacientes a comprender mejor los factores de riesgo
                            y tomar decisiones informadas.
                        """, style={
                            'color': '#f5f5f5',
                            'padding': '20px',
                            'backgroundColor': '#1e1e1e',
                            'borderRadius': '12px',
                            'boxShadow': '0 0 10px rgba(144,202,249,0.3)',
                            'fontSize': '20px',
                            'lineHeight': '1.8',
                            'marginTop': '25px',
                            'textAlign': 'justify'
                        })
                    ], style={'width': '60%', 'padding': '20px'}),

                    html.Div([
                        html.Img(src='/assets/heart.png', style={
                            'width': '100%',
                            'maxWidth': '400px',
                            'height': 'auto',
                            'borderRadius': '12px',
                            'boxShadow': '0 0 10px rgba(144,202,249,0.3)'
                        })
                    ], style={'width': '35%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'padding': '20px'})

                ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'flexWrap': 'wrap'})

            ], style={'padding': '40px'})
        ], style=estilo_tab),
            
      dcc.Tab(label='Descripción del Dataset', value="dataset", children=[
        html.Div([
            html.H2("Descripción del Dataset", style={
                'color': '#90caf9',
                'textAlign': 'center',
                'marginTop': '30px',
                'marginBottom': '30px',
                'fontWeight': 'bold'
            }),
    
            html.Div([
                html.Div([
                    html.P("""
                        El conjunto de datos utilizado proviene de una fuente médica anónima y contiene información 
                        sobre pacientes, incluyendo medidas clínicas y demográficas. 
                        Se emplea comúnmente para entrenar modelos de predicción del riesgo de enfermedad cardíaca.
                    """, style={
                        'color': '#f5f5f5',
                        'padding': '20px',
                        'backgroundColor': '#1e1e1e',
                        'borderRadius': '12px',
                        'boxShadow': '0 0 10px rgba(144,202,249,0.3)',
                        'fontSize': '18px',
                        'lineHeight': '1.8',
                        'textAlign': 'justify'
                    }),
    
                    html.P("""
                        En este análisis nos enfocaremos en las siguientes variables, por su alta relevancia 
                        diagnóstica o por su correlación con el estado de salud cardíaco:
                    """, style={
                        'color': '#f5f5f5',
                        'padding': '20px',
                        'backgroundColor': '#1e1e1e',
                        'borderRadius': '12px',
                        'boxShadow': '0 0 10px rgba(144,202,249,0.3)',
                        'fontSize': '18px',
                        'lineHeight': '1.8',
                        'marginTop': '20px',
                        'textAlign': 'justify'
                    }),
    
                    html.Ul([
                        html.Li([html.Span("age: ", style={'color': '#90caf9'}), "Edad del paciente."]),
                        html.Li([html.Span("sex: ", style={'color': '#90caf9'}), "Género (1 = hombre, 0 = mujer)."]),
                        html.Li([html.Span("cp: ", style={'color': '#90caf9'}), "Tipo de dolor torácico (0-3)."]),
                        html.Li([html.Span("thalach: ", style={'color': '#90caf9'}), "Frecuencia cardíaca máxima alcanzada."]),
                        html.Li([html.Span("oldpeak: ", style={'color': '#90caf9'}), "Depresión del ST inducida por ejercicio."]),
                        html.Li([html.Span("ca: ", style={'color': '#90caf9'}), "Número de vasos principales coloreados por fluoroscopía."]),
                        html.Li([html.Span("thal: ", style={'color': '#90caf9'}), "Resultado de la prueba de talio."]),
                        html.Li([html.Span("slope: ", style={'color': '#90caf9'}), "Pendiente del segmento ST."]),
                        html.Li([html.Span("target: ", style={'color': '#90caf9'}), "Variable objetivo (1 = enfermedad cardíaca, 0 = sano)."]),
                    ], style={
                        'fontSize': '18px',
                        'lineHeight': '1.7',
                        'paddingLeft': '40px',
                        'color': '#f5f5f5'
                    })
                ], style={'width': '60%', 'padding': '20px'}),
    
                html.Div([
                    html.Img(src='/assets/book.png', style={
                        'width': '100%',
                        'maxWidth': '400px',
                        'height': 'auto',
                        'borderRadius': '12px',
                        'boxShadow': '0 0 10px rgba(144,202,249,0.3)'
                    })
                ], style={'width': '35%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'padding': '20px'})
    
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'})
    
        ], style={'padding': '40px'})
    ], style=estilo_tab),


        dcc.Tab(label='Planteamiento del Problema', children=[
    html.Div([
        html.H2("Planteamiento del Problema", style={
            'color': '#90caf9',
            'textAlign': 'center',
            'marginTop': '30px',
            'marginBottom': '30px',
            'fontWeight': 'bold'
        }),

        html.Div([
            html.Div([
                html.P("""
                    Las enfermedades cardiovasculares son una de las principales causas de mortalidad en el mundo. 
                    Detectarlas de forma oportuna es vital para salvar vidas, pero muchos diagnósticos aún dependen 
                    de pruebas costosas o de acceso limitado.
                """, style={
                    'color': '#f5f5f5',
                    'padding': '20px',
                    'backgroundColor': '#1e1e1e',
                    'borderRadius': '12px',
                    'boxShadow': '0 0 10px rgba(255,255,255,0.1)',
                    'fontSize': '20px',
                    'lineHeight': '1.8',
                    'textAlign': 'justify'
                }),

                html.P("""
                    El presente proyecto tiene como propósito desarrollar una herramienta que permita analizar un conjunto de datos clínicos 
                    para predecir la probabilidad de enfermedad cardíaca en un paciente, basándonos en variables como edad, género, presión arterial,
                    colesterol, frecuencia cardíaca máxima, entre otras.
                """, style={
                    'color': '#f5f5f5',
                    'padding': '20px',
                    'backgroundColor': '#1e1e1e',
                    'borderRadius': '12px',
                    'boxShadow': '0 0 10px rgba(255,255,255,0.1)',
                    'fontSize': '20px',
                    'lineHeight': '1.8',
                    'marginTop': '25px',
                    'textAlign': 'justify'
                }),

                html.Div([
                    html.H4("🎯 Objetivo General", style={
                        'color': '#bbdefb',
                        'fontWeight': 'bold',
                        'marginTop': '20px'
                    }),
                    html.P("""
                        Construir un modelo predictivo basado en Random Forest que identifique con alta precisión y rapidez
                        la presencia o ausencia de enfermedad cardíaca en pacientes, a partir de variables clínicas fácilmente accesibles.
                    """, style={
                        'color': '#f5f5f5',
                        'backgroundColor': '#1e1e1e',
                        'padding': '20px',
                        'borderRadius': '12px',
                        'marginTop': '10px',
                        'boxShadow': '0 0 10px rgba(144,202,249,0.2)',
                        'fontSize': '19px',
                        'textAlign': 'justify'
                    })
                ])
            ], style={'width': '60%', 'padding': '20px'}),

            html.Div([
                html.Img(src='/assets/data.png', style={
                    'width': '100%',
                    'maxWidth': '400px',
                    'height': 'auto',
                    'borderRadius': '12px',
                    'boxShadow': '0 0 10px rgba(144,202,249,0.3)'
                })
            ], style={'width': '35%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'padding': '20px'})

        ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'flexWrap': 'wrap'})

    ], style={'padding': '40px'})
]),

        dcc.Tab(
            label='Objetivos y Justificación',
            children=[
                html.Div([
                    html.H2("🎯 Objetivos y Justificación", style={
                        'textAlign': 'center',
                        'color': '#90caf9',
                        'marginTop': '30px',
                        'marginBottom': '30px',
                        'fontWeight': 'bold',
                        'fontSize': '36px',
                        'textShadow': '0 0 6px rgba(144,202,249,0.3)'
                    }),
        
                    html.Div([
                        html.H3("🎯 Objetivo General", style={'color': '#bbdefb'}),
                        html.P("Desarrollar un modelo de machine learning que permita predecir de forma eficiente y precisa la presencia de enfermedades cardíacas a partir de variables clínicas y demográficas.",
                            style={
                                'backgroundColor': '#1e1e1e',
                                'padding': '20px',
                                'borderRadius': '10px',
                                'color': '#f5f5f5',
                                'fontSize': '18px',
                                'boxShadow': '0 0 10px rgba(144,202,249,0.3)',
                                'marginBottom': '20px'
                            }
                        ),
        
                        html.H3("📌 Objetivos Específicos", style={'color': '#bbdefb'}),
                        html.Ul([
                            html.Li("Seleccionar las variables más relevantes para el diagnóstico de enfermedades cardíacas."),
                            html.Li("Entrenar y evaluar un modelo Random Forest con métricas apropiadas para problemas médicos."),
                            html.Li("Identificar los factores con mayor importancia en la predicción de enfermedad."),
                            html.Li("Facilitar la visualización de los resultados a través de un dashboard interactivo.")
                        ], style={
                            'backgroundColor': '#1e1e1e',
                            'padding': '20px',
                            'borderRadius': '10px',
                            'color': '#f5f5f5',
                            'fontSize': '18px',
                            'lineHeight': '1.8',
                            'boxShadow': '0 0 10px rgba(144,202,249,0.3)',
                            'listStyleType': 'disc'
                        }),
        
                        html.H3("🧠 Justificación", style={'color': '#bbdefb', 'marginTop': '40px'}),
                        html.P("""
                            Las enfermedades del corazón representan una de las principales causas de muerte en el mundo. 
                            La detección temprana mediante herramientas de machine learning puede reducir drásticamente los riesgos 
                            asociados, permitiendo intervenciones médicas oportunas. Este modelo busca apoyar a profesionales de la salud 
                            mediante un enfoque interpretativo, transparente y replicable.
                        """, style={
                            'backgroundColor': '#1e1e1e',
                            'padding': '20px',
                            'borderRadius': '10px',
                            'color': '#f5f5f5',
                            'fontSize': '18px',
                            'boxShadow': '0 0 10px rgba(144,202,249,0.3)',
                            'textAlign': 'justify',
                            'lineHeight': '1.8',
                            'marginTop': '20px'
                        })
                    ], style={'padding': '30px'})
                ])
            ],
            style=estilo_tab
        ),

        dcc.Tab(label='Marco Teórico',
    children=[
        html.Div([
            html.H2("📚 Marco Teórico", style={
                'textAlign': 'center',
                'color': '#90caf9',
                'marginTop': '30px',
                'marginBottom': '30px',
                'fontWeight': 'bold',
                'fontSize': '36px',
                'textShadow': '0 0 6px rgba(144,202,249,0.3)'
            }),

            html.Div([
                html.H3("🔬 Enfermedades Cardíacas", style={'color': '#bbdefb'}),
                html.P("""
                    Las enfermedades cardíacas comprenden un conjunto de afecciones que afectan al corazón y vasos sanguíneos. 
                    Entre las más comunes se encuentran la enfermedad coronaria, insuficiencia cardíaca, arritmias y enfermedad valvular.
                    Factores como el colesterol alto, la hipertensión, el tabaquismo, la diabetes y la inactividad física incrementan el riesgo.
                """, style={
                    'backgroundColor': '#1e1e1e',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'color': '#f5f5f5',
                    'fontSize': '18px',
                    'lineHeight': '1.8',
                    'textAlign': 'justify',
                    'boxShadow': '0 0 10px rgba(144,202,249,0.3)'
                }),

                html.H3("📊 Machine Learning en Medicina", style={'color': '#bbdefb', 'marginTop': '30px'}),
                html.P("""
                    El uso de algoritmos de aprendizaje automático permite detectar patrones complejos en grandes volúmenes de datos. 
                    En este caso, se utiliza un modelo de clasificación (Random Forest) para predecir la presencia de enfermedad cardíaca 
                    a partir de variables clínicas como la edad, presión arterial, frecuencia cardíaca, entre otros.
                """, style={
                    'backgroundColor': '#1e1e1e',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'color': '#f5f5f5',
                    'fontSize': '18px',
                    'lineHeight': '1.8',
                    'textAlign': 'justify',
                    'boxShadow': '0 0 10px rgba(144,202,249,0.3)'
                }),

                html.H3("🌲 Random Forest", style={'color': '#bbdefb', 'marginTop': '30px'}),
                html.P("""
                    Random Forest es un modelo de tipo ensamble que crea múltiples árboles de decisión y combina sus predicciones 
                    para mejorar precisión y evitar el sobreajuste. Es robusto, funciona bien con datos mixtos y permite interpretar 
                    la importancia de las variables, siendo ideal para contextos médicos donde la transparencia es clave.
                """, style={
                    'backgroundColor': '#1e1e1e',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'color': '#f5f5f5',
                    'fontSize': '18px',
                    'lineHeight': '1.8',
                    'textAlign': 'justify',
                    'boxShadow': '0 0 10px rgba(144,202,249,0.3)'
                })
            ], style={'padding': '30px'})
        ])
    ],
    style=estilo_tab
),
 dcc.Tab(
    label='Metodología',
    value="metodologia",
    children=[
        html.Div([
            html.H2("🧪 Metodología", style={
                'textAlign': 'center',
                'color': '#90caf9',
                'marginTop': '30px',
                'marginBottom': '30px',
                'fontWeight': 'bold',
                'fontSize': '36px',
                'textShadow': '0 0 6px rgba(144,202,249,0.3)'
            }),

            html.Div([
                html.H3("a. Definición del Problema a Resolver", style={'color': '#bbdefb'}),
                html.P("""
                    El problema abordado es de clasificación binaria: predecir si un paciente tiene
                    o no una enfermedad cardíaca (target = 1 indica enfermedad, target = 0 indica sano).
                    Se pretende desarrollar un modelo predictivo que pueda identificar pacientes en riesgo
                    con base en variables clínicas y demográficas.
                """, style={
                    'backgroundColor': '#1e1e1e',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'color': '#f5f5f5',
                    'fontSize': '18px',
                    'lineHeight': '1.8',
                    'textAlign': 'justify',
                    'boxShadow': '0 0 10px rgba(144,202,249,0.3)'
                }),

                html.H3("b. Preparación de los Datos", style={'color': '#bbdefb', 'marginTop': '30px'}),
                html.Ul([
                    html.Li("Las variables categóricas fueron codificadas (one-hot o numéricamente)."),
                    html.Li("Las variables numéricas fueron escaladas o estandarizadas cuando fue necesario."),
                    html.Li("Los datos se dividieron en conjuntos de entrenamiento/validación y prueba (70%-30%).")
                ], style={
                    'color': '#f5f5f5',
                    'fontSize': '18px',
                    'lineHeight': '1.7',
                    'paddingLeft': '40px'
                }),

                html.H3("c. Selección del Modelo o Algoritmo", style={'color': '#bbdefb', 'marginTop': '30px'}),
                html.P("""
                    Se seleccionó Random Forest por su capacidad de manejar datos mixtos,
                    evitar el sobreajuste y proporcionar interpretabilidad mediante la importancia de variables.
                    El modelo combina múltiples árboles de decisión entrenados sobre subconjuntos aleatorios de los datos.
                """, style={
                    'backgroundColor': '#1e1e1e',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'color': '#f5f5f5',
                    'fontSize': '18px',
                    'lineHeight': '1.8',
                    'textAlign': 'justify',
                    'boxShadow': '0 0 10px rgba(144,202,249,0.3)'
                }),
                html.P("Representación matemática del modelo:", style={'color': '#f5f5f5', 'fontSize': '18px', 'marginTop': '15px'}),
                html.Img(
    src="https://latex.codecogs.com/svg.image?\\color{white} \\hat{y}=\\text{modo}(h_1(x),h_2(x),\\dots,h_n(x))",
    style={'height': '60px'}
),


                html.H3("d. Entrenamiento y Evaluación del Modelo", style={'color': '#bbdefb', 'marginTop': '30px'}),
                html.Ul([
                    html.Li("El modelo fue entrenado con validación cruzada (k-fold, k=5)."),
                    html.Li("Se optimizaron hiperparámetros como el número de árboles, profundidad y número mínimo de muestras por hoja."),
                    html.Li("Se evaluó el desempeño usando métricas como Accuracy, Recall, Precision, F1-score y AUC-ROC."),
                    html.Li("Se priorizó el Recall sobre la clase positiva (enfermedad) para minimizar los falsos negativos.")
                ], style={
                    'color': '#f5f5f5',
                    'fontSize': '18px',
                    'lineHeight': '1.7',
                    'paddingLeft': '40px',
                    'marginBottom': '30px'
                })
            ], style={'padding': '30px'})
        ])
    ],
    style=estilo_tab
),

        
        dcc.Tab(label='Análisis Exploratorio de Datos', value="eda", children=[
            dcc.Tabs(id="eda-subtabs", value="distribuciones", children=[
                dcc.Tab(label='Distribuciones', value="distribuciones", children=[
                    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'flex-start'}, children=[
                        html.Div(children=graficos_como_componentes(pie), style={'width': '32%', 'marginRight': '1%'}),
                        html.Div(children=graficos_como_componentes(primeras_barras), style={'width': '65%', 'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-evenly'})
                    ]),
                    html.Div(style={'marginTop': '40px'}, children=[
                        html.Div(children=graficos_como_componentes(resto_barras), style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-evenly'})
                    ]),
                    html.Div(children=graficos_como_componentes(histogramas), style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-evenly'})
                ], style=estilo_tab),

                dcc.Tab(label='Boxplots', value="boxplots", children=[
                    html.Div(children=graficos_como_componentes(boxplots), style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})
                ], style=estilo_tab),

                dcc.Tab(label='Correlación e Importancia', value='correlacion_importancia', children=[
                    html.Div(
                        style={
                            'display': 'flex',
                            'flexWrap': 'wrap',
                            'justifyContent': 'space-evenly',
                            'gap': '30px'
                        },
                        children=graficos_como_componentes(correlaciones)
                    ),
                    html.Div(
                        style={
                            'display': 'flex',
                            'flexWrap': 'wrap',
                            'justifyContent': 'space-evenly',
                            'gap': '30px',
                            'marginTop': '250px'
                        },
                        children=graficos_como_componentes(importancias)
                    )
                ], style=estilo_tab)
            ])
        ], style=estilo_tab),


dcc.Tab(label='Resultados del Modelo', value="modelo", children=[
    html.Div(style={
        'backgroundColor': '#1e1e1e',
        'padding': '40px 80px',
        'borderRadius': '10px',
        'boxShadow': '0px 0px 10px #333'
    }, children=[
        html.H2("📊 Evaluación del Modelo Random Forest", style=estilo_subtitulo),

        html.P("El modelo fue entrenado con validación cruzada y GridSearchCV, maximizando el recall sobre la clase positiva. A continuación, se muestran las métricas principales de desempeño:",
               style=estilo_parrafo),

        # Tabla de métricas
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in ["Métrica", "Valor"]],
            data=[
                {"Métrica": "Accuracy", "Valor": "0.79"},
                {"Métrica": "Recall", "Valor": "0.90"},
                {"Métrica": "Precision", "Valor": "0.76"},
                {"Métrica": "F1 Score", "Valor": "0.83"},
                {"Métrica": "AUC ROC", "Valor": "0.87"},
                {"Métrica": "Tiempo de entrenamiento (s)", "Valor": "9.43"},
            ],
            style_cell={
                'backgroundColor': '#1e1e1e',
                'color': '#f5f5f5',
                'fontSize': '16px',
                'textAlign': 'center',
            },
            style_header={
                'backgroundColor': '#303f9f',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_table={'marginTop': '20px', 'marginBottom': '40px'}
        ),

        # Visualizaciones
        html.Div([
            html.Img(src="/assets/confusion.png", style={'width': '48%', 'marginRight': '4%'}),
            html.Img(src="/assets/roc.png", style={'width': '48%'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '30px'}),

        html.H3("📈 Evaluación del Overfitting", style=estilo_subtitulo),
        html.Ul([
            html.Li("🔁 Recall entrenamiento: 0.9826", style=estilo_parrafo),
            html.Li("🧪 Recall prueba: 0.9000", style=estilo_parrafo),
            html.Li("📊 Prueba t pareada sobre el recall: t = 1.6615, p = 0.1030", style=estilo_parrafo),
            html.Li("✅ Conclusión: No hay evidencia de overfitting, el modelo generaliza correctamente.", style=estilo_parrafo)
        ]),

        html.H3("🧠 Interpretación Final", style=estilo_subtitulo),
        html.P("""
            El modelo Random Forest logró un excelente desempeño, especialmente en la métrica priorizada (Recall), lo cual es clave en contextos médicos
            para minimizar los falsos negativos. La curva ROC sugiere buena discriminación entre clases, y el análisis de overfitting indica que el modelo 
            mantiene una generalización robusta. Esta herramienta puede ser de gran ayuda para la detección temprana de enfermedades cardíacas.
        """, style=estilo_parrafo)
    ])
], style=estilo_tab)
        
    ], style=estilo_tabs)
])

# Ejecutar servidor
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
