## Basic Information About the Incidents

- **Years:** 2017 to 2025
- **Total records before initial processing:** 4,069,582
- **Number of attributes:** 37

## File Repository

- [Radars](https://dados.gov.br/dados/conjuntos-dados/radar)
- [Incidents on Brazilian Federal Highways](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf)
  - [Data dictionary](https://drive.google.com/file/d/11xcaEgl1hpyfl2hnlFaa0MsxERd6uaKF/view)

### Repository Directory Structure

**`database/`**
Directory for storing the datasets used in the experiments. Includes raw data and, where applicable, intermediate or already-processed versions. This separation ensures reproducibility and traceability of transformations throughout the analysis pipeline. It contains the following subfolders (omitted due to storage limitations):

- **`datasets_originais/`**: contains the original traffic incident datasets covering the period from 2017 to 2025. These data are kept in their raw form, without any processing, ensuring traceability and reproducibility of the analyses.
- **`security/`**: directory for storing backup copies generated during experimental cleaning and transformation steps. Its purpose is to preserve intermediate versions, allowing recovery in case of inconsistencies or the need to audit the process.

**`notebooks/`**
Contains notebooks developed throughout the project, organized according to their purpose in the data science workflow.

**`notebooks/models/`**
Gathers notebooks focused on predictive modeling. Includes steps such as final data preparation for modeling, training of machine learning algorithms, hyperparameter tuning, and model performance evaluation.

**`notebooks/treatments/`**
Contains notebooks related to data preprocessing and exploratory analysis. Covers activities such as cleaning, transformation, feature engineering, and descriptive statistical analysis, forming the foundation for the modeling stage.

**`utils/`**
Directory containing implementations of auxiliary algorithms for data processing and normalization. Although these methods were developed within the project's context, they were not used in the final version of the experiments presented. They are nevertheless kept in the repository for documentation purposes, potential reuse, and methodological transparency.

---

### Attribute List and Types

Data columns (total 37 columns):

| ID | Attribute                | Type    |
|----|--------------------------|---------|
| 0  | id                       | float64 |
| 1  | pesid                    | float64 |
| 2  | data_inversa             | object  |
| 3  | dia_semana               | object  |
| 4  | horario                  | object  |
| 5  | uf                       | object  |
| 6  | br                       | float64 |
| 7  | km                       | object  |
| 8  | municipio                | object  |
| 9  | causa_principal          | object  |
| 10 | causa_acidente           | object  |
| 11 | ordem_tipo_acidente      | int64   |
| 12 | tipo_acidente            | object  |
| 13 | classificacao_acidente   | object  |
| 14 | fase_dia                 | object  |
| 15 | sentido_via              | object  |
| 16 | condicao_metereologica   | object  |
| 17 | tipo_pista               | object  |
| 18 | tracado_via              | object  |
| 19 | uso_solo                 | object  |
| 20 | id_veiculo               | float64 |
| 21 | tipo_veiculo             | object  |
| 22 | marca                    | object  |
| 23 | ano_fabricacao_veiculo   | float64 |
| 24 | tipo_envolvido           | object  |
| 25 | estado_fisico            | object  |
| 26 | idade                    | float64 |
| 27 | sexo                     | object  |
| 28 | ilesos                   | float64 |
| 29 | feridos_leves            | float64 |
| 30 | feridos_graves           | float64 |
| 31 | mortos                   | float64 |
| 32 | latitude                 | object  |
| 33 | longitude                | object  |
| 34 | regional                 | object  |
| 35 | delegacia                | object  |
| 36 | uop                      | object  |

Dataset after removing records with duplicate `pesid` values: **632,618 records**

---

### Null Records per Attribute

| Variable                  | Missing Values |
|---------------------------|----------------|
| id                        | 0              |
| pesid                     | 28,286         |
| data_inversa              | 0              |
| dia_semana                | 0              |
| horario                   | 0              |
| uf                        | 0              |
| br                        | 1,404          |
| km                        | 1,404          |
| municipio                 | 0              |
| causa_principal           | 0              |
| causa_acidente            | 0              |
| ordem_tipo_acidente       | 0              |
| tipo_acidente             | 41             |
| classificacao_acidente    | 10             |
| fase_dia                  | 0              |
| sentido_via               | 0              |
| condicao_metereologica    | 0              |
| tipo_pista                | 0              |
| tracado_via               | 0              |
| uso_solo                  | 0              |
| id_veiculo                | 14             |
| tipo_veiculo              | 14             |
| marca                     | 0              |
| ano_fabricacao_veiculo    | 14             |
| tipo_envolvido            | 28,286         |
| estado_fisico             | 28,286         |
| idade                     | 79,822         |
| sexo                      | 28,286         |
| ilesos                    | 28,286         |
| feridos_leves             | 28,286         |
| feridos_graves            | 28,286         |
| mortos                    | 28,286         |
| latitude                  | 0              |
| longitude                 | 0              |
| regional                  | 31             |
| delegacia                 | 239            |
| uop                       | 436            |

---

### General Data

| Year | Records | With Injured Victims | No Victims | With Fatal Victims |
|------|---------|----------------------|------------|--------------------|
| 2017 | 89,567  | 53,699               | 30,683     | 5,184              |
| 2018 | 69,333  | 49,571               | 15,253     | 4,508              |
| 2019 | 67,558  | 51,275               | 11,683     | 4,599              |
| 2020 | 63,586  | 47,457               | 11,602     | 4,525              |
| 2021 | 64,567  | 47,457               | 11,602     | 4,525              |
| 2022 | 64,607  | 48,436               | 11,506     | 4,664              |
| 2023 | 67,767  | 51,945               | 10,963     | 4,858              |
| 2024 | 73,156  | 56,154               | 11,779     | 5,222              |
| 2025 | 72,477  | 56,141               | 11,128     | 5,207              |

---

### Processing Steps Applied

1. Concatenation of all datasets into a single base
2. Attribute name normalization (removal of spaces, uppercase letters, and special characters)
3. Removal of records with duplicate `pesid` values (keeping only the first occurrence)
4. Conversion of `latitude` and `longitude` attributes to float type
5. Removal of records outside Brazilian territory (based on latitude and longitude)
6. Processing and splitting of the `tracado_via` attribute into new derived attributes
7. Determination of whether the incident date is a public holiday
8. Creation of a `turno` (shift) attribute based on the `horario` attribute, to replace `fase_dia`
9. Splitting of `data_inversa` into separate `dia`, `mes`, and `ano` columns
10. Rounding of the incident kilometer marker to an integer value
11. Determination of maximum vehicle speed based on vehicle category, road type, and land use
12. Inclusion of radar positioning data on the highways
13. Conversion of radar latitude and longitude to float
14. Determination of the distance from each incident location to the nearest radar
15. Quantification of the number of incidents per kilometer on each highway

---

### Total Attributes After Initial Processing

| #  | Column                 | Non-Null Count | Dtype          |
|----|------------------------|----------------|----------------|
| 0  | id                     | 632,560        | float64        |
| 1  | pesid                  | 604,276        | float64        |
| 2  | data_inversa           | 632,560        | datetime64[ns] |
| 3  | dia_semana             | 632,560        | object         |
| 4  | horario                | 632,560        | object         |
| 5  | uf                     | 632,560        | object         |
| 6  | br                     | 631,157        | float64        |
| 7  | km                     | 631,157        | object         |
| 8  | municipio              | 632,560        | object         |
| 9  | causa_principal        | 632,560        | object         |
| 10 | causa_acidente         | 632,560        | object         |
| 11 | ordem_tipo_acidente    | 632,560        | int64          |
| 12 | tipo_acidente          | 632,519        | object         |
| 13 | classificacao_acidente | 632,550        | object         |
| 14 | fase_dia               | 632,560        | object         |
| 15 | sentido_via            | 632,560        | object         |
| 16 | condicao_metereologica | 632,560        | object         |
| 17 | tipo_pista             | 632,560        | object         |
| 18 | tracado_via            | 632,560        | object         |
| 19 | uso_solo               | 632,560        | object         |
| 20 | id_veiculo             | 632,546        | float64        |
| 21 | tipo_veiculo           | 632,546        | object         |
| 22 | marca                  | 632,560        | object         |
| 23 | ano_fabricacao_veiculo | 632,546        | float64        |
| 24 | tipo_envolvido         | 604,276        | object         |
| 25 | estado_fisico          | 604,276        | object         |
| 26 | idade                  | 552,744        | float64        |
| 27 | sexo                   | 604,276        | object         |
| 28 | ilesos                 | 604,276        | float64        |
| 29 | feridos_leves          | 604,276        | float64        |
| 30 | feridos_graves         | 604,276        | float64        |
| 31 | mortos                 | 604,276        | float64        |
| 32 | latitude               | 632,560        | float64        |
| 33 | longitude              | 632,560        | float64        |
| 34 | regional               | 632,529        | object         |
| 35 | delegacia              | 632,321        | object         |
| 36 | uop                    | 632,124        | object         |
| 37 | em_obras               | 632,560        | int64          |
| 38 | intersecao_de_vias     | 632,560        | int64          |
| 39 | aclive                 | 632,560        | int64          |
| 40 | tunel                  | 632,560        | int64          |
| 41 | ponte                  | 632,560        | int64          |
| 42 | curva                  | 632,560        | int64          |
| 43 | retorno_regulamentado  | 632,560        | int64          |
| 44 | rotatoria              | 632,560        | int64          |
| 45 | reta                   | 632,560        | int64          |
| 46 | declive                | 632,560        | int64          |
| 47 | viaduto                | 632,560        | int64          |
| 48 | desvio_temporario      | 632,560        | int64          |
| 49 | feriado                | 632,560        | int64          |
| 50 | turno                  | 632,560        | object         |
| 51 | ano                    | 632,560        | int32          |
| 52 | mes                    | 632,560        | int32          |
| 53 | dia                    | 632,560        | int32          |
| 54 | vel_max                | 632,560        | int64          |
| 55 | vel_min                | 632,560        | int64          |
| 56 | geometry               | 632,560        | geometry       |
| 57 | latitude_radar         | 632,560        | float64        |
| 58 | longitude_radar        | 632,560        | float64        |
| 59 | distancia_radar_m      | 632,560        | float64        |
| 60 | total_ocorrencia       | 631,157        | float64        |
| 61 | gravidade              | 632,560        | int64          |

---

### Attributes Excluded from `valores_atributos.txt`

```python
'id', 'pesid', 'data_inversa', 'dia',
'geometry', 'latitude_radar', 'longitude_radar',
'distancia_radar_m', 'geometry', 'distancia_radar_m'
```

### Attributes Excluded from Further Research

```python
id_desconsiderados = ['id', 'pesid', 'id_veiculo']

originated_others = ['data_inversa', 'fase_dia', 'horario', 'tracado_via', 'latitude', 'longitude']

high_granularity = ['municipio', 'delegacia', 'uop', 'da']

derived_from_incident = ['causa_principal', 'causa_acidente', 'ordem_tipo_acidente', 'tipo_acidente',
    'tipo_envolvido', 'estado_fisico', 'idade', 'sexo', 'ilesos', 'feridos_leves', 'feridos_graves',
    'mortos', 'classificacao_acidente']

low_occurrence = ['em_obras', 'rotatoria', 'retorno_regulamentado', 'viaduto',
    'desvio_temporario', 'ponte', 'desvio_temporario']

multicollinearity = ['aclive', 'tunel', 'curva', 'latitude_radar', 'longitude_radar', 'geometry']

vehicle_data = ['tipo_veiculo', 'marca', 'ano_fabricacao_veiculo', 'regional']
```

### Attributes Retained

```python
retained = ['dia_semana', 'uf', 'br', 'km', 'sentido_via', 'condicao_metereologica',
    'tipo_pista', 'uso_solo', 'intersecao_de_vias', 'reta', 'declive',
    'feriado', 'turno', 'ano', 'mes', 'vel_max', 'vel_min',
    'distancia_radar_m', 'total_ocorrencia', 'gravidade']
```

### Resulting Dataset

- **Records:** 632,560
- **Attributes:** 20

**Null values per attribute:**

| Attribute              | Null Records |
|------------------------|--------------|
| dia_semana             | 0            |
| uf                     | 0            |
| br                     | 1,403        |
| km                     | 1,403        |
| sentido_via            | 0            |
| condicao_metereologica | 0            |
| tipo_pista             | 0            |
| uso_solo               | 0            |
| intersecao_de_vias     | 0            |
| reta                   | 0            |
| declive                | 0            |
| feriado                | 0            |
| turno                  | 0            |
| ano                    | 0            |
| mes                    | 0            |
| vel_max                | 0            |
| vel_min                | 0            |
| distancia_radar_m      | 0            |
| total_ocorrencia       | 1,403        |
| gravidade              | 0            |

After removing null records:

- **Records:** 631,157
- **Attributes:** 20

---

## Normalization

### Attributes considered and types

| Attribute              | Data Type   |
|------------------------|-------------|
| dia_semana             | categorical |
| uf                     | categorical |
| br                     | categorical |
| km                     | numeric     |
| sentido_via            | binary      |
| condicao_metereologica | categorical |
| tipo_pista             | categorical |
| uso_solo               | binary      |
| intersecao_de_vias     | binary      |
| reta                   | binary      |
| declive                | binary      |
| feriado                | categorical |
| turno                  | categorical |
| ano                    | categorical |
| mes                    | categorical |
| vel_max                | categorical |
| distancia_radar_m      | numeric     |
| total_ocorrencia       | numeric     |
| gravidade              | binary      |

---

### Useful References

- https://www.mdpi.com/2078-2489/11/5/270
- https://arxiv.org/abs/2010.14921
- https://arxiv.org/pdf/2310.05840
- https://www.tandfonline.com/doi/abs/10.1080/13588265.2022.2074643

---

### Models Used

- Logistic Regression
- Random Forest
- CatBoost

---

### Results

#### Logistic Regression

| Variable               | Logit Coefficient | AME       |
|------------------------|------------------:|----------:|
| tipo_pista             | -0.199743         | -0.022118 |
| declive                |  0.157100         |  0.017396 |
| total_ocorrencia       | -0.152582         | -0.016896 |
| intersecao_de_vias     | -0.146470         | -0.016219 |
| vel_max                |  0.126518         |  0.014010 |
| distancia_radar_m      |  0.118738         |  0.013148 |
| condicao_metereologica | -0.106258         | -0.011766 |
| turno_sin              | -0.102607         | -0.011362 |
| turno_cos              |  0.097712         |  0.010820 |
| uf                     | -0.088061         | -0.009751 |
| dia_semana_cos         |  0.060390         |  0.006687 |
| uso_solo               | -0.056962         | -0.006308 |
| reta                   | -0.054028         | -0.005983 |
| br                     |  0.028925         |  0.003203 |
| dia_semana_sin         | -0.027064         | -0.002997 |
| mes_sin                | -0.024480         | -0.002711 |
| sentido_via            |  0.016470         |  0.001824 |
| km                     | -0.007854         | -0.000870 |
| mes_cos                | -0.003150         | -0.000349 |
| feriado                | -0.000381         | -0.000042 |

#### Random Forest

| Attribute              | SHAP Global E[φ_k] | SHAP Importance E[\|φ_k\|] |
|------------------------|-------------------:|---------------------------:|
| tipo_pista             | 0.003358           | 0.037167                   |
| vel_max                | 0.005549           | 0.033232                   |
| total_ocorrencia       | 0.000089           | 0.026792                   |
| uf_br                  | -0.000253          | 0.018654                   |
| distancia_radar_m      | -0.000979          | 0.016608                   |
| turno                  | -0.002999          | 0.011952                   |
| condicao_metereologica | 0.003180           | 0.009821                   |
| uso_solo               | 0.000003           | 0.007156                   |
| dia_semana             | -0.000178          | 0.006084                   |
| km                     | 0.000107           | 0.003542                   |
| declive                | 0.000022           | 0.002007                   |
| reta                   | -0.000388          | 0.001789                   |
| mes                    | 0.000251           | 0.001484                   |
| feriado                | -0.000027          | 0.000771                   |
| intersecao_de_vias     | -0.000435          | 0.000600                   |
| sentido_via            | 0.000033           | 0.000311                   |

#### CatBoost

| Attribute              | SHAP Global E[φ_k] | SHAP Importance E[\|φ_k\|] |
|------------------------|-------------------:|---------------------------:|
| vel_max                | 0.009001           | 0.053324                   |
| total_ocorrencia       | -0.000914          | 0.033825                   |
| tipo_pista             | 0.002250           | 0.030565                   |
| turno                  | -0.006626          | 0.028205                   |
| uf_br                  | 0.001014           | 0.025404                   |
| distancia_radar_m      | -0.001799          | 0.021425                   |
| condicao_metereologica | 0.005059           | 0.015971                   |
| uso_solo               | 0.000301           | 0.013845                   |
| dia_semana             | -0.000393          | 0.009396                   |
| km                     | -0.000443          | 0.008564                   |
| reta                   | -0.001344          | 0.006765                   |
| declive                | 0.000387           | 0.006706                   |
| mes                    | 0.000604           | 0.004204                   |
| intersecao_de_vias     | -0.000673          | 0.001882                   |
| sentido_via            | 0.000157           | 0.001194                   |
| feriado                | -0.000043          | 0.001192                   |