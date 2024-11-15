# Calculadora Forex Pro

Uma calculadora profissional para traders do mercado Forex, que permite calcular tamanhos de lote e gerenciar riscos de forma eficiente.

## 🚀 Recursos

- Cálculo automático de tamanho de lote
- Gerenciamento de risco em tempo real
- Suporte a múltiplos pares de moedas
- Interface profissional e intuitiva
- Indicador de status do mercado

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta na OpenExchangeRates para API Key

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://seu-repositorio/calculadora-forex-pro.git
cd calculadora-forex-pro
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```
OPENEXCHANGERATES_API_KEY=sua_api_key_aqui
```

## 🖥️ Execução Local

Para executar a aplicação localmente:

```bash
streamlit run app.py
```

## 🚀 Deploy

Para fazer deploy no Streamlit Cloud:

1. Faça push do código para seu repositório GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório
4. Configure as variáveis de ambiente no Streamlit Cloud:
   - OPENEXCHANGERATES_API_KEY

## 📝 Configuração das Variáveis de Ambiente no Streamlit Cloud

1. Acesse as configurações do seu app no Streamlit Cloud
2. Vá para a seção "Secrets"
3. Adicione sua API key no formato:
```toml
OPENEXCHANGERATES_API_KEY = "sua_api_key_aqui"
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
