#!/usr/bin/env python3

import argparse
import boto3


class TemplateGenerator:

    def __init__(self, bucket, log_level, out_path, region):
        self.bucket = bucket
        self.log_level = log_level
        self.out_path = out_path
        self.region = region
        self.s3_website = "https://s3-{}.amazonaws.com/{}/".format(self.region, self.bucket)
        self.bucket_conn = self.s3_bucket()
        self.obj_dict = {}
        self.template_gen()

    def s3_bucket(self):
        """
        establishes and connects to the bucket
        :return: s3 bucket object
        """
        s3 = boto3.resource('s3')
        return s3.Bucket(self.bucket)

    def parse_objects(self):
        """
        iterates through the objects in the given bucket
        :return: none, but updates self.obj_dict
        """
        for obj in self.bucket_conn.objects.filter(Prefix="images"):
            if obj.size != 0:
                obj_full_path = obj.key
                obj_file = obj.key.split("/")
                obj_album = obj_file[1]
                obj_key = obj_file[2]
                obj_url = self.s3_website + obj_full_path.replace(" ", "+")
                obj_thumb_url = obj_url.split("/")
                obj_thumb_url[4] = "thumbs"
                obj_thumb_url = "/".join(obj_thumb_url)
                try:
                    self.obj_dict[obj_album]["keys"].append({obj_key: {"obj_full_path": obj_full_path},
                                                                       "obj_url": obj_url,
                                                                       "obj_thumb_url": obj_thumb_url})
                except KeyError:
                    self.obj_dict.update({obj_album: {"keys":[obj_key]}})
            else:
                pass

        return self.obj_dict

    def template_gen(self):
        template_dict = self.parse_objects()


def main():
    TemplateGenerator(args.bucket, args.log_level, args.output_path, args.region)


if __name__ == "__main__":
    # Arguments for usability
    parser = argparse.ArgumentParser(description="Generates templates for phugo from an s3 bucket")
    parser.add_argument("bucket", help="s3 bucket to read from e.g. img.taylorm.cc")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "ERROR", "CRITICAL"],
                        default="ERROR", help="Chose the loglevel from the available choices; default is ERROR.")
    parser.add_argument("--output-path", default="pwd",
                        help="Choose the output directory, this would be the \"content\" directory.")
    parser.add_argument("--region", default="us-west-1",
                        help="Specify region so S3 full url is valid for object(s)")

    args = parser.parse_args()

    main()
