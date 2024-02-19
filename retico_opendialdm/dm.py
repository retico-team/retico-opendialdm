"""A module for Dialogue Management provided by PyOpenDial"""
from multipledispatch import dispatch

# retico
from retico_core import abstract
from retico_core import IncrementalUnit
from retico_core.dialogue import DialogueActIU
from retico_opendialdm.concept_val import ConceptVal

# opendial
import sys
import os
sys.path.append(os.environ['PYOD'])
from dialogue_system import DialogueSystem
from datastructs.assignment import Assignment
from modules.simulation.simulator import Simulator
from readers.xml_domain_reader import XMLDomainReader
from bn.distribs.distribution_builder import CategoricalTableBuilder
from dialogue_state import DialogueState
from modules.module import Module
from collections.abc import Collection
from bn.values.none_val import NoneVal

class DialogueDecisionIU(abstract.IncrementalUnit):
    """A Dialogue Manager Decision.

    This IU represents a Dialogue Decision together with concepts and their
    values. In this implementation only a single decision can be expressed with a
    single IU.

    Attributes:
        decision (string): A representation of the current act as a string.
        concepts (dict): A dictionary of names of concepts being mapped on to
            their actual values.
    """

    @staticmethod
    def type():
        return "Dialogue Decision Incremental Unit"

    def __init__(self, creator=None, iuid=0, previous_iu=None, grounded_in=None,
                 payload=None, decision=None, concepts=None, **kwargs):
        """Initialize the DialogueDecisionIU with decision.

        Args:
            act (string): A representation of the act.
            concepts (dict): A representation of the concepts as a dictionary.
        """
        super().__init__(creator=creator, iuid=iuid, previous_iu=previous_iu,
                         grounded_in=grounded_in, payload=payload)
        self.decision = decision
        self.concepts = {}
        if concepts:
            self.concepts = concepts
        self.confidence = 0.0

    def set_act(self, decision, concepts=None, confidence=1.0):
        """Set the act and concept of the IU.

        Old acts or concepts will be overwritten.

        Args:
            act (string): The act of the IU as a string.
            concepts (dict): A dictionary containing the new concepts.
            confidence (float): Confidence of the act prediction
        """
        self.decision = decision
        if concepts:
            self.concepts = concepts
        self.confidence = confidence
        self.payload = {'decision':decision, 'concepts':concepts}


class OpenDialModule(abstract.AbstractModule, Module):
    """The OpenDial module for Dialogue Management.

    Attributes:
        domain_dir (str): The path to the directory of the domain model (XML) for OpenDial
    """

    @staticmethod
    def name():
        return "OpenDial DM Module"

    @staticmethod
    def description():
        return "A Module providing Dialogue Management provided by OpenDial"

    @staticmethod
    def input_ius():
        return [DialogueActIU,IncrementalUnit]

    @staticmethod
    def output_iu():
        return DialogueDecisionIU

    def __init__(self, domain_dir, variables=None, **kwargs):
        """Initializes the OpenDialModule.

        Args:
            domain_dir (str): The path to the directory of the domain model (XML) for OpenDial
        """
        super().__init__(**kwargs)
        self.domain_dir = domain_dir
        self._system = DialogueSystem()
        self.cache = None
        self._paused = False
        self._input_iu = None
        self._variables = variables
        self._prior_state = {}

    # def new_utterance(self):
    #     self._system.add_content('concept', ConceptVal('','',0)) 
    #     super().new_utterance()

    def process_update(self, update_message):
        
        for iu,um in update_message:
            if um == abstract.UpdateType.ADD:
                self.process_iu(iu)
            elif um == abstract.UpdateType.REVOKE:
                self.process_revoke(iu)

    def process_iu(self, input_iu):
        state = input_iu.payload
        update_occured = False
        '''
        The DM can handle any attr/valu info, so we are assuming any IU that has
        something for updating the DM uses a dict as its payload
        '''
        if  type(state)!=dict: return

        print("DM got an IU", type(input_iu))
        for key in state:
            if self._variables is not None and key in self._variables:
                val = state[key]
                if isinstance(val, str) and val.isdigit():
                    val = float(val)
                if isinstance(val, int):
                    val = float(val)
                if key in self._prior_state:
                    if self._prior_state[key] == val: # no need to update
                        # print(self._prior_state)
                        pass
                #     else:
                #         print('dm state update {}={}'.format(key, val))
                # else:
                #     print('dm state update {}={}'.format(key, val))
                if isinstance(val, list):
                    val = ' '.join(val)
                self._prior_state[key] = val
                # print(key, type(key), val, type(val))
                self._system._cur_state.add_to_state(Assignment(key, val))
                update_occured = True
        if update_occured:
            self._system.update() # update opendial after the full state has been inserted

        return None

    def process_revoke(self, revoked_iu):
        pass #for now
        #print('dm revoke({})'.format(revoked_iu.payload))

    def setup(self):
        self._system.change_domain(XMLDomainReader.extract_domain(self.domain_dir))
        self._system.change_settings(self._system.get_settings())
        self._system.attach_module(self) # modules can read the dialogue state
        self._system.start_system()

    '''
    Everything below here belongs to the OpenDial Module 
    '''

    def start(self):
        """
        Starts the module.
        """
        self._paused = False

    @dispatch(DialogueState, Collection)
    def trigger(self, state, update_vars):
        # print(f"update vars: {update_vars}")
        if 'decision' in update_vars and state.has_chance_node('decision'):
            action = str(state.query_prob('decision').get_best())
            print(f"action: {action}")
            output_iu = self.create_iu(self._input_iu)
            output_iu.set_act(action, {})
            # print(f"dm output iu: {output_iu}. ")
            # print(output_iu.payload)
            new_um = abstract.UpdateMessage.from_iu(output_iu, abstract.UpdateType.ADD)     
            self.append(new_um)
            # concept_val = state.query_prob('concept').get_best()
            # if isinstance(concept_val, ConceptVal):
            #     output_iu = self.create_iu(self._input_iu)
            #     output_iu.set_act(action, {concept_val._concept:concept_val._value}, concept_val._confidence)
            #     self.append(output_iu)


    @dispatch(bool)
    def pause(self, to_pause):
        """
        Pauses the module.

        :param to_pause: whether to pause the module or not
        """
        self._paused = to_pause

    def is_running(self):
        """
        Returns whether the module is currently running or not.

        :return: whether the module is running or not.
        """
        return not self._paused