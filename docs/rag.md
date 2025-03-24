---
layout: obsidian
share: "true"
parent: Interests
---

## System Prompts

System prompts are a core component that shapes AI model behavior by providing precise control over how AI models process and respond to user inputs. They can be configured at three different levels: for the current chat (which overrides all others), for a specific user, or for a specific AI model. 

When you create a system prompt, it becomes part of the instruction set that's sent to the underlying language model. This isn't just appending text - it's structurally integrated into the model's context window:

1. **Context Window Integration**: The system prompt is positioned at the beginning of the context window, establishing the behavioral framework before any user input.

2. **Prompt Template Mechanism**: When a user interacts with the model, combine the system prompt with other components using a predefined template structure before sending it to the language model.

## Context Window Integration

The context window is the memory space where the language model processes information. System prompts are strategically positioned within this context window to guide model behavior.

### How It Works:

1. **Priority Positioning**: 
   When you create a system prompt, place it at the beginning of the context window, which gives it priority influence over the model's behavior.

2. **Hierarchical Override System**:
   Implement a hierarchical system where chat-level prompts override user-level prompts, which override model-level prompts. This allows for flexible control at different scopes.

3. **Context Window Management**:
   Since context windows have token limits, carefully manages how much space system prompts occupy to leave room for conversation history and retrieved knowledge.

### Example:

Let's say you create the following system prompts:

**Model-level system prompt** :

```text
You are a helpful assistant specializing in technical documentation. Always format code examples with proper syntax highlighting and explain complex concepts with analogies.
```

**User-level system prompt** :

```text
When responding to this user, prioritize brevity and focus on practical examples. Use American English spelling.
```

**Chat-level system prompt** :

```text
For this conversation, act as a Python expert focusing on FastAPI development. Provide inline comments for all code examples.
```

When the user asks a question in this chat, construct the context window in this order:
1. Chat-level system prompt (highest priority)
2. Retrieved knowledge (if any)
3. Conversation history
4. Current user message

The model-level prompt is completely overridden by the user-level prompt, which is then overridden by the chat-level prompt. This means the model will act as a Python/FastAPI expert (chat-level instruction), rather than a general technical documentation specialist (model-level instruction).

## Prompt Template Mechanism

The prompt template mechanism combines different elements before sending them to the language model.

### How It Works:

1. **Template Structure**:
   Use a template structure to consistently format how different elements are combined. This includes placeholders for system prompts, retrieved information, conversation history, and the current query.

2. **RAG Template Customization**:
   For knowledge retrieval, use a specific RAG template that can be customized in the admin settings. This template determines how retrieved context is presented to the model.

3. **Dynamic Assembly**:
   When a user sends a message, dynamically assemble components based on what's relevant for that specific interaction.

### Example:

Let's look at how a RAG template might be structured and applied:

**Custom RAG Template**:

```text
I'll provide you with some relevant information to help answer the user's question.

CONTEXT:
{context}

With this information in mind, please respond to the following query:
{query}

Only use information from the CONTEXT. If the CONTEXT doesn't contain enough information to answer fully, acknowledge this limitation.
```

When a user asks "How do I implement authentication in FastAPI?" while referencing a documentation file with `#fastapi-docs`, here's how the template mechanism works:

1. **Knowledge Retrieval**: The system searches the referenced document for information about FastAPI authentication.

2. **Template Population**:

```text
I'll provide you with some relevant information to help answer the user's question.

CONTEXT:
FastAPI supports several authentication methods including:
- OAuth2 with Password (and hashing), Bearer with JWT tokens
- OAuth2 with Password (and hashing), Bearer with JWT tokens + database users
- HTTP Basic
- API Keys in headers, query parameters, or cookies
- ...etc...

With this information in mind, please respond to the following query:
How do I implement authentication in FastAPI?

Only use information from the CONTEXT. If the CONTEXT doesn't contain enough information to answer fully, acknowledge this limitation.
```

3. **System Prompt Integration**: Finally, the chat-level system prompt is added at the beginning:

```text
For this conversation, act as a Python expert focusing on FastAPI development. Provide inline comments for all code examples.

I'll provide you with some relevant information to help answer the user's question.
...
```

This combined prompt is what gets sent to the language model. The template structure ensures that the model receives information in a consistent format that maximizes its understanding of the task.

By carefully designing these templates and controlling the information flow into the context window, you create a structured environment for the language model that helps shape responses according to user needs while making optimal use of both system instructions and retrieved knowledge.​​​​​​​​​​​​​​​​

## How Knowledge Integration Works

Implements Retrieval Augmented Generation (RAG) to enhance the model's capabilities by incorporating context from diverse sources. This works by retrieving relevant information from documents, combining it with a predefined RAG template, and then prefixing this to the user's prompt.

The technical implementation follows this workflow:

