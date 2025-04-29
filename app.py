
import streamlit as st
import pandas as pd

st.set_page_config(page_title="PowerTech Motor", layout="centered")

st.markdown(
    "<h1 style='color: gold; text-align: center;'>PowerTech Motor</h1>"
    "<h3 style='color: gold; text-align: center;'>Control de Mantenimiento</h3>"
    "<p style='color: gray; text-align: center;'>Ing. Ronny Calva</p>",
    unsafe_allow_html=True
)

# Conexión a Google Sheets (CSV export)
sheet_url = 'https://docs.google.com/spreadsheets/d/1Fmwe1G9mM6WQlRb4QIHq4FIoZYl2Jm3-/edit#gid=0'
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(csv_export_url)

menu = st.selectbox("Selecciona una opción", ["Buscar Vehículo", "Agregar Vehículo"])

if menu == "Buscar Vehículo":
    placa = st.text_input("Ingresa la placa", "").upper()
    if placa:
        resultado = df[df["Placa"] == placa]
        if not resultado.empty:
            index = resultado.index[0]
            for col in df.columns:
                nuevo_valor = st.text_input(f"{col}:", resultado.iloc[0][col])
                df.at[index, col] = nuevo_valor
            if st.button("Guardar Cambios"):
                df.to_csv("/mnt/data/temp.csv", index=False)
                st.success("Datos actualizados (requiere subir el archivo manualmente si usas local).")
            if st.button("Eliminar Registro"):
                df.drop(index=index, inplace=True)
                df.to_csv("/mnt/data/temp.csv", index=False)
                st.success("Registro eliminado (requiere subir el archivo manualmente si usas local).")
        else:
            st.warning("No se encontró esa placa.")

elif menu == "Agregar Vehículo":
    nueva_fila = {}
    for col in df.columns:
        valor = st.text_input(f"{col}:", key=col)
        nueva_fila[col] = valor
    if st.button("Agregar Registro"):
        df.loc[len(df)] = nueva_fila
        df.to_csv("/mnt/data/temp.csv", index=False)
        st.success("Vehículo agregado (requiere subir el archivo manualmente si usas local).")
