import os
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FormValidation, SlotSet, EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from algoliasearch.search_client import SearchClient
import requests


client = SearchClient.create("BQCT474121", "b72f4c8a6b93d0afc8221d06c66e1e66")
index = client.init_index("dev_clothes_v2")

MOCK_DATA = json.load(open("actions/mock_data.json", "r"))

message_clothes_girls = {
    "attachment": {
        "type": "template",
        "payload": {"template_type": "generic", "elements": MOCK_DATA["CLOTHES_GIRLS"]},
    }
}

message_clothes_boys = {
    "attachment": {
        "type": "template",
        "payload": {"template_type": "generic", "elements": MOCK_DATA["CLOTHES_BOYS"]},
    }
}


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
            if clothes_type == "pantalones" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_PANTALONES"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de pantalón como: \n- Morado\n- Amarillo\n- Negro\n- Rosado\n- Celeste\n- Rojo\n- Palo de Rosa"
                )
                return {"color": None}
            
            if clothes_type == "blusas" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_BLUSAS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de blusas como: \n- Morado\n- Amarillo\n- Negro\n- Rosado\n- Celeste\n- Rojo"
                )
                return {"color": None}
            
            if clothes_type == "pijamas" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_PIJAMAS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de pijamas como: \n- Morado\n- Amarillo\n- Rojo\n- Celeste"
                )
                return {"color": None}

            if clothes_type == "busos" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_GIRLS_BUSOS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores como: \n- Rosado\n- Amarillo\n- Negro"
                )
                return {"color": None} 
            
            return {"color": slot_value}

        if gender == "niño":
            if clothes_type == "busos" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_BOYS_BUSOS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de busos como: \n- Azul\n- Plomo\n- Negro\n- Beige\n- Celeste\n- Amarillo\n- Rojo"
                )
                return {"color": None} 
            
            if clothes_type == "polos" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_BOYS_POLOS"]:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores de polos como: \n- Rojo\n- Celeste\n- Azul\n- Anaranjado\n- Verde\n- Amarillo"
                )
                return {"color": None} 
            
            if clothes_type == "pantalones" and slot_value.lower() not in MOCK_DATA["ALLOWED_COLORS_BOYS_PANTALONES"]:
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
        print("category", slot_value)

        if gender == "niña":
            if slot_value.lower() not in MOCK_DATA["ALLOWED_CLOTHES_GIRLS"]:
                dispatcher.utter_message(
                    text=f"Lo siento eso no tenemos, pero te cuento que contamos con los siguientes tipos de ropa para niñas:",
                )
                dispatcher.utter_message(json_message=message_clothes_girls)

                return {"category": None}
            else:
                dispatcher.utter_message(text=f"Excelente elección 👍🏻")
                return {"category": slot_value}

        if gender == "niño":
            if slot_value.lower() not in MOCK_DATA["ALLOWED_CLOTHES_BOYS"]:
                dispatcher.utter_message(
                    text=f"Te cuento que contamos con los siguientes tipos de ropa para niños:"
                )
                dispatcher.utter_message(json_message=message_clothes_girls)
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
