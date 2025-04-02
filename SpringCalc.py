import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🌀 Gedempte Veer Calculator")

# Invoer
m = st.number_input("Massa (m) in kg", value=1.0, step=0.1)
c = st.number_input("Demping (c) in Ns/m", value=10.0, step=0.1)
k = st.number_input("Veerconstante (k) in N/m", value=100.0, step=1.0)
x0 = st.number_input("Beginpositie x(0) in m", value=1.0)
v0 = st.number_input("Beginsnelheid x'(0) in m/s", value=0.0)

# Discriminant
d = c**2 - 4 * m * k

st.markdown("---")

# Classificatie
damping_type = ""
if d > 0:
    damping_type = "Overgedempt"
elif d == 0:
    damping_type = "Kritisch gedempt"
else:
    damping_type = "Ondergedempt"

st.subheader(f"📊 Type demping: {damping_type}")

# Berekening oplossingen
if d >= 0:
    lambda1 = (-c + np.sqrt(d)) / (2 * m)
    lambda2 = (-c - np.sqrt(d)) / (2 * m)
    st.write(f"Oplossing: x(t) = A·e^({lambda1:.2f}t) + B·e^({lambda2:.2f}t)")
else:
    alpha = -c / (2 * m)
    omega = np.sqrt(4 * m * k - c**2) / (2 * m)
    st.write(r"Oplossing: $x(t) = e^{" + f"{alpha:.2f}t" + r"}(A \cos(" + f"{omega:.2f}t" + r") + B \sin(" + f"{omega:.2f}t" + r"))$")

# Plot
st.markdown("---")
st.subheader("📈 Simulatie van x(t)")
t = np.linspace(0, 10, 1000)

if d < 0:
    alpha = -c / (2 * m)
    omega = np.sqrt(4 * m * k - c**2) / (2 * m)
    A = x0
    B = (v0 - alpha * x0) / omega
    x = np.exp(alpha * t) * (A * np.cos(omega * t) + B * np.sin(omega * t))
else:
    lambda1 = (-c + np.sqrt(d)) / (2 * m)
    lambda2 = (-c - np.sqrt(d)) / (2 * m)
    A = (v0 - lambda2 * x0) / (lambda1 - lambda2)
    B = x0 - A
    x = A * np.exp(lambda1 * t) + B * np.exp(lambda2 * t)

fig, ax = plt.subplots()
ax.plot(t, x)
ax.set_xlabel("Tijd (s)")
ax.set_ylabel("Verplaatsing x(t) (m)")
ax.set_title("Beweging van een gedempte massa-veer")
ax.grid(True)
st.pyplot(fig)

st.caption("Gemaakt door Kris Brabander")
