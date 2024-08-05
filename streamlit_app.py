import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

st.title('Smoothies')

name_on_order=st.text_input('Name')
st.write('The name on your smoothie will be:',name_on_order)

session = get_active_session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list=st.multiselect(
    'Choose up to 5'
    , my_dataframe
)

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!',icon="✅")
