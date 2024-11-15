import streamlit as st
import requests

# Funções auxiliares
def obter_cotacao(par_moedas):
    """
    Obtém a cotação para o par de moedas especificado.
    :param par_moedas: Par de moedas no formato 'USD/BRL', 'EUR/USD', etc.
    :return: Taxa de câmbio atual para o par de moedas.
    """
    base, quote = par_moedas.split('/')
    url = 'https://openexchangerates.org/api/latest.json'
    params = {
        'app_id': 'edd30e082f404192ae8c03219d82e3f6',  # Substitua pela sua chave da API
        'symbols': f"{base},{quote}"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValueError("Erro ao obter a cotação. Verifique sua API Key e a conexão com a internet.")

    data = response.json()
    if 'rates' not in data or base not in data['rates'] or quote not in data['rates']:
        raise ValueError(f"Cotações para {par_moedas} não encontradas.")

    return data['rates'][quote] / data['rates'][base]

def calcular_lote_e_risco(risco_brl, par_moedas, pips):
    """
    Calcula o tamanho do lote e o risco em termos do par de moedas operado.
    :param risco_brl: Quantia de risco em BRL.
    :param par_moedas: Par de moedas no formato 'BASE/QUOTE' (ex.: 'USD/BRL').
    :param pips: Quantidade de pips para a operação.
    :return: Tamanho do lote e risco na moeda da contraparte.
    """
    # Converter BRL para USD
    taxa_brl_usd = obter_cotacao('USD/BRL')

    risco_usd = risco_brl / taxa_brl_usd

    # Obter a cotação do par de moedas operado
    taxa_cambio = obter_cotacao(par_moedas)

    # Calcula o tamanho do lote
    tamanho_lote = risco_usd / (pips / taxa_cambio)

    return tamanho_lote, risco_usd

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Calculadora de Lote e Risco",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cabeçalho da página
st.title("Calculadora de Lote e Risco")
st.markdown(
    """
    ### Ferramenta Profissional para Traders
    Realize cálculos precisos de tamanho de lote e risco em poucos passos.
    """
)

# Criação de seções principais
with st.sidebar:
    st.header("Configurações da Operação")
    
    risco_brl = st.number_input(
        "Risco em BRL:", min_value=0.0, step=0.01, value=100.0, help="Quantia de risco definida em reais."
    )

    par_moedas = st.text_input(
        "Par de moedas (ex.: USD/JPY):", value="USD/BRL", help="Digite o par de moedas no formato BASE/QUOTE."
    ).upper()

    pips = st.number_input(
        "Quantidade de pips:", min_value=0.0, step=0.1, value=50.0, help="Informe o tamanho do stop loss em pips."
    )

    calcular = st.button("Calcular")

# Área de exibição de resultados
with st.container():
    st.markdown("---")
    st.header("Resultados")

    if calcular:
        try:
            # Ajustar pips
            pips_adjusted = pips * 1.20  # Ajuste do valor de pips

            # Realizar cálculo
            tamanho_lote, risco_usd = calcular_lote_e_risco(risco_brl, par_moedas, pips_adjusted)

            # Exibir resultados
            st.success("Cálculo realizado com sucesso!")
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Tamanho do Lote", f"{tamanho_lote:.2f}")

            with col2:
                st.metric("Risco em USD", f"${risco_usd:.2f}")

            st.balloons()

        except ValueError as e:
            st.error(f"Erro: {e}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
    else:
        st.info("Configure os parâmetros no menu lateral e clique em 'Calcular' para ver os resultados.")
