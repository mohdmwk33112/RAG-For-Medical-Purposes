#!/usr/bin/env python
# coding: utf-8

# In[1]:


import chromadb
client = chromadb.PersistentClient(path="./database.sqlite")


# In[5]:


import chromadb.utils.embedding_functions as embedding_functions

# use directlye 
google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="")

# pass documents to query for .add and .query
collection = client.get_or_create_collection(name="medicine", embedding_function=google_ef)


# In[81]:


from pprint import pprint
query = "tell me the harm of the Advil cant be used  for"
results = collection.query(
    query_texts=[query], # Chroma will embed this for you
    n_results=10 # how many results to return
)
pprint(results)

# In[43]:


import google.generativeai as genai

# In[67]:


# Replace with your Gemini API key
api_key = ""

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")


# In[83]:


retrieved_docs = results['documents'][0]  # Retrieved documents
safe_docs = [doc for doc in retrieved_docs if "misuse" not in doc and "illegal" not in doc]
print("Retrieved Documents:", safe_docs)

# In[85]:


# Combine the query and retrieved context
context = "\n".join(safe_docs)
full_prompt = f"""
Disclaimer: The following is for educational purposes only. Consult a licensed healthcare professional for medical advice.

Context:
{context}

Query:
{query}
"""

# Generate answer with Gemini/

response = model.generate_content(
    full_prompt,
    safety_settings=[
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "HIGH"}
    ],
)

print("Generated Answer:", response.text)

# In[89]:


import pandas as pd

# In[107]:


df = pd.read_csv("./drugLibTrain_raw.csv")

df.shape

clean_df = df.dropna()

cleaned_df = clean_df.iloc[:,:8]
cleaned_df.head()



# In[109]:


documents = []

for i, row in cleaned_df.iterrows():
    documents.append("the drug name is "+row[1]+" and the condition to take this drug is "+row[5]+" and its side effects is "+row[7])

for i in range(5):
    print(documents[i])

# In[115]:


ids=1692
id=0
for index in range(len(documents)):
    collection.add(
        documents=documents[id],
        ids=[str(ids)]
    )
    id = id + 1
    ids = ids+1
print("Data successfully added to ChromaDB!")

# In[119]:


print(id)

# In[125]:


index = ids+1
for index in range(len(documents)):
    collection.add(
        documents=documents[id],
        ids=[str(ids)]
    )
    id = id + 1
    ids = ids+1
    print(ids)
print("Data successfully added to ChromaDB!")

# In[123]:


print(ids)

# In[ ]: