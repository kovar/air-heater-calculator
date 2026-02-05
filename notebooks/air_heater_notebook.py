import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium")


@app.cell
def _(delta_t_slider, flow_slider, mdot_kgs, mo, power_w):
    mo.md(f"""
    # Nitrogen Heater Power Calculator

    | Parameter  | Adjustment        | Unit |
    | :---:      | :---:            | :---: |
    | Flow rate  | {flow_slider} | SCFM |
    | Delta T    | {delta_t_slider} | K |

    **Mass flow rate**  
    {mdot_kgs * 1000:.2f} g/s

    **Required heater power**  
    **{power_w:.0f} W** ({power_w / 1000:.2f} kW)

    *Assumptions: N₂, isobaric heating at ~1 bar, Cp ≈ 1040 J/(kg·K),  
    no losses, steady flow after expansion.*
    """)
    return


@app.cell
def _(mo):
    flow_slider = mo.ui.slider(
        start=0.0,
        stop=20.0,
        step=0.1,
        value=5.0,
        label="Flow rate (SCFM)",
        show_value=True,
    )
    delta_t_slider = mo.ui.slider(10, 50, value=30, label="ΔT (°C)")
    return delta_t_slider, flow_slider


@app.cell
def _(delta_t_slider):
    SCFM_TO_KG_S = 0.00055807      # kg/s per SCFM
    CP_N2 = 1040.0                 # J/(kg·K) ≈ constant in this range
    DELTA_T = delta_t_slider.value          # °C (heater outlet – inlet)
    return CP_N2, DELTA_T, SCFM_TO_KG_S


@app.cell
def _(CP_N2, DELTA_T, SCFM_TO_KG_S, flow_slider):
    flow_scfm = flow_slider.value
    mdot_kgs = flow_scfm * SCFM_TO_KG_S
    power_w = flow_scfm * SCFM_TO_KG_S * CP_N2 * DELTA_T
    return mdot_kgs, power_w


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