1. **Document Processing**:
   - Documents are uploaded to the Documents section of the Workspace
   - These documents are then processed into chunks and embedded into a vector database 
   - The system stores both the original documents and their chunked/embedded version
1. **Vector Database Integration**:
   - Consider Open WebUI's RAG implementation defined in specific files: retrieval/vector/main.py (interface for vector database interaction) and retrieval/vector/connector.py (selects the specific vector database client). 
   - It supports multiple vector database backends like Chroma and Milvus

3. **Retrieval Process During Chat**:
   - Triggers the RAG pipeline based on context
   - The system performs hybrid search (combining BM25 text search with vector embedding similarity) 
   - Retrieved chunks are reranked based on relevance
   - These chunks are then integrated into the prompt using a RAG template


## Document Processing: Foundation of Effective RAG

Document processing transforms raw content into machine-understandable representations that enable accurate information retrieval.

### Advanced Chunking Strategies

The chunking strategy significantly impacts RAG performance. While the simplest approach is splitting text by character count, more sophisticated methods include splitting by tokens, sentences, paragraphs, or HTML headers. For code documents, using Abstract Syntax Tree (AST) parsers is recommended to maintain meaningful code chunks.

Modern chunking approaches prioritize semantic coherence over arbitrary size limits:

```python
def semantic_chunking(document, min_size=100, max_size=1000):
    """
    Split document into semantically meaningful chunks using natural boundaries
    """
    # Extract all potential boundary points (paragraphs, headers, etc.)
    boundaries = find_semantic_boundaries(document)
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for segment in boundaries:
        segment_size = len(segment)
        
        # Case 1: Segment fits within current chunk size limits
        if current_size + segment_size <= max_size:
            current_chunk.append(segment)
            current_size += segment_size
            
        # Case 2: Segment is too large by itself, needs splitting
        elif segment_size > max_size:
            # If we have content in current_chunk, finalize it
            if current_chunk:
                chunks.append(''.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Split large segment into smaller pieces
            subsegments = recursive_split(segment, max_size)
            chunks.extend(subsegments)
            
        # Case 3: Adding segment would exceed max_size
        else:
            # Finalize current chunk
            if current_size >= min_size:
                chunks.append(''.join(current_chunk))
            
            # Start new chunk with this segment
            current_chunk = [segment]
            current_size = segment_size
    
    # Add final chunk if it has content
    if current_chunk and current_size >= min_size:
        chunks.append(''.join(current_chunk))
        
    return chunks
```

**Best Practices:**

1. **Hierarchical Chunking**: Create multiple granularity levels to allow for both precise and context-rich retrieval.

2. **Overlap Strategy**: Include context overlap between chunks to maintain coherence when retrieving information that crosses chunk boundaries.

3. **Document Structure Awareness**: Respect natural document structures like sections, subsections, and paragraphs when chunking.

4. **Dynamic Chunk Sizing**: Adjust chunk size based on document type - technical documents may benefit from smaller chunks while narrative content often needs larger chunks.

### Metadata Enrichment

Adding metadata to document chunks significantly enhances retrieval effectiveness by enabling filtering and providing contextual information.

```python
def extract_metadata(document, chunk_text, chunk_index):
    """
    Extract rich metadata from document and chunk
    """
    # Basic metadata
    metadata = {
        "chunk_id": f"{document.id}_{chunk_index}",
        "document_id": document.id,
        "document_title": document.title,
        "source": document.source,
        "creation_date": document.creation_date,
        "last_modified": document.last_modified,
        "chunk_index": chunk_index,
        "total_chunks": document.total_chunks,
    }
    
    # Advanced metadata extraction
    metadata.update({
        "estimated_reading_time": estimate_reading_time(chunk_text),
        "language": detect_language(chunk_text),
        "content_type": classify_content_type(chunk_text),
        "named_entities": extract_entities(chunk_text),
        "complexity_score": calculate_complexity(chunk_text),
        "keywords": extract_keywords(chunk_text),
        "parent_section": identify_parent_section(document, chunk_text),
    })
    
    return metadata
```

**Best Practices:**

1. **Hierarchical Context**: Track document structure through metadata (chapter, section, subsection).

2. **Domain-Specific Metadata**: Add industry-specific metadata like legal document jurisdiction or medical document specialization.

3. **Cross-References**: Track relationships between chunks and documents to enable broader context retrieval.

## Vector Database Integration: The Retrieval Engine

The vector database is the technical backbone of any RAG system, storing and indexing embeddings for efficient similarity search.

### Embedding Model Selection

Selecting the appropriate embedding model is crucial for RAG performance. The MTEB Leaderboard on Hugging Face is a good starting point, particularly focusing on the Retrieval Average column which represents NDCG@10 scores across datasets. 

When selecting an embedding model, consider vector dimension, average retrieval performance, and model size. Although embedding APIs provide ease of use, they involve trade-offs such as potential scaling limitations.

