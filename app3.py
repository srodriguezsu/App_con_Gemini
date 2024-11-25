import streamlit as st
import re
import pandas as pd
from io import BytesIO

# Configuración de la app
st.title("Generador de archivo Excel con regex")
st.write(
    """
    Esta aplicación utiliza expresiones regulares para procesar un archivo 
    CSV y genera un archivo Excel estructurado con los datos encontrados.
    """
)

# Cargar el archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo regex_productos.csv", type="csv")

if uploaded_file:
    # Leer el contenido del archivo
    content = uploaded_file.read().decode("utf-8")

    # Expresión regular para extraer los datos
    pattern = re.compile(
        r"(?P<nombre>[A-Z][a-z]+\s[A-Z][a-z]+),"
        r"(?P<valor>\d+\.\d+),"
        r"(?P<fecha>\d{2}/\d{2}/\d{2}),"
        r"(?P<telefono>\+57\s\d+),"
        r"(?P<correo>\S+@\S+\.\w+),"
        r"(?P<producto>.+?),"
        r"(?P<serie>\d+)"
    )

    # Extraer los datos
    matches = pattern.findall(content)
    if matches:
        data = []
        for match in matches:
            data.append(
                {
                    "Número de Serie": match[6],
                    "Nombre del Producto": match[5],
                    "Valor": float(match[1]),
                    "Fecha de Compra": match[2],
                    "Contacto (Nombre)": match[0],
                    "Correo Electrónico": match[4],
                    "Teléfono": match[3],
                }
            )

        # Crear un DataFrame
        df = pd.DataFrame(data)

        # Mostrar la tabla en la app
        st.write("Datos procesados:")
        st.dataframe(df)

        # Convertir a Excel
        # def to_excel(dataframe):
            # output = BytesIO()
            # with pd.ExcelWriter(output, engine="openpyxl") as writer:
            #     dataframe.to_excel(writer, index=False, sheet_name="Productos")
            # processed_data = output.getvalue()
            # return processed_data

        # excel_data = to_excel(df)

        # # Botón de descarga
        # st.download_button(
        #     label="Descargar archivo Excel",
        #     data=excel_data,
        #     file_name="productos_procesados.xlsx",
        #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        # )
    else:
        st.error("No se encontraron coincidencias en el archivo. Verifica el formato.")
