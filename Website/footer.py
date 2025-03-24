import streamlit as st

def add_footer():
    footer_code = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #F4F0EC;
            color: black;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
        a {
            color: #fff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        Contact: <a href="mailto:stu240535@mail.uni-kiel.de">Tyra Kausch</a> |
        <a href="mailto:stu240868@mail.uni-kiel.de">Emilie Terhaar</a> |
        <a href="mailto:stu239831@mail.uni-kiel.de">Sara Rolfs</a>
    </div>
    """
    st.markdown(footer_code, unsafe_allow_html=True)