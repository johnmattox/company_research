# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 18:33:20 2019

@author: johnm
"""

import pandas as pd
import numpy as np

def concatena_cols_df(df,cols):
    df = df.copy()
    df['dummy_col'] = 0
    for col in cols:
        df['dummy_col'] = df['dummy_col'] + df[col].fillna(0)
    return df['dummy_col']

# Consolida DRE

df_DRE = pd.read_csv('historic_data/historico_DRE.csv',sep=';',encoding='latin-1')
df_DRE.columns = [k.strip() for k in df_DRE.columns]

dict_cols = {'1 - Receita bruta':['receita bruta de vendas e ou serviços','receitas da intermediação financeira'],
             '2 - Deduções sobre receita bruta':['deduções da receita bruta'],
             '3 - Receita líquida':['receita líquida de vendas e ou serviços'],
             '4 - Custo de mercadorias e serviços vendidos (CMV)':['custo de bens e ou serviços vendidos',
                                                                   'despesas da intermediação financeira'],
             '5 - Resultado bruto':['resultado bruto','resultado bruto intermediação financeira'],
             '6 - Despesas com vendas':['despesas com vendas'],
             '7.1 - Receitas operacionais':['outras receitas operacionais','receitas',
                                            'outras despesas receitas operacionais',
                                            'receitas de prestação de serviços'],
             '7.2 - Despesas gerais, administrativas e de pessoal':['despesas gerais e administrativas',
                                                                    'perdas pela não recuperabilidade de ativos',
                                                                    'despesas', 'despesas de pessoal',
                                                                    'despesas tributárias','outras despesas operacionais',
                                                                    'outras despesas administrativas'],
             '8 - EBITDA':[],
             '9 - Depreciações e amortizações':[],
             '10 - EBIT':[],
             '11.1 - Receitas financeiras':['receitas financeiras'],
             '11.2 - Despesas financeiras':['despesas financeiras'],
             '12 - EBT':['resultado antes tributação participações'],
             '13.1 - IR e taxas':['provisão para ir e contribuição social'],
             '13.2 - Restituição de IR e taxas':['ir diferido'],
             '14 - Participação de acionistas':['part. de acionistas não controladores',
                                                'participações contribuições estatutárias',
                                                'reversão dos juros sobre capital próprio'],
             '15 - Resultado do período':['lucro prejuízo do período']
            }
vars_consolidacao_originais_base = ['resultado bruto','resultado da equivalência patrimonial','financeiras',
                                    'resultado não operacional','resultado antes tributação participações',
                                    'lucro prejuízo do período','resultado bruto intermediação financeira',
                                    'resultado operacional']

df_DRE_simp = df_DRE[['safra','ticker']].copy()
for lin in dict_cols.keys():
    if '3 - ' in lin:
        df_DRE_simp[lin] = concatena_cols_df(df_DRE,dict_cols[lin])
        df_DRE_simp[lin] = [l1 - l2 if l3==0 else l3 for (l1,l2,l3) in zip(df_DRE_simp['1 - Receita bruta'],\
                                                                           df_DRE_simp['2 - Deduções sobre receita bruta'],\
                                                                           df_DRE_simp['3 - Receita líquida'])]
    elif '5 - ' in lin and 'bruto' in lin:
        df_DRE_simp[lin] = df_DRE_simp['3 - Receita líquida'] + \
        df_DRE_simp['4 - Custo de mercadorias e serviços vendidos (CMV)']
    elif '8 - ' in lin:
        df_DRE_simp[lin] = df_DRE_simp['5 - Resultado bruto'] + df_DRE_simp['6 - Despesas com vendas'] \
        + df_DRE_simp['7.1 - Receitas operacionais'] + df_DRE_simp['7.2 - Despesas gerais, administrativas e de pessoal']
    elif '9 - ' in lin:
        df_DRE_simp[lin] = 0
    elif '10 - ' in lin:
        df_DRE_simp[lin] = df_DRE_simp['8 - EBITDA'] + df_DRE_simp['9 - Depreciações e amortizações']
    elif '12 - ' in lin:
        df_DRE_simp[lin] = df_DRE_simp['10 - EBIT'] + df_DRE_simp['11.2 - Despesas financeiras'] \
        + df_DRE_simp['11.1 - Receitas financeiras']
    elif '15 - ' in lin:
        df_DRE_simp[lin] = df_DRE_simp['12 - EBT'] + df_DRE_simp['13.1 - IR e taxas'] + \
        df_DRE_simp['13.2 - Restituição de IR e taxas'] + df_DRE_simp['14 - Participação de acionistas']
    else:
        df_DRE_simp[lin] = concatena_cols_df(df_DRE,dict_cols[lin])
        
df_DRE.to_csv('historic_data/DRE_consolidado.csv',sep=';',encoding='latin-1',index=False)
        
# Consolida BP
        
df_BP = pd.read_csv('historic_data/historico_balanco_patrimonial.csv',sep=';',encoding='latin-1')
df_BP.columns = [k.strip() for k in df_BP.columns]

dict_cols_BP = {'Ativo Circulante':{'Caixa Equivalentes e Disponibilidades':
                                    ['ativo - caixa e equivalentes de caixa',
                                     'ativo - aplicações financeiras',
                                     'ativo - aplicações interfinanceiras de liquidez',
                                     'ativo - disponibilidades'],
                                    'Estoques':['ativo - estoques'],
                                    'Títulos e Valores Mobiliários':['ativo - títulos e valores mobiliários'],
                                    'Contas a receber arrendamentos e biologicos':['ativo - contas a receber',
                                                                                   'ativo - operações de arrendamento mercantil',
                                                                                   'ativo - ativos biológicos',
                                                                                   'ativo - relações interdependências',
                                                                                   'ativo - relações interfinanceiras'
                                                                                  ],
                                    'Operacoes de credito':['ativo - operações de crédito',
                                                            'ativo - outros créditos'],
                                    'Despesas antecipadas':['ativo - despesas antecipadas'],
                                    'Taxas e tributos a recuperar':['ativo - tributos a recuperar'],
                                    'Outros ativos circulantes':['ativo - outros ativos circulantes',
                                                                 'ativo - outros valores e bens'],
                                   },
#                 'Ativo Nao Circulante':{'ativo nao circulante summary':['ativo total','ativo - ativo total','Ativo Circulante']},
                'Ativo Nao Circulante granulares':{'Aplicacoes financeiras amortizadas':['ativo - aplicações financeiras avaliadas ao custo amortizado',
                                                                              'ativo - contas a receber 1',
                                                                              'ativo - aplicações financeiras avaliadas a valor justo',
                                                                              'ativo - aplicações interfinanceiras de liquidez 1'],
                                        'Estoques a comercializar e arrendamentos':['ativo - estoques 1',
                                                                                    'ativo - operações de arrendamento mercantil 1'],
                                        'Despesas antecipadas':['ativo - despesas antecipadas 1'],
                                        'Tributos diferidos':['ativo - tributos diferidos'],
                                        'Investimentos e operacoes de credito':['ativo - investimentos',
                                                                                'ativo - operações de crédito 1'],
                                        'Títulos e valores mobiliários':['ativo - títulos e valores mobiliários 1'],
                                        'Outros ativos nao circulantes':['ativo - outros ativos não circulantes',
                                                                         'ativo - ativo permanente',
                                                                         'ativo - ativo realizável a longo prazo',
                                                                         'ativo - ativos biológicos 1',
                                                                         'ativo - outros créditos 1',
                                                                         'ativo - outros valores e bens 1',
                                                                         'ativo - relações interdependências 1',
                                                                         'ativo - relações interfinanceiras 1'],
                                        'Imobilizado':['ativo - imobilizado'],
                                        'Intangível':['ativo - intangível']
                },
                'Passivo Circulante':{'Emprestimos e financiamentos':['passivo - empréstimos e financiamentos'],
                                      'Recebíveis de fornecedores':['passivo - fornecedores'],
                                      'Obrig. sociais e trabalhistas':['passivo - obrigações sociais e trabalhistas'],
                                      'Captações no Mercado Aberto e depósitos':['passivo - captações no mercado aberto',
                                                                                 'passivo - depósitos'],
                                      'Recursos de aceites cambiais':['passivo - recursos de aceites e emissão de títulos'],
                                      'Relações interdependencias e interfinanceiras':['passivo - relações interdependências',
                                                                                       'passivo - relações interfinanceiras'],
                                      'Passivos sobre ativos a venda':['passivo - passivos sobre ativos não-correntes a venda e descontinuados'],
                                      'Provisoes':['passivo - provisões'],
                                      'Lucros nao distribuídos':['passivo - dividendos e jcp a pagar'],
                                      'Obrigacoes fiscais': ['passivo - obrigações fiscais'],
                                      'Obrigacoes por emprestimos e repasses':['passivo - obrigações por empréstimos',
                                                                               'passivo - obrigações por repasse do exterior',
                                                                               'passivo - obrigações por repasse do país'],
                                      'Outros passivos circulantes':['passivo - outros',
                                                                     'passivo - outras obrigações']
                },
                'Passivo Nao Circulante':{'Emprestimos e financiamentos':['passivo - empréstimos e financiamentos 1'],
                                          'Captações no Mercado Aberto e depósitos':['passivo - captações no mercado aberto 1',
                                                                                     'passivo - depósitos 1',
                                                                                     'passivo - passivo exigível a longo prazo'],
                                          'Provisoes para contingencias':['passivo - provisões 1'],
                                          'Receitas Diferidas':['passivo - lucros e receitas a apropriar'],
                                          'Recursos de aceites cambiais':['passivo - recursos de aceites e emissão de títulos 1'],
                                          'Relações interdependencias e interfinanceiras':['passivo - relações interdependências 1',
                                                                                           'passivo - relações interfinanceiras 1'],
                                          'Obrigacoes por emprestimos e repasses':['passivo - obrigações por empréstimos 1',
                                                                                   'passivo - obrigações por repasse do exterior 1',
                                                                                   'passivo - obrigações por repasse do país 1'],
                                          'Passivos sobre ativos a venda':['passivo - passivos sobre ativos não-correntes a venda e descontinuados 1'],
                                          'Provisoes para aumento de capital':['passivo - adiantamento para futuro aumento capital'],
                                          'Tributos diferidos':['passivo - tributos diferidos'],
                                          'Outros passivos nao circulantes':['passivo - outros 1',
                                                                             'passivo - outras obrigações 1'],
                                          'Resultados de exercicios futuros':['passivo - resultados de exercícios futuros']
                },
                'Patrimonio Liquido':{'Capital social':['pl - capital social realizado'],
                                      'Particip. acionaistas nao controladores':['passivo - participação dos acionistas não controladores'],
                                      'Reserva para aumento de capital':['pl - adiantamento para futuro aumento capital'],
                                      'Ajustes de PL':['pl - ajustes acumulados de conversão',
                                                       'pl - ajustes de avaliação patrimonial'],
                                      'Reserva de capital':['pl - reservas'],
                                      'Reserva de lucros':['pl - lucros ou prejuízos acumulados'],
                                      'Outros resultados':['pl - outros resultados abrangentes']
                }
    
}

vars_desconsiderar_bp = ['ativo - ativo circulante','ativo - diferido','passivo total','passivo - passivo circulante',
                         'passivo - passivo não circulante','patrimônio líquido']

df_BP_concat = df_BP[['ticker','safra']].copy()
df_BP_concat['ativo total tabela'] = df_BP[['ativo total','ativo - ativo total']].sum(axis=1)
df_BP_concat['passivo total tabela'] = df_BP['passivo total']
df_BP_concat['patrimônio líquido tabela'] = df_BP['patrimônio líquido']
for k in dict_cols_BP.keys():
    sigla = 'PL'
    if k != 'Patrimonio Liquido':
        sigla = ''
        if 'Ativo' in k:
            sigla+='A'
        else:
            sigla+='P'
            
        if 'Nao' in k:
            sigla+='NC'
        else:
            sigla+='C'
    
    for sk in dict_cols_BP[k].keys():
        df_BP_concat['%s - %s'%(sigla,sk)] = df_BP[dict_cols_BP[k][sk]].sum(axis=1)
        
df_BP_concat.to_csv('historic_data/BP_consolidado.csv',sep=';',encoding='latin-1',index=False)