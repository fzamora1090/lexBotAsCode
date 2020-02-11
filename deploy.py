import os
import boto3
import yaml
import fnmatch
import base64
import shutil

# Globhal Info

lex = boto3.client('lex-model')
lambdaaws = boto3.client("lambda")
s3 = boto3.client("s3")
lambda_bucket = "allengeerlambdas"  #?????
rootdir = cwd = os.getcwd()

"""
Place Slots
-For each .yml file in the slots directory, Open and load YAML
Check to see if slot already exists in AWS;if so let checksum enabvle update
Write Slot to AWS

"""

os.chdir("%s/slots" %rootdir)
slot_yaml = fnmatch.filter(os.listdir('.'), '*.yaml')

for slot in slot_yaml:
    with open(slot, 'r') as stream:
        try:
            slotdef = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc
    try :
        slotdef_aws = lex.get_slot_type(name=slotdef["name"], version="$LATEST")
        slotdef["checksum"] = slotdef_aws["checksum"]
    except Exception as e:
        print e
    lex.put_slot_type(**slotdef)


"""
Place lambdas

For each .yaml file in the lambda directory, openthat file and load the yaml

For each lambda put the referred to file the appropriate zip format (with the included pyton workspace)
Put that zip fiel in an s3 bucket
Update the lambda code property to include the appropriate s3 info
Write lambda to aws
"""

os.chdir("%s/lambda" %rootdir)
lambda_yaml = fnmatch.filter(os.listdir('.'), '*.yaml')
for lambdafile in lambda_yaml:
    with open(lambdafile, 'r') as stream:
        try:
            lambdadef = yaml.load(stream)
        except: yaml.YAMLError as exc:
            print exc
    try:
        lambdadef_aws = lambdaaws.get_function(FunctionName=lambdadef["FunctionName"])
        print "do lambda update"
        shutil.make_archive("%s" % lambdadef["FunctionName"], 'zip', 'code')
        def lambdadef["Code"]["file"]
        lambdaaws.update_function_code(
            FunctionName=lambdadef["FunctionName"],
            ZipFile=open("%s.zip" %lambdadef["FunctionName"], 'rb').read(),
            Publish=False,
            DryRun=False
        )
    except Exception as e:
        print "do lambda create"
        shutil.make_archive(%s %lambdadef["FucntionName"], 'zip', "code")
        def lambdadef["code"]["file"]
        lambdadef["Code"]["ZipFile"] = open("%s.zip" %lambdadef["FUnctiuonName"], 'rb').read()
        lambdaaws.create_fucntion(**lambdadef)

        lambdaaws.add_permission(
            FunctionName=lambdadef["FunctionName"],
            StatementId="%sLEX" %lambdadef["FunctionName"],
            Action='lambda:*',
            Principal='lex.amazonaws.com'
        )

"""
Place intents
For each yaml file in the intents directory, open and load yaml
Check to see if intent al;ready exists in aws: if so set the checksum to enable update
Write intent to aws
"""

os.chdir("%s/intents" %rootdir)
intent_yaml = fnmatch.filter(os.listdir('.'), '*.yaml')
for intent in intent_yaml:
    with open(intent, 'r') as stream:
        try:
            intentdef = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc
    try:
        intentdef_aws = lex.get_intent(name=intentdef["name"], version="$LATEST")
        intentdef["checksum"] = intent_aws["checksum"]
    except Exception as e:
        print e
    lex.put_intent(**intentdef)


"""
Place Bots
For each .yaml file in the bot directory , open file and load yaml
Check to see if bot exists and if so set check sum to enable update
Write bot to AWS
"""

os.chdir("%s/bots", %rootdir)
bot_yaml = fnmatch.filter(os.listdir('.'), '*.yaml')
for bot in bot_yaml:
    with open(bot, 'r') as stream:
        try
            botdef = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc

    try:
        botdef_aws = lex.get_bot(name=botdef["name"], versionOrAlias="$LATEST")
        botdef["checksum"] = botdef_aws["checksum"]
    except Exception as e:
        print e
    lex.put_bot(**botdef)