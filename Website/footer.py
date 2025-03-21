def add_footer():
    footer_code = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #F0F2F6;
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
        Contact: <a href="mailto:stu240535@mail.uni-kiel.de">stu240535@mail.uni-kiel.de</a> |
        <a href="mailto:stu240535@mail.uni-kiel.de">Emilie Terhaars Stu-Mail</a> |
        <a href="mailto:stu240535@mail.uni-kiel.de">Sara Rolfs Stu-Mail</a> |
        <a href="www.google.com">poster link here?</a>
    </div>
    """
    st.markdown(footer_code, unsafe_allow_html=True)