```python
def select_embedding_model(data_domain, retrieval_requirements):
    """
    Select optimal embedding model based on domain and requirements
    """
    # Define important selection criteria
    criteria = {
        "retrieval_performance": 0.7,  # Weight for retrieval benchmark scores
        "inference_speed": 0.2,        # Weight for inference latency
        "model_size": 0.1,             # Weight for model size (smaller is better for deployment)
    }
    
    # Candidate models with their characteristics
    candidates = {
        "openai-text-embedding-3-large": {
            "retrieval_performance": 0.95,
            "inference_speed": 0.6,
            "model_size": 0.4,
            "dimension": 3072,
            "suitable_domains": ["general", "technical", "creative", "finance"],
            "hosting_options": ["api-only"]
        },
        "voyage-2": {
            "retrieval_performance": 0.90,
            "inference_speed": 0.7,
            "model_size": 0.5,
            "dimension": 1024,
            "suitable_domains": ["general", "conversational", "commerce"],
            "hosting_options": ["api-only"]
        },
        "bge-large-en-v1.5": {
            "retrieval_performance": 0.82,
            "inference_speed": 0.8,
            "model_size": 0.7,
            "dimension": 1024,
            "suitable_domains": ["general", "factual", "technical"],
            "hosting_options": ["api", "self-hosted"]
        }
        # Add more models as needed
    }
    
    # Calculate scores for each model
    scores = {}
    for model, attributes in candidates.items():
        # Check domain compatibility
        if data_domain not in attributes["suitable_domains"]:
            continue
            
        # Calculate weighted score
        score = (
            criteria["retrieval_performance"] * attributes["retrieval_performance"] +
            criteria["inference_speed"] * attributes["inference_speed"] +
            criteria["model_size"] * attributes["model_size"]
        )
        
        scores[model] = score
    
    # Return highest scoring model
    return max(scores.items(), key=lambda x: x[1])[0]
```

**Best Practices:**

1. **Domain-Specific Evaluation**: Always test embedding models on your specific data domain, as general benchmarks may not reflect your use case.

2. **Dimension Considerations**: Dense embeddings with higher dimensions often capture more semantic nuance but require more storage and computation resources.

3. **Multi-Model Approach**: Consider using different embedding models for different content types (code, technical documentation, conversational content).

### Advanced Search Techniques

Modern RAG systems go beyond simple vector similarity search to improve retrieval quality:

```python
def hybrid_search(query, collection, config):
    """
    Implement hybrid search combining vector similarity and keyword-based approaches
    """
    # Get query embedding
    query_embedding = get_embedding(query)
    
    # 1. Vector similarity search
    vector_results = vector_db.similarity_search(
        collection=collection,
        query_vector=query_embedding,
        top_k=config["VECTOR_TOP_K"]
    )
    
    # 2. BM25 keyword search 
    bm25_results = text_index.search(
        collection=collection,
        query=query,
        top_k=config["BM25_TOP_K"]
    )
    
    # 3. Optional: Filter by metadata if specified
    if config.get("METADATA_FILTERS"):
        vector_results = apply_metadata_filters(vector_results, config["METADATA_FILTERS"])
        bm25_results = apply_metadata_filters(bm25_results, config["METADATA_FILTERS"])
    
    # 4. Combine results with weighted fusion
    combined_results = {}
    alpha = config.get("HYBRID_ALPHA", 0.7)  # Weight for vector search
    
    # Add vector search results with appropriate weight
    for result in vector_results:
        doc_id = result["id"]
        combined_results[doc_id] = {
            "score": result["score"] * alpha,
            "content": result["content"],
            "metadata": result["metadata"]
        }
    
    # Add BM25 results with appropriate weight
    for result in bm25_results:
        doc_id = result["id"]
        if doc_id in combined_results:
            # If already in results, add weighted BM25 score
            combined_results[doc_id]["score"] += result["score"] * (1 - alpha)
        else:
            # If not in results, add with BM25 score
            combined_results[doc_id] = {
                "score": result["score"] * (1 - alpha),
                "content": result["content"],
                "metadata": result["metadata"]
            }
    
    # 5. Cross-encoder reranking for top candidates
    if config.get("USE_RERANKER", False):
        reranker_candidates = sorted(
            combined_results.values(), 
            key=lambda x: x["score"], 
            reverse=True
        )[:config.get("RERANK_TOP_K", 20)]
        
        reranked_results = rerank_results(query, reranker_candidates, config)
        return reranked_results
    
    # Sort by final score and return top results
    sorted_results = sorted(
        combined_results.values(), 
        key=lambda x: x["score"], 
        reverse=True
    )[:config.get("FINAL_TOP_K", 10)]
    
    return sorted_results
```

**Best Practices:**

