# -*- coding: utf-8 -*-
"""
Full preprocessing pipeline for traffic accident dataset.
Includes all modeling attributes.
"""

import warnings
from dataclasses import dataclass
from typing import Dict, Optional, List

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


# =========================================================
# SPECIFICATION
# =========================================================

@dataclass
class ColumnSpec:
    name: str
    description: str
    role: str
    dtype: str
    units: Optional[str] = None
    domain: Optional[str] = None
    encoding: Optional[str] = None
    notes: Optional[str] = None


ENCODINGS_V1: Dict[str, Dict] = {

    "dia_semana": {
        "domingo": 0, "segunda-feira": 1, "terça-feira": 2,
        "quarta-feira": 3, "quinta-feira": 4,
        "sexta-feira": 5, "sábado": 6,
    },

    "condicao_metereologica": {
        "Céu Claro": 0,
        "CÃ©u Claro": 0,
        "Sol": 0,
        "Ignorado": 0,
        "Nublado": 1,
        "Nevoeiro/Neblina": 1,
        "Vento": 1,
        "Chuva": 2,
        "Garoa/Chuvisco": 2,
        "Granizo": 2,
        "Neve": 2,
    },

    "tipo_pista": {"Simples": 0, "Dupla": 1, "Múltipla": 2, "MÃºltipla": 2},

    "turno": {"madrugada": 0, "manhã": 1, "tarde": 2, "noite": 3},

    "sentido_via": {"Crescente": 1, "Decrescente": 0},

    "uso_solo": {"Sim": 1, "Não": 0, "NÃ£o": 0},
}


MODEL_COLUMNS = [
    "dia_semana",
    "uf",
    "br",
    "km",
    "sentido_via",
    "condicao_metereologica",
    "tipo_pista",
    "uso_solo",
    "feriado",
    "turno",
    "mes",
    "vel_max",
    "distancia_radar_m",
    "total_ocorrencia",
]

SPLIT_COLUMN = "ano"

BINARY_COLUMNS = [
    "gravidade",
    "declive",
    "reta",
    "intersecao_de_vias",
]


# =========================================================
# CORE FUNCTIONS
# =========================================================

def encode_attribute(df: pd.DataFrame, attribute: str, mapping: Dict) -> None:
    df[attribute] = df[attribute].map(mapping)
    if df[attribute].isna().any():
        warnings.warn(f"[encode_attribute] Valores não mapeados em '{attribute}'")
    df[attribute] = pd.to_numeric(df[attribute], errors="coerce")


def encode_cyclical(df: pd.DataFrame, column: str, period: int) -> List[str]:
    df[f"{column}_sin"] = np.sin(2 * np.pi * df[column] / period)
    df[f"{column}_cos"] = np.cos(2 * np.pi * df[column] / period)
    df.drop(columns=[column], inplace=True)
    return [f"{column}_sin", f"{column}_cos"]


def ordinal_encode(df: pd.DataFrame,
                   column: str,
                   numeric_sort: bool = False) -> None:

    if numeric_sort:
        categories = sorted(
            pd.to_numeric(df[column], errors="coerce").dropna().unique()
        )
    else:
        categories = sorted(df[column].dropna().unique())

    mapping = {cat: idx for idx, cat in enumerate(categories)}
    df[column] = df[column].map(mapping)

    if df[column].isna().any():
        warnings.warn(f"[ordinal_encode] Valores não mapeados em '{column}'")


# =========================================================
# PREPROCESS
# =========================================================

def preprocess(df: pd.DataFrame,
               encodings: Dict[str, Dict] = ENCODINGS_V1,
               validate: bool = True,
               normalize: bool = True) -> pd.DataFrame:

    df = df.copy()

    # Garante existência das colunas
    required_cols = list(dict.fromkeys(
        MODEL_COLUMNS + BINARY_COLUMNS + [SPLIT_COLUMN]
    ))

    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan

    df = df[required_cols]

    # Codificações categóricas
    for att, mapping in encodings.items():
        if att in df.columns:
            encode_attribute(df, att, mapping)

    ordinal_encode(df, "uf", numeric_sort=False)
    ordinal_encode(df, "br", numeric_sort=True)

    # =============================
    # Codificação cíclica
    # =============================
    expanded_columns = MODEL_COLUMNS.copy()

    for col, period in [("dia_semana", 7),
                        ("mes", 12),
                        ("turno", 4)]:

        if col in df.columns:
            new_cols = encode_cyclical(df, col, period)
            expanded_columns.remove(col)
            expanded_columns.extend(new_cols)

    # Conversão numérica segura
    df = df.apply(pd.to_numeric, errors="coerce")

    # =====================================================
    # NORMALIZAÇÃO (somente atributos modeláveis)
    # =====================================================
    if normalize:

        scaler = StandardScaler()

        cols_to_normalize = [
            col for col in expanded_columns
            if col not in BINARY_COLUMNS and col != SPLIT_COLUMN
        ]

        scaled_array = scaler.fit_transform(df[cols_to_normalize])

        df[cols_to_normalize] = scaled_array

    # =====================================================
    # SELEÇÃO FINAL
    # =====================================================
    final_columns = list(dict.fromkeys(
        expanded_columns + [SPLIT_COLUMN] + BINARY_COLUMNS
    ))

    df = df[final_columns]

    if validate:
        _validate(df)

    return df


# =========================================================
# VALIDATION
# =========================================================

def _validate(df: pd.DataFrame):

    if "mes_sin" in df.columns:
        if df[["mes_sin", "mes_cos"]].abs().max().max() > 1:
            warnings.warn("Erro na codificação cíclica.")

    if df.isna().sum().sum() > 0:
        warnings.warn("Existem valores NaN após preprocess.")


# =========================================================
# MAIN
# =========================================================

def main(input_csv: str,
         output_processed_csv: str = "processed.csv"):

    df_raw = pd.read_csv(input_csv, sep=";", encoding="latin_1")
    df_proc = preprocess(df_raw)

    df_proc.to_csv(output_processed_csv, index=False, encoding="utf-8")

    return df_proc