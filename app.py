import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Custom CSS for better styling
def load_css():
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stApp {
            background-color: #f8f9fa;
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        .stMetricValue {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .market-status {
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-weight: bold;
        }
        .market-open {
            background-color: #d4edda;
            color: #155724;
        }
        .market-closed {
            background-color: #f8d7da;
            color: #721c24;
        }
        </style>
    """)

def obter_cotacao(par_moedas):
    """Obtém cotação da API usando a chave armazenada em variável de ambiente"""
    api_key = os.getenv('OPENEXCHANGERATES_API_KEY')
    if not api_key:
        raise ValueError("API Key não encontrada nas variáveis de ambiente")
        
    base, quote = par_moedas.split('/')
    url = 'https://openexchangerates.org/api/latest.json'
    params = {
        'app_id': api_key,
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
    taxa_brl_usd = obter_cotacao('USD/BRL')
    risco_usd = risco_brl / taxa_brl_usd
    taxa_cambio = obter_cotacao(par_moedas)
    tamanho_lote = risco_usd / (pips / taxa_cambio)
    return tamanho_lote, risco_usd

def is_market_open():
    now = datetime.utcnow()
    if now.weekday() >= 5:  # Saturday or Sunday
        return False
    hour = now.hour
    return 22 <= hour <= 23 or 0 <= hour < 21

def main():
    # Page Configuration
    st.set_page_config(
        page_title="Calculadora Forex Pro",
        page_icon="💱",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load custom CSS
    load_css()

    # Header Section
    st.title("💱 Calculadora Forex Profissional")
    st.markdown("---")

    # Market Status Indicator
    market_status = is_market_open()
    status_col1, status_col2 = st.columns([3, 1])
    with status_col1:
        st.markdown("### Análise de Risco e Dimensionamento de Posição")
    with status_col2:
        if market_status:
            st.markdown('<p class="market-status market-open">Mercado Aberto</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="market-status market-closed">Mercado Fechado</p>', unsafe_allow_html=True)

    # Main Layout
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Parâmetros da Operação")
        
        risco_brl = st.number_input(
            "Risco em BRL 💰",
            min_value=0.0,
            step=10.0,
            value=100.0,
            help="Defina o valor máximo que está disposto a arriscar em Reais"
        )

        pares_disponiveis = ["EUR/USD", "GBP/USD", "USD/JPY", "USD/BRL", "EUR/BRL"]
        par_moedas = st.selectbox(
            "Par de Moedas 🔄",
            options=pares_disponiveis,
            help="Selecione o par de moedas para sua operação"
        )

        pips = st.number_input(
            "Stop Loss (em pips) 📏",
            min_value=0.0,
            step=1.0,
            value=50.0,
            help="Digite o tamanho do seu stop loss em pips"
        )

        calcular = st.button("Calcular Posição 🎯", use_container_width=True)

    with col2:
        st.markdown("### Resultados da Análise")
        
        if calcular:
            try:
                with st.spinner('Calculando...'):
                    pips_adjusted = pips * 1.20
                    tamanho_lote, risco_usd = calcular_lote_e_risco(risco_brl, par_moedas, pips_adjusted)

                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    
                    with metrics_col1:
                        st.metric(
                            "Tamanho do Lote",
                            f"{tamanho_lote:.2f}",
                            "Lote Padrão"
                        )
                    
                    with metrics_col2:
                        st.metric(
                            "Risco em USD",
                            f"${risco_usd:.2f}",
                            "Valor em Dólar"
                        )
                    
                    with metrics_col3:
                        st.metric(
                            "Risco em BRL",
                            f"R${risco_brl:.2f}",
                            "Valor em Real"
                        )

                    st.success("✅ Cálculos realizados com sucesso!")
                    
            except Exception as e:
                st.error(f"❌ Erro no cálculo: {str(e)}")
        else:
            st.info("👈 Configure os parâmetros e clique em 'Calcular Posição' para ver os resultados")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <small>Desenvolvido para Traders Profissionais • Atualizado em tempo real • Dados de mercado via OpenExchangeRates</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
