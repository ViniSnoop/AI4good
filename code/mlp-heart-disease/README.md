# MLP Heart Disease
> Classificação de risco de doença cardíaca com Multilayer Perceptron implementada do zero em Python e visualizador interativo em Streamlit.

## O que faz
- **MLP do zero**: Implementação pura com NumPy de forward propagation e backpropagation com Binary Cross-Entropy e ativação Sigmoid.
- **Balanceamento de classes**: Técnica de oversampling (50/50) para balancear as classes no conjunto de treino.
- **Visualizador Streamlit**: Interface interativa para inspeção passo a passo:
  - Topologia da rede com pesos e ativações por neurônio por época.
  - Curvas de treinamento de Loss (BCE) e Acurácia.
  - Heatmaps das matrizes de pesos e normas de gradientes.

## Como Executar
```bash
# Ativar venv e executar a aplicação Streamlit
streamlit run mlp_heart_disease.py
```
