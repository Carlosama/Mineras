import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(page_title="Prueba Azure SQL", layout="wide")
st.title("Prueba Azure SQL")

st.write("App iniciando...")

@st.cache_resource
def init_connection():
    cfg = st.secrets["azure_sql"]
    return pyodbc.connect(
        "DRIVER={"
        + cfg["driver"]
        + "};SERVER="
        + cfg["server"]
        + ";DATABASE="
        + cfg["database"]
        + ";UID="
        + cfg["username"]
        + ";PWD="
        + cfg["password"]
        + ";Encrypt=yes;TrustServerCertificate=no;"
    )

@st.cache_data(ttl=600)
def cargar_preview(minera: str):
    conn = init_connection()
    query = """
        SELECT TOP 50
            UPPER(LTRIM(RTRIM(FinalTAG))) AS FinalTAG,
            Fecha_Ingreso
        FROM dbo.mantenimientos
        WHERE FinalTAG IS NOT NULL
          AND LTRIM(RTRIM(FinalTAG)) <> ''
          AND Fecha_Ingreso IS NOT NULL
          AND UPPER(LTRIM(RTRIM(FinalTAG))) LIKE ?
        ORDER BY Fecha_Ingreso DESC
    """
    return pd.read_sql(query, conn, params=[f"{minera}%"])

minera = st.selectbox(
    "Minera",
    ["SPNC", "ANTU", "CEN", "GABY", "MEL", "LOMAS", "ABRA", "MICH", "REF", "FRANKE"]
)

try:
    df = cargar_preview(minera)
    st.success("Conexión OK")
    st.write(df.head(20))
    st.write("Filas:", len(df))
except Exception as e:
    st.error("Falló la conexión o la consulta.")
    st.exception(e)
