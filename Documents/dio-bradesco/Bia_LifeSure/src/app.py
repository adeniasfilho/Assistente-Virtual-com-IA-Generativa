import json
import pandas as pd
import requests
import streamlit as st 

#Carregar Dados
OLLAMA_URL="http://localhost:11434/api/generate"
MODELO="gpt-oss"
perfil_investidor=json.load(open('C:/Users/Adenias/Documents/dio-bradesco/Bia_LifeSure/data/perfil_investidor.json'))
transacoes=pd.read_csv('C:/Users/Adenias/Documents/dio-bradesco/Bia_LifeSure/data/transacoes.csv')
historico_atendimento=pd.read_csv('C:/Users/Adenias/Documents/dio-bradesco/Bia_LifeSure/data/historico_atendimento.csv')
renda_idade_4=pd.read_csv('C:/Users/Adenias/Documents/dio-bradesco/Bia_LifeSure/data/renda_idade_4.csv')
produtos_financeiros=json.load(open('C:/Users/Adenias/Documents/dio-bradesco/Bia_LifeSure/data/produtos_financeiros.json'))

#Montar Contexto
contexto=f"""
CLIENTE: {perfil_investidor['nome']}, {perfil_investidor['idade']} anos, perfil{perfil_investidor['perfil_investidor']}
OBJETIVO: {perfil_investidor['objetivo_principal']}
PATRIMONIO: R$ {perfil_investidor['patrimonio_total']} | RESERVA: R$ {perfil_investidor['reserva_emergencia_atual']}

TRANSAÇÕES ANTERIORES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico_atendimento.to_string(index=False)}

RENDA IDADE:
{renda_idade_4.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos_financeiros, indent=2, ensure_ascii=False)}

PERFIL INVESTIDOR:
{json.dumps(perfil_investidor, indent=2, ensure_ascii=False)}
"""
#System Prompt
SYSTEM_PROMPT= """"Você é Bia_LifeSure, Assistente Especialista em Seguros Bradesco / Proteção Financeira

OBJETIVO PRINCIPAL:
Ajudar o cliente a entender o valor estratégico do seguro como ferramenta de planejamento financeiro e proteção familiar, sem pressão comercial.

REGRAS:
INICIE sempre a interação com o usuário da seguinte forma: “Olá, meu nome é Bia Life Sure e meu propósito é te instruir sobre seguros e realizar uma simulação caso queira.”
O usuário responder “Sim, sim, yes, Yes” para simulação  fazer redirecionamento direto para o link https://www.bradescoseguros.com.br/clientes .
O usuário responder “Sim, sim, yes, Yes” para dúvidas de preenchimento de documentação, pergunte: “Qual é a sua dúvida?”.
Responda apenas com informações corretas e atualizadas.  
Se a pergunta for muito específica ou exigir cotação real, oriente o cliente a realizar simulação oficial junto à Bradesco Seguros / corretor / canal oficial com redirecionamento direto para o link https://www.bradescoseguros.com.br/clientes .
Se a pergunta for muito específica ou exigir explicação sobre custos futuros, oriente o cliente a realizar simulação oficial junto à Bradesco Seguros / corretor / canal oficial com redirecionamento direto para o link https://www.bradescoseguros.com.br/clientes/produtos/previdencia-privada .
NUNCA invente valores exatos de prêmio sem dados completos do perfil.  
NUNCA incentive omissão ou fraude na DPS – isso pode invalidar a apólice e gerar ações judiciais.
Responda a pergunta de forma sucinta, direta e com exemplos, com no máximo três(3)parágrafos.
Não encontrado dados na base de conhecimento para resposta, responda: “Não possuo esta informação; encaminharei você ao site do Bradesco Seguros - Clube de Vantagens redirecionamento direto para o link https://www.bradescoseguros.com.br/clientes .
O usuário responder "Não,não,No,no realizar uma simulação, contratação de seguro de vida, residencial, viagem, capitalização ou dental, responda: “Foi uma experiência rica com você e tenha um excelente dia e semana!”.

Agora responda à pergunta ou necessidade do cliente seguindo rigorosamente o estilo e a estrutura acima.
"""
#Chamar OLLAMA
def perguntar(msg):
    prompt=f"""
    {SYSTEM_PROMPT}
    
    CONTEXTO DO CLIENTE:
    {contexto}
    
    Pergunta: {msg} """
    r=requests.post(OLLAMA_URL, json={"model":MODELO, "prompt":prompt, "steam":False})
    return r.json()['response']

#Interface
st.title("Bia_LifeSure, Assistente Especialista em Seguros Bradesco / Proteção Financeira!")
if pergunta := st.chat_input("Sua dúvida sobre seguros..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))


