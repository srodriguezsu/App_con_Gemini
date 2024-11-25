import streamlit as st
import re
import pandas as pd

# Título y descripción de la app
st.title("📜 Desenmascara el Texto")
st.write(
    """
    ¿Qué secretos esconde tu texto?  
    Carga un archivo o escribe algo, y selecciona un filtro para encontrar correos electrónicos, números, fechas, palabras largas y más.  
    **¡Descubre lo que nunca imaginaste!**  
    """
)

# Cargar texto
st.header("🔍 Carga o escribe tu texto")
texto_subido = st.file_uploader("Sube un archivo de texto (.txt)", type="txt")
texto_usuario = st.text_area("O escribe tu texto aquí:", height=200)

# Unificar entrada de texto
if texto_subido:
    texto = texto_subido.read().decode("utf-8")
else:
    texto = texto_usuario

# Opciones de filtros
st.header("🎛️ Filtros para analizar el texto")
filtro = st.selectbox(
    "Elige un filtro para buscar patrones:",
    [
        "Correos electrónicos",
        "Números de teléfono",
        "Fechas (formato DD/MM/YY)",
        "Palabras largas (+7 letras)",
        "Palabras repetidas",
    ],
)

# Regex para cada filtro
patrones = {
    "Correos electrónicos": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "Números de teléfono": r"\+?\d{1,3}\s?\d{10}",
    "Fechas (formato DD/MM/YY)": r"\b\d{2}/\d{2}/\d{2}\b",
    "Palabras largas (+7 letras)": r"\b[a-zA-Z]{7,}\b",
    "Palabras repetidas": r"\b(\w+)\b(?=.*\b\1\b)",
}

# Procesar texto
if texto and filtro:
    st.write(f"Buscando: **{filtro}** en el texto...")

    patron = patrones[filtro]
    coincidencias = re.findall(patron, texto, re.IGNORECASE)

    if coincidencias:
        st.success(f"¡Se encontraron {len(coincidencias)} coincidencias! 🎉")
        st.write(coincidencias)

        # Crear DataFrame para mostrar resultados en tabla
        df = pd.DataFrame(coincidencias, columns=["Resultados"])
        st.dataframe(df)

        # Descargar resultados como CSV
        @st.cache_data
        def convertir_csv(data):
            return data.to_csv(index=False).encode("utf-8")

        csv_data = convertir_csv(df)
        st.download_button(
            label="📥 Descargar resultados",
            data=csv_data,
            file_name="resultados.csv",
            mime="text/csv",
        )
    else:
        st.warning("No se encontraron coincidencias. ¿Seguro que tu texto contiene este patrón?")

# Consejos y curiosidades
st.sidebar.title("🎯 Consejos divertidos")
st.sidebar.write(
    """
    - Usa **Correos electrónicos** para encontrar emails ocultos en tus textos.
    - Descubre **Fechas importantes** en registros o libros.
    - Encuentra **Palabras repetidas** para análisis literarios o corrección.
    - Usa **Números de teléfono** para limpiar bases de datos.
    - ¡Juega buscando **Palabras largas** en juegos de vocabulario!
    """
)
