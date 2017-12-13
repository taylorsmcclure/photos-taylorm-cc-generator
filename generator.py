#!/usr/bin/env python3

from datetime import datetime
from textwrap import dedent
import argparse
import boto3
import os


class TemplateGenerator:

    def __init__(self, bucket, log_level, out_path, region):
        self.bucket = bucket
        self.log_level = log_level
        self.out_path = out_path
        self.region = region
        self.s3_website = "https://s3-{}.amazonaws.com/{}/".format(self.region, self.bucket)
        self.bucket_conn = self.s3_bucket()
        self.obj_dict = {}
        # Only work in the specified output path
        os.chdir(self.out_path)
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
                    self.obj_dict[obj_album]["keys"].append({"key": obj_key,
                                                             "obj_full_path": obj_full_path,
                                                             "obj_url": obj_url,
                                                             "obj_thumb_url": obj_thumb_url})
                except KeyError:
                    self.obj_dict.update({obj_album: {"keys": [{"key": obj_key,
                                                                "obj_full_path": obj_full_path,
                                                                "obj_url": obj_url,
                                                                "obj_thumb_url": obj_thumb_url}]}})
            else:
                pass

    def template_gen(self):
        self.parse_objects()
        for album in self.obj_dict:
            index = self.make_index(album)
            self.write_index_file(album, index)

    def make_index(self, album):
        """
        Makes the index template for the album
        :param album: key for the album in self.obj_dict
        :return: Text template
        """
        albumthumb = self.obj_dict[album]["keys"][0]["obj_thumb_url"]
        date = datetime.now().strftime("%Y-%m-%d")
        header = "+++\nalbumthumb = \"{0}\"\ndate = \"{1}\"\ntitle = \"{2}\"\n+++\n".format(albumthumb, date, album)

        body = ""

        for key in self.obj_dict[album]["keys"]:
            full_path = key["obj_url"]
            thumb_path = key["obj_thumb_url"]
            photo_title = key["key"]

            # Using four curly brace so format doesn't try to replace it
            add_body = "{{{{< photo full=\"{0}\" thumb=\"{1}\" alt=\"{2}\" phototitle=\"{2}\" description=\"{2}\" >}}}}\n".format(full_path, thumb_path, photo_title)

            body = body + add_body

        index = header + body

        return index

    def write_index_file(self, album, index):
        """
        Creates album directory if not exists, then writes the _index.md to disk
        :param index: Text that needs to be in _index.md
        :return: nothing
        """
        path = self.out_path + "/" + album + "/_index.md"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            index = dedent(index)
            f.writelines(index)

    # TODO: Need to implement update to index if I add additional pictures to albums
    def update_index(self):
        pass


def main():
    TemplateGenerator(args.bucket, args.log_level, args.output_path, args.region)


if __name__ == "__main__":
    # Arguments for usability
    parser = argparse.ArgumentParser(description="Generates templates for phugo from an s3 bucket")
    parser.add_argument("bucket", help="s3 bucket to read from e.g. img.taylorm.cc")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "ERROR", "CRITICAL"],
                        default="ERROR", help="Chose the loglevel from the available choices; default is ERROR.")
    parser.add_argument("--output-path", default=os.getcwd(),
                        help="Choose the output directory, this would be the \"content\" directory.")
    parser.add_argument("--region", default="us-west-1",
                        help="Specify region so S3 full url is valid for object(s)")

    args = parser.parse_args()

    main()
