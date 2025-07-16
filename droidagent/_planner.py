import os
import logging
import time

from .config import agent_config
from .app_state import AppState

from .types.action import *
from .types.task import Task
from .utils.logger import Logger
from .prompts.plan import *
from .memories.working_memory import WorkingMemory

from collections import defaultdict

RETRY_COUNT = 3


logger = Logger(__name__)


class Planner:
    def __init__(self, memory, prompt_recorder=None):
        self.memory = memory
        self.prompt_recorder = prompt_recorder

    """
    Task-based planning (independence between planner and actor)
    """
    def plan_task(self):
        logger.info("Starting task planning...")
        
        try:
            task_desc, task_end_condition, plan, first_action = prompt_new_task(self.memory, self.prompt_recorder)
            
            if task_desc is None or first_action is None:
                logger.warning("Task planning failed: task_desc or first_action is None")
                return None
            
            logger.info(f"Task planned successfully: {task_desc}")
            
            task = Task(task_desc, None, plan=plan, end_condition=task_end_condition) # TODO: seperate task summary and description

            # TODO: Separate to a component that can universally record visitied states/activities
            task.add_explored_state(AppState.current_gui_state)
            task.add_explored_activity(AppState.current_activity)

            task.entry_id = self.memory.task_memory.record_task(task, f'{agent_config.persona_name} planned a new task: {task.summary}')
            
            self.memory.working_memory = WorkingMemory(task)
            self.memory.working_memory.add_step(first_action, AppState.current_activity, 'ACTION')
            
            logger.info(f"Task planning completed successfully, first action: {first_action}")
            return first_action
            
        except Exception as e:
            logger.error(f"Task planning failed with exception: {str(e)}")
            return None
