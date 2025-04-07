

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Warfarin Dosing Simulator", layout="centered")

st.title("💊 Warfarin Dosing Simulator")

st.sidebar.header("🧬 Пациентски параметри")

# Входни параметри
age = st.sidebar.slider("Възраст", 18, 100, 65)
weight = st.sidebar.slider("Тегло (кг)", 40, 120, 75)
cyp2c9 = st.sidebar.selectbox("Генотип CYP2C9", ["*1/*1", "*1/*2", "*1/*3", "*2/*2", "*2/*3", "*3/*3"])
vkorc1 = st.sidebar.selectbox("Генотип VKORC1", ["G/G", "G/A", "A/A"])
initial_inr = st.sidebar.slider("Начален INR", 1.0, 4.0, 1.3)

# Евристична доза
dose_factor = {"*1/*1": 1.0, "*1/*2": 0.8, "*1/*3": 0.6, "*2/*2": 0.5, "*2/*3": 0.4, "*3/*3": 0.3}
vkorc1_factor = {"G/G": 1.0, "G/A": 0.8, "A/A": 0.6}
base_dose = 5.0
recommended_dose = base_dose * dose_factor[cyp2c9] * vkorc1_factor[vkorc1]

st.subheader("📋 Препоръчителна начална доза:")
st.success(f"{recommended_dose:.2f} mg/day")

# Симулиране на INR
days = 15
inr_values = [initial_inr]
for day in range(1, days):
    noise = np.random.normal(0, 0.1)
    inr = inr_values[-1] + (recommended_dose - 5.0) * 0.2 + noise
    inr = max(0.5, min(inr, 6.0))
    inr_values.append(inr)

# Графика
st.subheader("📈 INR стойности за 15 дни")
fig, ax = plt.subplots()
ax.plot(range(1, days + 1), inr_values, marker='o')
ax.axhline(2.0, color='green', linestyle='--', label='Терапевтичен минимум')
ax.axhline(3.0, color='green', linestyle='--', label='Терапевтичен максимум')
ax.set_xlabel("Ден")
ax.set_ylabel("INR")
ax.set_title("Прогноза на INR")
ax.legend()
st.pyplot(fig)
