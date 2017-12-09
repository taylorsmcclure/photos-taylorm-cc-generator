# PHUGO Static Template Generator

## Description

This python3 script utilizes boto3 to read all the image objects in a given bucket, then it will generate a markdown based template for the use of [phugo](https://github.com/aerohub/phugo). Example: [My Template](https://github.com/taylorsmcclure/photos-taylorm-cc/blob/master/content/California/_index.md)

## Perquisites

* A s3 read-only permitted access key and secret access key
* AWS CLI access configured through [credential/config files](http://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html)

## Usage

```
usage: generator.py [-h] [--log-level {DEBUG,INFO,ERROR,CRITICAL}]
                    [--output-path OUTPUT_PATH] [--region REGION]
                    bucket

Generates templates for phugo from an s3 bucket

positional arguments:
  bucket                s3 bucket to read from e.g. img.taylorm.cc

optional arguments:
  -h, --help            show this help message and exit
  --log-level {DEBUG,INFO,ERROR,CRITICAL}
                        Chose the loglevel from the available choices; default
                        is ERROR.
  --output-path OUTPUT_PATH
                        Choose the output directory, this would be the
                        "content" directory.
  --region REGION       Specify region so S3 full url is valid for object(s)
```

*TODO:* No meaningful logging or verbose options are available at this point
