import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from fmpy import simulate_fmu
from fmpy.util import create_plotly_figure


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    dbc.Container(
        [
            html.Img(src=app.get_asset_url('Heater.png'), style={'max-width': '80%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})
        ],
        className='my-5'
    ),
    dbc.Container(
        [
            dbc.Form(
                [
                    dbc.Button('Simulate', id='simulate-button', color='primary', className='mr-4'),
                    dbc.InputGroup(
                        [
                            dbc.Input(id='stop-time', value='10', style={'text-align': 'right', 'width': '5rem'}),
                            dbc.InputGroupAddon('s', addon_type="append", style={'width': '2rem'})
                        ], className='mr-4'
                    )
                ], inline=True
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label('TAmb', html_for='TAmb', width=6),
                                    dbc.Col(
                                        dbc.InputGroup(
                                            [
                                                dbc.Input(id='TAmb', value='283.15', style={'text-align': 'right'}),
                                                dbc.InputGroupAddon('K', addon_type='append'),
                                            ], size='sm'
                                        ),
                                        width=6,
                                    ),
                                    html.Small("Ambient temperature", className='form-text text-muted ml-3')
                                ],
                                row=True, className='mb-2'
                            )
                        ],
                        width=12, lg=4, style={'margin-top': '2rem'}
                    ),
                    dbc.Col(id='result-col', width=12, lg=8),
                ], className='mt-4'
            ),
        ],
        id='simulation-container'
    ),

])


@app.callback(
    Output('result-col', 'children'),
    [Input('simulate-button', 'n_clicks')],
    [State('stop-time', 'value'), State('TAmb', 'value')]
)
def update_output_div(n_clicks, stop_time, TAmb):

    try:
        result = simulate_fmu(filename='Heater.fmu', stop_time=stop_time, start_values={'TAmb': TAmb})
        fig = create_plotly_figure(result=result)
        return dcc.Graph(figure=fig)
    except Exception as e:
        return dbc.Alert("Simulation failed. %s" % e, color='danger'),


if __name__ == "__main__":
    app.run_server()
