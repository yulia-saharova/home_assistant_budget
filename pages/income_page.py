import streamlit as st
from database.session_manager import get_db_session

from repositories.transaction_repo import TransactionRepository
from repositories.category_repo import CategoryRepository


CATEGORY_INCOME = {1: 'Зарплата', 2: 'Возвраты', 3: 'Дополнительный доход'}




def main():

    @st.cache_resource
    def get_repos():
        return {
            "transaction": TransactionRepository(),
            "category": CategoryRepository()
        }

    repositories = get_repos()

    st.set_page_config(page_title="Доходы", page_icon="📈")
    
    try:

        with st.expander('Фильтры', expanded=True):
            with st.container(horizontal=True):

                st.date_input(label='Дата от', max_value='today', format='DD/MM/YYYY')
                st.date_input(label='Дата до', max_value='today', format='DD/MM/YYYY')
                select_category = st.multiselect('Категория', CATEGORY_INCOME.values(), placeholder='Выберите категорию')
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

    

if __name__ == "__main__":
    main()   
    
