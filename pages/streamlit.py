import streamlit as st



def main():
    st.set_page_config(page_title="Finance Tracker", layout="wide")


    main_page = st.Page("main_page.py", title="Главная", icon=":material/home:")    
    add_expence_page = st.Page("add_expence_page.py", title="Добавить расход", icon=":material/wallet:")
    expence_page = st.Page("expence_page.py", title="Расходы", icon=":material/wallet:")

    add_income_page = st.Page("add_income_page.py", title="Добавить доход", icon=":material/money_bag:")
    income_page = st.Page("income_page.py", title="Доходы", icon=":material/money_bag:")

    stats_page = st.Page("stats_page.py", title="Статистика", icon=":material/monitoring:")    



    pg = st.navigation(
        {
            "Главная": [main_page],
            "Доходы": [income_page, add_income_page],
            "Расходы": [expence_page, add_expence_page],
            "Статистика": [stats_page],
        }
    )
    pg.run()



if __name__ == "__main__":
    main()   
    