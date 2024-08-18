import streamlit as st
from st_aggrid import AgGrid,ColumnsAutoSizeMode,GridOptionsBuilder,GridUpdateMode
import pandas as pd
from components.data_store import ddb_ops 
from utils import util_functions as uf
from components.login import users
def create_table(data):
    df = pd.DataFrame(data)
    grid_options = {
        "columnDefs":   [
                    {"field": "job_status"},
                    {"field": "token_id"},
                    {"field": "user_id"},
                ],
        "rowSelection": "single"
    }
    grid_response = AgGrid(
        df,
        grid_options,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
        theme='streamlit',
        #rowSelection='single',
        #cellSelection='single',
        #on_grid_ready=get_row_data # Callback function
    )
    return grid_response
def get_row_data(grid_response):
    selected_rows = grid_response['selected_rows']
    if selected_rows:
        selected_row = selected_rows[0]
        # Process the selected row data here
        st.write(selected_row)

def AgGrid_with_display_rules(df):
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=False, groupable=False)
    gd.configure_selection(selection_mode='single', use_checkbox=False)
    gridoptions = gd.build()
    grid_table = AgGrid(df, gridOptions=gridoptions,
                        #update_mode=GridUpdateMode.VALUE_CHANGED,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        height=400,
                        allow_unsafe_jscode=True
                        )
    sel_row = grid_table["selected_rows"]
    st.write(sel_row)
    return grid_table, sel_row

def render_table_bad(data,title,link_status='Completed'):
    st.title(title)
    # Sample data for demonstration
    # data = [
    #     {"user_id": "user1", "job_status": "Completed", "token_id": "token1"},
    #     {"user_id": "user2", "job_status": "Pending", "token_id": "token2"},
    #     {"user_id": "user3", "job_status": "Completed", "token_id": "token3"}
    # ]

    # Create a table
    # data = pd.DataFrame(data)
    # st.table(data)
    # ddb_results = uf.get_secret('DDB_RESULTS')    
    # user_id=users.get_userid()
    # # Iterate over the data and display links for completed jobs
    # for index,row in data.iterrows():
    #     #print(row)
    #     if row["job_status"] == link_status:
    #         st.markdown(f"[View Details]({st.markdown(f'javascript:void(0);', unsafe_allow_html=True)})")
    #         token_id = row['token_id']
    #         row_data = ddb_ops.query_ddb(ddb_results,'token_id',token_id,sk_name='user_id',sk_val=user_id)
    #         #st.write(row_data)
    #         st.button("Click to View", key = f'vw_btn_{token_id}',on_click=lambda: create_prepopulated_form(row_data[0]))
    # Create the table
    #grid_response = create_table(data)
    #agg = AgGrid_with_display_rules(data)
    # Access selected row data
    #selected_rows = grid_response['selected_rows']
    #if selected_rows:
        #selected_row = selected_rows[0]
        #st.write(selected_row)
def render_table(data):
    # # Show user table 
    data_cols = data.columns
    st_cols = st.columns((1,10),vertical_alignment="bottom")
    #fields = ["№", 'user_id', 'token_id', 'job_status']
    # for col, field_name in zip(st_cols[1:], data_cols):
    #     # header
    #     col.write(field_name)
    for x,token_id in enumerate(data['token_id']):
        #st_cols[0].button(x,disabled=True,use_container_width=True)
        st_cols[0].button(label=str(x),key=str(x)+data['token_id'][x],disabled=True,use_container_width=True)
        completed = data['job_status'][x]=='Completed'
        do_action = st_cols[1].button(data['token_id'][x], key=x,use_container_width=True,disabled=not completed)
        if do_action:
            st.write('Clicked')
        #st_cols[1].write(data['token_id'][x])
        #st_cols[2].write(data['job_status'][x])
        #completed = data['job_status'][x]='Completed'  # flexible type of button
        #button_type = "G" if completed=='Completed' else ''
        #button_phold = st_cols[1].empty()  # create a placeholder
        #do_action = button_phold.button(data['token_id'][x], key=x,use_container_width=True)
#@st.cache_data
def get_user_data():
    ddb_usr=uf.get_secret('DDB_USERS')
    user_id=users.get_userid()
    data = ddb_ops.query_ddb(ddb_usr, pk_name='user_id',pk_val=user_id)
    return pd.DataFrame(data)
def get_results_data(token_id):
    ddb_results=uf.get_secret('DDB_RESULTS')
    user_id=users.get_userid()
    data = ddb_ops.query_ddb(ddb_results,'token_id',token_id,sk_name='user_id',sk_val=user_id)
    return data

def paginate():
    """Displays a table with all jobs for a user."""
    # ddb_usr=uf.get_secret('DDB_USERS')
    # user_id=users.get_userid()
    # data = ddb_ops.query_ddb(ddb_usr, pk_name='user_id',pk_val=user_id)
    #   # Replace with your actual data retrieval logic
    #   data = [
    #       {"image_id": "1234", "invoice_amount": 100.00, "invoice_date": "2024-08-17", "tax_amount": 10.00, "status": "Completed"},
    #       {"image_id": "5678", "invoice_amount": 200.50, "invoice_date": "2024-08-15", "tax_amount": 15.25, "status": "Failed"},
    #   ]
    #st.header("All Jobs")
    #st.write("This page shows details of all your jobs.")
    # Create a DataFrame from the data
    #df = pd.DataFrame(data)
    # Display the DataFrame as a table
    # render_table(get_data(),'Click for details')
    user_table = get_user_data()
    st.title('All Jobs')
    st.table(user_table)
    results_tbl = []
    for x,row in user_table.iterrows():
        if row['job_status']=='Completed':
            token_id = row['token_id']
            row_data = get_results_data(token_id)
            #st.write(type(row_data[0]))
            results_tbl.append(row_data[0])
            #st.write(token_id)
    st.title('Completed Jobs')
    
    st.table(pd.DataFrame(results_tbl))
    #render_table(get_user_data())