1. **Hybrid Retrieval**: Combine vector search with traditional methods like BM25 text search for improved results. Hybrid search balances statistical keyword matching with semantic understanding. 

2. **Reranking**: Implement two-stage retrieval with initial broad candidate generation followed by more precise cross-encoder reranking.

3. **Relevance Thresholds**: Apply minimum score thresholds to filter out low-relevance results that might harm LLM performance.

4. **Context Window Management**: Dynamically adjust the number of retrieved documents based on their length to optimize context window usage.

## Retrieval Process During Chat: The User Experience

The retrieval component integrates into the chat flow to seamlessly enhance LLM responses without disrupting user experience.

### Query Processing

Modern query processing goes beyond direct retrieval:

```python
def process_query(user_query, chat_history=None, user_context=None):
    """
    Process user query for optimal retrieval
    """
    # 1. Query understanding and classification
    query_intent = classify_query_intent(user_query, chat_history)
    
    if query_intent == "INFORMATIONAL":
        # For fact-based queries, enhance retrieval
        search_strategy = "thorough"
    elif query_intent == "CONVERSATIONAL":
        # For chat-like interactions, optimize for relevance
        search_strategy = "contextual"
    elif query_intent == "COMMAND":
        # For action-oriented queries, minimal retrieval
        search_strategy = "minimal"
    else:
        # Default to balanced approach
        search_strategy = "balanced"
    
    # 2. Query expansion/reformulation for better retrieval
    if search_strategy in ["thorough", "balanced"]:
        expanded_query = expand_query(user_query, chat_history)
    else:
        expanded_query = user_query
    
    # 3. Generate embeddings
    query_embedding = get_embedding(expanded_query)
    
    # 4. Determine search parameters based on strategy
    search_params = get_search_params(search_strategy, user_context)
    
    return {
        "original_query": user_query,
        "processed_query": expanded_query,
        "embedding": query_embedding,
        "search_strategy": search_strategy,
        "search_params": search_params
    }
```

**Best Practices:**

1. **Query Understanding**: Analyze query intent to customize retrieval approach.

2. **Query Reformulation**: Generate search-optimized versions of user queries to improve retrieval by focusing on key terms. 

3. **Hypothetical Document Embeddings**: An advanced technique like HyDE first generates a hypothetical answer to a question, then uses that hypothetical document for embedding rather than the query itself. 

### RAG Template Construction

The RAG template is crucial for structuring how retrieved information is presented to the LLM:

```python
def create_rag_template(retrieved_chunks, query, template_type="standard"):
    """
    Create RAG prompt template integrating retrieved information
    """
    # Format retrieved chunks with source information
    formatted_chunks = []
    for i, chunk in enumerate(retrieved_chunks):
        source_info = f"[Source {i+1}: {chunk['metadata']['source']}]"
        formatted_chunks.append(f"{source_info}\n{chunk['content']}")
    
    # Combine all context
    context = "\n\n".join(formatted_chunks)
    
    # Select appropriate template based on type
    if template_type == "standard":
        template = f"""
        I'll provide you with information to help answer the user's question.

        CONTEXT:
        {context}

        USER QUESTION:
        {query}

        Based on the CONTEXT provided, please answer the USER QUESTION.
        If the answer cannot be determined from the CONTEXT, say so rather than speculating.
        Always cite your sources when providing specific information.
        """
    
    elif template_type == "analytical":
        template = f"""
        I'll provide you with information to help analyze the user's question.

        CONTEXT:
        {context}

        USER QUESTION:
        {query}

        Based on the CONTEXT provided, please analyze the USER QUESTION through these steps:
        1. Summarize the key information from all sources
        2. Compare and contrast any different perspectives
        3. Draw reasoned conclusions based only on the provided context
        4. Highlight any areas where more information would be needed
        
        Always cite your sources when providing specific information.
        """
    
    elif template_type == "critical":
        template = f"""
        I'll provide you with information to critically evaluate the user's question.

        CONTEXT:
        {context}

        USER QUESTION:
        {query}

        Based on the CONTEXT provided, please:
        1. Evaluate the evidence related to the USER QUESTION
        2. Identify any conflicting information or viewpoints
        3. Assess the reliability and relevance of the sources
        4. Provide a nuanced response that acknowledges complexity
        
        Always cite your sources when providing specific information.
        """
    
    return template
```

**Best Practices:**

1. **Explicit Instructions**: Provide clear directives to the LLM about how to use the retrieved context.

2. **Source Attribution**: Include source information for all retrieved chunks to enable proper citation.

3. **Context Boundaries**: Clearly separate retrieved information from the user query and instructions.

4. **Task-Specific Templates**: Use different templates optimized for different query types.

5. **Open Source Frameworks**:
   - LangChain and LlamaIndex documentation
   - Verba: Open Source Modular RAG Application
   - Haystack by Deepset for production RAG pipelines

