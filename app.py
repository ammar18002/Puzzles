import streamlit as st
import pandas as pd
from sudoku_solver import sudoku_validator, find_empty_cell, valid, solve, sudoku_solver, sudoku_check_or_solve
from PIL import Image
# import pytesseract
import base64

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Sudoku Solver Web App", page_icon="🧩", layout="wide")

# ---------- SESSION STATE FOR NAVIGATION ----------
if "page" not in st.session_state:
    st.session_state.page = "start"

# ---------- BACKGROUND HELPERS ----------
def set_background_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def set_gradient_background(colors):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, {colors[0]}, {colors[1]}, {colors[2]});
            color: white;
        }}
        h1, h2, h3 {{
            font-style: italic;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- START PAGE ----------
if st.session_state.page == "start":
    set_gradient_background(["#ff006e", "#8338ec", "#3a86ff"])  # gradient bg

    st.markdown("<h1 style='text-align:center; color:white;'>🧩 Sudoku Solver Web App</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:white;'>Welcome! Ready to begin?</h3>", unsafe_allow_html=True)

    if st.button("🚀 Start", use_container_width=True):
        st.session_state.page = "upload"
        st.rerun()

# ---------- UPLOAD PAGE ----------
elif st.session_state.page == "upload":
    st.markdown("<h1 style='text-align:center;'>📂 Upload Your Sudoku</h1>", unsafe_allow_html=True)
    st.write("✨ Upload a Sudoku puzzle as **.txt** or **image** 📝🖼️")

    # TXT upload
    uploaded_txt = st.file_uploader("Upload Sudoku TXT", type="txt")
    if uploaded_txt is not None:
        grid = []
        for line in uploaded_txt.read().decode("utf-8").splitlines():
            row = [int(x) for x in line.strip().split()]
            grid.append(row)

        st.subheader("📝 Uploaded Sudoku Grid")
        df = pd.DataFrame(grid)
        st.dataframe(df)

        # ---------- BUTTONS ----------
        col1, col2, col3 = st.columns(3)

        # Validate puzzle
        with col1:
            if st.button("🔎 Validate Puzzle"):
                if sudoku_validator(grid):
                    if any(0 in row for row in grid):
                        st.info("✅ Puzzle is valid so far, but incomplete.")
                    else:
                        st.success("✅ Puzzle is valid and complete!")
                else:
                    st.error("❌ Puzzle is invalid.")

        # Solve puzzle
        with col2:
            if st.button("🧩 Solve Sudoku"):
                solved_grid = [row[:] for row in grid]  # copy
                if solve(solved_grid):   # try solving directly
                    st.success("🎉 Sudoku Solved")
                    st.dataframe(pd.DataFrame(solved_grid))
                    st.session_state["solved_grid"] = solved_grid
                else:
                    st.error("⚠️ Sudoku could not be solved")

        # Validate solution
        with col3:
            if st.button("✅ Validate Solution"):
                check_grid = st.session_state.get("solved_grid", grid)
                if any(0 in row for row in check_grid):
                    st.warning("⚠️ Grid is incomplete. Please solve first.")
                else:
                    if sudoku_validator(check_grid):
                        st.success("🎉 The solution is valid!")
                    else:
                        st.error("❌ The solution is NOT valid.")

    # ---------Image upload-----------
    uploaded_img = st.file_uploader("Upload Sudoku Image", type=["jpg", "png"])
    if uploaded_img is not None:
        img = Image.open(uploaded_img)
        st.image(img, caption="Uploaded Sudoku", use_container_width=True)
        text = pytesseract.image_to_string(img)
        st.write("📖 Extracted Text from Image:")
        st.code(text)

    # Go to about page
    if st.button("➡️ Next", use_container_width=True):
        st.session_state.page = "about"
        st.rerun()

# ---------- ABOUT PAGE ----------
elif st.session_state.page == "about":
    set_gradient_background(["#000000", "#3a0ca3", "#7209b7"])  # black → purple
    st.markdown("<h2 style='text-align:center;'>🙏 Thanks for using...</h2>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align:center;'>Made by <i>Ammar</i> ✨</h3>", unsafe_allow_html=True)
