# Trello Reporter

The Trello Reporter is a small app that reads cards from [Trello] lists, and
reports on any that haven't seen activity within a specified (per-list) time
window.

I originally created the reporter to help keep my Trello-based [GTD] workflow
on track. Thus, it's primarily designed to run on [AWS Lambda], be triggered by
scheduled CloudWatch events, and send email reports with Amazon SES. However,
it can also run locally and print reports directly to a terminal.

[Trello]: https://trello.com/
[GTD]: https://gettingthingsdone.com/
[AWS Lambda]: https://aws.amazon.com/lambda/

## Setup

0. Install [Pipenv](https://docs.pipenv.org/), then run `pipenv install` to
   pull down dependencies.
0. Get a [Trello API key and token](https://trello.com/app-key).

### Environment

The following environment variables must be defined:

* `TRELLO_KEY`: Your Trello API key, obtained via the link above.
* `TRELLO_TOKEN`: Your Trello API token, generated and authorized to access
  your account via the link above.

If you plan to send email reports from outside of AWS environments, you must
also [configure Boto 3][Boto 3] using environment variables or a credential /
config file.

[Boto 3]: https://boto3.readthedocs.io/en/latest/guide/configuration.html

### Configuration

The report configuration is a JSON object with the following structure:

* `emailAddress`: The email address to which the report should be sent. Ignored
  when emails are not in use.
* `subject`: The subject of the email. Ignored when emails are not in use.
* `heading`: A short text snippet that will be included at the top of the
  report.
* `lists`: An array of objects with the following structure:
  - `listId`: The ID of the Trello list to analyze.
  - `timeDelta`: The amount of time since last activity after which a card
    should be considered "old" and reported on. The fields of this object are
    directly passed as keyword arguments to [Python's `timedelta`
    constructor][timedelta].

In AWS Lambda, this object should be passed as event data to your Lambda
function. For example, in a CloudWatch Events rule, [use the Constant (JSON
text) option][CloudWatch setup] when configuring your function's input.

Outside of AWS Lambda, this configuration is picked up from `config.json` in
the current directory by default. A custom file can be specified on the command
line if desired.

[timedelta]: https://docs.python.org/3/library/datetime.html#datetime.timedelta
[CloudWatch setup]: https://aws.amazon.com/blogs/compute/simply-serverless-use-constant-values-in-cloudwatch-event-triggered-lambda-functions/

## Usage

With everything set up, simply run the following locally to generate a report:

```sh
pipenv run ./main.py
```

Use `-h` to see available arguments.

### AWS Lambda

Run `make` to create a `lambda-package.zip` containing the reporter and all
dependencies.

With that, a _high-level_ overview of the Lambda function setup in the AWS
Console is as follows:

* **Code entry type:** Upload a .ZIP file
* **Function package:** (upload the generated file from above; it should be
  small enough that you won't need to upload to S3)
* **Runtime:** Python 3.6
* **Handler:** `main.lambda_handler`
* **Environment variables:** `TRELLO_KEY` and `TRELLO_TOKEN` from above
* **Execution role:** Create an IAM role that allows the SES `SendEmail` action

With the function set up, you can configure a trigger like CloudWatch Events.
