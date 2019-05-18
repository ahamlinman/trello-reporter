import boto3


def send_email(email_address, subject, body):
    ses = boto3.client("ses")
    return ses.send_email(
        Source=email_address,
        Destination={"ToAddresses": [email_address]},
        Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
    )
