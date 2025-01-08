import pandas as pd
import random
import re
import os

# Load your dataset
file_path = r"C:\Users\Wael\Desktop\cleaned_data.csv"  # Replace with your actual file path
data = pd.read_csv(file_path)

# Helper function to clean and truncate text
def clean_text(text, max_length=50):
    """
    Clean and truncate text to make it suitable for queries.
    """
    if pd.isna(text):
        return ""
    # Remove unnecessary characters
    text = re.sub(r"[;\n\r]+", ", ", str(text))  # Replace semicolons and newlines with commas
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    # Truncate text to max_length words
    words = text.split()
    return " ".join(words[:max_length]) + ("..." if len(words) > max_length else "")

# Generate queries with preprocessing and validation
max_chunks = len(data)
queries = []

complexity_levels = ["simple", "intermediate", "complex"]
complexity_weights = [0.4, 0.4, 0.2]

templates = {
    "simple": [
        "Tell me about the side effects of {value1}.",
        "What can you tell me about {value1}'s side effects?",
    ],
    "intermediate": [
        "What are the side effects of {value1}, and how does it compare to {value2}?",
        "How does {value1} compare to {value2} in terms of side effects?",
    ],
    "complex": [
        # Adjusted to compare between two values only
        "Compare the side effects of {value1} and {value2}.",
        "How does {value1} influence {value2} in terms of side effects?",
    ],
}

while len(queries) < 50:  # Loop until we generate at least 50 queries
    complexity = random.choices(complexity_levels, weights=complexity_weights, k=1)[0]
    
    if complexity == "simple":
        col = random.choice(data.columns)
        value1_row = data[col].dropna().sample(1)  # Sample one value from the column
        value1 = clean_text(value1_row.values[0])  # Clean the selected value
        query = random.choice(templates["simple"]).format(value1=value1)
        chunk_ids = data[data[col] == value1].index.tolist()  # Get all chunk IDs where the value matches
    
    elif complexity == "intermediate":
        col1, col2 = random.sample(data.columns.tolist(), 2)
        value1_row = data[col1].dropna().sample(1)  # Sample one value from col1
        value2_row = data[col2].dropna().sample(1)  # Sample one value from col2
        value1 = clean_text(value1_row.values[0])  # Clean the selected value
        value2 = clean_text(value2_row.values[0])  # Clean the selected value
        
        chunk_ids1 = data[data[col1] == value1].index.tolist()  # Get chunk IDs where value1 is found in col1
        chunk_ids2 = data[data[col2] == value2].index.tolist()  # Get chunk IDs where value2 is found in col2
        chunk_ids = list(set(chunk_ids1 + chunk_ids2))  # Combine unique chunk IDs from both columns
        
        query = random.choice(templates["intermediate"]).format(value1=value1, value2=value2)
    
    elif complexity == "complex":
        col1, col2 = random.sample(data.columns.tolist(), 2)  # Compare only two columns
        value1_row = data[col1].dropna().sample(1)  # Sample one value from col1
        value2_row = data[col2].dropna().sample(1)  # Sample one value from col2
        value1 = clean_text(value1_row.values[0])  # Clean the selected value
        value2 = clean_text(value2_row.values[0])  # Clean the selected value
        
        chunk_ids1 = data[data[col1] == value1].index.tolist()  # Get chunk IDs where value1 is found in col1
        chunk_ids2 = data[data[col2] == value2].index.tolist()  # Get chunk IDs where value2 is found in col2
        chunk_ids = list(set(chunk_ids1 + chunk_ids2))  # Combine unique chunk IDs from both columns
        
        query = random.choice(templates["complex"]).format(value1=value1, value2=value2)
    
    # Limit to top 3 chunk IDs (if available)
    chunk_ids = chunk_ids[:3]  # Take the first 3 chunk IDs
    
    # Skip overly verbose queries
    if len(query.split()) > 60:
        continue
    
    # Print the query and chunk_ids
    print(f"Query: {query}")
    print(f"Top 3 Chunk IDs: {chunk_ids}")
    
    queries.append({
        "query": query,
        "chunk_ids": chunk_ids,  # Top 3 chunk IDs related to the query
        "complexity": complexity
    })

# Save queries to a CSV
output_file_path = "rag_queries_with_two_value_comparison.csv"
absolute_path = os.path.abspath(output_file_path)
queries_df = pd.DataFrame(queries)
queries_df.to_csv(output_file_path, index=False)

print(f"Enhanced RAG test queries with two-value comparison successfully saved to {absolute_path}")
