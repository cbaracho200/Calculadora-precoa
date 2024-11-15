import streamlit as st
import requests
from datetime import datetime
import os

# Configurações iniciais e constantes
API_KEY = st.secrets["OPENEXCHANGERATES_API_KEY"]

# Definição dos estilos em uma função separada
def local_css():
    st.markdown("""
        <style>
        /* Estilos para containers principais */
        .stApp {
            max-width: 100%;
            padding: 1rem;
        }
        
        /* Estilos para cartões/métricas */
        div.css-1r6slb0.e1tzin5v2 {
            background-color: #FFFFFF;
            border: 1px solid #EEEEEE;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Estilização dos botões */
        .stButton > button {
            width: 100%;
            background-color: #3498db;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: 500;
        }
        
        .stButton > button:hover {
            background-color: #2980b9;
        }
        
        /* Estilos para status do mercado */
        .market-status {
            padding: 8px 16px;
            border-radius: 5px;
            font-weight: 500;
            text-align: center;
            margin: 10px 0;
        }
        
        .market-open {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .market-closed {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        /* Estilos para inputs */
        .stNumberInput {
            margin-bottom: 1rem;
        }
        
        /* Estilos para títulos */
        h1, h2, h3 {
            color: #2c3e50;
            margin-bottom: 1rem;
        }
        
        /* Estilos para mensagens de erro/sucesso */
        .stAlert {
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Footer personalizado */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f8f9fa;
            padding: 1rem;
            text-align: center;
            border-top: 1px solid #dee2e6;
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            .stApp {
                padding: 0.5rem;
            }
            
            div.css-1r6slb0.e1tzin5v2 {
                padding: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def obter_cotacao(par_moedas):
    """
    Obtém cotação da API usando a chave armazenada nos secrets do Streamlit
    """
    try:
        base, quote = par_moedas.split('/')
        url = 'https://openexchangerates.org/api/latest.json'
        params = {
            'app_id': API_KEY,
            'base': 'USD',  # A versão gratuita só permite USD como base
            'symbols': f"{quote}"
        }

        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            st.error(f"Erro na API: {response.status_code} - {response.text}")
            return None

        data = response.json()
        
        # Se estamos convertendo de/para USD
        if base == 'USD':
            return data['rates'][quote]
        elif quote == 'USD':
            return 1 / data['rates'][base]
        else:
            # Para outros pares, precisamos fazer conversão cruzada
            usd_to_quote = data['rates'][quote]
            usd_to_base = data['rates'][base]
            return usd_to_quote / usd_to_base

    except Exception as e:
        st.error(f"Erro ao obter cotação: {str(e)}")
        return None

def calcular_lote_e_risco(risco_brl, par_moedas, pips):
    """
    Calcula o tamanho do lote e o risco com tratamento de erros melhorado
    """
    try:
        # Primeiro obtemos USD/BRL
        taxa_brl_usd = obter_cotacao('USD/BRL')
        if not taxa_brl_usd:
            return None, None

        risco_usd = risco_brl / taxa_brl_usd
        
        # Depois obtemos a cotação do par desejado
        taxa_cambio = obter_cotacao(par_moedas)
        if not taxa_cambio:
            return None, None

        # Cálculo do tamanho do lote
        tamanho_lote = risco_usd / (pips / taxa_cambio)
        
        return tamanho_lote, risco_usd

    except Exception as e:
        st.error(f"Erro no cálculo: {str(e)}")
        return None, None

def is_market_open():
    """
    Verifica se o mercado Forex está aberto
    """
    now = datetime.utcnow()
    if now.weekday() >= 5:  # Sábado ou Domingo
        return False
    hour = now.hour
    return 21 <= hour <= 23 or 0 <= hour < 20  # Horário de mercado em UTC

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Calculadora Forex Pro",
        page_icon="💱",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Carrega os estilos CSS
    local_css()

    # Cabeçalho
    st.title("💱 Calculadora Forex Profissional")
    
    # Status do Mercado
    market_status = is_market_open()
    status_text = "MERCADO ABERTO" if market_status else "MERCADO FECHADO"
    status_class = "market-open" if market_status else "market-closed"
    
    st.markdown(f"""
        <div class="market-status {status_class}">
            {status_text}
        </div>
    """, unsafe_allow_html=True)

    # Layout Principal
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

        pares_disponiveis = [
            "EUR/USD", "GBP/USD", "USD/JPY", "USD/BRL", "EUR/BRL",
            "GBP/BRL", "AUD/USD", "USD/CAD", "USD/CHF"
        ]
        
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

        calcular = st.button("Calcular Posição 🎯")

    with col2:
        st.markdown("### Resultados da Análise")
        
        if calcular:
            with st.spinner('Calculando posição...'):
                pips_adjusted = pips * 1.20  # Ajuste de 20% para segurança
                resultado = calcular_lote_e_risco(risco_brl, par_moedas, pips_adjusted)
                
                if resultado and None not in resultado:
                    tamanho_lote, risco_usd = resultado
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Tamanho do Lote",
                            f"{tamanho_lote:.2f}",
                            "Lotes"
                        )
                    
                    with col2:
                        st.metric(
                            "Risco em USD",
                            f"${risco_usd:.2f}",
                            "USD"
                        )
                    
                    with col3:
                        st.metric(
                            "Risco em BRL",
                            f"R${risco_brl:.2f}",
                            "BRL"
                        )
                    
                    st.success("✅ Cálculos realizados com sucesso!")
                else:
                    st.error("❌ Não foi possível realizar os cálculos. Verifique os dados inseridos.")
        else:
            st.info("👈 Configure os parâmetros e clique em 'Calcular Posição'")

    # Footer
    st.markdown("""
        <div class='footer'>
            <small>Desenvolvido para Traders Profissionais • Dados em Tempo Real • v1.0.0</small>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
