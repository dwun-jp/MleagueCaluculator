import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"


def load_score_tables():
    return {
        "non_dealer_tsumo": pd.read_csv(DATA_DIR / "子ツモ@点数計算.csv"),
        "non_dealer_ron": pd.read_csv(DATA_DIR / "子ロン@点数計算.csv"),
        "dealer_tsumo": pd.read_csv(DATA_DIR / "親ツモ@点数計算.csv"),
        "dealer_ron": pd.read_csv(DATA_DIR / "親ロン@点数計算.csv"),
    }
