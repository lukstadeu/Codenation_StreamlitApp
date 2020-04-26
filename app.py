import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib as plt


def carrega_dados():

    st.subheader('Faça o upload do arquivo com o dataset(csv) a ser analisado')
     
    arq = st.file_uploader('Escolha o arquivo:',type = 'csv')

    if arq is not None:
        df = pd.read_csv(arq,index_col = False)         
        return df       
    

def exibir_informacoes_basicas(df):
    st.subheader('Conhecendo o dataset:')

    st.write('O arquivo .csv importado possui ', df.shape[0], 'linhas e ', df.shape[1], ' colunas.')

    variaveis_selecionadas = st.multiselect('Variáveis disponíveis para visualização', list(df.columns.sort_values()), default=list(df.columns.sort_values()))


    qtd_linhas = st.slider('Escolha a quantidade linhas a serem exibidas.', min_value=2, max_value=df.shape[0])

    st.write('Exibindo ',qtd_linhas,' linhas do dataset:')
    st.dataframe(df[variaveis_selecionadas].head(qtd_linhas ))

    

    st.write("""
    Referente a qualidade dos dados, um importante fator a ser analisado é quantidade de valores ausentes no dataset. 
    \nÉ importante realizar algum tipo de tratamento sobre os valores ausentes, pois informações ausentes podem impactar modelos de Machine Learning.
    \nAlguns dos tratamentos mais comumente utilizados são: a inserção da média; mediana;moda dos valores ou até mesmo exclusão da coluna, entre outros.
    \nO tipo de tratamento a ser aplicado depende da analíse do problema para ver o que faz mas sentido.
    """ )

    st.write("Segue abaixo uma visão dos tipos das variáveis e também dos valores ausentes:")
    st.write(pd.DataFrame({'Tipo' : df.dtypes, '# Valores ausentes': df.isna().sum(), '% Valores ausentes' : (df.isna().sum() / df.shape[0]) * 100}))


def exibir_informacoes_variaveis_numericas(numericas,n):
    st.subheader('Variáveis numéricas')

    st.write("""
    Para as variáveis numéricas podemos obter também outras informações interesantes, como média, mediana, valor máximo e mínimo.
    \nPara o dataset atual temos """, n,"""variáveis numéricas presentes no dataset e seguem abaixo as informações sobre elas.
    """)

    st.write(pd.DataFrame({ 'Média' : numericas.mean(), 'Mediana': numericas.median(), 'Valor máximo' : numericas.max(), 'Valor mínimo' : numericas.min() }))


def exibir_informacoes_variaveis_categoricas(categoricas,n):
    st.subheader('Variáveis categóricas')

    
    st.write("""
    Em Data Science as variáveis categóricas são dados que demandam atenção quando pensamos em implementar modelos de Machine Learning.
    \n Os algoritmos mais conhecidos de Machine Learning utilizam dados numéricos, então variáveis categóricas (não-numéricas) precisam ser analisadas e tratadas conforme a necessidade
    necessidade do modelo a ser implementado.
    """)

    st.write('Para o dataset atual temos ', n, ' variáveis categóricas e podemos obter a Moda (valor mais frequente) para cada uma delas.')

    st.write('Selecione as variáveis que você deseja ver a moda:')

    variaveis_selecionadas = st.multiselect('Variáveis disponíveis:', list(categoricas.columns), default=list(categoricas.columns))

    st.write(categoricas[variaveis_selecionadas].mode())


def exibir_correlacao(numericas):
    st.subheader('Correlação entre as variáveis')

    st.write("""
    A correlação entre as vavriáveis é medida através do coeficiente de correlação e o coeficiente de variação nos demonstra como
    uma variável se comporta em um cenário que outra variável está variando, tentando identificar se a variação de ambas possuem relação.

    \n\n Abaixo seguem os 3 métodos mais conhecidos para o cálculo do coeficente de correlação:

    - Pearson
    - Spearman
    - Kendall """)

    st.write(""" No [link](https://pt.wikipedia.org/wiki/Correla%C3%A7%C3%A3o) podemos verificar mais informações sobre o uso de cada um dos coeficientes.

    \nEscolha as variáveis que deseja verificar a correlação. """)

    
    variaveis_selecionadas = st.multiselect('Variáveis disponíveis:', list(numericas.columns), default=list(numericas.columns))
   
    metodo_selecionado = st.radio('Selecione o método para cálculo da correção', ('Pearson','Spearman','Kendall'))


    if (variaveis_selecionadas)== 0:
        variaveis_selecionadas = list(numericas.columns)


    # Tratamento no nome do método selecionado, pois para o parâmetro precisa ser passado com todas letras minúsculas
    corr = numericas[variaveis_selecionadas].corr(method = metodo_selecionado[0].lower() + metodo_selecionado[1:])
    
    st.write('Correlação', metodo_selecionado.capitalize())
    st.write(corr)


    st.write('Finalizando, podemos ver um HeatMap das correlações para facilitar a visualização.')

    sns.heatmap(corr, cmap='bwr', fmt='.2f', square=True, linecolor='white', annot=True)
    st.pyplot()
    
def about():

    st.write(""" \n\n\n Linkedin: https://www.linkedin.com/in/lucastr/
    \nGitHub: https://github.com/lukstadeu
    \n\n Abril\\2020 """)



def main():

    st.header('Análise Inicial do Dataset')

    st.image('./images/ds_imagem.jpeg')

    st.write("""Esta é uma pequena demonstração das funcionalidades presentes no [Streamlit](https://www.streamlit.io/) que é um framework que facilita a construção de data apps. """)
    
    
    dados = carrega_dados()

    if dados is not None:

        exibir_informacoes_basicas(dados)

        variaveis_numericas = list(dados.select_dtypes(include=['int64','float64']))
        qtd_variaveis_numericas = len(variaveis_numericas)

        if qtd_variaveis_numericas > 0: 
            exibir_informacoes_variaveis_numericas(dados[variaveis_numericas],qtd_variaveis_numericas)

        variaveis_categoricas = list(dados.select_dtypes(include=['object']))
        qtd_variaveis_categoricas= len(variaveis_categoricas)

        if qtd_variaveis_categoricas > 0: 
            exibir_informacoes_variaveis_categoricas(dados[variaveis_categoricas],qtd_variaveis_categoricas)

        exibir_correlacao(dados[variaveis_numericas])

        
    about()


if __name__ == '__main__':
	main()
