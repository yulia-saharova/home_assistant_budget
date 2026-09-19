import streamlit as st



CATEGORY_INCOME = {1: 'Зарплата', 2: 'Возвраты', 3: 'Дополнительный доход'}




def main():


    st.set_page_config(page_title="Доходы", page_icon="📈")
    

    tab1, tab2 = st.tabs(["Добавить приход", "Просмотр"])


    with tab1:
        #date_income = st.date_input('Дата', max_value=date.today())
        income = st.number_input("Сумма", min_value=0.0)
        category = st.selectbox("Категория", CATEGORY_INCOME.values())
        comment = st.text_input('Комментарий')

        if st.button("Добавить приход"):
            st.success(f"Добавлен приход {income} в категорию {category}")

    with tab2:
        uploaded_file = st.file_uploader("Загрузить файл CSV", type=["csv"])

    

if __name__ == "__main__":
    main()   
    
