from rest_framework import views, response, exceptions, renderers
from datetime import datetime
from django.utils import timezone
from ChatBot.functions import process_api_exception, exception_handler
from ChatBot.models import BotQuestions, Bots, Customers
from ChatBot.serializers import ClientQuestionSerializer
import json


class Customer(views.APIView):

    def post(self, request):

        Customers(name="Apollo").save()
        return response.Response({
            "status": "success"
        })


class Bot(views.APIView):

    def post(self, request):
        customer = Customers.objects.get(name="Apollo")
        Bots(customer=customer).save()
        return response.Response({
            "status": "success"
        })


class ClientConfiguration(views.APIView):

    def get(self, request):

        """

        :param request:
        :return:
        """
        result = {
            "message": "bot must be non empty",
            "response": "",
            "status": "failed"
        }
        try:
            if request.query_params["bot"] != "":
                result.update(
                    self.retrieve_sections(request.query_params["bot"])
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
            "message": "bot must be non empty",
            "response": "",
            "status": "failed"
        }
        try:
            if request.data["bot"] != "":
                result["message"], questions = self.validate_questions(
                    request.data["questions"]
                )
                if result["message"] == "":
                    result = self.create_or_update_sections(
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

    def create_or_update_sections(self, bot, questions):

        """
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
            bot_info = Bots.objects.filter(id=bot)
            result["message"] = "invalid bot"
            if bot_info:
                sections_info = BotQuestions.objects.filter(
                    bot=bot_info[0]
                )
                if sections_info:
                    BotQuestions.objects.filter(
                        bot=bot_info[0]
                    ).delete()
                for question in questions:
                    question_obj = BotQuestions()
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
                    # question_obj.created_by_id = auth_result["user"].id
                    question_obj.date_created = datetime.now(
                        tz=timezone.utc
                    )
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

    def retrieve_sections(self, bot):

        result = {
            "status": "failed",
            "message": ""
        }
        try:
            questions_info = json.loads(
                renderers.JSONRenderer().render(
                    ClientQuestionSerializer(
                        BotQuestions.objects.filter(
                            bot_id=bot
                        ), many=True
                    ).data
                )
            )
            for question in questions_info:
                question["suggested_answers"] = eval(
                    question["suggested_answers"]
                )
                question["suggested_jump"] = eval(
                    question["suggested_jump"]
                )
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
