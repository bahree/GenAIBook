# Form recognizer (now called Document Intelligence) isn't available on conda yet, so we'll use pip
# pip install azure-ai-formrecognizer 
# conda install -c conda-forge azure-core 
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

#endpoint = "YOUR_FORM_RECOGNIZER_ENDPOINT"
#key = "YOUR_FORM_RECOGNIZER_KEY"
endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
key = os.getenv("DOC_INTELLIGENCE_KEY")

# sample document
pdf_file = "./data/test.pdf"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Open the file in binary mode
with open(pdf_file, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", f.read())
result = poller.result()

# poller = document_analysis_client.begin_analyze_document_from_url(
#     "prebuilt-layout", pdf_file)
# result = poller.result()

for style in enumerate(result.styles):
    print(
        "Document contains {} content".format(
         "handwritten" if style.is_handwritten else "no handwritten"
        )
    )

for page in result.pages:
    for line_idx, line in enumerate(page.lines):
        print(
         "...Line # {} has text content '{}'".format(
        line_idx,
        line.content.encode("utf-8")
        )
    )

    for selection_mark in page.selection_marks:
        print(
         "...Selection mark is '{}' and has a confidence of {}".format(
         selection_mark.state,
         selection_mark.confidence
         )
    )

for table_idx, table in enumerate(result.tables):
    print(
        "Table # {} has {} rows and {} columns".format(
        table_idx, table.row_count, table.column_count
        )
    )
        
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
            cell.row_index,
            cell.column_index,
            cell.content.encode("utf-8"),
            )
        )

print("----------------------------------------")