## Hybrid Search in RAG Systems: In-Depth Implementation Guide

Hybrid search combines the strengths of vector-based semantic search with keyword-based retrieval techniques like BM25 to create more robust and accurate retrieval systems. Let's explore how this works in detail with practical implementation examples.

Hybrid search is a keyword-sensitive semantic search approach that combines vector search and keyword search algorithms to take advantage of their respective strengths while mitigating their limitations.

### Key Components and Their Roles

1. **Vector (Dense) Search**:
   - Uses embedding models to transform text into high-dimensional vectors
   - Captures semantic meaning and relationships between concepts
   - Excels at finding conceptually similar content even when keywords differ

2. **Keyword (Sparse) Search**:
   - Uses algorithms like BM25 or TF-IDF to find exact matches
   - Focuses on term frequency and document frequency
   - Excels at precise matching of specific terms, abbreviations, and names

3. **Fusion Mechanism**:
   - Combines results from both approaches into a unified ranking
   - Balances the precision of keyword search with the semantic understanding of vector search

## Implementation Approaches

Let's examine several implementations of hybrid search with detailed code examples:

### 1. Basic Parallel Retrieval with Score Fusion

```python
def hybrid_search(query, collection_name, config):
    """
    Perform hybrid search combining vector similarity and BM25
    
    Args:
        query (str): The user query
        collection_name (str): Name of the document collection
        config (dict): Configuration parameters
        
    Returns:
        list: Combined and ranked search results
    """
    # Step 1: Query text preprocessing
    preprocessed_query = preprocess_text(query)
    
    # Step 2: Generate query embedding
    query_embedding = embedding_model.embed_query(preprocessed_query)
    
    # Step 3: Perform vector similarity search
    vector_results = vector_db.similarity_search(
        collection_name=collection_name,
        query_vector=query_embedding,
        top_k=config.get("VECTOR_TOP_K", 20),
        filter=config.get("METADATA_FILTERS", None)
    )
    
    # Step 4: Perform BM25 keyword search
    bm25_results = bm25_index.search(
        collection_name=collection_name,
        query=preprocessed_query,
        top_k=config.get("BM25_TOP_K", 20),
        filter=config.get("METADATA_FILTERS", None)
    )
    
    # Step 5: Apply score fusion using a weighted combination
    combined_results = score_fusion(
        vector_results=vector_results,
        bm25_results=bm25_results,
        alpha=config.get("VECTOR_WEIGHT", 0.7)  # Weight for vector scores (0-1)
    )
    
    # Step 6: Return top results
    top_k = config.get("FINAL_TOP_K", 10)
    return combined_results[:top_k]
```

### 2. Score Fusion Implementation

There are multiple ways to combine the scores from different retrieval methods. Here are two popular techniques:

#### Linear Combination (Weighted Sum)

```python
def linear_score_fusion(vector_results, bm25_results, alpha=0.7):
    """
    Combine vector and BM25 results using weighted sum of scores
    
    Args:
        vector_results (list): Results from vector search
        bm25_results (list): Results from BM25 search
        alpha (float): Weight for vector scores (0-1)
        
    Returns:
        list: Combined results sorted by final score
    """
    # Normalize scores from each method to [0, 1] range
    vector_max = max([r['score'] for r in vector_results]) if vector_results else 1.0
    bm25_max = max([r['score'] for r in bm25_results]) if bm25_results else 1.0
    
    combined_docs = {}
    
    # Process vector results
    for result in vector_results:
        doc_id = result['id']
        normalized_score = result['score'] / vector_max if vector_max > 0 else 0
        combined_docs[doc_id] = {
            'document': result['document'],
            'vector_score': normalized_score,
            'bm25_score': 0,
            'final_score': alpha * normalized_score
        }
    
    # Process BM25 results and combine with vector results
    for result in bm25_results:
        doc_id = result['id']
        normalized_score = result['score'] / bm25_max if bm25_max > 0 else 0
        
        if doc_id in combined_docs:
            # Document exists in vector results
            combined_docs[doc_id]['bm25_score'] = normalized_score
            combined_docs[doc_id]['final_score'] += (1 - alpha) * normalized_score
        else:
            # Document only in BM25 results
            combined_docs[doc_id] = {
                'document': result['document'],
                'vector_score': 0,
                'bm25_score': normalized_score,
                'final_score': (1 - alpha) * normalized_score
            }
    
    # Convert to list and sort by final score
    results_list = list(combined_docs.values())
    results_list.sort(key=lambda x: x['final_score'], reverse=True)
    
    return results_list
```

#### Reciprocal Rank Fusion (RRF)

Reciprocal Rank Fusion (RRF) is a popular technique for combining results from different retrieval methods. Instead of directly combining scores, RRF uses the rank positions of documents in each result list.

