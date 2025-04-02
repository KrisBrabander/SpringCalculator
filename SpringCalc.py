import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Engineering Tools", layout="wide")
st.title("🛠️ Engineering Tools")

# Tabs
opties = ["Gedempte Veer"]
tab1, = st.tabs(opties)

with tab1:
    st.markdown("""
    ## 🌀 Gedempte Veer Simulator
    Visualiseer de beweging van een massa aan een gedempte veer — met formules, grafieken en animatie.
    """)

    st.info("""
    ℹ️ **Wat stelt dit voor?**
    Een massa hangt aan een veer en kan op en neer bewegen. Door demping (zoals wrijving) zal deze trilling uiteindelijk stoppen.

    De beginpositie `x(0)` is de **afwijking vanaf het evenwicht**:
    - `x(0) > 0`: je trekt de massa omlaag voordat je loslaat.
    - `v(0) ≠ 0`: je geeft de massa een zetje omhoog of omlaag.

    Zonder afwijking of zetje blijft de massa gewoon hangen.
    """)

    # Sidebar: invoer
    st.sidebar.header("🔧 Instellingen")
    m = st.sidebar.number_input("Massa m (kg)", value=1.0, step=0.1)
    c = st.sidebar.number_input("Demping c (Ns/m)", value=10.0, step=0.1)
    k = st.sidebar.number_input("Veerconstante k (N/m)", value=100.0, step=1.0)
    x0 = st.sidebar.number_input("Beginpositie x(0) (m)", value=1.0)
    v0 = st.sidebar.number_input("Beginsnelheid x'(0) (m/s)", value=0.0)
    duur = st.sidebar.slider("Simulatieduur (seconden)", 2, 20, 10)

    # Dempingstype bepalen
    d = c**2 - 4 * m * k
    if d > 0:
        damping_type = "Overgedempt"
    elif d == 0:
        damping_type = "Kritisch gedempt"
    else:
        damping_type = "Ondergedempt"

    st.success(f"📊 Dempingstype: **{damping_type}**")

    # Tijd-as
    t = np.linspace(0, duur, 500)

    # Oplossing berekenen
    if d < 0:
        alpha = -c / (2 * m)
        omega = np.sqrt(4 * m * k - c**2) / (2 * m)
        A = x0
        B = (v0 - alpha * x0) / omega
        x = np.exp(alpha * t) * (A * np.cos(omega * t) + B * np.sin(omega * t))
        formule = r"x(t) = e^{%.2f t} ( %.2f \cos(%.2f t) + %.2f \sin(%.2f t) )" % (alpha, A, omega, B, omega)
    else:
        lambda1 = (-c + np.sqrt(d)) / (2 * m)
        lambda2 = (-c - np.sqrt(d)) / (2 * m)
        A = (v0 - lambda2 * x0) / (lambda1 - lambda2)
        B = x0 - A
        x = A * np.exp(lambda1 * t) + B * np.exp(lambda2 * t)
        formule = r"x(t) = %.2f e^{%.2f t} + %.2f e^{%.2f t}" % (A, lambda1, B, lambda2)

    st.markdown("---")
    st.subheader("📐 Oplossingsformule")
    st.latex(formule)

    # Samenvatting van resultaten
    st.markdown("---")
    st.subheader("📊 Samenvatting van resultaten")
    st.write(f"**Maximale uitwijking**: {np.max(np.abs(x)):.3f} meter")
    st.write(f"**Gemiddelde uitwijking**: {np.mean(np.abs(x)):.3f} meter")
    st.write(f"**Laatste uitwijking (na {duur}s)**: {x[-1]:.3f} meter — geeft aan hoe dicht de massa bij stilstand is")

    nuldoorgangen = (np.where(np.diff(np.sign(x)))[0].size) // 2
    st.write(f"**Aantal nulpassen (oscillaties)**: {nuldoorgangen}")

    energie_start = 0.5 * k * x0**2 + 0.5 * m * v0**2
    energie_verlies = "niet exact berekend (hangt af van c), maar energie daalt door demping"
    st.write(f"**Initiële energie**: {energie_start:.3f} J")
    st.write(f"**Energieverlies**: {energie_verlies}")

    if d < 0:
        frequentie = omega / (2 * np.pi)
        periode = 1 / frequentie
        st.write(f"**Trillingsfrequentie**: {frequentie:.2f} Hz")
        st.write(f"**Trillingsperiode**: {periode:.3f} s")

    # Plot statische grafiek
    st.markdown("---")
    st.subheader("📈 Verplaatsing in de tijd")
    fig, ax = plt.subplots()
    ax.plot(t, x, color="royalblue", linewidth=2)
    ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    ax.set_xlabel("Tijd (s)")
    ax.set_ylabel("x(t) (m)")
    ax.set_title("Massa aan gedempte veer")
    ax.grid(True)
    st.pyplot(fig)

    # Plot animatie
    st.subheader("🎥 Veeranimatie")
    frames = []
veerhoogte = 1.2  # constante lengte van de veer boven het blok  # constante lengte van de veer boven het blok
    for i in range(0, len(t), 5):
        blok_y = -x[i]
        veer_y = [0, blok_y]
        veer_x = [0, 0]
    frames.append(go.Frame(
            data=[
            go.Scatter(x=veer_x, y=veer_y, mode="lines", line=dict(color="gray", width=4)),
            go.Scatter(x=[0], y=[blok_y], mode="markers", marker=dict(size=50, color="saddlebrown", symbol="square"))
        ],
            name=str(i)
        ))

    layout = go.Layout(
        xaxis=dict(range=[-1, 1], zeroline=False, visible=False),
        yaxis=dict(range=[-max(x0, 1.5), max(x0, 1.5)], title="Hoogte (m)"),
        width=450,
        height=450,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor="white",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="▶️ Afspelen", method="animate", args=[None])],
            showactive=False
        )]
    )

    fig_anim = go.Figure(
        data=[
        go.Scatter(x=[0, 0], y=[0, -x[0]], mode="lines", line=dict(color="gray", width=4)),
        go.Scatter(x=[0], y=[-x[0]], mode="markers", marker=dict(size=50, color="saddlebrown", symbol="square"))
    ],
        layout=layout,
        frames=frames
    )

    st.plotly_chart(fig_anim)

    st.caption("✨ Gemaakt door Kris met hulp van ChatGPT — versie 'high-end' 🚀")
