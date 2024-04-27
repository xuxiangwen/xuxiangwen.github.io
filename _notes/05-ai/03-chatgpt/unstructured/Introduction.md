## Resource

- [unstructured github](https://github.com/Unstructured-IO/unstructured)
- [unstructured documentation](https://unstructured-io.github.io/unstructured/)
- **Unstructured API**
  - API Key: iQEOMjxOc9MICDRzdJxKgX8QUVhkuA
  - Base URL (for Unstructured client SDK): [https://eipi-bq662oxi.api.unstructuredapp.io](https://eipi-bq662oxi.api.unstructuredapp.io/)
  - Full URL (for direct API calls): https://eipi-bq662oxi.api.unstructuredapp.io/general/v0/general

## Product Offerings

### Unstructured API Services

- **Unstructured SaaS API**: A scalable, highly-optimized API service hosted on Unstructured’s infrastructure. Learn more and access the API here: [SaaS API](https://unstructured-io.github.io/unstructured/apis/saas_api.html).
- **Azure and AWS Marketplace APIs**: Enables deployment of the Unstructured API on cloud infrastructure. Access via [Azure Marketplace](https://unstructured-io.github.io/unstructured/apis/azure_marketplace.html) or [AWS Marketplace](https://unstructured-io.github.io/unstructured/apis/aws_marketplace.html).

### Enterprise Platform

- **Enterprise Platform**: Scheduled for launch in early 2024, this platform is designed to offer comprehensive enterprise-grade support and solutions.

### Open Source Solutions

- **Unstructured Core Library**: The open-source library offering core functionalities of Unstructured. Access it at the [unstructured GitHub repository](https://github.com/Unstructured-IO/unstructured).
- **Model Inference for Layout Parsing**: Specialized in model inference for layout parsing tasks. Explore this at the [unstructured-inference GitHub repository](https://github.com/Unstructured-IO/unstructured-inference).
- **Self Hosting API**: Offers an API for self-hosting purposes. More details can be found at the [unstructured-api GitHub repository](https://github.com/Unstructured-IO/unstructured-api).

## Quick Start

代码：[Getting Started on Google Colab](https://colab.research.google.com/drive/1U8VCjY2-x8c6y5TYMbSFtQGlQVFHCVIW#scrollTo=jZp37lfueaeZ)

### Installation in Linux

~~~
pip install "unstructured[all-docs]"
~~~



### Installation in Windows

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

### Instagram

## Document Elements

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