```python
def reciprocal_rank_fusion(vector_results, bm25_results, k=60):
    """
    Combine results using Reciprocal Rank Fusion
    
    Args:
        vector_results (list): Results from vector search
        bm25_results (list): Results from BM25 search
        k (int): Constant to stabilize scores for low ranks
        
    Returns:
        list: Combined results sorted by RRF score
    """
    # Create dictionaries with document IDs as keys and ranks as values
    vector_ranks = {result['id']: idx + 1 for idx, result in enumerate(vector_results)}
    bm25_ranks = {result['id']: idx + 1 for idx, result in enumerate(bm25_results)}
    
    # Get all unique document IDs
    all_doc_ids = set(vector_ranks.keys()).union(set(bm25_ranks.keys()))
    
    # Calculate RRF scores
    rrf_scores = {}
    for doc_id in all_doc_ids:
        # Get ranks (default to max possible rank + 1 if not in results)
        v_rank = vector_ranks.get(doc_id, len(vector_results) + 1)
        b_rank = bm25_ranks.get(doc_id, len(bm25_results) + 1)
        
        # Calculate RRF score: 1/(k + rank) for each method
        rrf_score = (1 / (k + v_rank)) + (1 / (k + b_rank))
        
        # Find the document in either result list
        doc = next((r['document'] for r in vector_results if r['id'] == doc_id), 
                  next((r['document'] for r in bm25_results if r['id'] == doc_id), None))
        
        rrf_scores[doc_id] = {
            'document': doc,
            'vector_rank': v_rank,
            'bm25_rank': b_rank,
            'rrf_score': rrf_score
        }
    
    # Convert to list and sort by RRF score
    results_list = list(rrf_scores.values())
    results_list.sort(key=lambda x: x['rrf_score'], reverse=True)
    
    return results_list
```

## Beyond Basic Hybrid: Advanced Techniques

### Two-Stage Hybrid Search

A more sophisticated approach uses a sequential process: Step 1: BM25 quickly fetches documents with the search keywords. Step 2: VectorDB digs deeper to find contextually related documents. Step 3: The Ensemble Retriever runs both systems, combines their findings, and reranks the results.

```python
def two_stage_hybrid_search(query, collection_name, config):
    """
    Perform two-stage hybrid search with initial BM25 filtering followed by 
    vector similarity ranking for enhanced precision
    
    Args:
        query (str): User query
        collection_name (str): Name of document collection
        config (dict): Configuration parameters
        
    Returns:
        list: Final ranked results
    """
    # Step 1: BM25 retrieval to get initial candidate set
    bm25_candidates = bm25_index.search(
        collection_name=collection_name,
        query=query,
        top_k=config.get("BM25_CANDIDATES", 100)
    )
    
    # Early return if no results from BM25
    if not bm25_candidates:
        return []
    
    # Extract document IDs for filtering vector search
    candidate_ids = [doc['id'] for doc in bm25_candidates]
    
    # Step 2: Get query embedding for vector search
    query_embedding = embedding_model.embed_query(query)
    
    # Step 3: Perform vector search on the BM25 candidate set
    reranked_results = vector_db.similarity_search(
        collection_name=collection_name,
        query_vector=query_embedding,
        filter={"id": {"$in": candidate_ids}},
        top_k=config.get("FINAL_TOP_K", 10)
    )
    
    return reranked_results
```

### Cross-Encoder Reranking

For even higher precision, implement a cross-encoder reranking step:

```python
def rerank_with_cross_encoder(query, results, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
    """
    Rerank results using a cross-encoder model for higher precision
    
    Args:
        query (str): Original query
        results (list): Initial search results
        model_name (str): Name of cross-encoder model
        
    Returns:
        list: Reranked results
    """
    # Initialize cross-encoder
    from sentence_transformers import CrossEncoder
    cross_encoder = CrossEncoder(model_name)
    
    # Prepare pairs for scoring
    pairs = [(query, result['document']) for result in results]
    
    # Score all pairs
    scores = cross_encoder.predict(pairs)
    
    # Add scores to results
    for i, score in enumerate(scores):
        results[i]['cross_encoder_score'] = float(score)
    
    # Sort by cross-encoder score
    reranked_results = sorted(results, key=lambda x: x['cross_encoder_score'], reverse=True)
    
    return reranked_results
```

## Performance Benchmarking and Tuning

Research studies show that hybrid search consistently outperforms both BM25 and semantic similarity on retrieval datasets when using appropriate fusion methods. Azure AI Search benchmarks indicate that hybrid retrieval with semantic ranking offers significant benefits in search relevance.

To optimize your hybrid search implementation:

