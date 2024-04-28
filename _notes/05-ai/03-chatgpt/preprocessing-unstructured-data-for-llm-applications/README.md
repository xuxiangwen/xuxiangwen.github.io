# [DLAI - Preprocessing Unstructured Data for LLM Applications (deeplearning.ai)](https://learn.deeplearning.ai/courses/preprocessing-unstructured-data-for-llm-applications/lesson/1/introduction)



## Overview of LLM Data Preprocessing

### Data Preprocessing and LLMs

- Retrieval Augmented Generation(RAG): A technique for grounding LLM responses on, validated external information.

- Contextual Integration: RAG apps load context into a database, then retrieve content to insert into a prompt.

- Industry Application:

  For industry user cases, relevant content comes from diverse document types, such as PDFs, Word docs, email, and webpages.

![image-20240425162446823](images/image-20240425162446823.png)

### Preprocessing Outputs

![image-20240425162009525](images/image-20240425162009525.png)

### Why is Data Preprocessing Hard?

![image-20240425162715318](images/image-20240425162715318.png)

## Normalizing the Content

 [Lesson_2_Student.ipynb](lesson2\Lesson_2_Student.ipynb) 

> `unstructured`是一个灵活的工具，可以处理各种文档格式，包括Markdown、、XML和HTML文档。

### Normalizing Diverse Documents

![image-20240425171546626](images/image-20240425171546626.png)

### Data Serialization

![image-20240425172121866](images/image-20240425172121866.png)

### HTML Page

![image-20240425172230646](images/image-20240425172230646.png)

### MS PowerPoint

![image-20240425172922671](images/image-20240425172922671.png)

### PDF with Complex Layout and Tables

![image-20240425173244799](images/image-20240425173244799.png)

## Metadata Extraction and Chunking

 [Lesson_3_Student.ipynb](lesson3\Lesson_3_Student.ipynb) 

> ChromaDB 是一款开源的向量数据库，专门为大型语言模型 (LLM) 应用而设计。它基于分布式 NoSQL 数据库 Apache Cassandra 构建，并提供了一个用户友好的 API 用于存储、索引和搜索向量嵌入。

### What is Metadata?

![image-20240426114006444](images/image-20240426114006444.png)

![image-20240426113834515](images/image-20240426113834515.png)

### Semantic Search for LLMs

面向LLM的语义搜索

![image-20240426114053745](images/image-20240426114053745.png)

![image-20240426114600756](images/image-20240426114600756.png)

### Hybrid Search

![image-20240426115017258](images/image-20240426115017258.png)

#### Example: Most Recent Information

Tell me the most recent information about the Super Bowl.

![image-20240426115036555](images/image-20240426115036555.png)

### Chunking

![image-20240426181249232](images/image-20240426181249232.png)

#### Chunking From Elements

![image-20240426181914580](images/image-20240426181914580.png)

#### Example

![image-20240426182134796](images/image-20240426182134796.png)

## Preprocessing PDFs and Images

### Document Image Analysis

![image-20240428175029370](images/image-20240428175029370.png)

### DIA Methods

![image-20240428175300053](images/image-20240428175300053.png)

### Document Layout Detection (DLD)

![image-20240428175542873](images/image-20240428175542873.png)

![image-20240428175650640](images/image-20240428175650640.png)

### Vision Transformers

![image-20240428175835753](images/image-20240428175835753.png)

![image-20240428180029627](images/image-20240428180029627.png)

### Advantages & Disadvantages

![image-20240428180210351](images/image-20240428180210351.png)

## Extracting Tables

### Table Extraction

![image-20240428204450456](images/image-20240428204450456.png)

### Table Transformers

![image-20240428204631429](images/image-20240428204631429.png)

![image-20240428204734847](images/image-20240428204734847.png)

### Vision Transformers

![image-20240428204900131](images/image-20240428204900131.png)

### OCR Postprocessing

![image-20240428205046145](images/image-20240428205046145.png)

## Build Your Own RAG Bot

