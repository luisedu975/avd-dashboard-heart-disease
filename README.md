# Dashboards Heart Disease (UCI)

Aplicação em Streamlit com dois dashboards, construída a partir da minha EDA do dataset Heart Disease (UCI id=45, Cleveland).

🔗 **App publicado:** https://SEU-APP.streamlit.app

## Dashboards
- **Laboratório:** mapa de calor de correlação e histogramas por variável quantitativa, com filtros de variáveis, idade e colesterol no painel lateral.
- **KPIs Clínicos:** métricas e gráficos voltados a um cardiologista na triagem de pacientes (prevalência, idade, frequência cardíaca máxima, colesterol, taxa de doença por tipo de dor, faixa etária e sexo).

## Estrutura
- `app.py`: aplicação Streamlit
- `data/`: dataset (`heart_disease.csv`)
- `notebooks/`: EDA
- `entregas/`: rascunhos dos dashboards e declaração de uso de IA
- `prompts/`: prompts utilizados

## Como rodar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Autor
Luis Eduardo - CESAR School