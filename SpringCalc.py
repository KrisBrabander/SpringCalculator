import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Gedempte Veer", layout="centered")
st.title("🌀 Gedempte Veer Simulator")
st.markdown("Visualiseer de beweging van een gedempte massa-veer.")

# Invoer
st.sidebar.header("🔧 Invoerparameters")
m = st.sidebar.number_input("Massa (m) in kg", value=1.0, step=0.1)
c = st.sidebar.number_input("Demping (c) in Ns/m", value=10.0, step=0.1)
k = st.sidebar.number_input("Veerconstante (k) in N/m", value=100.0, step=1.0)
x0 = st.sidebar.number_input("Beginpositie x(0) in m", value=1.0)
v0 = st.sidebar.number_input("Beginsnelheid x'(0) in m/s", value=0.0)
duur = st.sidebar.slider("Simulatieduur (s)", 2, 20, 10)

# Discriminant
d = c**2 - 4 * m * k

# Classificatie
damping_type = ""
if d > 0:
    damping_type = "Overgedempt"
elif d == 0:
    damping_type = "Kritisch gedempt"
else:
    damping_type = "Ondergedempt"

st.subheader(f"📊 Type demping: {damping_type}")

# Tijd
st.markdown("---")
t = np.linspace(0, duur, 500)

# Berekening oplossing
if d < 0:
    alpha = -c / (2 * m)
    omega = np.sqrt(4 * m * k - c**2) / (2 * m)
    A = x0
    B = (v0 - alpha * x0) / omega
    x = np.exp(alpha * t) * (A * np.cos(omega * t) + B * np.sin(omega * t))
    st.latex(r"x(t) = e^{%.2f t} ( %.2f \cos(%.2f t) + %.2f \sin(%.2f t) )" % (alpha, A, omega, B, omega))
else:
    lambda1 = (-c + np.sqrt(d)) / (2 * m)
    lambda2 = (-c - np.sqrt(d)) / (2 * m)
    A = (v0 - lambda2 * x0) / (lambda1 - lambda2)
    B = x0 - A
    x = A * np.exp(lambda1 * t) + B * np.exp(lambda2 * t)
    st.latex(r"x(t) = %.2f e^{%.2f t} + %.2f e^{%.2f t}" % (A, lambda1, B, lambda2))

# Plot statische grafiek
st.markdown("---")
st.subheader("📈 Simulatie van de veerbeweging (verplaatsing over tijd)")
fig, ax = plt.subplots()
ax.plot(t, x, color="blue")
ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
ax.set_xlabel("Tijd (s)")
ax.set_ylabel("Verplaatsing x(t) (m)")
ax.set_title("Beweging van de massa aan de veer")
ax.grid(True)
st.pyplot(fig)

# Plot animatie
st.subheader("🎥 Animatie van de massa aan de veer")
frames = []
for i in range(0, len(t), 5):
    frames.append(go.Frame(
        data=[go.Scatter(x=[0], y=[-x[i]], mode="markers", marker=dict(size=30, color="royalblue"))],
        name=str(i)
    ))

layout = go.Layout(
    xaxis=dict(range=[-1, 1], zeroline=False, visible=False),
    yaxis=dict(range=[-max(x0, 1.5), max(x0, 1.5)], title="Hoogte (m)"),
    width=400,
    height=400,
    showlegend=False,
    updatemenus=[dict(
        type="buttons",
        buttons=[dict(label="▶️ Afspelen", method="animate", args=[None])]
    )]
)

fig_anim = go.Figure(
    data=[go.Scatter(x=[0], y=[-x[0]], mode="markers", marker=dict(size=30, color="royalblue"))],
    layout=layout,
    frames=frames
)

st.plotly_chart(fig_anim)

st.caption("Gemaakt door Kris en ChatGPT ✨")
