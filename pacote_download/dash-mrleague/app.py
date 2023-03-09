from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# ================================================================
# ================================================================

#pio.templates.default = 'seaborn'

# Importando planilha e limpando os dados

df = pd.read_excel('testedatasetv2b.xlsx')

df['V'] = df['V'].fillna(0)
df['E'] = df['E'].fillna(0)
df['D'] = df['D'].fillna(0)
df['GOL'] = df['GOL'].fillna(0)
df['ASS'] = df['ASS'].fillna(0)
df['STG'] = df['STG'].fillna(0)
df['GC'] = df['GC'].fillna(0)
df['AMA'] = df['AMA'].fillna(0)
df['AZUL'] = df['AZUL'].fillna(0)
df['VER'] = df['VER'].fillna(0)
df['PP'] = df['PP'].fillna(0)
df['GS'] = df['GS'].fillna(0)
df['DD'] = df['DD'].fillna(0)
df['DP'] = df['DP'].fillna(0)
df['FALTA'] = df['FALTA'].fillna(0)


### configurando df
# # # corrida anual

df_geral = df.drop(["PARTIDA", "RODADA", "PARTIDA", "POSIÇÃO", "TIME"], axis=1)
df_geral = df_geral.groupby('PLAYER').sum().reset_index()
df_geral = df_geral.sort_values('PTS', ascending=False)
df_geral

# # # desempenho player by rodada

list_rodadas = df.RODADA.unique()
list_players = df['PLAYER'].unique()

# # # artilheiro

df_artilheiro = df.groupby('PLAYER').sum()
df_artilheiro = df_artilheiro.reset_index()
df_artilheiro = df_artilheiro.sort_values('GOL', ascending=False)
df_artilheiro = df_artilheiro.iloc[0:5]

df_artilheiro

# # # assistencias

df_assistencias = df.groupby('PLAYER').sum()
df_assistencias = df_assistencias.reset_index()
df_assistencias = df_assistencias.sort_values('ASS', ascending=False)
df_assistencias = df_assistencias.iloc[0:5]

df_assistencias

# ================================================================
# ================================================================

# Definindo o pre layout do dashboard

fig_geral = px.bar(data_frame=df_geral, x='PLAYER', y='PTS', text_auto='.2s', template='plotly_dark', hover_data=['PLAYER', 'V', 'E', 'D', 'GOL', 'ASS', 'STG'])
fig_geral.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig_geral.update_yaxes(showticklabels=False)
fig_geral.update_layout(
    autosize=True,
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    margin=dict(l=10, r=10, t=10, b=0)
)

fig_artilheiro = px.bar(data_frame=df_artilheiro, x='PLAYER', y='GOL', text_auto='.2s',template='plotly_dark', color_discrete_sequence=["purple"], title='TOP 5: ARTILHEIROS')
fig_artilheiro.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig_artilheiro.update_yaxes(showticklabels=False)
fig_artilheiro.update_layout(
    autosize=True,
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    margin=dict(l=30, r=30, t=30, b=30)
)

fig_assistencia = px.bar(data_frame=df_assistencias, x='PLAYER', y='ASS', text_auto='.2s',template='plotly_dark', color_discrete_sequence=["aquamarine"], title='TOP 5: ASSISTÊNCIAS')
fig_assistencia.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig_assistencia.update_yaxes(showticklabels=False)
fig_assistencia.update_layout(
    autosize=True,
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    margin=dict(l=30, r=30, t=30, b=30)
)


# layout: estrutura da pagina (como fica na visualização web)

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo", src=app.get_asset_url("logovector.png"),height=100),
                html.H2('Rumo ao Estrelato'),
                dbc.Button("2023", color="primary", id="location-button", size="lg")
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Total de Partidas"),
                            html.H3(style={'color': '#adfc92'}, id='total_partidas_card')
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px'})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Total de Gols"),
                            html.H3(style={'color': '#C124FF'}, id='total_gols_card')
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px'})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("1° ranking"),
                            html.H3(style={'color': '#E5A96B'}, id='primeiro_colocado_card')
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px'})
                ], md=4),
            ]),

            html.Div([
                html.H4('Ranking Geral: ', style={"margin-top": "40px"}),
                dcc.Graph(id='grafico_corrida_geral_esquerda', figure=fig_geral),
                html.H4('Desempenho geral por rodada: ', style={"margin-top": "40px"}),
                html.P('Selecione a rodada: ', style={'margin-top': '25px'}),
                dcc.Dropdown(id='drop_rodadas',
                             options=list_rodadas,
                            value=list_rodadas[0],
                            style={'margin-top': '10px'}
                            ),
                dcc.Graph(id='figura1', style={'margin-top': '25px'}),
                dcc.Graph(id='figura2', style={'margin-top': '25px'})
        ])
            ], md=5, style={'padding': '25px', 'background-color':'#242424'}),


        dbc.Col([
            html.Div([
                html.Img(id="logo_b", src=app.get_asset_url("capamr23.png"),height=270, style={'textAlign': 'center'}),
            ],style={'textAlign': 'center'}),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='top_artilheiro', figure=fig_artilheiro ,style={"margin-top": "40px", 'margin-left': '25px'})
                ], md=6),

                dbc.Col([
                    dcc.Graph(id='top_assistencias', figure=fig_assistencia, style={"margin-top": "40px"})
                ], md=6),
                     ]),

            html.Div([
                html.H4('DESEMPENHO INDIVIDUAL', style={"margin-top": "30px", 'textAlign': 'center'}),
                html.P('Selecione o player: ', style={'margin-top': '25px'}),
                html.Div([dcc.Dropdown(options=list_players, value=list_players[0], id='drop_players')],
                    style={"display": "inline-block", "width": "15%"}),
                html.P('Selecione a(s) rodada(s): ', style={'margin-top': '25px'}),
                dcc.RangeSlider(1, len(list_rodadas), 1, value=[1, len(list_rodadas)], id='slider_player'),
                dcc.Graph(id='figura3', style={'margin-left': '25px', 'margin-top': '25px'}),
                dcc.Graph(id='figura4', style={'margin-left': '25px', 'margin-top': '25px'})
                    ])

        ], md=7)
    ], class_name='g-0')
