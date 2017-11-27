#!/usr/bin/env python3

import argparse
import botocore
import boto3


class TemplateGenerator:

    def __init__(self, bucket, log_level):
        self.bucket = bucket
        self.log_level = log_level
        self.bucket_conn = self.s3_bucket()

        self.template_gen()

    def s3_bucket(self):
        """
        establishes and connects to the bucket
        :param bucket: s3 bucket to access
        :return: s3 bucket object
        """
        s3 = boto3.resource('s3')
        return s3.Bucket(self.bucket)

    def iter_objects(self):
        """
        iterates through the objects in the given bucket
        :return:
        """
        for obj in self.bucket_conn.objects.filter(Prefix="images"):
            print(obj)

    def template_gen(self):
        self.iter_objects()
        

def main():
    TemplateGenerator(args.bucket, args.log_level)


if __name__ == "__main__":
    # Optional arguments for usability
    parser = argparse.ArgumentParser(description="Generates templates for phugo from an s3 bucket")
    parser.add_argument("bucket", help="s3 bucket to read from e.g. img.taylorm.cc")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "ERROR", "CRITICAL"],
                        default="ERROR", help="Chose the loglevel from the available choices; default is ERROR.")

    args = parser.parse_args()

    main()