1. **Fusion Weight Tuning**:
   ```python
   def tune_fusion_weights(test_queries, ground_truth, collection_name):
       """
       Find optimal weights for hybrid search fusion
       
       Args:
           test_queries (list): List of test queries
           ground_truth (dict): Ground truth relevance judgments
           collection_name (str): Name of document collection
           
       Returns:
           float: Optimal alpha weight for vector search
       """
       best_score = 0
       best_alpha = 0.5
       
       # Test different weights
       for alpha in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
           config = {
               "VECTOR_TOP_K": 20,
               "BM25_TOP_K": 20,
               "FINAL_TOP_K": 10,
               "VECTOR_WEIGHT": alpha
           }
           
           total_ndcg = 0
           
           # Test each query
           for query_id, query_text in test_queries.items():
               results = hybrid_search(query_text, collection_name, config)
               
               # Calculate NDCG score
               ndcg_score = calculate_ndcg(
                   results=[r['id'] for r in results],
                   relevance=ground_truth[query_id],
                   k=10
               )
               
               total_ndcg += ndcg_score
           
           avg_ndcg = total_ndcg / len(test_queries)
           
           # Update best score if current is better
           if avg_ndcg > best_score:
               best_score = avg_ndcg
               best_alpha = alpha
               
           print(f"Alpha: {alpha}, Avg NDCG@10: {avg_ndcg:.4f}")
       
       print(f"\nBest alpha: {best_alpha}, Best NDCG@10: {best_score:.4f}")
       return best_alpha
   ```

2. **Document-specific Tuning**:
   
   Different document types may benefit from different fusion methods. For example, technical documents might need more weight on keyword search, while conceptual documents might benefit from higher vector search weights.

   ```python
   def get_document_type_weights(document_type):
       """
       Return recommended fusion weights based on document type
       
       Args:
           document_type (str): Type of document
           
       Returns:
           dict: Configuration weights
       """
       weights = {
           "technical_documentation": {
               "vector_weight": 0.4,  # More weight on keyword search for precision
               "bm25_weight": 0.6,
               "fusion_method": "linear"
           },
           "creative_content": {
               "vector_weight": 0.8,  # More weight on semantic search
               "bm25_weight": 0.2,
               "fusion_method": "linear"
           },
           "scientific_papers": {
               "vector_weight": 0.5,
               "bm25_weight": 0.5,
               "fusion_method": "rrf"  # RRF works well for scientific content
           },
           "product_catalog": {
               "vector_weight": 0.3,
               "bm25_weight": 0.7,  # More weight on exact matches for products
               "fusion_method": "linear"
           }
       }
       
       return weights.get(document_type, {
           "vector_weight": 0.5,
           "bm25_weight": 0.5,
           "fusion_method": "rrf"
       })
   ```

## Best Practices for Production Implementation

1. **Pre-computed BM25 Scores**:
   
   For large document collections, pre-compute and store BM25 statistics to improve query performance.

   ```python
   def precompute_bm25_stats(documents, collection_name):
       """
       Precompute BM25 statistics for a document collection
       
       Args:
           documents (list): List of documents
           collection_name (str): Name of collection
       """
       from rank_bm25 import BM25Okapi
       
       # Extract text from documents
       corpus = [doc['text'] for doc in documents]
       
       # Tokenize corpus
       tokenized_corpus = [doc.split() for doc in corpus]
       
       # Create BM25 index
       bm25 = BM25Okapi(tokenized_corpus)
       
       # Extract and store corpus-level statistics
       db.save_bm25_stats(
           collection_name=collection_name,
           avg_doc_length=bm25.avgdl,
           doc_count=len(corpus),
           term_frequencies=bm25.term_frequency,
           doc_frequencies=bm25.df,
           idf=bm25.idf
       )
       
       print(f"BM25 statistics precomputed and saved for collection {collection_name}")
   ```

2. **Vector Index Optimization**:
   
   Explicit sort orders override relevance-ranked results, so for hybrid search, avoid explicit sorting in your query to preserve the benefits of both similarity and BM25 relevance.

3. **Query-Time Settings**:
   
   Adapt the hybrid search strategy based on query characteristics:

   ```python
   def analyze_query_type(query):
       """
       Analyze query to determine optimal search strategy
       
       Args:
           query (str): User query
           
       Returns:
           dict: Configuration for this query type
       """
       query_length = len(query.split())
       has_quotes = '"' in query
       has_special_chars = bool(re.search(r'[^\w\s]', query))
       has_numbers = bool(re.search(r'\d', query))
       
       # Exact match queries (with quotes or short specific queries)
       if has_quotes or (query_length <= 3 and not has_special_chars):
           return {
               "VECTOR_WEIGHT": 0.2,  # More weight on keyword search
               "BM25_TOP_K": 30,
               "VECTOR_TOP_K": 10
           }
       
       # Numeric or code queries
       elif has_numbers or has_special_chars:
           return {
               "VECTOR_WEIGHT": 0.3,
               "BM25_TOP_K": 25,
               "VECTOR_TOP_K": 15
           }
       
       # Conceptual or long queries
       elif query_length > 10:
           return {
               "VECTOR_WEIGHT": 0.8,  # More weight on semantic search
               "BM25_TOP_K": 10,
               "VECTOR_TOP_K": 30
           }
       
       # Default balanced approach
       else:
           return {
               "VECTOR_WEIGHT": 0.5,
               "BM25_TOP_K": 20,
               "VECTOR_TOP_K": 20
           }
   ```

