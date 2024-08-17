import streamlit as st
import pandas as pd
def processed_jobs_page():
  """Displays a table with processed job data."""
  # Replace with your actual data retrieval logic
  data = [
      {"image_id": "1234", "invoice_amount": 100.00, "invoice_date": "2024-08-17", "tax_amount": 10.00, "status": "Completed"},
      {"image_id": "5678", "invoice_amount": 200.50, "invoice_date": "2024-08-15", "tax_amount": 15.25, "status": "Failed"},
  ]

  st.header("Processed Jobs")
  st.write("This page shows details of processed jobs.")

  # Create a DataFrame from the data
  df = pd.DataFrame(data)

  # Display the DataFrame as a table
  st.table(df)
