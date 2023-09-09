import streamlit as st


def clear_notes():
    st.session_state.amazing_note = ''

st.set_page_config(page_title="NoteBook", page_icon="📝", layout="wide")
st.title("📝Insights")

st.divider()
    
st.markdown(st.session_state.amazing_note)

st.button("clear notes", key='b1', on_click=clear_notes)