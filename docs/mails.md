# mails

## SES Forewarding

### 1. Verify Domain

- Verify your `MX` name.
- Register `TXT` DNS record for `_amazonses.yourdomain.com`
- sometime later verified. 

### 2. Verify Sender Email Address

- Verify a sender email address.
- For testing in sandbox, some recipients also should be verified.

### 3. Recieving: Create `default-rule-set`

- `Create a New Rule Set` for the verified `MX` domain name. i.e. `mail.yourdomain.com`
- Select `S3 Action`.
- Register `S3 Bucket` , and give `Object key prefix` like `emails`.

### 4. Put forwarding configuration (`emails.json`)

Put folloing JSON under `s3://mail.yourdomain.com/email/`:

~~~json
{
   "sender": "master@yourdomain.com",
   "region_name": "us-west-2",
   "forwards": {
      "info@yourdomain.com": ["someone@gmai.com"]
   }
}
~~~

### 5. Create Lambda is SES region.

Create following Lambda funtion:

~~~py
import os
from shares import getLogger, mails


def lambda_handler(event, context):
    logger = getLogger()
    try:
        s3bucket = os.environ.get('SES_S3_BUCKET', '')
        s3prefix = os.environ.get('SES_S3_PREFIX', '')
        mails.forwardSes(event, context, s3bucket, s3prefix)
        return {}

    except Exception as e:
        logger.error(e)
        raise e
~~~

- register `Environment Variables`, `SES_S3_BUCKET` and `SES_S3_PREFIX`
