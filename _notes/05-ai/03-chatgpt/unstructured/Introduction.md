## Skills

### Resource

- [unstructured github](https://github.com/Unstructured-IO/unstructured)
- [unstructured documentation](https://unstructured-io.github.io/unstructured/)

### Product Offerings

#### Unstructured API Services

- **Unstructured SaaS API**: A scalable, highly-optimized API service hosted on Unstructured’s infrastructure. Learn more and access the API here: [SaaS API](https://unstructured-io.github.io/unstructured/apis/saas_api.html).
- **Azure and AWS Marketplace APIs**: Enables deployment of the Unstructured API on cloud infrastructure. Access via [Azure Marketplace](https://unstructured-io.github.io/unstructured/apis/azure_marketplace.html) or [AWS Marketplace](https://unstructured-io.github.io/unstructured/apis/aws_marketplace.html).

#### Enterprise Platform

- **Enterprise Platform**: Scheduled for launch in early 2024, this platform is designed to offer comprehensive enterprise-grade support and solutions.

#### Open Source Solutions

- **Unstructured Core Library**: The open-source library offering core functionalities of Unstructured. Access it at the [unstructured GitHub repository](https://github.com/Unstructured-IO/unstructured).
- **Model Inference for Layout Parsing**: Specialized in model inference for layout parsing tasks. Explore this at the [unstructured-inference GitHub repository](https://github.com/Unstructured-IO/unstructured-inference).
- **Self Hosting API**: Offers an API for self-hosting purposes. More details can be found at the [unstructured-api GitHub repository](https://github.com/Unstructured-IO/unstructured-api).

### Quick Start

代码：[Getting Started on Google Colab](https://colab.research.google.com/drive/1U8VCjY2-x8c6y5TYMbSFtQGlQVFHCVIW#scrollTo=jZp37lfueaeZ)

#### Installation in Linux

~~~
pip install "unstructured[all-docs]"
~~~

#### Installation in Windows

This guide offers concise steps to swiftly install and validate your `unstructured` installation. For more comprehensive installation guide, please refer to [this page](http://localhost:63342/CHANGELOG.md/docs/build/html/installing.html).

1. **Installing the Python SDK**: You can install the core SDK using pip:

   ```
   pip install torch==2.1.2
   pip install pywin32
   pip install poppler
   pip install torchvision
   pip install huggingface-hub
   pip install layoutparser
   pip install unstructured
   ```

   Plain text files, HTML, XML, JSON, and Emails are immediately supported without any additional dependencies.

   If you need to process other document types, you can install the extras required by following the [Full Installation](https://unstructured-io.github.io/unstructured/installation/full_installation.html)

   For a complete set of extras catering to every document type, use:

   ```
   pip install "unstructured[all-docs]"
   ```

   

2. **System Dependencies**: Ensure the subsequent system dependencies are installed. Your requirements might vary based on the document types you’re handling:

   - libmagic-dev : Essential for filetype detection.
   - poppler-utils : Needed for images and PDFs.
   - tesseract-ocr : Essential for images and PDFs.
   - libreoffice : For MS Office documents.
   - pandoc : For EPUBs, RTFs, and Open Office documents. Please note that to handle RTF files, you need version 2.14.2 or newer. Running [this script](https://github.com/Unstructured-IO/unstructured/blob/main/scripts/install-pandoc.sh) will install the correct version for you.

#### Setting up `unstructured` for local inference

windows下安装好像有点问题。

#### Validating Installation

After installation, confirm the setup by executing the below Python code:

~~~powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/Unstructured-IO/unstructured/main/example-docs/example-10k.html -OutFile ./example-10k.html
Invoke-WebRequest -Uri https://raw.githubusercontent.com/Unstructured-IO/unstructured/main/example-docs/layout-parser-paper-fast.pdf -OutFile ./layout-parser-paper-fast.pdf
~~~

```python
from unstructured.partition.auto import partition
elements = partition(filename="example-docs/example-10k.html")
```

If you’ve opted for the “local-inference” installation, you should also be able to execute:

```
from unstructured.partition.auto import partition
elements = partition("example-docs/layout-parser-paper-fast.pdf")
```

The example documents in this section come from the [example-docs](https://github.com/Unstructured-IO/unstructured/tree/main/example-docs) directory in the `unstructured` repo.

### Document Elements

#### Document elements

Currently, the `unstructured` library supports the following element types:

- `type`
  - `FigureCaption`
  - `NarrativeText`
  - `ListItem`
  - `Title`
  - `Address`
  - `Table`
  - `PageBreak`
  - `Header`
  - `Footer`
  - `UncategorizedText`
  - `Image`
  - `Formula`
- `element_id`
- `metadata` - see: [Metadata page](https://unstructured-io.github.io/unstructured/metadata.html#metadata-label)
- `text`

#### Tables

For PDFs and images, table extraction requires a relatively expensive call to a table recognition model, and so for those document types table extraction is an option you need to enable. If you would like to extract tables for PDFs or images, pass in `infer_table_structure=True`. Here is an example (Note: this example requires the `pdf` extra. This can be installed with `pip install "unstructured[pdf]"`):

```
from unstructured.partition.pdf import partition_pdf

filename = "example-docs/layout-parser-paper.pdf"

elements = partition_pdf(filename=filename, infer_table_structure=True)
tables = [el for el in elements if el.category == "Table"]

print(tables[0].text)
print(tables[0].metadata.text_as_html)
```

> 报错
>
> ~~~
> This function will be deprecated in a future release and `unstructured` will simply use the DEFAULT_MODEL from `unstructured_inference.model.base` to set default model name
> ---------------------------------------------------------------------------
> AssertionError                            Traceback (most recent call last)
> File ~/miniconda3/envs/dev/lib/python3.10/site-packages/unstructured_pytesseract/pytesseract.py:461, in get_tesseract_version()
>     460     version = parse(str_version)
> --> 461     assert version >= TESSERACT_MIN_VERSION
>     462 except (AssertionError, InvalidVersion):
> 
> AssertionError: 
> 
> During handling of the above exception, another exception occurred:
> 
> SystemExit                                Traceback (most recent call last)
>     [... skipping hidden 1 frame]
> 
> Cell In[9], line 5
>       3 filename = "example-docs/layout-parser-paper.pdf"
> ----> 5 elements = partition_pdf(filename=filename, infer_table_structure=True)
>       6 tables = [el for el in elements if el.category == "Table"]
> ~~~
>

### Key Concepts

A RAG workflow can be broken down into the following steps:

1. **Data ingestion**: The first step is acquiring data from your relevant sources. We make this easy with our [source connectors](https://unstructured-io.github.io/unstructured/ingest/source_connectors.html).
2. **Data preprocessing and cleaning**: Once you’ve identified and collected your data sources, removing any unnecessary artifacts within the dataset is a good practice. At Unstructured, we have various tools for data processing in our [core functionalities](https://unstructured-io.github.io/unstructured/core.html).
3. **Chunking**: The next step is to break your text into digestible pieces for your LLM to consume. We provide the basic and context-aware chunking strategies. Please refer to the documentation [here](https://unstructured-io.github.io/unstructured/core/chunking.html).
4. **Embedding**: After chunking, you must convert the text into a numerical representation (vector embedding) that an LLM can understand. To use the various embedding models using Unstructured tools, please refer to [this page](https://unstructured-io.github.io/unstructured/core/embedding.html).
5. **Vector Database**: The next step is to choose a location for storing your chunked embeddings. There are many options for your vector database (AstraDB, ChromaDB, Clarifai, Milvus, Pinecone, Qdrant, Weaviate, and more). For complete list of Unstructured `Destination Connectors`, please visit [this page](https://unstructured-io.github.io/unstructured/ingest/destination_connectors.html).
6. **User Prompt**: Take the user prompt and grab the most relevant chunks of information in the vector database via similarity search.
7. **LLM Generation**: Once you’ve retrieved your relevant chunks, you pass the prompt + the context to the LLM for the LLM to generate a more accurate response.

### Example: Parsing a Document via SaaS API

~~~
# Make sure to replace the placeholders with the actual URL and API key from your email
# Include the path `/general/v0/general` in the URL.

curl -X 'POST' 'https://<REPLACE WITH THE URL IN THE EMAIL>' \
     -H 'accept: application/json'  \
     -H 'Content-Type: multipart/form-data'  \
     -H 'unstructured-api-key: <REPLACE WITH API KEY IN THE EMAIL>'  \
     -F 'files=@sample-docs/family-day.eml' 
~~~

### Partitioning

| Document Type                                                | Partition Function | Strategies                           | Table Support | Options                                                      |
| ------------------------------------------------------------ | ------------------ | ------------------------------------ | ------------- | ------------------------------------------------------------ |
| CSV Files (.csv)                                             | partition_csv      | N/A                                  | Yes           | None                                                         |
| E-mails (.eml)                                               | partition_eml      | N/A                                  | No            | Encoding; Max Partition; Process Attachments                 |
| E-mails (.msg)                                               | partition_msg      | N/A                                  | No            | Encoding; Max Partition; Process Attachments                 |
| EPubs (.epub)                                                | partition_epub     | N/A                                  | Yes           | Include Page Breaks                                          |
| Excel Documents (.xlsx/.xls)                                 | partition_xlsx     | N/A                                  | Yes           | None                                                         |
| HTML Pages (.html/.htm)                                      | partition_html     | N/A                                  | No            | Encoding; Include Page Breaks                                |
| Images (.png/.jpg/.jpeg/.tiff/.bmp/.heic)                    | partition_image    | “auto”, “hi_res”, “ocr_only”         | Yes           | Encoding; Include Page Breaks; Infer Table Structure; OCR Languages, Strategy |
| Markdown (.md)                                               | partition_md       | N/A                                  | Yes           | Include Page Breaks                                          |
| Org Mode (.org)                                              | partition_org      | N/A                                  | Yes           | Include Page Breaks                                          |
| Open Office Documents (.odt)                                 | partition_odt      | N/A                                  | Yes           | None                                                         |
| PDFs (.pdf)                                                  | partition_pdf      | “auto”, “fast”, “hi_res”, “ocr_only” | Yes           | Encoding; Include Page Breaks; Infer Table Structure; Max Partition; OCR Languages, Strategy |
| Plain Text (.txt/.text/.log)                                 | partition_text     | N/A                                  | No            | Encoding; Max Partition; Paragraph Grouper                   |
| PowerPoints (.ppt)                                           | partition_ppt      | N/A                                  | Yes           | Include Page Breaks                                          |
| PowerPoints (.pptx)                                          | partition_pptx     | N/A                                  | Yes           | Include Page Breaks                                          |
| ReStructured Text (.rst)                                     | partition_rst      | N/A                                  | Yes           | Include Page Breaks                                          |
| Rich Text Files (.rtf)                                       | partition_rtf      | N/A                                  | Yes           | Include Page Breaks                                          |
| TSV Files (.tsv)                                             | partition_tsv      | N/A                                  | Yes           | None                                                         |
| Word Documents (.doc)                                        | partition_doc      | N/A                                  | Yes           | Include Page Breaks                                          |
| Word Documents (.docx)                                       | partition_docx     | N/A                                  | Yes           | Include Page Breaks                                          |
| XML Documents (.xml)                                         | partition_xml      | N/A                                  | No            | Encoding; Max Partition; XML Keep Tags                       |
| Code Files (.js/.py/.java/ .cpp/.cc/.cxx/.c/.cs/ .php/.rb/.swift/.ts/.go) | partition_text     | N/A                                  | No            | Encoding; Max Partition; Paragraph Grouper                   |

### Metadata

All document types return the following metadata fields when the information is available from the source file:

| Metadata Field Name      | Short Description                                            | Details                                                      |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| filename                 | Filename                                                     |                                                              |
| file_directory           | File Directory                                               |                                                              |
| last_modified            | Last Modified Date                                           |                                                              |
| filetype                 | File Type                                                    |                                                              |
| coordinates              | XY Bounding Box Coordinates                                  | See notes below for further details about the bounding box.  |
| parent_id                | Element Hierarchy (Parent ID)                                | parent_id may be used to infer where an element resides within the overall hierarchy of a document. For instance, a NarrativeText element may have a Title element as a parent (a “sub-title”), which in turn may have another Title element as its parent (a “title). |
| category_depth           | Element Depth relative to other elements of the same category | Category depth is the depth of an element relative to other elements of the same category. It’s set by a document partitioner and enables the hierarchy post-processor to compute more accurate hierarchies. Category depth may be set using native document hierarchies, e.g. reflecting <H1>, <H2>, or <H3> tags within an HTML document or the indentation level of a bulleted list item in a Word document. |
| text_as_html             | HTML representation of extracted tables                      | Only applicable to table elements.                           |
| languages                | Document Languages                                           | At document level or element level. List is ordered by probability of being the primary language of the text. |
| emphasized_text_contents | Emphasized text (bold or italic) in the original document    |                                                              |
| emphasized_text_tags     | Tags on text that is emphasized in the original document     |                                                              |
| is_continuation          | True if element is a continuation of a previous element      | Only relevant for chunking, if an element was divided into two due to `max_characters`. |
| detection_class_prob     | Detection model class probabilities                          | From unstructured-inference, hi-res strategy.                |
