import os
import re
import streamlit as st
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# Database connection parameters
db_user = "root"
db_password = quote_plus("Cosmo@2023*")
db_host = "10.41.121.5"
db_name = "cosmo"

# Initialize SQLDatabase
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)

# Initialize LLM
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.environ["GOOGLE_API_KEY"])

# Create SQL query chain
chain = create_sql_query_chain(llm, db)

def execute_query(question):
    try:
        # Generate SQL query from the question
        response = chain.invoke({"question": question})

        # Clean the generated query
        cleaned_query = response.strip('```sql\n').strip('\n```')
        print(cleaned_query)
        # Execute the cleaned query
        result = db.run(cleaned_query)
        print(result)
        # Extract only the number from the result
        output = re.search(r"\d+", str(result)).group()

        return cleaned_query, output
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

# Streamlit interface
st.title("Chat with Your DB")

# Input from user
question = st.text_input("Enter your question:")

if st.button("Execute"):
    if question:
        cleaned_query, output = execute_query(question)
        
        if cleaned_query and output:
            st.write(f"The result is {output}")
        else:
            st.write("No result returned due to an error.")
    else:
        st.write("Please enter a question.")

#########used conda envirnment for this code#############