import os
import json
import time
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models.extractions import TextExtractionsV2, TextExtractionsV2ResultFormats
from ibm_watsonx_ai.metanames import TextExtractionsV2ParametersMetaNames
from ibm_watsonx_ai.helpers import DataConnection, S3Location

# Constants (inlined credentials/config)
API_KEY = "_PM3JFdQHVxWw6IEBUJyDCIzTK4kfN3j7lnzAo0hoe1r"
PROJECT_ID = "3c5e22f5-2904-426f-a28e-936123e30f5c"
ENDPOINT = "https://us-south.ml.cloud.ibm.com"
BUCKET = "bucket-xn1gsh6i2qfqpoc-rlongo"
COS_ACCESS_KEY_ID = "931df7b2de0946e5bedd06aed76bfeeb"
COS_SECRET_ACCESS_KEY = "9eab1c6d5e801b8d442f1381fd7de2105609046413f5d443"

# Paths
LOCAL_PDF = "../tests/data/first_page.pdf"
COS_INPUT_FILE = "input/first_page.pdf"
COS_OUTPUT_DIR = "output/"
COS_OUTPUT_FILE = "output/assembly.md"
LOCAL_OUTPUT = "./output/assembly.md"

def main():
    credentials = Credentials(
        api_key=API_KEY,
        url=ENDPOINT
    )

    client = APIClient(
        credentials=credentials,
        project_id=PROJECT_ID
    )

    # Create COS connection dynamically
    datasource_name = "bluemixcloudobjectstorage"
    connection_meta_props = {
        client.connections.ConfigurationMetaNames.NAME: f"Watsonx COS Connection",
        client.connections.ConfigurationMetaNames.DATASOURCE_TYPE: client.connections.get_datasource_type_id_by_name(datasource_name),
        client.connections.ConfigurationMetaNames.DESCRIPTION: f"Connection to external bucket: {BUCKET}",
        client.connections.ConfigurationMetaNames.PROPERTIES: {
            "bucket": BUCKET,
            "access_key": COS_ACCESS_KEY_ID,
            "secret_key": COS_SECRET_ACCESS_KEY,
            "url": "https://s3.us-south.cloud-object-storage.appdomain.cloud"
        }
    }

    connection_details = client.connections.create(meta_props=connection_meta_props)
    connection_asset_id = client.connections.get_id(connection_details)

    # Create document and result references
    document_reference = DataConnection(
        connection_asset_id=connection_asset_id,
        location=S3Location(bucket=BUCKET, path=COS_INPUT_FILE)
    )
    document_reference.set_client(client)
    document_reference.write(LOCAL_PDF)

    results_reference = DataConnection(
        connection_asset_id=connection_asset_id,
        location=S3Location(bucket=BUCKET, path=COS_OUTPUT_DIR)
    )

    # Set parameters using IBM SDK metanames
    parameters = {
        TextExtractionsV2ParametersMetaNames.MODE: "high_quality",
        TextExtractionsV2ParametersMetaNames.OCR_MODE: "enabled",
        TextExtractionsV2ParametersMetaNames.LANGUAGES: ["en"],
        TextExtractionsV2ParametersMetaNames.AUTO_ROTATION_CORRECTION: True,
        TextExtractionsV2ParametersMetaNames.CREATE_EMBEDDED_IMAGES: "enabled_placeholder",
        TextExtractionsV2ParametersMetaNames.OUTPUT_DPI: 72,
        TextExtractionsV2ParametersMetaNames.OUTPUT_TOKENS_AND_BBOX: True,
        TextExtractionsV2ParametersMetaNames.KVP_MODE: "invoice",
        "task_credentials_id": connection_asset_id
    }

    text_extractor = TextExtractionsV2(api_client=client, project_id=PROJECT_ID)

    print("Running WDU text extraction job...")
    result = text_extractor.run_job(
        document_reference=document_reference,
        results_reference=results_reference,
        parameters=parameters,
        result_formats=TextExtractionsV2ResultFormats.MARKDOWN
    )

    print("Raw job result response:")
    print(json.dumps(result, indent=2))
    job_id = text_extractor.get_job_id(extraction_details=result)
    print(f"Job submitted with ID: {job_id}")

    # Poll for completion
    while True:
        time.sleep(5)
        job_details = text_extractor.get_job_details(extraction_job_id=job_id)
        status = job_details["entity"]["results"]["status"]
        if status != "running":
            print("\n", status, sep="")
            break
        print(".", sep="", end="", flush=True)

    if status == "completed":
        print("Job completed. Downloading result...")
        results_ref = text_extractor.get_results_reference(extraction_job_id=job_id)
        os.makedirs(os.path.dirname(LOCAL_OUTPUT), exist_ok=True)
        results_ref.download_folder(local_dir=os.path.dirname(LOCAL_OUTPUT))
        print(f"Output saved to: {LOCAL_OUTPUT}")
        with open(LOCAL_OUTPUT, encoding="utf-8") as f:
            print(f.read(1000))
    else:
        print("Job failed. Fetching full job details from Watsonx...")
        print(json.dumps(job_details, indent=2))

if __name__ == "__main__":
    main()
