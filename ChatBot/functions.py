import os
import sys
import json
import smtplib
import base64
# from django.core.mail import send_mail
# from django.template import Context
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import get_template
from datetime import datetime
from django.utils import timezone
from bson.objectid import ObjectId


def time_stamp_to_date_format(date_from_db):
    return datetime.fromtimestamp(
        date_from_db / 1000,
        tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def exception_handler(e):

    # To get exception information from sys package
    exc_type, exc_msg, exc_obj = sys.exc_info()
    # To get file name in which file raised exception
    fileDetails = os.path.split(exc_obj.tb_frame.f_code.co_filename)
    file_app = fileDetails[0].split(os.sep)[-1]
    file_name = fileDetails[1]
    # save_exceptions(
    #     e.args[0],
    #     "exception in %sth line in %s file of %s application" % (
    #         str(exc_obj.tb_lineno), file_name, file_app)
    # )
    print("exception", e.args[0])
    print(type(e.args[0]))
    exc_loc = "exception in %sth line in %s file of %s application" % (
            str(exc_obj.tb_lineno),
            file_name,
            str(file_app)
        )
    result = {
        # "message": "Something went wrong",
        "status": "failed",
        "exception_located_on": exc_loc,
        "message": e.args[0],
        "code": 400,
    }
    if 'FAILED SQL' in e.args[0]:
        import datetime
        print("datetime", datetime)
        print("ObjectId", ObjectId)
        pymongo_error = eval(
            e.args[0].split('Pymongo error:')[1].split('Version:')[0]
        )
        if '11000' in e.args[0]:
            write_errors = pymongo_error['writeErrors']
            if len(write_errors) == 1:
                if 'keyValue' in write_errors[0]:
                    keyValue = write_errors[0]['keyValue']
                    result["message"] = "Not accepted duplicate" \
                                        " '%s' Key entry '%s' " % (
                        list(keyValue.keys())[0],
                        list(keyValue.values())[0]
                    )
                else:
                    error_msg = write_errors[0]['errmsg'].split('dup key:')
                    key_info = error_msg[0].split(
                        'index:'
                    )[1].strip().split('_')
                    value_info = error_msg[1].replace(
                        '{', ''
                    ).replace('}', '').replace(
                        ' ', ''
                    ).replace(':', '').replace(
                        '\"', ''
                    )
                    result["message"] = "Not accepted duplicate '%s' Key" \
                                        " entry '%s' at index '%s'" % (
                        key_info[0], value_info, key_info[1]
                    )
            else:
                result["message"] = "Not accepted duplicate Key entries"
        else:
            result["message"] = "Database Query Error"
    # result = {
    #     "status": "failed",
    #     "message": "Technical error noticed",
    #     "code": 400,
    #     "statustext": "bad request"}
    return result


def process_api_exception(e, result):
    # print("exception args", e.args)
    # print("exception default details", e.default_detail)
    # print("exception default code", e.default_code)
    print("exception details", e.detail)
    # print("exception codes", e.get_codes())
    # print("exception full details", e.get_full_details())
    print("type of exception details", type(e.detail))
    if isinstance(e.detail, list):
        result["message"] = e.detail[0]
    else:
        print("ReturnDict" in str(type(e.detail)))
        # print("type of e detail", type(e.detail.items()))
        # print("e detail items", e.detail.items())
        result["message"] = "API Error"
        a = {}
        for key, value in e.detail.items():
            a.update({key: value[0]})
        result["response"] = a
    return result


def validate_required_fields(answer_fields_info):

    answer_fields = ""
    message = "please provide non-empty value to answers parameter."
    if answer_fields_info:
        try:
            if type(answer_fields_info) is not list:
                answer_fields = json.loads(answer_fields_info)
            else:
                answer_fields = answer_fields_info
        except Exception:
            pass
        message = "invalid format for answers"
        # whether to check answer_fields is json or not #
        if type(answer_fields) is list:
            answer_fields = list(filter(None, answer_fields))
            message = "answers must have at least one answer info"
            # whether to check answer_fields has atleast one element or not #
            if len(answer_fields) > 0:
                message = ""
                for i in range(0, len(answer_fields)):
                    ans = answer_fields[i]
                    id_condition = type(ans["id"]) is not int
                    ans_condition = "answer" in ans and ans["answer"] != ""
                    ans_condition1 = type(ans["answer"]) is not (str or list)
                    if "id" not in ans:
                        message = "id missing in 'answers'" \
                                  " at index " + str(i + 1)
                        break
                    elif "id" in ans and ans["id"] == "":
                        message = "id must not be empty in" \
                                  " 'answers' at index " + str(i + 1)
                        break
                    elif "id" in ans and ans["id"] != "" and id_condition:
                        message = "id must be integer value in" \
                                  " 'answers' at index " + str(i + 1)
                        break
                    if "answer" not in ans:
                        message = "answer missing in 'answers'" \
                                  " at index " + str(i + 1)
                        break
                    elif "answer" in ans and ans["answer"] == "":
                        message = "answer must not be empty in" \
                                  " 'answers' at index " + str(i + 1)
                        break
                    elif ans_condition and ans_condition1:
                        message = "answer must be either string or list" \
                                  " value in 'answers' at index " + str(i + 1)
                        break
    return message, answer_fields


def email_save(template, context, recipient, subject, result,
               event_by, status_id=None):
    try:
        if not status_id:
            EmailStatus(
                recipient=recipient,
                template=template,
                context=context,
                subject=subject,
                status=result["status"],
                created_by_id=event_by,
                date_created=datetime.now(tz=timezone.utc)
            ).save()
        else:
            if result["status"] == "success":
                EmailStatus.objects.filter(id=status_id).update(
                    status=result["status"],
                    updated_by_id=event_by,
                    date_modified=datetime.now(tz=timezone.utc)
                )
        result.update({"status": "success", "message": "data saved"})
    except Exception as e:
        print("exception:::", e)
        result["message"] = "invalid details"
    return result


def send_email(template_path, context, recipient, subject,
               event_by, status_id=None):
    result = {}
    try:
        recipients = [recipient]
        bcc = []
        # bcc = ['mark.mortimer@firstmatch.org']
        cc = ['firstmatch.adelphoi@gmail.com']
        # cc = []
        message = MIMEMultipart()
        template = get_template(template_path)  # getting template
        html = template.render(context)  # render html
        message["From"] = "information@firstmatch.org"
        message["To"] = recipient
        message["Subject"] = subject
        if cc:
            # Recommended for mass emails
            message["Cc"] = "%s\r\n" % ",".join(cc)
            recipients.extend(cc)
        if bcc:
            # Recommended for mass emails
            # message["Bcc"] = "%s\r\n" % ",".join(bcc)
            recipients.extend(bcc)
        part1 = MIMEText(html, 'html')
        message.attach(part1)
        smtp_server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        print("user", base64.b64decode(EMAIL_HOST_USER).decode())
        smtp_server.login(
            base64.b64decode(EMAIL_HOST_USER).decode(),
            base64.b64decode(EMAIL_HOST_PASSWORD).decode()
        )
        print("login done")
        email_status = smtp_server.sendmail(
            base64.b64decode(EMAIL_HOST_USER).decode(),
            recipients,
            message.as_string()
        )
        print("mail sent")
        print("email_status", email_status)
        smtp_server.close()

        # subject = 'Thank you for registering to our site'
        # message = ' it  means a world to us '
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = ['adinarayana.bandari@roundsqr.net', ]
        # send_mail(subject, message, email_from, recipient_list)
        result.update({"status": "success", "message": "mail sent"})
    except Exception as e:
        result.update(exception_handler(e))
    print("email result", result)
    email_save(
        template_path,
        context,
        recipient,
        subject,
        result,
        event_by,
        status_id)
    return result