, fluid=True)

# definindo a callback
@app.callback(
    Output("total_partidas_card", "children"),
    Output("total_gols_card", "children"),
    Output("primeiro_colocado_card", "children"),
    Output("figura1", "figure"),
    Output("figura2", "figure"),
    Output("figura3", "figure"),
    Output("figura4", "figure"),
    Input("drop_rodadas", "value"),
    Input('drop_players', 'value'),
    Input('slider_player', 'value'),
)

def update_output(sel_rodada, sel_player, slider_rodada):
    # Rotina Card 1:
    df_numero_partidas = df.groupby('PARTIDA').count().reset_index()
    lista_qt_partidas = df_numero_partidas['PARTIDA'].tolist()
    qtde_partidas = len(lista_qt_partidas)

    # Rotina Card 2:
    lista_gols = df['GOL'].tolist()
    qtde_gols = sum(lista_gols)

    # Rotina Card 3:
    df_top_1 = df.groupby('PLAYER').sum().reset_index().sort_values('PTS', ascending=False)
    nome_top_1 = df_top_1.iloc[0,0]

    # 1- Rotina da Primeira Figura
    df_b = df.loc[df.RODADA == sel_rodada]
    df_rodada_player = df_b.groupby(['PLAYER']).sum()
    df_rodada_player = df_rodada_player.sort_values('PTS', ascending=False)
    df_rodada_player.reset_index()
    df_rodada_player.reset_index(inplace=True)
    # Definição da Primeira figura
    fig1 = px.bar(df_rodada_player, x='PLAYER', y='PTS', hover_data=['PLAYER', 'V', 'E', 'D', 'GOL', 'ASS', 'STG'], barmode="stack", text_auto='.2s', template='plotly_dark', title='Pontuação individual p/ rodada')
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig1.update_yaxes(showticklabels=False)
    fig1.update_layout(
    autosize=True,
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    margin=dict(l=10, r=10, t=90, b=0),
    )

    #figura2
    fig2 = px.bar(df_rodada_player, x='PLAYER', y=['V', 'E', 'D'], title='V/E/D p/ Rodada', barmode="group", text_auto='.2s', template='plotly_dark', color_discrete_map={'V': '#0F944D','E':'yellow','D': '#802A24'}, labels={"PLAYER": "Player", "value": "V E D"})
    fig2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig2.update_yaxes(showticklabels=False)
    fig2.update_layout(
    autosize=True,
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    margin=dict(l=10, r=10, t=30, b=60)
    )

    # B - Rotina da primeira figura
    df_p = df.loc[df['PLAYER'] == sel_player]
    df_p = df_p.loc[(df_p['RODADA'] >= slider_rodada[0]) & (df_p['RODADA'] <= slider_rodada[1])]
    df_player_teste = df_p.groupby(['PLAYER']).sum()
    df_player_teste.reset_index()
    df_player_teste.reset_index(inplace=True)


    #B - figura 1
    fig3 = px.bar(df_player_teste, x='PLAYER', y=['V', 'E', 'D', 'GOL'], barmode='group', template='plotly_dark', color_discrete_map={'V': '#0F944D','E':'yellow','D': '#802A24'})
    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig3.update_yaxes(showticklabels=False)
    fig3.update_layout(
    autosize=True,
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    margin=dict(l=10, r=10, t=30, b=60)
    )

    #B- Rotina da Segunda Figura Player
    df_p2 = df.loc[df['PLAYER'] == sel_player]
    df_p2 = df_p.loc[(df_p2['RODADA'] >= slider_rodada[0]) & (df_p['RODADA'] <= slider_rodada[1])]
    df_player_teste_b = df_p2.groupby(['RODADA']).sum()
    df_player_teste_b.reset_index()
    df_player_teste_b.reset_index(inplace=True)
    
    #B - Figura pts p/ player
    fig4 = px.line(df_player_teste_b, x='RODADA', y='PTS',template='plotly_dark', title='PONTUAÇÃO INDIVIDUAL P/ RODADA')
    fig4.update_layout(
        autosize=True,
        xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
        yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True,
    ),
        showlegend=False,
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
    )
    


    return qtde_partidas,qtde_gols,nome_top_1,fig1,fig2,fig3,fig4


# ================================================================
# ================================================================
#rodar programa

if __name__ == "__main__":
    app.run_server(debug=True)

