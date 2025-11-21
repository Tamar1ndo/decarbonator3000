# app/dropbox/service.py
import io
from typing import List

import dropbox
import pandas as pd

from .env import DROPBOX_TOKEN, WISE4051_ROOT, WISE4012_ROOT

dbx = dropbox.Dropbox(DROPBOX_TOKEN)


def _read_csvs_in_folder(folder_path: str) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []

    try:
        res = dbx.files_list_folder(folder_path)
    except dropbox.exceptions.ApiError as e:
        raise RuntimeError(f"Dropbox list_folder error for {folder_path}: {e}")

    for entry in res.entries:
        if isinstance(entry, dropbox.files.FileMetadata) and entry.name.lower().endswith(".csv"):
            _, resp = dbx.files_download(entry.path_display)
            df = pd.read_csv(io.BytesIO(resp.content))
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def _read_all_under(root_path: str) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []

    try:
        res = dbx.files_list_folder(root_path)
    except dropbox.exceptions.ApiError as e:
        raise RuntimeError(f"Dropbox list_folder error for {root_path}: {e}")

    for entry in res.entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            folder_df = _read_csvs_in_folder(entry.path_display)
            if not folder_df.empty:
                frames.append(folder_df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


# ---------- CO2 (WISE-4051, COM_1 Wd_0) ----------

def get_co2_all() -> List[int]:
    df = _read_all_under(WISE4051_ROOT)
    if "COM_1 Wd_0" not in df.columns:
        return []
    return df["COM_1 Wd_0"].dropna().astype(int).tolist()


def get_co2_daily(date_str: str) -> List[int]:
    folder = f"{WISE4051_ROOT}/{date_str}"
    df = _read_csvs_in_folder(folder)
    if df.empty or "COM_1 Wd_0" not in df.columns:
        return []
    return df["COM_1 Wd_0"].dropna().astype(int).tolist()


# ---------- Temperature (WISE-4012, COM_1 Wd_1) ----------

def get_temp_all() -> List[float]:
    df = _read_all_under(WISE4012_ROOT)
    if "COM_1 Wd_1" not in df.columns:
        return []
    return df["COM_1 Wd_1"].dropna().astype(float).tolist()


def get_temp_daily(date_str: str) -> List[float]:
    folder = f"{WISE4012_ROOT}/{date_str}"
    df = _read_csvs_in_folder(folder)
    if df.empty or "COM_1 Wd_1" not in df.columns:
        return []
    return df["COM_1 Wd_1"].dropna().astype(float).tolist()


# ---------- Humidity (WISE-4012, COM_1 Wd_2) ----------

def get_humid_all() -> List[float]:
    df = _read_all_under(WISE4012_ROOT)
    if "COM_1 Wd_2" not in df.columns:
        return []
    return df["COM_1 Wd_2"].dropna().astype(float).tolist()


def get_humid_daily(date_str: str) -> List[float]:
    folder = f"{WISE4012_ROOT}/{date_str}"
    df = _read_csvs_in_folder(folder)
    if df.empty or "COM_1 Wd_2" not in df.columns:
        return []
    return df["COM_1 Wd_2"].dropna().astype(float).tolist()
