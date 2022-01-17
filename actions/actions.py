import os
import json
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FormValidation, SlotSet, EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from algoliasearch.search_client import SearchClient
import requests
import pathlib
import time
from actions.utils import get_html_data, send_email
from pyairtable import Table
import datetime
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
base_id = os.getenv('BASE_ID')
table_name = os.getenv('TABLE_NAME')
api_key_airtable = os.getenv('API_KEY_AIRTABLE')

date = datetime.datetime.now().isoformat()
table = Table(api_key_airtable, base_id, table_name)
table2 = Table(api_key_airtable, base_id, 'Clothes')
# new_record = {
#         "name": 'ivan',
#         "email": 'email@gmail.com',
#         "feedback_value": int('3'),
#         "feedback_message": 'funciona',
#         "created_at": date
#     }

# table.create(new_record)

this_path = pathlib.Path(os.path.realpath(__file__))
email_content = get_html_data(f"{this_path.parent}/user_email.html")

# send_email("Gracias por tu aporte al desarrollo tecnológico", 'xavier.aguas@epn.edu.ec', email_content)

client = SearchClient.create("BQCT474121", "b72f4c8a6b93d0afc8221d06c66e1e66")
index = client.init_index("dev_clothes_v2")

names = pathlib.Path(f"{this_path.parent}/names1.txt").read_text().split("\n")

MOCK_DATA = json.load(open("actions/mock_data.json", "r"))

message_clothes_girls = {
    "type": "template",
    "payload": {"template_type": "generic", "elements": MOCK_DATA["CLOTHES_GIRLS"]},
}

message_clothes_boys = {
    "type": "template",
    "payload": {"template_type": "generic", "elements": MOCK_DATA["CLOTHES_BOYS"]},
}


class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        # most_recent_state = tracker.current_state()
        # person_id = most_recent_state["sender_id"]
        # r = requests.get(
        #     "https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}".format(
        #         person_id, fb_access_token
        #     )
        # ).json()
        # first_name = r["first_name"]

        # input_channel = tracker.get_latest_input_channel()

        # print('input_channel', input_channel)

        message = {
            "type": "template",
            "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Mira lo que tengo para ti",
                            "subtitle": "Ropa para niños y niñas",
                            "image_url": "https://res.cloudinary.com/ecommercejasmine/image/upload/v1641417391/clothes_i3vsm0.png",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "payload": "/request_clothes",
                                    "title": "Ropita" + " " + "👕" + " . ",
                                },
                            ]
                        },
                        {
                            "title": "¿Quién soy?",
                            "subtitle": "Asistente de Compras",
                            "image_url": "https://res.cloudinary.com/ecommercejasmine/image/upload/v1641417212/introducing_cialm6.png",
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "https://www.instagram.com/creacionesjasmina/",
                                    "title": " Conóceme 👩🏻‍🦰 .",
                                },
                            ]
                        },
                                                {
                            "title": "Mi Creador",
                            "subtitle": "El poder de la imaginación nos hace infinitos",
                            "image_url": "https://res.cloudinary.com/ecommercejasmine/image/upload/v1642204690/developer_bxr0na.png",
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "https://www.linkedin.com/in/xavier-iv%C3%A1n-aguas-5764b5133/",
                                    "title": " Descubre 👨🏻‍🚀 .",
                                },
                            ]
                        },
                    ],
            },
        }

        email_fill = tracker.get_slot("email_fill")
        feedback_fill = tracker.get_slot("email_fill")
        clothes_name_value = tracker.get_slot("clothes_name_value")

        if email_fill is None and feedback_fill is None:
            dispatcher.utter_message(
                response="utter_complete_information"
            )
            #dispatcher.utter_message(attachment=message)

        elif clothes_name_value == True:
            dispatcher.utter_message(
                text="Aquí vamos!"
            )
        else:
            dispatcher.utter_message(
                text="Empecemos!"
            )
            dispatcher.utter_message(
                text="Elige una opción para iniciar"
            )
            #dispatcher.utter_message(attachment=message)

        return [SlotSet("email_fill", True)]


