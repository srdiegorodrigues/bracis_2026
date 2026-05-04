# Comparing Explicability Frameworks for Accident Severity Prediction

Repositório do artigo submetido ao **BRACIS 2026**, que compara os frameworks de explicabilidade **SHAP** e **Efeitos Marginais Médios (AMEs)** aplicados à predição de gravidade de sinistros em rodovias federais brasileiras.

---

## Visão Geral

O objetivo central não é maximizar acurácia preditiva, mas investigar a **estabilidade e consistência** das variáveis explicativas entre diferentes paradigmas de modelagem — estatístico paramétrico (Regressão Logística + AMEs) e aprendizado de máquina (Random Forest e CatBoost + SHAP).

---

## Estrutura do Projeto

```
.
├── .gitattributes
├── .gitignore
├── README.md
│
└── notebooks/
    ├── models/                       # Modelos de aprendizado de máquina
    │   ├── logit_ame.ipynb           # Regressão Logística + AMEs
    │   ├── randomforest_shap.ipynb   # Random Forest + SHAP (TreeSHAP)
    │   └── catboost_shap.ipynb       # CatBoost + SHAP (TreeSHAP)
    │
    └── treatments/                   # Tratamento e preparação dos dados
```

---

## Dados

### Fonte

Registros abertos de sinistros de trânsito da **Polícia Rodoviária Federal (PRF)**, disponíveis no portal de dados abertos do governo federal, cobrindo o período de **2017 a 2025**.

- **Forma bruta:** 4.069.582 registros × 37 atributos
- **Após concatenação e deduplicação** (remoção de `pesid` duplicados): 632.618 registros
- **Base final** (após remoção de nulos e registros fora do território brasileiro): **631.157 registros × 22 atributos explicativos + variável-alvo**

### Variável-alvo

`grave` — binária: `1` = sinistro grave (com vítima fatal ou ferida grave), `0` = não grave.

Distribuição: **86,9% não graves** (548.510) | **13,1% graves** (82.647) — base desbalanceada.

---

## Pipeline de Dados

### 1. Concatenação e Limpeza

- Concatenação dos arquivos anuais (2017–2025)
- Remoção de registros duplicados por `pesid` (mantido apenas o primeiro)
- Padronização de nomes de atributos (remoção de espaços, acentuação e caracteres especiais)
- Exclusão de registros com coordenadas geográficas fora dos limites do Brasil

### 2. Engenharia de Atributos

Novos atributos derivados criados a partir da base bruta:

| Atributo | Descrição | Origem |
|---|---|---|
| `vel_max` | Velocidade máxima permitida (CTB, Art. 61) | Engenharia |
| `distancia_radar_m` | Distância geodésica ao radar de velocidade mais próximo (m) | DNIT + GeoPandas |
| `frequencia` | Frequência histórica de sinistros por km de rodovia | Calculado sobre a base PRF |
| `uf_br_km` | Concatenação de UF + rodovia federal + quilômetro | Engenharia |
| `turno` | Período do dia: Madrugada / Manhã / Tarde / Noite | Derivado de `horario` |
| `feriado` | Proximidade em dias ao feriado mais próximo | Biblioteca `holidays` (Python) |
| `pista_molhada` | Indica presença de umidade na via | Derivado de `condicao_metereologica` |
| `visibilidade_ruim` | Indica condições adversas de visibilidade | Derivado de `condicao_metereologica` |
| `condicao_ignorada` | Indica registros com valor "Ignorado" na condição meteorológica | Derivado de `condicao_metereologica` |
| `intersecao_de_vias`, `reta`, `declive` | Variáveis binárias de traçado viário | Derivado de `tracado_via` |

### 3. Codificação e Normalização

O pipeline foi estruturado em três etapas sequenciais:

**Etapa 1 — Variáveis cíclicas (sin/cos encoding):**
Variáveis temporais com periodicidade natural (`turno`, `dia_semana`, `mes`) foram transformadas em pares seno/cosseno, preservando a continuidade do ciclo sem introduzir ordem artificial. Resultado: 6 colunas (`turno_sin`, `turno_cos`, `dia_semana_sin`, `dia_semana_cos`, `mes_sin`, `mes_cos`).

