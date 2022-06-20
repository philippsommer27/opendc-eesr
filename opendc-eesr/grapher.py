import plotly.graph_objects as go
from plotly.subplots import make_subplots


def selector(name, **args):
    graph_func_lookup[name](args)


def energy_sources_comp(data):
    pass

def ranking_bar_chart(this, others, metric_name):
    pass


def rn_energy_adapt(dc_cons, ren_prod, x):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(y=dc_cons, x=x, name="DC Total Energy"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=ren_prod, x=x, name="Grid Renewable Energy"),
        secondary_y=True,
    )

    fig.update_layout(title_text="Clean Energy Adaptability",
                      template='simple_white',
                      font=dict(
                          size=26
                      ),
                      legend=dict(
                          x=0.55,
                          y=1.2
                      ),
                      width=950,
                      height=700
                      )

    fig.update_xaxes(title_text="Time (minutes)")

    fig.update_yaxes(title_text="Consumption <b>kWh</b>", secondary_y=False)
    fig.update_yaxes(title_text="Production <b>mWh</b>", secondary_y=True)

    write_path = "template/content/rn_energy_adapt.svg"
    fig.write_image(write_path)
    # pio.write_image(fig, write_path, width=1.5*300, height=0.75*300, scale=1)
    return write_path


graph_func_lookup = {
    "energy_sources_comp": energy_sources_comp,
    "rn_energy_adapt": rn_energy_adapt,
    "ranking_bar_chart": ranking_bar_chart,
}
