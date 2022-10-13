
from typing import Any, Text, Dict, List
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker, FormValidationAction
from dateutil import parser
import datetime
import time
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
)
from actions.parsing import (
    parse_duckling_time_as_interval,
    parse_duckling_time,
    get_entity_details,
    parse_duckling_currency,
)
from producer import (
    sendClientToTopic,
    sendNameToTopic, 
    sendBudgetToTopic, 
    sendPeopleResourceToTopic, 
    sendDaysResourceToTopic, 
    sendDeliveryDateToTopic,
    sendDeveloperToTopic,
    sendQualityToTopic,
    sendDevopsToTopic,
    sendSupportToTopic
)
from actions.custom_forms import CustomFormValidationAction
from database.connection_db import list_known_names, list_known_projects_Id,get_template
from consumer import consumeMessage
import json
import datetime
from kafka import KafkaConsumer
   




class ActionCreateProject(Action):
    """Create project from O"."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_create_project"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        """Executes the action"""
        slots = {
            "AA_CONTINUE_FORM": None,
            "zz_confirm_form": None,
            "client":None,
            "project_name": None,
            "amount-of-money": None,
            "number": None,
            "people_ressource":None,
            "days_ressource":None,
            "developer":None,
            "quality":None,
            "devops":None,
            "support":None,
            "delivery_date":None
        }

              

        if tracker.get_slot("zz_confirm_form") == "yes":
            amount_of_money = float(tracker.get_slot("amount-of-money"))
            client = tracker.get_slot("client")
            project_name = tracker.get_slot("project_name")
            people_ressource = int(tracker.get_slot("people_ressource"))
            days_ressource = int(tracker.get_slot("days_ressource"))
            developer= int(tracker.get_slot("developer"))
            quality= int(tracker.get_slot("quality"))
            devops= int(tracker.get_slot("devops"))
            support= int(tracker.get_slot("support"))
            delivery_date = tracker.get_slot("delivery_date")
            sendClientToTopic(client)
            sendNameToTopic(project_name)
            sendBudgetToTopic(amount_of_money)
            sendPeopleResourceToTopic(people_ressource)
            sendDaysResourceToTopic(days_ressource)
            sendDeveloperToTopic(developer)
            sendQualityToTopic(quality)
            sendDevopsToTopic(devops)
            sendSupportToTopic(support)
            sendDeliveryDateToTopic(delivery_date)

            dispatcher.utter_message(response="utter_data_saved")
            dispatcher.utter_message(text=f" I'will go back with  notification after chekching your budget 😀")
            dispatcher.utter_message(response="utter_ask_whatelse") 

      
        else:
            dispatcher.utter_message(response="utter_project_cancelled")
            dispatcher.utter_message(response="utter_ask_whatelse") 

        return [SlotSet(slot, value) for slot, value in slots.items()]

    
class ValidateCreateProjectForm(CustomFormValidationAction):
    """Validates Slots of the create_project_form"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "validate_create_project_form"
    
    async def validate_client(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'client' slot"""
        List = ["BNA", "BIAT","UIB","QNB"]
        if value in List:
            return {"client": value}
        
        dispatcher.utter_message(response="utter_unknown_client")
        return {"client": None}


    async def validate_project_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'project_name' slot"""
        # It is possible that both Spacy & DIET extracted the project_name
        # Just pick the first one


        name = value.lower() if value else None
        known_names = list_known_names()
       
        if name is not None and name not in known_names:
            return {"project_name": name.title()}

      

        dispatcher.utter_message(response="utter_unknown_name", project_name=value)
        return {"project_name": None}



    async def validate_amount_of_money(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'amount-of-money' slot"""
        budget_balance = 1000
        try:
            entity = get_entity_details(
                tracker, "amount-of-money"
            ) or get_entity_details(tracker, "number")
            amount_currency = parse_duckling_currency(entity)
            
            if not amount_currency:
                raise TypeError
            if budget_balance > float(amount_currency.get("amount-of-money")):
                dispatcher.utter_message(response="utter_insufficient_budget")
                return {"amount-of-money": None}
            return amount_currency
        except (TypeError, AttributeError):
            dispatcher.utter_message(response="utter_no_budget_amount:")
            return {"amount-of-money": None}
        

    
    async def validate_people_ressource(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'people_ressource' slot"""
        if int(value) <= 0:
            dispatcher.utter_message(text=f" We only accept number of people ressource > 0")
            return {"people_ressource": None}
        return {"people_ressource": value}
    
    async def validate_days_ressource(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'days_ressource' slot"""
        if int(value) <= 0:
            dispatcher.utter_message(text=f" We only accept number of days ressource > 0")
            return {"days_ressource": None}
        return {"days_ressource": value}
    
    async def validate_developer(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'developer' slot"""
        if int(value) < 0:
            dispatcher.utter_message(text=f" We only accept number of profil developer >= 0")
            return {"developer": None}
        return {"developer": value}
    
    async def validate_quality(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'quality' slot"""
        if int(value) < 0:
            dispatcher.utter_message(text=f" We only accept number of profil QA >= 0")
            return {"quality": None}
        return {"quality": value}
    async def validate_devops(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'devops' slot"""
        if int(value) < 0:
            dispatcher.utter_message(text=f" We only accept number of profil devops >= 0")
            return {"devops": None}
        return {"devops": value}
    async def validate_support(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'support' slot"""
        if int(value) < 0:
            dispatcher.utter_message(text=f" We only accept number of profil IT support >= 0")
            return {"support": None}
        return {"support": value}
    
    
    async def validate_delivery_date(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'delivery_date' slot"""
    
        currDate = datetime.datetime.now().date()
        if value <= str(currDate):
            dispatcher.utter_message(text=f" The delivery date must be greater than {currDate} ")
            return {"delivery_date": None}
        return {"delivery_date": value}


    async def validate_zz_confirm_form(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'zz_confirm_form' slot"""
        if value in ["yes", "no"]:
            return {"zz_confirm_form": value}

        return {"zz_confirm_form": None}


class ActionShowMethod(Action):
    """Shows Methods how to create project"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_show_method"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
     
        dispatcher.utter_message(response="utter_project_method")
        dispatcher.utter_message(response="utter_ask_whatelse") 

        events = []
        active_form_name = tracker.active_form.get("name")
        if active_form_name:
            # keep the tracker clean for the predictions with form switch stories
            events.append(UserUtteranceReverted())
            # trigger utter_ask_{form}_AA_CONTINUE_FORM, by making it the requested_slot
            events.append(SlotSet("AA_CONTINUE_FORM", None))
            # avoid that bot goes in listen mode after UserUtteranceReverted
            events.append(FollowupAction(active_form_name))

        return events
    
class ActionCopyProject(Action):
    """ Copy Project"."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_copy_project"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        """Executes the action"""
        slots = {
            "project_id": None,
        }
        print(tracker.get_slot("project_id") )
        Id = tracker.get_slot("project_id")
        print(Id) 
        Id1 = str(Id)   
        known_Id = list_known_projects_Id()
        if Id is not None and Id1  in known_Id:
            res = get_template(Id)
            print(res)
            print(res[1]) 
            dispatcher.utter_message(text=f" You find atteched a copy of project template with Id {Id}") 
            dispatcher.utter_message(
                text=f" project name : {res[0]}\n- Budget : {res[1]}\n- days/people needed : {res[3]}/{res[2]}\n- grade : Developer, numbers :{res[6]}\n- grade : Quality, numbers :{res[7]}\n- grade : DevOps, numbers :{res[8]}\n- grade : IT Support, numbers :{res[9]}\n- Sum salaries of employees : {res[10]}\n- Delivery Date : {res[4]}\n- Budget_Monthly : {res[5]}") 
            dispatcher.utter_message(response="utter_ask_whatelse") 
        else:
            dispatcher.utter_message(response="utter_unknown_project_id")

        return [SlotSet(slot, value) for slot, value in slots.items()]
class ActionSessionStart(Action):
    """Executes at start of session"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_session_start"

    @staticmethod
    def _slot_set_events_from_tracker(
        tracker: "Tracker",
    ) -> List["SlotSet"]:
        """Fetches SlotSet events from tracker and carries over keys and values"""

        # when restarting most slots should be reset
        relevant_slots = ["currency"]

        return [
            SlotSet(
                key=event.get("name"),
                value=event.get("value"),
            )
            for event in tracker.events
            if event.get("event") == "slot" and event.get("name") in relevant_slots
        ]
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Executes the custom action"""
        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        events.extend(self._slot_set_events_from_tracker(tracker))


        # add `action_listen` at the end
        events.append(ActionExecuted("action_listen"))

        return events
class ActionRestart(Action):
    """Executes after restart of a session"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_restart"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Executes the custom action"""
        return [Restarted(), FollowupAction("action_session_start")]