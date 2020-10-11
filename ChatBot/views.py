from rest_framework import views, response, exceptions, renderers, viewsets, decorators, authentication
from datetime import datetime, timedelta
from django.utils import timezone
from ChatBot.functions import (
    process_api_exception,
    exception_handler,
    time_stamp_to_date_format,
    send_email
)
from ChatBot.models import (
    BotConfiguration,
    Bots,
    Admin,
    Customers,
    CustomerBots,
    Conversation
)
from ChatBot.serializers import (
    ClientQuestionSerializer,
    CustomerSerializer,
    CustomerListSerializer,
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
    CustomerRetrieveSerializer,
    CustomerDeleteSerializer,
    BotSerializer,
    BotListSerializer,
    BotCreateSerializer,
    BotRetrieveSerializer,
    BotUpdateSerializer,
    CustomerBotSerializer,
    CustomerBotListSerializer,
    CustomerBotCreateSerializer,
    CustomerBotRetrieveSerializer,
    CustomerBotUpdateSerializer,
)
import json
from geoip import geolite2
from itertools import groupby
# from django.core.serializers.json import DjangoJSONEncoder
from bson.json_util import dumps
from django.db.models.expressions import RawSQL
from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from ChatBot.settings import STATICFILES_DIRS
import time
from random import randint, choice
import string
import base64
import jwt
import uuid


