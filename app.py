import io
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from extract import MODEL, Receipt, check, extract, suggested_name

st.set_page_config(page_title="Local Receipt Sorter", page_icon="🧾", layout="wide")
st.title("Local Receipt Sorter")
st.caption(f"Runs on this computer with {MODEL} through Ollama. Your files are never uploaded anywhere.")

files = st.file_uploader(
    "Add receipts and invoices", type=["pdf", "png", "jpg", "jpeg", "webp"], accept_multiple_files=True
)

if files and st.button("Extract details", type="primary"):
    rows, bar = [], st.progress(0.0)
    with tempfile.TemporaryDirectory() as tmp:
        for i, f in enumerate(files):
            p = Path(tmp) / f.name
            p.write_bytes(f.getvalue())
            try:
                r = extract(p)
                flags = check(r)
            except Exception as e:  # keep going if one file fails
                r, flags = Receipt(), [f"extraction failed: {e}"]
            rows.append({"file": f.name, **r.model_dump(),
                         "new_name": suggested_name(r, f.name), "flags": "; ".join(flags)})
            bar.progress((i + 1) / len(files))
    st.session_state.df = pd.DataFrame(rows)

if "df" in st.session_state:
    df = st.session_state.df
    n_flagged = int((df["flags"] != "").sum())
    st.write(f"{len(df)} files processed. **{n_flagged} need a look.** Edit any cell, then export.")
    edited = st.data_editor(df, use_container_width=True, num_rows="dynamic")

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        edited.to_excel(xw, index=False, sheet_name="Receipts")
    c1, c2 = st.columns(2)
    c1.download_button("Download CSV", edited.to_csv(index=False), "receipts.csv", "text/csv")
    c2.download_button("Download Excel", buf.getvalue(), "receipts.xlsx")
