# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas 

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)


name_on_order = st.text_input("Name of Smoothie")
st.write("The name of your Smoothie will be:", name_on_order)

cnx=st.connection("snowflake") 

session= cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# convert snowpark dataframe into pandas dataframe
pd_df= my_dataframe.to_pandas()
#st.dataframe(pd_df)

ingredients_list= st.multiselect("Choose upto 5 ingredients:"
                                 ,my_dataframe
                                ,max_selections=5
                                )


# st.write(ingredients_list)
# st.text(ingredients_list)
if ingredients_list:
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
      
        ingredients_string +=fruit_chosen+''

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df= st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)



    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    time_to_insert= st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered', icon="✅")

   
    st.stop()

    
        
        
    

