
"""
AI-Powered Data Pipeline Automation

ETL pipeline:
Extract -> Transform -> Validate -> Load

Author: Venkata Santhoshi Bommareddy
"""

import logging
from pathlib import Path
import pandas as pd
import numpy as np


logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class DataPipeline:

    def __init__(self, source_path, output_path):
        self.source_path = Path(source_path)
        self.output_path = Path(output_path)
        self.data = None

    def extract(self):
        logging.info("Starting extraction")

        self.data = pd.read_csv(self.source_path)

        logging.info(
            "Loaded %s records",
            len(self.data)
        )

    def transform(self):
        logging.info("Starting transformation")

        self.data.columns = (
            self.data.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        self.data.drop_duplicates(inplace=True)

        numeric_columns = self.data.select_dtypes(
            include=np.number
        ).columns

        for column in numeric_columns:
            self.data[column] = self.data[column].fillna(
                self.data[column].median()
            )

        text_columns = self.data.select_dtypes(
            include="object"
        ).columns

        for column in text_columns:
            self.data[column] = self.data[column].fillna(
                "Unknown"
            )

        logging.info("Transformation completed")

    def validate(self):

        report = {
            "records": len(self.data),
            "columns": len(self.data.columns),
            "missing_values": int(
                self.data.isnull().sum().sum()
            ),
            "duplicates": int(
                self.data.duplicated().sum()
            )
        }

        logging.info(report)

        return report

    def load(self):

        self.output_path.parent.mkdir(
            exist_ok=True
        )

        self.data.to_csv(
            self.output_path,
            index=False
        )

        logging.info("Output generated")


if __name__ == "__main__":

    pipeline = DataPipeline(
        "data/customer_transactions.csv",
        "output/processed_transactions.csv"
    )

    pipeline.extract()
    pipeline.transform()

    validation = pipeline.validate()

    print(validation)

    pipeline.load()
