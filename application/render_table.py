def ():
    st.title("Data Table")

    # Sample data for demonstration
    data = [
        {"user_id": "user1", "job_status": "Completed", "token_id": "token1"},
        {"user_id": "user2", "job_status": "Pending", "token_id": "token2"},
        {"user_id": "user3", "job_status": "Completed", "token_id": "token3"}
    ]

    # Create a table
    st.table(data)

    # Iterate over the data and display links for completed jobs
    for row in data:
        if row["job_status"] == "Completed":
            st.markdown(f"[View Details]({st.markdown(f'javascript:void(0);', unsafe_allow_html=True)})")
            st.button("Click to View", on_click=lambda: create_prepopulated_form(fetch_data_from_dynamodb(row["token_id"])))

if __name__ == "__main__":
    main()
