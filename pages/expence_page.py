import streamlit as st
from streamlit_pagination import pagination_component
import sys
import pandas as pd

sys.path.insert(0, r'D:\ds_projects\home_assistant_budget')


from database.session_manager import get_db_session



from repositories.transaction_repo import TransactionRepository
from repositories.category_repo import CategoryRepository


CATEGORY_EXPENSES = {1: 'Питание', 2: 'Здоровье', 3: 'Подписки', 4: 'Одежда, обувь и аксессуары', 5: 'Жильё', 6: 'Красота и быт',
                     7: 'Кафе и рестораны', 8: 'Развлечения (в т.ч. в интернете)', 9: 'Питомец', 10: 'Психолог', 11: 'Клининг',
                     12: 'Общественный транспорт', 13: 'Связь и интернет', 14: 'Непредвиденные покупки', 15: 'Нежелательные траты + кредиты'}


def main():

    @st.cache_resource
    def get_repos():
        return {
            "transaction": TransactionRepository(),
            "category": CategoryRepository()
    }

    repositories = get_repos()

    st.set_page_config(page_title="Расходы", page_icon="📈")

    try:

        with st.expander('Фильтры', expanded=True):
            with st.container(horizontal=True):

                st.date_input(label='Дата от', max_value='today', format='DD/MM/YYYY')
                st.date_input(label='Дата до', max_value='today', format='DD/MM/YYYY')
                select_category = st.multiselect('Категория', CATEGORY_EXPENSES.values(), placeholder='Выберите категорию')
                text_comment = st.text_input('Поиск по комментариям', placeholder='Поиск')

            with st.container(horizontal=True, horizontal_alignment='right'):
                st.button('Применить', icon=':material/done:')
                st.button('Очистить', icon=':material/backspace:')
                
    
        with get_db_session() as db:
            transactions = repositories['transaction'].get_transactions_with_categories(db)
                    
            if transactions:
                data = []
                for t in transactions:
                    data.append({
                        "Date": t.date.strftime("%d-%m-%Y"),
                        "Amount": f"{t.amount:,.2f} ₽",
                        "Category": t.category_rel.name_category if t.category_rel else "N/A",
                        "Comment": t.comment or ""
                    })


                   
                st.dataframe(data, use_container_width=True)

                        
                # Итого
                total = sum(t.amount for t in transactions)
                st.metric("Total", f"{total:,.2f} ₽")
            else:
                st.info("No transactions found")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.exception(e)  
       


    # with tab2:
    #     df = pd.DataFrame(columns=['Date','Amount','Category', 'Comment'])
    #     config = {
    #         'Date' : st.column_config.DatetimeColumn('Date', required=True),
    #         'Amount' : st.column_config.NumberColumn('Amount', min_value=0, max_value=100000000, required=True),
    #         'Category' : st.column_config.TextColumn('Category test', required=True),
    #         'Comment' : st.column_config.TextColumn('Comment', width='large'),

    #     }

    #     result = st.data_editor(df, column_config = config, num_rows='dynamic')
    
    # with tab3:

    #     col1, col2 = st.columns(2)
    #     with col1:
    #         year = st.number_input("Year", 2020, 2030, 2024)
    #     with col2:
    #         month = st.number_input("Month", 1, 12, datetime.now().month)

    #     if st.button("Get Stats"):
    #         try:
    #             with get_db_session() as db:
    #                 stats = repositories["transaction"].get_monthly_stat(db, year, month)
                                                            
    #                 col1, col2, col3 = st.columns(3)
    #                 col1.metric("Total", f"{stats['total']:,.2f} ₽")
    #                 col2.metric("Transactions", stats["count"])
                                                    
    #         except Exception as e:
    #             st.error(f"Error: {e}")
                    


if __name__ == "__main__":
    main()