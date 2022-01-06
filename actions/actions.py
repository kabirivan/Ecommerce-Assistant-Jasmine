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

client = SearchClient.create("BQCT474121", "b72f4c8a6b93d0afc8221d06c66e1e66")
index = client.init_index("dev_clothes_v2")

names = pathlib.Path("data/names1.txt").read_text().split("\n")

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

        email_fill = tracker.get_slot("email_fill")
        print('email_fill', email_fill)
        if email_fill == False:
            dispatcher.utter_message(
                response="utter_complete_information"
            )
        else:
            dispatcher.utter_message(
                text="Empecemos!"
            )

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

        dispatcher.utter_message(attachment=message)
        return [SlotSet("email_fill", True)]


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

        if gender == "niña":
            if clothes_type == "legging" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_LEGGINGS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de pantalón como: \n- Rojo\n- Azul\n- Morado\n- Negro\n- Gris\n- Celeste\n- Verde\n- Fucsia\n- Turquesa\n- Café"
                )
                return {"color": None}

            if clothes_type == "blusa" and (slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_BLUSAS"]):
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de blusas como: \n- Morado\n- Amarillo\n- Beige\n- Celeste\n- Plomo"
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
                    text=f"Por el momento disponemos de colores de busos como: \n- Azul\n- Plomo\n- Negro\n- Beige\n- Celeste\n- Amarillo\n- Rojo"
                )
                return {"color": None}

            if clothes_type == "polo" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_BOYS_POLOS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de polos como: \n- Rojo\n- Celeste\n- Azul\n- Anaranjado\n- Verde\n- Amarillo"
                )
                return {"color": None}

            if clothes_type == "pantalon" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_BOYS_PANTALONES"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de pantalones como: \n- Amarillo\n- Azul\n- Rojo\n- Plomo\n- Gris"
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
                dispatcher.utter_message(attachment=message_clothes_girls)

                return {"category": None}
            else:
                dispatcher.utter_message(text=f"Excelente elección 👍🏻")
                return {"category": slot_value}

        if gender == "niño":
            if slot_value.lower() not in MOCK_DATA["ALLOWED_CLOTHES_BOYS"]:
                dispatcher.utter_message(
                    text=f"Te cuento que contamos con los siguientes tipos de ropa para niños:"
                )
                dispatcher.utter_message(attachment=message_clothes_boys)
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

        # message = {
        #     "text": "Pick a color:",
        #     "quick_replies": [
        #         {
        #             "content_type": "text",
        #             "title": "Red",
        #             "payload": "<POSTBACK_PAYLOAD>",
        #         },
        #         {
        #             "content_type": "text",
        #             "title": "Green",
        #             "payload": "<POSTBACK_PAYLOAD>",
        #         },
        #         {
        #             "content_type": "text",
        #             "title": "Green",
        #             "payload": "<POSTBACK_PAYLOAD>",
        #         },
        #         {
        #             "content_type": "text",
        #             "title": "Green",
        #             "payload": "<POSTBACK_PAYLOAD>",
        #         },
        #         {
        #             "content_type": "text",
        #             "title": "Green",
        #             "payload": "<POSTBACK_PAYLOAD>",
        #         },
        #         {
        #             "content_type": "text",
        #             "title": "Green",
        #             "payload": "<POSTBACK_PAYLOAD>",
        #         },
        #         {
        #             "content_type": "text",
        #             "title": "Green",
        #             "payload": "<POSTBACK_PAYLOAD>",
        #         },
        #         {
        #             "content_type": "text",
        #             "title": "Green",
        #             "payload": "<POSTBACK_PAYLOAD>",
        #         },
        #     ],
        # }

        if gender == "niña":
            dispatcher.utter_message(
                text=f"Te cuento que contamos con los siguientes tipos de ropa para niñas 👧🏻:"
            )
            dispatcher.utter_message(attachment=message_clothes_girls)
        else:

            dispatcher.utter_message(
                text=f"Te cuento que contamos con los siguientes tipos de ropa para niños 👦🏻:"
            )
            dispatcher.utter_message(attachment=message_clothes_boys)

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
            dispatcher.utter_message(attachment=message)
            # text = f"No disponemos de ese producto en específico. Pero te revisar estos que también son bonitos..."
            # buttons = [{"title": 'Ver más', "payload": '/action_more_productos'}, {"title": 'No gracias', "payload": 'utter_chitchat/thanks'}]
            dispatcher.utter_message(response="utter_ask_feedback_value")

            slots_to_reset = ["gender", "size", "color", "category"]

            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            text = f"No disponemos de ese producto en específico. Pero te revisar estos que también son bonitos..."
            #buttons = [{"title": 'Ver más', "payload": '/action_more_productos'}, {"title": 'No gracias', "payload": 'utter_chitchat/thanks'}]
            dispatcher.utter_message(text=text)

            slots_to_reset = ["gender", "size", "color", "category"]
            return [SlotSet(slot, None) for slot in slots_to_reset]


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

        if name is None:
            dispatcher.utter_message(
                text=f"Hasta pronto {name}, fue un placer chatear contigo 🤗.")
        else:
            dispatcher.utter_message(
                text=f"Chao, cuidate mucho, gracias por escribirme 😊.")
        return []


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
                print('Validacion')
                return ["name_spelled_correctly"] + domain_slots
        return domain_slots

    async def extract_name_spelled_correctly(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        intent = tracker.get_intent_of_latest_message()
        first_name = tracker.get_slot("first_name")
        print('first_name', first_name)
        if first_name is not None and intent == "give_name":
            return {"name_spelled_correctly": None}
        elif intent == "affirm":
            return {"name_spelled_correctly": intent == "affirm"}
        elif intent == "deny":
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
            return {"first_name": tracker.get_slot("first_name"), "name_spelled_correctly": True}
        elif tracker.get_slot("first_name") and intent == "deny":
            return {"first_name": None, "name_spelled_correctly": None}
        elif tracker.get_slot("name_spelled_correctly") is None:
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

        print('tesst', tracker.get_slot("requested_slot"))
        print(f"First name given = {slot_value} length = {len(slot_value)}")

        if tracker.get_slot("requested_slot") == "first_name":
            print('first_name_p', tracker.get_slot("first_name"))
            if len(slot_value) <= 1:
                dispatcher.utter_message(
                    text=f"El nombre es muy corto, parece que te faltan caracteres.")
                return {"first_name": None}
            else:
                print('slot_value', slot_value)
                return {"first_name": slot_value, "last_first_name": slot_value}

        return {"first_name": tracker.get_slot("last_first_name")}


class ValidateFeedbackForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_feedback_form"

    def validate_feedback_value(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `feedback_value` value."""
        print('feedback_value', slot_value)
        if slot_value not in ['1', '2', '3', '4']:
            buttons = [{"title": 'Malo', "payload": '/give_feedback{{"feedback_value": "1"}}'}, {"title": 'Regular', "payload": '/give_feedback{{"feedback_value": "2"}}'},
                       {"title": 'Bueno', "payload": '/give_feedback{{"feedback_value": "3"}}'}, {"title": 'Excelente', "payload": '/give_feedback{{"feedback_value": "4"}}'}]
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
        print('message', message)

        if len(message) <= 5:
            dispatcher.utter_message(
                text=f"La reseña es muy corta, ¿quiero saber que piensas de mi?.")
        return {"feedback_message": slot_value}


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
        print('message', tracker.get_slot("feedback_message"))

        if feedback_fill == False:
            dispatcher.utter_message(text=f"Gracias por tu reseña, es muy importante para mi mejoramiento.",
                                     image="https://media.giphy.com/media/BYoRqTmcgzHcL9TCy1/giphy.gif")
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

        if feedback_fill == False:
            dispatcher.utter_message(
                text=f"Aún no has dejado una reseña.")
            dispatcher.utter_message(response="utter_ask_feedback_value")
            return []

        dispatcher.utter_message(
            text=f"Esto fue lo que mencionaste acerca de mi")
        dispatcher.utter_message(
            text=f"Mensaje: {feedback_message}")

        return []