## Integrating with LLM Framework

Finally, here's how to integrate hybrid search with the RAG prompt template:

```python
def generate_rag_response(query, context, llm_model="gpt-3.5-turbo", system_prompt=None):
    """
    Generate response using retrieved context
    
    Args:
        query (str): User query
        context (list): Retrieved context from hybrid search
        llm_model (str): Name of LLM model
        system_prompt (str): Optional system prompt
        
    Returns:
        str: Generated response
    """
    # Format context for prompt
    formatted_context = "\n\n".join([
        f"Document {i+1} (Source: {doc['metadata'].get('source', 'Unknown')}): {doc['text']}"
        for i, doc in enumerate(context)
    ])
    
    default_system_prompt = """
    You are a helpful assistant that provides accurate information based on the given context.
    When answering the question, use only the information provided in the context.
    If the context doesn't contain the answer, acknowledge that you don't have enough information.
    Always cite your sources by referring to the document numbers.
    """
    
    system_prompt = system_prompt or default_system_prompt
    
    # Prepare prompt for LLM
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{formatted_context}\n\nQuestion: {query}"}
    ]
    
    # Call LLM API
    response = llm_client.chat.completions.create(
        model=llm_model,
        messages=messages,
        max_tokens=1000,
        temperature=0.3
    )
    
    return response.choices[0].message.content
```

## Conclusion

Implementing hybrid search in your RAG system combines the strengths of both semantic search and keyword-based retrieval. By properly configuring fusion methods, tuning weights, and implementing reranking, you can significantly improve information retrieval quality over either approach alone. This makes your RAG system more accurate, resilient to different query types, and better able to handle specialized terminology and exact matches.

For further reading, I recommend exploring:
1. LangChain's Ensemble Retrievers documentation
2. Weaviate's Hybrid Search implementation
3. Microsoft's Azure AI Search hybrid retrieval benchmarks
4. The "Reciprocal Rank Fusion" paper by Cormack et al.

## Citations

[1] "Optimizing RAG with Hybrid Search & Reranking", VectorHub by Superlinked. 

[2] "Hybrid Search Explained", Weaviate.

[3] "About hybrid search", Vertex AI, Google Cloud.

[4] "Hybrid Search: Combining BM25 and Semantic Search for Better Results with Langchain".

[5] "Hybrid search using both BGE and BM25", Issue #17, FlagOpen/FlagEmbedding.

[6] "Azure AI Search: Outperforming vector search with hybrid retrieval and reranking", Microsoft Community Hub.

[7] "Hybrid search - Azure AI Search", Microsoft Learn.​​​​​​​​​​​​​​​​


## Technical Architecture for Knowledge Integration

The knowledge integration process is surprisingly sophisticated:

1. **Embedding Models**:
   - For better RAG performance, users can install embedding models like paraphrase-multilingual directly in Ollama. 

2. **Chunking Strategies**:
   - RAG isn't appropriate for all document tasks - when you need summarization, translation, or file comparison, you might need full documents instead of chunks 
   - Chunking is used to divide documents into smaller sections, which helps the system zero in on relevant passages and reduces the token count the LLM needs to process 

3. **Knowledge Base Management**:
   - Different knowledge bases might require different prompting strategies for optimal results. There are discussions about implementing a system for managing multiple RAG prompts and associating them with specific knowledge bases. 
   - Architecture is modular enough that you could extend it to:
	   - Query a graph database instead of using the built-in vector search
	   - Return results from graph traversals as context
	   - Process complex relationships that exist in the 

## Further Reading and Resources

For those looking to deepen their understanding, here are key resources:

1. **Embedding Models and Evaluation**:
   - MTEB Leaderboard on Hugging Face for embedding model benchmarks
   - "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks" paper
   - LangChain's embedding documentation

2. **Vector Databases**:
   - Pinecone, Milvus, Weaviate, and Chroma documentation
   - "Vector Search for Developers" by Pinecone
   - "Practical Vector Search" online course

3. **Advanced RAG Techniques**:
   - "Enhancing RAG with Query Transformations" by LlamaIndex
   - "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" paper
   - "Recursive Retrieval Augmented Generation" by Google Research

4. **Research Papers**:
   - "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (original RAG paper)
   - "Improving Language Models by Retrieving from Trillions of Tokens" (RETRO paper)
   - "Large Language Models with Controllable Working Memory" for understanding context management