class CustomerViewSet(viewsets.ViewSet):

    serializer_class = CustomerSerializer

    def list(self, request):
        queryset = Customers.objects.all().filter(
            is_deleted=False).order_by('-date_joined')
        serializer_context = {
            'request': request,
        }
        serializer = CustomerListSerializer(
            queryset,
            many=True,
            context=serializer_context)
        return response.Response(serializer.data)

    def create(self, request):

        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
            requested_data = request.data
            print("requested_data", requested_data)
            requested_data = self.validate_requested_data(requested_data)
            characters = string.ascii_letters + string.digits
            password = "".join(
                choice(characters) for x in range(randint(8, 16))
            )
            serializer_context = {
                'request': request,
            }
            requested_data.update({
                "created_by_id": 1,  # auth_result["user"].id,
                "date_joined": datetime.now(tz=timezone.utc),
                "password": base64.b64encode(bytes(password.encode())).decode(),
            })
            customer_serializer = CustomerCreateSerializer(
                data=requested_data,
                context=serializer_context)
            customer_serializer.is_valid(raise_exception=True)
            customer_serializer.save()
            template = "emails/customer_register.html"
            context = {
                'point_of_contact': customer_serializer.data["name"],
                'org_name': requested_data["org_name"],
                'username': requested_data["mobile"],
                'password': password,
                'login_url': "chatbot.roundsqr.net/clients",
                'official_signature': 'RAJA DEVARAKONDA'
            }
            recipient = requested_data["email_id"]
            subject = "Congrats RoundSqr Customer"
            send_email(
                template,
                context,
                recipient,
                subject,
                1,  # auth_result["user"].id
            )
            result.update({
                "message": "customer created",
                "status": "success",
                "response": {"customer_id": customer_serializer.data["id"]}
            })
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            result.update(exception_handler(e))
        print("result", result)
        return response.Response(result)

    def retrieve(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        queryset = Customers.objects.all().filter(is_deleted=False)
        customer = get_object_or_404(queryset, pk=pk)
        serializer_context = {
            'request': request,
        }
        serializer = CustomerRetrieveSerializer(
            customer, context=serializer_context)
        customer_details = json.loads(renderers.JSONRenderer().render(
            serializer.data).decode())

        # user_info = Users.objects.filter(id=customer.user_id)
        # if user_info:
        #     customer_details.update({
        #         "email_id": user_info[0].__dict__["email_id"],
        #         "mobile": user_info[0].__dict__["mobile"]
        #     })

        return response.Response(customer_details)

    def update(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
            requested_data = request.data
            print("requested_data", requested_data)
            requested_data = self.validate_requested_data(requested_data)
            requested_data.update({
                "updated_by_id": 1,  # auth_result["user"].id,
                "date_modified": datetime.now(tz=timezone.utc),
            })
            queryset = Customers.objects.all().filter(is_deleted=False)
            customer = get_object_or_404(queryset, pk=pk)

            serializer_context = {
                'request': request,
            }
            customer_serializer = CustomerUpdateSerializer(
                customer,
                data=requested_data,
                context=serializer_context
            )
            customer_serializer.is_valid(raise_exception=True)
            customer_serializer.save()
            result.update({
                "message": "customer updated",
                "status": "success",
                "response": {"customer_id": int(pk)}
            })
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            result.update(exception_handler(e))
        print("result", result)
        return response.Response(result)

    def delete(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            queryset = Customers.objects.all().filter(is_deleted=False)
            customer = get_object_or_404(queryset, pk=pk)
            customer.delete()
            # serializer_context = {
            #     'request': request,
            # }
            # required_info = {
            #     "is_deleted": True,
            #     "date_modified": datetime.now(tz=timezone.utc),
            #     "updated_by_id": 1  # auth_result["user"].id
            # }
            # serializer = CustomerDeleteSerializer(
            #     customer,
            #     data=required_info,
            #     context=serializer_context
            # )
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            result.update({
                "message": "customer deleted.",
                "status": "success"
            })
        except Exception as e:
            result.update(exception_handler(e))
        return response.Response(result)

    def validate_requested_data(self, requested_data):

        if not re.match(r"^[A-Z][A-Za-z\s'.-]{2,30}$", requested_data["name"]):
            raise exceptions.ValidationError({
                "name": ["Invalid `%s` value." % requested_data["name"]]
            })
        if "gender" in requested_data:
            try:
                requested_data["gender"] = int(requested_data["gender"])
                if int(requested_data["gender"]) not in [1, 2]:
                    raise exceptions.ValidationError({
                        "gender": [
                            "Invalid choice `%s`." % requested_data["gender"]
                        ]
                    })
            except ValueError:
                raise exceptions.ValidationError({
                    "gender": ["Integer required not string."]
                })
            if requested_data["gender"] == 1:
                requested_data["gender"] = "Female"
            elif requested_data["gender"] == 2:
                requested_data["gender"] = "Male"
        if requested_data["mobile"] == "":
            raise exceptions.ValidationError({
                "mobile": ["Invalid `%s` value." % requested_data["mobile"]]
            })
        return requested_data


class BotViewSet(viewsets.ViewSet):

    serializer_class = BotSerializer

    def list(self, request):
        queryset = Bots.objects.all().filter().order_by('-date_created')
        serializer_context = {
            'request': request,
        }
        serializer = BotListSerializer(
            queryset,
            many=True,
            context=serializer_context)
        return response.Response(serializer.data)

    def create(self, request):

        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
            requested_data = request.data
            print("requested_data", requested_data)
            # requested_data = self.validate_requested_data(requested_data)
            serializer_context = {
                'request': request,
            }
            requested_data.update({
                "created_by_id": 1,  # auth_result["user"].id,
                "date_created": datetime.now(tz=timezone.utc),
            })
            bot_serializer = BotCreateSerializer(
                data=requested_data,
                context=serializer_context)
            bot_serializer.is_valid(raise_exception=True)
            bot_serializer.save()
            result.update({
                "message": "bot created",
                "status": "success",
                "response": {"bot_id": bot_serializer.data["id"]}
            })
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            result.update(exception_handler(e))
        print("result", result)
        return response.Response(result)

    def retrieve(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        queryset = Bots.objects.all()
        bot = get_object_or_404(queryset, pk=pk)
        serializer_context = {
            'request': request,
        }
        serializer = BotRetrieveSerializer(
            bot, context=serializer_context)
        bot_details = json.loads(renderers.JSONRenderer().render(
            serializer.data).decode())

        bot_details.update({
            "bot_id_text": "%s%s" % (str(bot_details["name"]), str(bot_details["id"]).zfill(4)),
        })
        return response.Response(bot_details)

    def update(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
            requested_data = request.data
            print("requested_data", requested_data)
            # requested_data = self.validate_requested_data(requested_data)
            requested_data.update({
                "updated_by_id": 1,  # auth_result["user"].id,
                "date_modified": datetime.now(tz=timezone.utc),
            })
            queryset = Bots.objects.all()
            bot = get_object_or_404(queryset, pk=pk)

            serializer_context = {
                'request': request,
            }
            bot_serializer = BotUpdateSerializer(
                bot,
                data=requested_data,
                context=serializer_context
            )
            bot_serializer.is_valid(raise_exception=True)
            bot_serializer.save()
            result.update({
                "message": "bot updated",
                "status": "success",
                "response": {"bot_id": int(pk)}
            })
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            result.update(exception_handler(e))
        print("result", result)
        return response.Response(result)

    def delete(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            queryset = Bots.objects.all()
            bot = get_object_or_404(queryset, pk=pk)
            bot.delete()
            result.update({
                "message": "bot deleted.",
                "status": "success"
            })
        except Exception as e:
            result.update(exception_handler(e))
        return response.Response(result)


class CustomerBotViewSet(viewsets.ViewSet):

    serializer_class = CustomerBotSerializer

    def list(self, request):
        queryset = CustomerBots.objects.all().filter().order_by('-date_created')
        serializer_context = {
            'request': request,
        }
        serializer = CustomerBotListSerializer(
            queryset,
            many=True,
            context=serializer_context)
        return response.Response(serializer.data)

    def create(self, request):

        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
            requested_data = request.data
            print("requested_data", requested_data)
            requested_data = self.validate_requested_data(requested_data)
            bot_queryset = Bots.objects.all()
            customer_queryset = Customers.objects.all()
            bot = get_object_or_404(bot_queryset, pk=requested_data["bot"])
            customer = get_object_or_404(customer_queryset, pk=requested_data["customer"])
            serializer_context = {
                'request': request,
            }
            bot_id_text = "%s%s" % (str(bot.name), str(bot.id).zfill(4))
            requested_data.update({
                "created_by_id": 1,  # auth_result["user"].id,
                "date_created": datetime.now(tz=timezone.utc),
                "bot_id_text": bot_id_text,
                "customer_id_text": "%s_%s" % (str(customer.org_name), str(bot_id_text)),
            })
            bot_serializer = CustomerBotCreateSerializer(
                data=requested_data,
                context=serializer_context)
            bot_serializer.is_valid(raise_exception=True)
            bot_serializer.save()
            result.update({
                "message": "bot mapped to customer",
                "status": "success",
                "response": {"mapping_id": bot_serializer.data["id"]}
            })
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
            if "customer_id_text" in result["response"]:
                result["response"] = {"customer_bot": "mapping already existed."}
        except Exception as e:
            result.update(exception_handler(e))
        print("result", result)
        return response.Response(result)

    def retrieve(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        queryset = CustomerBots.objects.all()
        bot = get_object_or_404(queryset, pk=pk)
        serializer_context = {
            'request': request,
        }
        serializer = CustomerBotRetrieveSerializer(
            bot, context=serializer_context)
        bot_details = json.loads(renderers.JSONRenderer().render(
            serializer.data).decode())
        return response.Response(bot_details)

    def update(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
            requested_data = request.data
            print("requested_data", requested_data)
            # requested_data = self.validate_requested_data(requested_data)
            requested_data.update({
                "updated_by_id": 1,  # auth_result["user"].id,
                "date_modified": datetime.now(tz=timezone.utc),
            })
            queryset = CustomerBots.objects.all()
            customer_bot = get_object_or_404(queryset, pk=pk)

            serializer_context = {
                'request': request,
            }
            bot_serializer = CustomerBotUpdateSerializer(
                customer_bot,
                data=requested_data,
                context=serializer_context
            )
            bot_serializer.is_valid(raise_exception=True)
            bot_serializer.save()
            result.update({
                "message": "customer bot mapping updated",
                "status": "success",
                "response": {"mapping_id": int(pk)}
            })
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            result.update(exception_handler(e))
        print("result", result)
        return response.Response(result)

    def delete(self, request, pk=None):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            queryset = CustomerBots.objects.all()
            bot = get_object_or_404(queryset, pk=pk)
            bot.delete()
            result.update({
                "message": "customer bot deleted.",
                "status": "success"
            })
        except Exception as e:
            result.update(exception_handler(e))
        return response.Response(result)

    def validate_requested_data(self, requested_data):

        if 'customer' not in requested_data:
            raise exceptions.ValidationError({
                "customer": ["This field is required."]
            })
        if 'bot' not in requested_data:
            raise exceptions.ValidationError({
                "bot": ["This field is required."]
            })
        return requested_data


class BotProperties(views.APIView):

    def get(self, request):

        result = {
            "message": "source_url must be required",
            "status": "failed"
        }
        try:
            if request.query_params["source_url"]:
                queryset = CustomerBots.objects.all()
                bot = get_object_or_404(queryset, source_url=request.query_params["source_url"])
                serializer_context = {
                    'request': request,
                }
                serializer = CustomerBotRetrieveSerializer(
                    bot, context=serializer_context)
                bot_details = json.loads(renderers.JSONRenderer().render(
                    serializer.data).decode())
                result.update({
                    "message": "bot ui properties",
                    "status": "success",
                    "response": bot_details
                })
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            result.update(exception_handler(e))
        print("result", result)
        return response.Response(result)


class ClientConfiguration(views.APIView):

    def get(self, request):

        """

        :param request:
        :return:
        """
        result = {
            "message": "customer must be non empty",
            "response": "",
            "status": "failed"
        }
        try:
            if request.query_params["customer"] != "":
                result["message"] = "customer must be non empty"
                if request.query_params["bot"] != "":
                    result.update(
                        self.retrieve_sections(
                            request.query_params["customer"],
                            request.query_params["bot"]
                        )
                    )
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        print("result", result)
        return response.Response(result)

    def post(self, request):

        """

        :param request:
        :return:
        """
        result = {
            "message": "customer must be non empty",
            "response": "",
            "status": "failed"
        }
        try:
            if request.data["customer"] != "":
                if request.data["bot"] != "":
                    result["message"], questions = self.validate_questions(
                        request.data["questions"]
                    )
                    if result["message"] == "":
                        result = self.create_or_update_sections(
                            request.data["customer"],
                            request.data["bot"],
                            questions,
                        )
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        print("result", result)
        return response.Response(result)

    def create_or_update_sections(self, customer, bot, questions):

        """
        :param customer:
        :param questions:
        :param bot
        :return result:
        Here the process like, if the sections and it's questions have ids in
         the form of section_id, question_id respectively we need to update
          them otherwise create.
        """
        result = {
            "status": "failed",
            "message": ""
        }
        try:
            customer_info = Customers.objects.filter(id=customer)
            result["message"] = "invalid customer"
            if customer_info:
                bot_info = Bots.objects.filter(id=bot)
                result["message"] = "invalid bot"
                if bot_info:
                    sections_info = BotConfiguration.objects.filter(
                        customer=customer_info[0],
                        bot=bot_info[0]
                    )
                    if sections_info:
                        BotConfiguration.objects.filter(
                            customer=customer_info[0],
                            bot=bot_info[0]
                        ).delete()
                    for question in questions:
                        question_obj = BotConfiguration()
                        question_obj.customer = customer_info[0]
                        question_obj.bot = bot_info[0]
                        question_obj.question = question["question"]
                        if "description" in question:
                            question_obj.description = question["description"]
                        question_obj.question_id = question["question_id"]
                        question_obj.answer_type = question[
                            "answer_type"
                        ].upper()
                        if question['answer_type'].lower() in [
                            'select',
                            'checkbox',
                            'radio'
                        ]:
                            question_obj.suggested_answers = question[
                                "suggested_answers"
                            ]
                        if "suggested_jump" in question:
                            question_obj.suggested_jump = question[
                                "suggested_jump"
                            ]
                        if question["answer_type"].lower() in [
                            'text',
                            'number'
                        ]:
                            question_obj.validation1 = question["validation1"]
                            question_obj.validation2 = question["validation2"]
                            question_obj.error_msg = question["error_msg"]
                        question_obj.required = question["required"]
                        question_obj.related = question["related"]
                        # question_obj.created_by_id = auth_result["user"].id
                        question_obj.date_created = datetime.now(
                            tz=timezone.utc
                        )
                        if "is_first_question" in question:
                            question_obj.is_last_question = question["is_first_question"]
                        if "is_last_question" in question:
                            question_obj.is_last_question = question["is_last_question"]
                        if "is_lead_gen_question" in question:
                            question_obj.is_lead_gen_question = question["is_lead_gen_question"]
                        question_obj.save()
                    result.update({
                        "message": "bot configuration done",
                        "status": "success"
                    })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            print("exception")
            result.update(exception_handler(e))
        return result

    def retrieve_sections(self, customer, bot):

        result = {
            "status": "failed",
            "message": ""
        }
        try:
            questions_info = json.loads(
                renderers.JSONRenderer().render(
                    ClientQuestionSerializer(
                        BotConfiguration.objects.filter(
                            customer_id=customer,
                            bot_id=bot
                        ), many=True
                    ).data
                )
            )
            for question in questions_info:
                question["suggested_answers"] = eval(
                    question["suggested_answers"]
                )
                try:
                    question["suggested_jump"] = eval(
                        question["suggested_jump"]
                    )
                except:
                    pass
            result.update({
                "message": "client configuration",
                "status": "success",
                "response": questions_info
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            print("exception")
            result.update(exception_handler(e))
        return result

    def validate_questions(self, questions_info):

        """

        :param questions_info:
        :return:
        """

        questions = ""
        message = "questions must be non empty list"
        if questions_info:
            try:
                if not isinstance(questions_info, list):
                    questions = json.loads(questions_info)
                else:
                    questions = questions_info
            except Exception:
                pass
            message = "questions must be list"
            if isinstance(questions, list):
                questions = list(filter(None, questions))
                message = "questions must have at least one question info"
                # whether to check questions has at least one element or not
                if len(questions) > 0:
                    message = ""
                    question_names = []
                    for j in range(0, len(questions)):
                        question = questions[j]
                        if "question" not in question:
                            message = "question missing in 'questions' at" \
                                      " index %s" % (str(j + 1))
                            break
                        elif not question["question"]:
                            message = "question must be non empty in" \
                                      " 'questions' at index %s" % (str(j + 1))
                            break
                        if question["question"] not in question_names:
                            question_names.append(question["question"])
                        else:
                            message = "question must be unique in" \
                                      " 'questions' at index %s" % (str(j + 1))
                            break
                        if "question_id" not in question:
                            message = "question_id missing in 'questions'" \
                                      " at index %s" % (str(j + 1))
                            break
                        elif not isinstance(question["question_id"], int):
                            message = "question_id must be integer in" \
                                      " 'questions' at index %s" % (str(j + 1))
                            break
                        if "answer_type" not in question:
                            message = "answer_type missing in 'questions'" \
                                      " at index %s" % (str(j + 1))
                            break
                        elif question["answer_type"].upper() not in [
                            'TEXT',
                            'NUMBER',
                            'SELECT',
                            'CHECKBOX',
                            'RADIO',
                            'FILE',
                            'DATE',
                        ]:
                            message = "answer_type must be either 'TEXT'," \
                                      " 'NUMBER', 'SELECT', 'CHECKBOX'," \
                                      " 'RADIO', 'FILE' or 'DATE' in" \
                                      " 'questions' at index %s" % (str(j + 1))
                            break
                        if question["answer_type"].lower() in [
                            'text',
                            'number'
                        ]:
                            if "validation1" not in question:
                                message = "validation1 missing in" \
                                          " 'questions' at index %s" % (str(j + 1))
                                break
                            elif not question["validation1"]:
                                message = "validation1 must be non empty in" \
                                          " 'questions' at index %s" % (str(j + 1))
                                break
                            if "validation2" not in question:
                                message = "validation2 missing in" \
                                          " 'questions' at index %s" % (str(j + 1))
                                break
                            elif not question["validation2"]:
                                message = "validation2 must be non empty in" \
                                          " 'questions' at index %s" % (str(j + 1))
                                break
                            if "error_msg" not in question:
                                message = "error_msg missing in" \
                                          " 'questions' at index %s" % (str(j + 1))
                                break
                            elif not question["error_msg"]:
                                message = "error_msg must be non empty in" \
                                          " 'questions' at index %s" % (str(j + 1))
                                break
                        if "required" not in question:
                            message = "required missing in 'questions' at" \
                                      " index %s" % (str(j + 1))
                            break
                        elif question["required"].lower() not in [
                            'yes', 'no'
                        ]:
                            message = "required must be either 'yes' or" \
                                      " 'no' in 'questions' at index %s" % (str(j + 1))
                            break
                        else:
                            question["required"] = question[
                                "required"].lower()
                        if "related" not in question:
                            message = "related missing in 'question'" \
                                      " at index " + str(j + 1)
                            break
                        elif question["related"].lower() not in [
                            'true',
                            'false'
                        ]:
                            message = "related must be either 'true'" \
                                      " or 'false' in 'question'" \
                                      " at index " + str(j + 1)
                            break
                        else:
                            question["related"] = question["related"].lower()
                            print('related', question['related'])
                            if question["related"] == 'true':
                                question["related"] = True
                            else:
                                question["related"] = False
                            print('related', question['related'])
                        if "is_first_question" in question:
                            if question["is_first_question"] == "true":
                                question["is_first_question"] = True
                            else:
                                question["is_first_question"] = False
                        if "is_last_question" in question:
                            if question["is_last_question"] == "true":
                                question["is_last_question"] = True
                            else:
                                question["is_last_question"] = False
                        if "is_lead_gen_question" in question:
                            if question["is_lead_gen_question"] == "true":
                                question["is_lead_gen_question"] = True
                            else:
                                question["is_lead_gen_question"] = False

                        if question['answer_type'].lower() in [
                            'select',
                            'checkbox',
                            'radio'
                        ]:
                            if not question["suggested_answers"]:
                                message = "suggested_answers must be non" \
                                          " empty in 'questions' at index" \
                                          " %s" % (str(j + 1))
                                break

        return message, questions


class ClientForm(views.APIView):

    def post(self, request):

        result = {
            "message": "non empty raw data required",
            "status": "failed",
            "response": ""
        }
        try:
            body_raw_input = request.body.decode()
            print('body_raw_input', body_raw_input)
            if body_raw_input:
                result["message"], bot_info = self.validate_bot_info(body_raw_input)
                if not result["message"]:
                    func_res = self.bot_conversation(bot_info, request)
                    if isinstance(func_res, dict):
                        result.update(func_res)
                    if isinstance(func_res, list):
                        result = func_res
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        print("result", result)
        return response.Response(result)

    def bot_conversation(self, bot_info, request):

        result = {
            "message": "Invalid bot_info",
            "status": "failed",
            "response": ""
        }
        try:
            # bot_id = bot_info["bot_id"]
            source_url = bot_info["location"]
            customer_bot = CustomerBots.objects.get(source_url=source_url)  # bot_id will changed to source_url
            result = ClientConfiguration().retrieve_sections(customer_bot.customer_id, customer_bot.bot_id)
            if result["status"] == "success":
                errors = []
                questions = result["response"]
                result["response"] = ""
                result["status"] = "failed"
                questions = sorted(questions, key=lambda x: x['question_id'])
                next_question = questions[0]
                print('ip', bot_info["ip"])
                match = geolite2.lookup(bot_info["ip"])
                print('ip match', match)
                print('current question', bot_info['question'])
                if bot_info['question'].lower() != "welcome":
                    session_id = bot_info["sessionId"]
                    result["message"] = "invalid session"
                    print("session keys", request.session.keys())
                    if "chat_session_%s" % str(bot_info["sessionId"]) not in request.session:
                        return result
                    result["message"] = "session and location not matched"
                    if request.session.get("chat_session_%s" % str(bot_info["sessionId"])) != bot_info["location"]:
                        return result
                    print("Check1")
                    submitted_question = [
                        question for question in questions if question[
                            'question'
                        ] == bot_info['question']
                    ]
                    if not submitted_question:
                        result["message"] = "invalid question"
                        return result
                    submitted_question = submitted_question[0]
                    print('submitted_question', submitted_question)
                    # next_question = [question for question in questions if question[
                    #     'question_id'
                    # ] == int(submitted_question['question_id']) + 1]
                    # if not next_question:  # or 'thanks' in submitted_question['question'].lower():
                    #     result["message"] = "no more questions"
                    #     return result
                    # next_question = next_question[0]
                    if 'related' in submitted_question:
                        is_related = submitted_question['related']
                        sug_answers = submitted_question['suggested_answers']
                        sug_jump = submitted_question['suggested_jump']
                        validity1 = submitted_question["validation1"]
                        validity2 = submitted_question["validation2"]
                        error_msg = submitted_question["error_msg"]
                        print('is_related', is_related)
                        if is_related:
                            print("this is related question")
                            if len(sug_answers) > 0:
                                print("current answer", bot_info["text"])
                                if bot_info['text'] in sug_answers:
                                    next_index = sug_answers.index(
                                        bot_info['text'])
                                    print('next_index', next_index)
                                    if isinstance(sug_jump, list):
                                        if next_index < len(sug_jump):
                                            next_question = sug_jump[
                                                next_index]
                                            print('next_question', next_question)
                                            next_question = [
                                                question
                                                for question in questions
                                                if question[
                                                    'question'
                                                ] == next_question
                                            ][0]
                                        elif len(sug_jump) == 1:
                                            next_question = sug_jump[0]
                                            print('next_question', next_question)
                                            next_question = [
                                                question
                                                for question in questions
                                                if question[
                                                    'question'
                                                ] == next_question
                                            ][0]
                                    else:
                                        next_question = sug_jump
                                        print('next_question', next_question)
                                        next_question = [
                                            question
                                            for question in questions
                                            if question[
                                                'question'
                                            ] == next_question
                                        ][0]
                                else:
                                    result["message"] = "invalid answer"
                                    return result
                            else:
                                if submitted_question["answer_type"] == "TEXT":
                                    contains_digit = any(map(str.isdigit, bot_info["text"]))
                                    print('contains_digit', contains_digit)
                                    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
                                    contains_specials = regex.search(bot_info["text"])
                                    print('contains_specials', contains_specials)
                                    contains_email = re.match(
                                        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                                        bot_info["text"]
                                    )
                                    print('contains_email', contains_email)
                                    contains_phone_number = re.match(r'(^[+0-9]{1,3})*([0-9]{10,11}$)', bot_info["text"])
                                    print('contains_phone_number', contains_phone_number)
                                    print('validity1', validity1)
                                    print('validity2', validity2)
                                    print('error_msg', error_msg)
                                    if validity1 == "Contains":
                                        if validity2 == "Numbers":
                                            if contains_digit:
                                                errors.append(error_msg)
                                        elif validity2 == "Special characters":
                                            if contains_specials:
                                                errors.append(error_msg)
                                        elif validity2 == "Both":
                                            if contains_digit and contains_specials:
                                                errors.append(error_msg)
                                        elif validity2 == "Email address":
                                            if contains_email:
                                                errors.append(error_msg)
                                        elif validity2 == "Phone number":
                                            if contains_phone_number:
                                                errors.append(error_msg)
                                    elif validity1 == "Not Contains":
                                        if validity2 == "Numbers":
                                            if not contains_digit:
                                                errors.append(error_msg)
                                        elif validity2 == "Special characters":
                                            if not contains_specials:
                                                errors.append(error_msg)
                                        elif validity2 == "Both":
                                            if not (contains_digit and contains_specials):
                                                errors.append(error_msg)
                                        elif validity2 == "Email address":
                                            if not contains_email:
                                                errors.append(error_msg)
                                        elif validity2 == "Phone number":
                                            if not contains_phone_number:
                                                errors.append(error_msg)
                                    print("errors", errors)
                                    if errors:
                                        next_question = submitted_question
                                    else:
                                        if isinstance(sug_jump, list):
                                            next_question = sug_jump[0]
                                        else:
                                            next_question = sug_jump
                                        print('next_question', next_question)
                                        next_question = [
                                            question
                                            for question in questions
                                            if question[
                                                   'question'
                                               ] == next_question
                                        ][0]
                    print('bot', customer_bot.bot)
                    con_obj = Conversation()
                    con_obj.bot = customer_bot.bot
                    con_obj.customer = customer_bot.customer
                    con_obj.text = bot_info["text"]
                    con_obj.ip_address = bot_info["ip"]
                    con_obj.session_id = session_id
                    con_obj.sender = "me"
                    if match:
                        con_obj.latitude = match.location[0]
                        con_obj.longitude = match.location[1]
                    con_obj.update_date_time = datetime.now(tz=timezone.utc)
                    con_obj.save()
                else:
                    session_id = str(uuid.uuid4())
                    print('session_id', session_id)
                    request.session[
                        "chat_session_%s" % session_id
                    ] = str(bot_info["location"])
                    request.session.set_expiry(86400)
                # print('questions', questions)
                suggested_answers = [{
                    "payload": sug_ans,
                    "title": sug_ans
                } for sug_ans in next_question["suggested_answers"]]
                required_next_question = {
                    'id': next_question['id'],
                    'bot': next_question['bot'],
                    'question': next_question['question'],
                    'question_id': next_question['question_id'],
                    'answer_type': next_question['answer_type'],
                    'suggested_answers': suggested_answers,
                    'is_last_question': next_question["is_last_question"],
                    'sessionId': session_id
                }
                result = {
                    "message": "next question info",
                    "status": "success",
                    "response": required_next_question
                }
                if errors:
                    required_next_question.update({"error_msg": errors[0]})
                    con_obj = Conversation()
                    con_obj.bot = customer_bot.bot
                    con_obj.customer = customer_bot.customer
                    con_obj.text = errors[0]
                    con_obj.ip_address = bot_info["ip"]
                    con_obj.session_id = session_id
                    con_obj.sender = 'bot'
                    con_obj.update_date_time = datetime.now(tz=timezone.utc)
                    con_obj.save()
                con_obj = Conversation()
                con_obj.bot = customer_bot.bot
                con_obj.customer = customer_bot.customer
                con_obj.text = required_next_question["question"]
                con_obj.ip_address = bot_info["ip"]
                con_obj.session_id = session_id
                con_obj.sender = 'bot'
                con_obj.update_date_time = datetime.now(tz=timezone.utc)
                con_obj.save()
                result = [required_next_question]
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except Exception as e:
            print("exception")
            result.update(exception_handler(e))
        return result

    def validate_bot_info(self, bot_info):

        bot_obj = ""
        message = "please provide non-empty value to bot_info parameter."
        if bot_info:
            try:
                if not isinstance(bot_info, dict):
                    bot_obj = json.loads(bot_info)
                else:
                    bot_obj = bot_info
            except Exception:
                pass
            message = "bot_info must be dict"
            if isinstance(bot_obj, dict):
                message = ""
                # if "bot_id" not in bot_obj:
                #     message = "bot_id missing in 'bot_info'"
                if "question" in bot_obj:
                    if 'text' not in bot_obj:
                        message = "text missing in 'bot_info'"
                if "ip" not in bot_obj:
                    message = "ip missing in 'bot_info'"
                if "sessionId" not in bot_obj:
                    message = "sessionId missing in 'bot_info'"
                if "location" not in bot_obj:
                    message = "location missing in 'bot_info'"

        return message, bot_obj


class SessionAnalytics(views.APIView):

    def get(self, request, **kwargs):

        result = {
            "message": "Value required for 'days_count' field.",
            "status": "failed"
        }
        try:
            if request.query_params["days_count"]:
                try:
                    days_count = int(request.query_params["days_count"])
                    if kwargs['slug'] == "geo":
                        result[
                            "message"
                        ] = "Value required for 'latitude' field."
                        if request.query_params['latitude']:
                            try:
                                latitude = float(
                                    request.query_params['latitude']
                                )
                                result[
                                    "message"
                                ] = "Value required for 'longitude' field."
                                if request.query_params['longitude']:
                                    try:
                                        longitude = float(
                                            request.query_params['longitude']
                                        )
                                        result[
                                            "message"
                                        ] = "Value required for" \
                                            " 'radius' field."
                                        if request.query_params['radius']:
                                            try:
                                                radius = float(
                                                    request.query_params[
                                                        'radius'
                                                    ]
                                                )
                                                result.update(
                                                    self.process_metrics(
                                                        days_count,
                                                        latitude,
                                                        longitude,
                                                        radius
                                                    )
                                                )
                                            except ValueError:
                                                result[
                                                    "message"
                                                ] = "'radius' must be integer."
                                    except ValueError:
                                        result[
                                            "message"
                                        ] = "'longitude' must be float."
                            except ValueError:
                                result[
                                    "message"
                                ] = "'latitude' must be float."
                    else:
                        result.update(
                            self.process_metrics(
                                int(request.query_params["days_count"])
                            )
                        )
                except ValueError:
                    result["message"] = "'days_count' must be integer."
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        print("result", result)
        return response.Response(result)

    def process_metrics(
            self,
            days_count,
            latitude=None,
            longitude=None,
            radius=None
    ):

        result = {
            "message": "",
            "status": "failed"
        }
        try:
            current_date = datetime.now(tz=timezone.utc)
            start_date = current_date - timedelta(days=days_count)
            print('current_date', current_date.date())
            print('start_date', start_date.date())
            actual_dates = []
            for i in range(days_count):
                actual_dates.append(
                    datetime.strftime(
                        start_date + timedelta(days=i),
                        "%Y-%m-%d"
                    )
                )
            print('actual_dates', actual_dates)
            if latitude and longitude and radius:
                """
                Return objects sorted by distance to specified coordinates
                which distance is less than max_distance given in kilometers
                """
                # Great circle distance formula
                gcd_formula = "6371 * acos(least(greatest(cos(radians(%s))" \
                              " * cos(radians(latitude)) * cos(radians(" \
                              "longitude) - radians(%s)) + sin(radians(%s))" \
                              " * sin(radians(latitude)), -1), 1))"
                distance_raw_sql = RawSQL(
                    gcd_formula,
                    (latitude, longitude, latitude)
                )
                sessions = Conversation.objects.filter(
                    time_stamp__date__gte=start_date.date(),
                    time_stamp__date__lte=current_date.date()
                ).values('time_stamp').annotate(
                    distance=distance_raw_sql
                ).order_by('distance')
                if radius is not None:
                    sessions = sessions.filter(distance__lt=radius)
            else:
                sessions = Conversation.objects.filter(
                    time_stamp__date__gte=start_date.date(),
                    time_stamp__date__lt=current_date.date()
                ).values('time_stamp')
            sessions = json.loads(dumps(sessions))
            print('sessions', sessions)
            result["message"] = "no graph data"
            if sessions:
                for session in sessions:
                    session["name"] = time_stamp_to_date_format(
                        session["time_stamp"]["$date"]
                    ).split()[0]
                    del session["time_stamp"]
                graph_data = unique_and_count(sessions)
                existed_dates = [record["name"] for record in graph_data]
                print('existed_dates', existed_dates)
                for ac_date in actual_dates:
                    if ac_date not in existed_dates:
                        graph_data.append({
                            "name": ac_date,
                            "value": 0
                        })
                graph_data.sort(key=lambda x: x['name'])
                result.update({
                    "message": "graph data",
                    "status": "success",
                    "response": graph_data
                })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            print("exception")
            result.update(exception_handler(e))
        return result


def canonicalize_dict(x):

    """Return a (key, value) list sorted by the hash of the key"""
    return sorted(x.items(), key=lambda x: hash(x[0]))


def unique_and_count(lst):

    """Return a list of unique dicts with a 'count' key added"""
    grouper = groupby(sorted(map(canonicalize_dict, lst)))
    return [dict(k + [("value", len(list(g)))]) for k, g in grouper]


class AssetsUploader(views.APIView):

    def post(self, request, **kwargs):
        # token_auth = TokenAuthentication()
        # auth_result = token_auth.authenticate(request)
        # if "error" in auth_result:
        #     return response.Response(
        #         auth_result,
        #     )
        result = {
            "message": "resource not found",
            "status": "failed"
        }
        try:
            if kwargs["slug"] in ['image', 'file']:
                if request.FILES["asset"]:
                    return self.assets_upload_processor(
                        kwargs["slug"],
                        request.FILES["asset"]
                    )
                else:
                    result["message"] = "please upload an asset"
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        return response.Response(result)

    def assets_upload_processor(self, asset_type, asset):

        result = {
            "message": "",
            "status": "failed"
        }
        try:
            fileName = asset.name
            fileType = fileName.split('.')[-1]
            ASSET_DIR = ""
            if asset_type == "image":
                result["message"] = "only 'png', 'jpg', 'jpeg' files are allowed."
                if fileType in ("png", "jpg", "jpeg"):
                    ASSET_DIR = os.path.join(
                        STATICFILES_DIRS[0],
                        'images',
                        'logos'
                    )

            elif asset_type == 'file':
                result["message"] = "only 'pdf', 'doc', 'docx', 'xls' or 'xlsx' files are allowed."
                if fileType in ('pdf', 'doc', 'docx', 'xls', 'xlsx'):
                    ASSET_DIR = os.path.join(
                        STATICFILES_DIRS[0],
                        'documents'
                    )
            if ASSET_DIR:
                if not os.path.exists(ASSET_DIR):
                    os.makedirs(ASSET_DIR)
                filePath = os.path.join(
                    ASSET_DIR,
                    str(int(time.time())) + "_" + fileName
                )
                filePath = filePath.replace(" ", '_')
                default_storage.save(
                    "%s" % filePath,
                    ContentFile(asset.read())
                )  # to default storage file path address
                path = 'static%s' % str(filePath.split('static')[1])
                result.update({
                    "message": "asset uploaded successfully",
                    "status": "success",
                    "response": path
                })
        except Exception as e:
            result.update(exception_handler(e))
        return response.Response(result)


class Analytics(views.APIView):

    def get(self, request, **kwargs):

        result = {
            "message": "Value required for 'days_count' field.",
            "status": "failed"
        }
        try:
            days_count = 30
            if "days_count" in request.query_params:
                days_count = int(request.query_params["days_count"])
            result.update(self.process_metrics(days_count, kwargs["slug"]))
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except ValueError:
            result["message"] = "'days_count' must be integer."
        print("result", result)
        return response.Response(result)

    def process_metrics(self, days_count, grpah_type):

        result = {
            "message": "",
            "status": "failed"
        }
        try:
            current_date = datetime.now(tz=timezone.utc)
            start_date = current_date - timedelta(days=days_count)
            print('current_date', current_date.date())
            print('start_date', start_date.date())
            actual_dates = []
            for i in range(days_count):
                actual_dates.append(
                    datetime.strftime(
                        start_date + timedelta(days=i),
                        "%Y-%m-%d"
                    )
                )
            print('actual_dates', actual_dates)
            sessions = Conversation.objects.filter(
                time_stamp__date__gte=start_date.date(),
                time_stamp__date__lt=current_date.date()
            ).values('time_stamp')
            sessions = json.loads(dumps(sessions))
            print('sessions', sessions)
            result["message"] = "no graph data"
            if sessions:
                for session in sessions:
                    session["name"] = time_stamp_to_date_format(
                        session["time_stamp"]["$date"]
                    ).split()[0]
                    del session["time_stamp"]
                graph_data = unique_and_count(sessions)
                existed_dates = [record["name"] for record in graph_data]
                print('existed_dates', existed_dates)
                for ac_date in actual_dates:
                    if ac_date not in existed_dates:
                        graph_data.append({
                            "name": ac_date,
                            "value": 0
                        })
                graph_data.sort(key=lambda x: x['name'])
                result.update({
                    "message": "graph data",
                    "status": "success",
                    "response": graph_data
                })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            print("exception")
            result.update(exception_handler(e))
        return result


@decorators.api_view(['POST'])
def register_admin(request):

    result = {
        "message": "admin already existed",
        "status": "failed"
    }
    email_id = "raja@roundsqr.com"
    mobile = 9959047000
    admin_info = Admin.objects.filter(mobile=mobile, email_id=email_id)
    if not admin_info:
        characters = string.ascii_letters + string.digits
        password = "".join(
            choice(characters) for x in range(randint(8, 16))
        )
        admin_obj = Admin()
        admin_obj.name = "Raja Devarakonda"
        admin_obj.email_id = email_id
        admin_obj.mobile = mobile
        admin_obj.password = base64.b64encode(bytes(password.encode())).decode()
        admin_obj.date_created = datetime.now(tz=timezone.utc)
        admin_obj.save()
        result.update({
            "message": "admin registered successfully",
            "status": "success"
        })
    return response.Response(result)


class Login(views.APIView):

    def post(self, request, *args, **kwargs):
        result = {
            "message": "Invalid credentials",
            "status": "failed",
            "response": {}
        }
        try:
            username = request.data['mobile']
            password = base64.b64encode(bytes(
                request.data['password'].encode()
            )).decode()
            if kwargs["slug"] == "admin":
                user_model = Admin
                user_model_str = 'Admin'
            else:
                user_model = Customers
                user_model_str = 'Customers'
            user = user_model.objects.filter(
                mobile=username,
                password=password
            )
            if not user:
                result.update({"message": "Invalid Credentials"})
            else:
                last_login = datetime.now(tz=timezone.utc)
                payload = {
                    'id': user[0].id,
                    'mobile': user[0].mobile,
                    'timestamp': datetime.timestamp(last_login),
                    'user_model': user_model_str
                }
                jwt_token = {
                    'token': jwt.encode(
                        payload, "SECRET_KEY", algorithm='HS256'
                    )
                }
                user[0].last_login = last_login
                user[0].is_logged_in = True
                user[0].token = jwt_token["token"].decode()
                user[0].save()
                result.update({
                    "message": "successfully loggedIn",
                    "status": "success",
                })
                result["response"].update({
                    "token": jwt_token["token"],
                    "is_pwd_updated": user[0].is_password_updated,
                    "user_id": user[0].id,
                    "user_name": user[0].name,
                })
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except Exception as e:
            result.update(exception_handler(e))
        return response.Response(result)


class Logout(views.APIView):

    def post(self, request, **kwargs):

        token_auth = TokenAuthentication()
        auth_result = token_auth.authenticate(request)
        if "error" in auth_result:
            return response.Response(
                auth_result,
            )
        if kwargs["slug"] == "admin":
            user_model = Admin
        else:
            user_model = Customers
        print('auth_result', auth_result["user"])
        user_info = user_model.objects.filter(
            id=auth_result["user"].id
        ).update(token=None, is_logged_in=False)
        print('user_info', user_info)
        if user_info:
            if "user_details_%s" % str(
                    auth_result["user"].id
            ) in request.session:
                del request.session[
                    "user_details_%s" % str(auth_result["user"].id)
                ]
            return response.Response(
                {"message": "Successfully Logged Out"}
            )
        return response.Response({
            "message": "Logout Failed"
        })


class TokenAuthentication(authentication.BaseAuthentication):

    model = None

    def get_model(self):
        return Users

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        print("auth", auth)
        if not auth or auth[0].lower() != b'bearer':
            return {"error": "Invalid Authorization"}
        if len(auth) == 1:
            msg = {'error': 'Invalid token header. No credentials provided.'}
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = {'error': 'Invalid token header'}
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = {'error': 'Null token not allowed'}
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = {
                'error': 'Invalid token header.'
                         ' Token string should not'
                         ' contain invalid characters.'
            }
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, token, request):

        # model = self.get_model()
        msg = {'error': "Token mismatch", 'status': "401"}
        jwt_sign = jwt.ExpiredSignature
        jwt_token = jwt.InvalidTokenError
        try:
            payload = jwt.decode(token, "SECRET_KEY")
            mobile = payload['mobile']
            user_id = payload['id']
            user_model = payload['user_model']
            if user_model == "Admin":
                user_model = Admin
            else:
                user_model = Customers
            # if "user_details_%s" % str(
            #         user_id
            # ) not in request.session:
            #     Users.objects.filter(
            #         email_id=email,
            #         id=user_id,
            #     ).update(is_logged_in=False, token="")
            #     return {"error": "Session expired."}
            timestamp = payload['timestamp']
            last_login = datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")
            user = user_model.objects.get(
                mobile=mobile,
                id=user_id,
            )
            if user.is_logged_in:
                db_last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S")
                if not user or last_login != db_last_login:
                    raise exceptions.AuthenticationFailed(msg)
                return {"user": user, "token": token}
            else:
                return {"error": "Please Login"}
        except jwt_sign or jwt.DecodeError or jwt_token:
            return {'error': "Token is invalid", "status": "403"}
        except Admin.DoesNotExist or Customers.DoesNotExist:
            return {'error': "Internal server error", "status": "500"}

    def authenticate_header(self, request):
        return 'Token'


class ForgotPassword(views.APIView):

    def get(self, request, **kwargs):
        print("PATH_INFO", request.META["PATH_INFO"])
        print("kwargs slug", kwargs)
        result = {
            "message": "",
            "status": "failed"
        }
        try:
            email_id = self.validate_emailid(
                request.query_params["email_id"].lower()
            )  # requested_data)
            if "HTTP_ORIGIN" in request.META:
                WEB_HOST = request.META["HTTP_ORIGIN"]
            else:
                WEB_HOST = "%s://%s" % (
                    request.META["wsgi.url_scheme"],
                    request.META["HTTP_HOST"])
            context = {
                'point_of_contact': "",
                'username': email_id,
                'password': "",
                'login_url': "%s/login" % WEB_HOST,
                'official_signature': 'RAJA DEVARAKONDA'
            }
            if "admin" in request.META["PATH_INFO"]:
                org_name = "RoundSqr"
                user_info = Admin.objects.get(email_id=email_id)
                context["point_of_contact"] = user_info.full_name
                context["password"] = base64.b64decode(
                    user_info.password
                ).decode()
            else:  # if "organizations" in request.META["PATH_INFO"]:
                customer = Customers.objects.get(
                    email_id=email_id,
                    is_deleted=False
                )
                org_name = customer.org_name
                context["point_of_contact"] = customer.name
                context["password"] = base64.b64decode(
                    customer.password).decode()
            template = "emails/forgot_password.html"
            recipient = email_id
            subject = "Your %s account password" % org_name
            send_email(template, context, recipient, subject, None)
            result.update({
                "message": "password retrieved successfully",
                "status": "success"
            })
        except Admin.DoesNotExist:
            result["message"] = "invalid email_id"
        except Customers.DoesNotExist:
            result["message"] = "invalid email_id"
        except KeyError as e:
            result.update({
                "message": "API Error",
                "response": {e.args[0]: "This field is required."}
            })
        except exceptions.APIException as e:
            result = process_api_exception(e, result)
        except Exception as e:
            result.update(exception_handler(e))
        print("result", result)
        return response.Response(result)

    def validate_emailid(self, email_id):
        if not re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            email_id
        ):
            raise exceptions.ValidationError({
                "email": ["Invalid `%s` value." % email_id]
            })
        return email_id