class ActionIntroducingMe(Action):
    def name(self) -> Text:
        return "action_introducing_me"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        message = {
            "type": "template",
            "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Mira lo que tengo para ti",
                            "subtitle": "Ropa para niños y niñas",
                            "image_url": "https://res.cloudinary.com/ecommercejasmine/image/upload/v1641417391/clothes_i3vsm0.png",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "payload": "/request_clothes",
                                    "title": "Ropita" + " " + "👕" + " . ",
                                },
                            ]
                        },
                        {
                            "title": "¿Quién soy?",
                            "subtitle": "Asistente de Compras",
                            "image_url": "https://res.cloudinary.com/ecommercejasmine/image/upload/v1641417212/introducing_cialm6.png",
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "https://www.instagram.com/creacionesjasmina/",
                                    "title": " Conóceme 👩🏻‍🦰 .",
                                },
                            ]
                        },
                    ],
            },
        }

        dispatcher.utter_message(text="Mira, esto es para ti!")
        #dispatcher.utter_message(attachment=message)

        return []


class ValidateClothesForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_clothes_form"

    @staticmethod
    def is_int(string: Any) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_gender(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `gender` value."""

        if slot_value.lower() not in MOCK_DATA["ALLOWED_GENDERS"]:
            dispatcher.utter_message(response="utter_ask_gender")
            return {"gender": None}
        else:
            return {"gender": slot_value}

    def validate_color(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `color` value."""

        gender = tracker.get_slot("gender")
        clothes_type = tracker.get_slot("category")
        print('gender', gender)
        print('clothes_type', clothes_type)
        print('colors', slot_value)

        intent_name = tracker.latest_message["intent"]["name"]
        if intent_name == "deny":
            return {"color": "no"}

        if intent_name == "affirm":
            dispatcher.utter_message(
                text=f"Esto es lo que tengo para ti."
            )

        if gender == "niña":
            if clothes_type == "legging" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_LEGGINGS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de pantalón como: \n- Rojo\n- Azul\n- Morado\n- Negro\n- Gris\n- Celeste\n- Verde\n- Fucsia\n- Turquesa\n- Café"
                )
                return {"color": None}

            if clothes_type == "blusa" and (slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_BLUSAS"]):
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de blusas como: \n- Morado\n- Amarillo\n- Beige\n- Celeste\n- Plomo\n- Turquesa"
                )
                return {"color": None}

            if clothes_type == "pijama" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_PIJAMAS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de pijamas como: \n- Morado\n- Amarillo\n- Rosada\n- Celeste\n- Verde"
                )
                return {"color": None}

            return {"color": slot_value}

        if gender == "niño":
            if clothes_type == "buso" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_BOYS_BUSOS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de busos como: \n- Azul\n- Rojo\n- Beige\n- Plomo\n- Amarillo"
                )
                return {"color": None}

            if clothes_type == "polo" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_BOYS_POLOS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de polos como: \n- Café\n- Verde\n- Azul\n- Rojo"
                )
                return {"color": None}

            if clothes_type == "pantalon" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_BOYS_PANTALONES"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de pantalones como: \n- Azul\n- Rojo\n- Plomo\n- Gris"
                )
                return {"color": None}

            return {"color": slot_value}

    def validate_category(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `category` value."""
        gender = tracker.get_slot("gender")
        print("gender2", gender)
        print("category", slot_value)

        if gender is None and (slot_value.lower() in MOCK_DATA["ALLOWED_CLOTHES_GIRLS"]):
            SlotSet("gender", "niña")
            print("works!")
            return {"gender": "niña"}

        if gender is None and (slot_value.lower() in MOCK_DATA["ALLOWED_CLOTHES_BOYS"]):
            return {"gender": "niño"}

        if gender == "niña":
            if slot_value.lower() not in MOCK_DATA["ALLOWED_CLOTHES_GIRLS"]:
                dispatcher.utter_message(
                    text=f"Lo siento eso no tenemos, pero te cuento que contamos con los siguientes tipos de ropa para niñas:",
                )
                #dispatcher.utter_message(attachment=message_clothes_girls)

                return {"category": None}
            else:
                dispatcher.utter_message(text=f"Excelente elección 👍🏻")
                return {"category": slot_value}

        if gender == "niño":
            if slot_value.lower() not in MOCK_DATA["ALLOWED_CLOTHES_BOYS"]:
                dispatcher.utter_message(
                    text=f"Te cuento que contamos con los siguientes tipos de ropa para niños:"
                )
                #dispatcher.utter_message(attachment=message_clothes_boys)
                return {"category": None}
            else:
                dispatcher.utter_message(text=f"Excelente elección 👍🏻")
                return {"category": slot_value}

    def validate_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `size` value."""
        print("size", slot_value)

        if isinstance(slot_value, list):
            slot_value = slot_value[0]

        if self.is_int(slot_value) and (int(slot_value) >= 1 and int(slot_value) <= 5):
            return {"size": slot_value}
        else:
            gender = tracker.get_slot("gender")
            if gender == "niña":
                dispatcher.utter_message(
                    text=f"Lo siento 😭, para esa edad no disponemos. Te cuento que tenemos ropa para niñas de 1 a 5 años:"
                )
            if gender == "niño":
                dispatcher.utter_message(
                    text=f"Lo siento 😭, para esa edad no disponemos. Te cuento que tenemos ropa para niños de 1 a 5 años:"
                )
            return {"size": None}


class AskForCategoryAction(Action):

    def name(self) -> Text:
        return "action_ask_category"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        gender = tracker.get_slot("gender")

        if gender == "niña":
            dispatcher.utter_message(
                text=f"Te cuento que contamos con los siguientes tipos de ropa para niñas 👧🏻:"
            )
            #dispatcher.utter_message(attachment=message_clothes_girls)
        else:

            dispatcher.utter_message(
                text=f"Te cuento que contamos con los siguientes tipos de ropa para niños 👦🏻:"
            )
            #dispatcher.utter_message(attachment=message_clothes_boys)

        return []


class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    @staticmethod
    def search_gender_age_category(parameters):
        objects = index.search(
            "",
            {
                "facetFilters": [
                    ["gender:{0[0]}".format(parameters)],
                    ["age:{0[1]}".format(parameters)],
                    ["category:{0[2]}".format(parameters)],
                ]
            },
        )

        return objects

    @staticmethod
    def search_gender_age_color(parameters):
        objects = index.search(
            "",
            {
                "facetFilters": [
                    ["gender:{0[0]}".format(parameters)],
                    ["age:{0[1]}".format(parameters)],
                    ["color:{0[3]}".format(parameters)],
                ]
            },
        )

        return objects

    @staticmethod
    def search_gender_age_category_color(parameters):
        objects = index.search(
            "",
            {
                "facetFilters": [
                    ["gender:{0[0]}".format(parameters)],
                    ["age:{0[1]}".format(parameters)],
                    ["category:{0[2]}".format(parameters)],
                    ["color:{0[3]}".format(parameters)],
                ]
            },
        )

        return objects

    @staticmethod
    def search_gender_age(parameters):
        objects = index.search(
            "",
            {
                "facetFilters": [
                    ["gender:{0[0]}".format(parameters)],
                    ["age:{0[1]}".format(parameters)],
                ]
            },
        )

        return objects

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get slots and save as tuple
        parameters = [
            tracker.get_slot("gender"),
            tracker.get_slot("size"),
            tracker.get_slot("category"),
            tracker.get_slot("color"),
        ]

        if parameters[0] == "niño":
            parameters[0] = "M"
        else:
            parameters[0] = "F"

        print(parameters)

        date = datetime.datetime.now().isoformat()
        new_record = {
                    "category": parameters[2],
                    "age": parameters[1],
                    "color": parameters[3],
                    "gender": parameters[0],
                    "created_at": date
                }

        table2.create(new_record)

        if parameters[3] == "no":
            objects = self.search_gender_age_category(parameters)
        else:
            objects = self.search_gender_age_category_color(parameters)

        clothes = objects["hits"]

        product = []
        for x in clothes:
            print(x["name"])
            product.append(
                {
                    "title": x["name"],
                    "subtitle": "{0}\nStock: {1} disponibles \nPrecio: ${2}".format(
                        x["material"], x["quantity"], x["price"]
                    ),
                    "image_url": x["image"],
                    "buttons": [
                        {
                            "title": "Comprar",
                            "url": "https://www.instagram.com/creacionesjasmina/",
                            "type": "web_url",
                        }
                    ],
                }
            )

        message = {
            "type": "template",
            "payload": {"template_type": "generic", "elements": product},
        }

        if clothes:
            #dispatcher.utter_message(attachment=message)  # Show respuestas

            feedback_fill = tracker.get_slot("feedback_fill")
            # count_find_product = tracker.get_slot("count_find_product")
            # print('count_find_product', count_find_product)

            # if count_find_product < 1.0:
            #     result_finds = 1.0 - count_find_product
            #     update_count = count_find_product + 1
            #     dispatcher.utter_message(
            #         text=f"Debes buscar por lo menos {int(result_finds)} veces para dejar un comentario")
            #     dispatcher.utter_message(response="utter_anything_else")

            #     slots_to_reset = {
            #         "gender": None,
            #         "size": None,
            #         "color": None,
            #         "category": None,
            #         "clothes_name_value": None,
            #         "count_find_product": update_count
            #     }

            #     return [SlotSet(k, v) for k, v in slots_to_reset.items()]

            # else:
            if feedback_fill is None:
                time.sleep(5)
                dispatcher.utter_message(
                    response="utter_ask_feedback_value")
            else:
                dispatcher.utter_message(response="utter_anything_else")

            slots_to_reset = {
                "gender": None,
                "size": None,
                "color": None,
                "category": None,
                "clothes_name_value": None,

            }

            return [SlotSet(k, v) for k, v in slots_to_reset.items()]

        else:
            # provide out of stock
            text = f"No disponemos de ese producto en específico pero puedes seguir buscando. Tengo bonitos modelos..."
            # buttons = [{"title": 'Ver más', "payload": '/action_more_productos'}, {"title": 'No gracias', "payload": 'utter_chitchat/thanks'}]
            dispatcher.utter_message(text=text)
            dispatcher.utter_message(response="utter_anything_else")

        slots_to_reset = {
            "gender": None,
            "size": None,
            "color": None,
            "category": None,
            "clothes_name_value": None,
        }

        return [SlotSet(k, v) for k, v in slots_to_reset.items()]


class ActionGoodbye(Action):
    def name(self) -> Text:
        return "action_goodbye_world"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("first_name")

        if name:
            dispatcher.utter_message(
                text=f"Hasta pronto {name}, fue un placer chatear contigo 🤗.",
                image="https://media.giphy.com/media/jUwpNzg9IcyrK/giphy.gif"
            )
        else:
            dispatcher.utter_message(
                text=f"Chao, cuidate mucho, gracias por escribirme 😊.",
                image="https://media.giphy.com/media/GB0lKzzxIv1te/giphy.gif")

        slots_to_reset = ["gender", "size", "color",
                          "category", "clothes_name_value"]
        return [SlotSet(slot, None) for slot in slots_to_reset]


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        first_name = tracker.get_slot("first_name")
        if first_name is not None:
            if first_name.upper() not in names:
                return ["name_spelled_correctly"] + domain_slots
        return domain_slots

    async def extract_name_spelled_correctly(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        intent = tracker.get_intent_of_latest_message()
        first_name = tracker.get_slot("first_name")
        print('first_name', first_name)
        # if first_name is not None and intent == "give_name":
        #     print('Lo lleno')
        #     return {"name_spelled_correctly": None}
        if intent == "affirm":
            print('esta bien escrito')
            return {"name_spelled_correctly": intent == "affirm"}
        elif intent == "deny":
            print('esta mal escrito')
            return {"name_spelled_correctly": None}

    def validate_name_spelled_correctly(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name_spelled_correctly` value."""

        print('slot_spelled', tracker.get_slot("name_spelled_correctly"))
        intent = tracker.get_intent_of_latest_message()
        print('intent', intent)

        if tracker.get_slot("name_spelled_correctly"):
            print('todo bien')
            return {"first_name": tracker.get_slot("first_name"), "name_spelled_correctly": True}
        elif tracker.get_slot("first_name") and intent == "deny":
            print('aplasto negar')
            return {"first_name": None, "name_spelled_correctly": None}
        elif tracker.get_slot("name_spelled_correctly") is None:
            print('no se lleno')
            return {"name_spelled_correctly": None}

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        if isinstance(slot_value, list):
            slot_value = slot_value[0]

        if tracker.get_slot("requested_slot") == "first_name":
            if len(slot_value) <= 1:
                dispatcher.utter_message(
                    text=f"El nombre es muy corto, parece que te faltan caracteres.")
                return {"first_name": None}
            else:
                print('slot_value', slot_value)
                return {"first_name": slot_value.capitalize(), "last_first_name": slot_value.capitalize()}

        return {"first_name": tracker.get_slot("last_first_name")}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email` value."""

        # If the name is super short, it might be wrong.

        if (re.fullmatch(regex, slot_value)):
            # dispatcher.utter_message(
            #     response="utter_thumbsup")
            return {"email": slot_value}
        else:
            dispatcher.utter_message(
                text=f"Parece que la dirección de correo es inválida. Vuelve a ingresarla, por favor.")
            return {"email": None}


class ValidateFeedbackForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_feedback_form"

    # async def required_slots(
    #     self,
    #     domain_slots: List[Text],
    #     dispatcher: "CollectingDispatcher",
    #     tracker: "Tracker",
    #     domain: "DomainDict",
    # ) -> Optional[List[Text]]:
    #     feedback_value = tracker.get_slot("feedback_value")
    #     if feedback_value is not None:
    #         if feedback_value in ['1', '2', '3', '4', '5']:
    #             return ["feedback_message"] + domain_slots
    #     return domain_slots


    # async def extract_feedback_message(
    #     self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    # ) -> Dict[Text, Any]:
    #     feedback_value = tracker.get_slot("feedback_value")
    #     text_of_last_user_message = tracker.latest_message.get("text")
        
    #     if feedback_value == '1':
    #         dispatcher.utter_message(
    #             text=f"Lo siento que no te haya agradado, voy a mejorar gracias a tu mensaje.")
    #     elif feedback_value == '2':
    #         dispatcher.utter_message(
    #             text=f"Chuta, creo que debo mejorar. Voy a ser mejor para la próxima vez.")
    #     elif feedback_value == '3':
    #         dispatcher.utter_message(
    #             text=f"Voy a tomar tus comentarios al pie de la letra para mejorar. No te defraudaré!")
    #     elif feedback_value == '4':
    #         dispatcher.utter_message(
    #             text=f"Gracias por tu comentario, de seguro la próxima vez que me escribas te sorprenderé.")
    #     else:
    #         dispatcher.utter_message(
    #             text=f"Gracias por tus palabras, me ayuda a mejorar constantemente")
        
    #     return {}

    def validate_feedback_value(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `feedback_value` value."""
        print('feedback_value', slot_value)

        if slot_value not in ['1', '2', '3', '4', '5']:
            buttons = [{"title": 'Malo', "payload": '/give_feedback{{"feedback_value": "1"}}'}, {"title": 'Regular', "payload": '/give_feedback{{"feedback_value": "2"}}'},
                       {"title": 'Bueno', "payload": '/give_feedback{{"feedback_value": "3"}}'}, {"title": 'Muy Bueno', "payload": '/give_feedback{{"feedback_value": "4"}}'}, {"title": 'Excelente', "payload": '/give_feedback{{"feedback_value": "5"}}'}]
            dispatcher.utter_message(
                text=f"La valoración que mencionas no existe. Por favor selecciona una de las siguientes valoraciones:", buttons=buttons)
            return {"feedback_value": None}
        else:
            return {"feedback_value": slot_value}

    def validate_feedback_message(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `feedback_message` value."""

        message = slot_value
        text_of_last_user_message = tracker.latest_message.get("text")
        print('message', message)

        if len(text_of_last_user_message) <= 5:
            dispatcher.utter_message(
                text=f"La reseña es muy corta, ¿quiero saber que piensas de mi?.")
            return {"feedback_message": None}
        return {"feedback_message": text_of_last_user_message}


class ActionThanksFeedback(Action):
    def name(self) -> Text:
        return "action_thanks_feedback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        feedback_fill = tracker.get_slot("feedback_fill")
        email = tracker.get_slot("email")

        if feedback_fill is None:
            dispatcher.utter_message(text=f"Gracias por tu reseña, con esto puedo seguir mejorando cada vez más.",
                                     image="https://media.giphy.com/media/Guccz4Oq87bncsm1j4/giphy-downsized.gif")

            date = datetime.datetime.now().isoformat()
            new_record = {
                    "name": tracker.get_slot("first_name"),
                    "email": email,
                    "feedback_value": int(tracker.get_slot("feedback_value")),
                    "feedback_message": tracker.get_slot("feedback_message"),
                    "created_at": date
                }

            table.create(new_record)


            is_mail_sent = send_email("Gracias por tu aporte al desarrollo tecnológico", email, email_content)

            if is_mail_sent:
                dispatcher.utter_message(text=f"Pronto, recibirás un correo con mucho cariño para ti.")
            
            return [SlotSet('feedback_fill', True)]

        dispatcher.utter_message(
            text=f"Ya has dejado tu reseña. Muchas gracias, me ayuda a crecer.")
        return []


class ActionThanksFeedback(Action):
    def name(self) -> Text:
        return "action_feedback_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        feedback_message = tracker.get_slot("feedback_message")
        feedback_fill = tracker.get_slot("feedback_fill")
        print('feedback_fill', feedback_fill)

        if feedback_fill is None:
            dispatcher.utter_message(
                text=f"Aún no has dejado una reseña.")
            dispatcher.utter_message(response="utter_ask_feedback_value")
            return []

        dispatcher.utter_message(
            text=f"Esto fue lo que mencionaste acerca de mi")
        dispatcher.utter_message(
            text=f"Mensaje: {feedback_message}")

        return []


class ActionMyIntroduction(Action):
    def name(self) -> Text:
        return "action_who_you_are"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        email_fill = tracker.get_slot("email_fill")
        print('intent', tracker.get_intent_of_latest_message())
        if (tracker.get_intent_of_latest_message() == "request_clothes" or tracker.get_intent_of_latest_message() == "inform") and email_fill is None:
            dispatcher.utter_message(
                text=f"Antes de mostrarte la ropita quisiera presentarme.")
            dispatcher.utter_message(
                text=f"Mi nombre es Jasmine, soy un asistente de compras.")
            return [SlotSet("clothes_name_value", True)]

        elif (tracker.get_intent_of_latest_message() == "request_clothes" or tracker.get_intent_of_latest_message() == "inform") and email_fill == True:
            return [SlotSet("clothes_name_value", True)]

        dispatcher.utter_message(
            text=f"Mi nombre es Jasmine, soy un asistente de compras.")
        return [SlotSet("clothes_name_value", False)]


class ActionStopRequestClothes(Action):
    """Stops quote form and clears collected data."""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "action_stop_clothes_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        reset_slots = ["gender", "size", "color",
                       "category", "clothes_name_value"]
        # Reset the slot values.
        return [SlotSet(slot, None) for slot in reset_slots]


class ActionStopRequestFeedback(Action):
    """Stops quote form and clears collected data."""

    def name(self) -> Text:
        """Unique identifier for the action."""
        return "action_stop_feedback_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        reset_slots = ["feedback_value", "feedback_message"]
        # Reset the slot values.
        return [SlotSet(slot, None) for slot in reset_slots]


class ActionReviewFeedbackFill(Action):
    def name(self) -> Text:
        return "action_feedack_already_fill"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        feedback_fill = tracker.get_slot("feedback_fill")

        if feedback_fill is True:
            dispatcher.utter_message(
                text=f"Tú ya me has dejado un mensajito para mejorar, pero puedes seguir buscando más ropa.")
        return []
