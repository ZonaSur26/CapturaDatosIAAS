import streamlit as st

def render():
    st.title("Infección Polimicrobiana")
    
    es_polimicrobiana = st.radio("¿SE TRATA DE UNA INFECCIÓN POLIMICROBIANA?", ["No", "Sí"], index=None, horizontal=True)
    
    if es_polimicrobiana == "Sí":
        st.info("Por favor, indique los microorganismos adicionales aislados:")
        
        # Usamos un número dinámico de campos o una lista
        num_micro = st.number_input("Número de microorganismos adicionales:", min_value=1, max_value=5, value=1)
        
        for i in range(num_micro):
            st.text_input(f"Microorganismo adicional {i+1}", key=f"micro_extra_{i}")
            
    if st.button("Guardar Infección Polimicrobiana"):
        st.success("Datos de infección polimicrobiana guardados.")

if __name__ == "__main__":
    render()