**Etapa 2 — Variável categórica de alta cardinalidade (`uf_br_km`):**
Aplicação de **Target Encoding com suavização bayesiana** (`smoothing=10`), ajustado exclusivamente sobre o conjunto de treinamento para evitar data leakage.

**Etapa 3 — Variáveis numéricas contínuas:**
`vel_max`, `distancia_radar_m` e `frequencia` normalizadas com **MinMaxScaler** para o intervalo `[0, 1]`, com scaler ajustado apenas no treino.

### 4. Divisão Temporal

| Conjunto | Período | Registros |
|---|---|---|
| Treino | 2017–2024 | 558.847 |
| Teste | 2025 | 72.310 |

A divisão temporal preserva a ordem cronológica dos eventos, evita vazamento de informação futura e fornece avaliação mais realista em séries temporais.

---

## Modelos

### Regressão Logística — `logit_ame.ipynb`

- Implementação via `statsmodels`
- Adicionada constante (`add_constant`)
- Desbalanceamento tratado por **ponderação de classes** (peso inversamente proporcional à frequência)
- Interpretabilidade via **Efeitos Marginais Médios (AME)**:

$$AME_k = E\left[\frac{\partial P(Y=1 \mid X)}{\partial x_k}\right]$$

- **Métricas (teste 2025):** Accuracy 0.851 | AUC 0.586

### Random Forest — `randomforest_shap.ipynb`

- `RandomForestClassifier` do `scikit-learn`
- Configuração: `n_estimators=300`, `max_depth=8`, `min_samples_leaf=50`, `class_weight="balanced"`, `random_state=42`
- Interpretabilidade via **TreeSHAP** (`output_type="probability"`)
- Análise de variáveis cíclicas com recombinação sin/cos dos valores SHAP
- **Métricas (teste 2025):** Accuracy 0.627 | AUC 0.574

### CatBoost — `catboost_shap.ipynb`

- `CatBoostClassifier` com tratamento nativo de variáveis categóricas
- Configuração moderada e padronizada, sem otimização exaustiva de hiperparâmetros
- Interpretabilidade via **TreeSHAP** (`output_type="probability"`)
- `RANDOM_STATE = 42` em todos os modelos para reprodutibilidade
- **Métricas (teste 2025):** AUC ≈ 0.58

> Configurações moderadas foram adotadas intencionalmente em vez de otimização exaustiva, em linha com o objetivo explicativo do estudo (garantir comparabilidade e estabilidade das interpretações).

---

## Métricas de Explicabilidade Comparadas

Para cada variável `k`, dois agregados globais são extraídos e comparados entre SHAP e AME:

- **Efeito médio com sinal** — `E[φ_k]` (SHAP) / `AME_k`: direção do efeito sobre a probabilidade de gravidade
- **Importância absoluta** — `E[|φ_k|]` (SHAP) / `|AME_k|`: magnitude do efeito para ranqueamento

As comparações focam em **sinal e posição relativa de ranking**, e não em magnitudes absolutas (que diferem por construção matemática entre os dois frameworks).

---

## Principais Resultados

- **Núcleo estável** (consistente nos três modelos e em ambos os frameworks): `uf_br_km`, `vel_max`, `frequencia`
- **Periferia volátil** (comportamento modelo-específico): `turno`, `tipo_pista`, `distancia_radar_m`, `pista_molhada`
- **AUC ≈ 0.58** nos três modelos confirma teto preditivo estrutural dos dados administrativos da PRF
- A divergência de sinal em `distancia_radar_m` entre SHAP (modelos de árvore) e AME (logística) é um achado central: indica que o efeito da fiscalização eletrônica é contextual e heterogêneo

---

## Dependências Principais

```
pandas
numpy
scikit-learn
statsmodels
catboost
shap
geopandas
matplotlib
holidays
```

---

## Reprodutibilidade

Todos os modelos utilizam `RANDOM_STATE = 42`. O pipeline de pré-processamento (scaler e encoder) é ajustado exclusivamente sobre o conjunto de treino e aplicado por transformação ao conjunto de teste, garantindo integridade da avaliação temporal.
