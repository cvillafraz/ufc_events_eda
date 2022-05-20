import os
import re
import logging
import boto3
import ufc_events_eda.utils.paths as path
from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO)


def _upload_file(file_path: str, bucket: str, object_name: str):
    """Upload a file to an S3 bucket.

    Args:
        file_path (str): Path to file to upload.
        bucket (str): Name of the S3 bucket.
        object_name (str): Name of the S3 object.
    """

    s3 = boto3.client("s3")
    try:
        s3.upload_file(
            file_path,
            bucket,
            object_name,
        )
        logging.info(f"Uploaded {object_name} to {bucket}.")
    except ClientError as e:
        logging.error(e)


def upload():
    """Upload all files in the reports/figures directory to Amazon S3."""

    for file in os.listdir(path.reports_figures_dir()):
        if re.search(r"html$|mp4$", file):
            _upload_file(str(path.reports_figures_dir(file)), "ufceventseda", file)
    logging.info("Upload complete.")


if __name__ == "_main__":
    logging.info("Uploading files to S3.")
    upload()
