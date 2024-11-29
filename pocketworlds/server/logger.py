"""
Author: Adam Loeckle
Date: 11/26/2024

"""

import logging
from datetime import datetime
import uuid

class Logger:
    _instance = None
    
    def __new__(cls, name: str, log_dir: str = "logs"):
        cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, name: str, log_dir: str = "logs"):

        if not hasattr(self, 'session_data'):
            # Session tracking
            self.session_id = str(uuid.uuid4())[:8]
            self.session_start = datetime.now()
            self.interaction_count = 0
            self.session_data = {
                'name': name,
                'session_id': self.session_id,
                'start_time': self.session_start,
                'interactions': []
            }

            time = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"{log_dir}/{name}_session_{self.session_id}_{time}.log"

            self.logger = logging.getLogger(f"{name}_{self.session_id}")
            self.logger.setLevel(logging.INFO)

            # Clear any existing handlers
            self.logger.handlers = []

            file_handler = logging.FileHandler(log_filename)
            formatter = logging.Formatter(
                '%(asctime)s [session: %(session_id)s] [interaction: %(interaction)s] - %(message)s'
            )
            file_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            
            # Log session start
            self.log_with_context("Session started")

    def log_with_context(self, message: str, level: str = 'info', metadata: dict = None):
        self.interaction_count += 1
        extra = {
            'session_id': self.session_id,
            'interaction': self.interaction_count
        }
        
        if metadata:
            message = f"{message} | metadata: {metadata}"
            
        if level == 'info':
            self.logger.info(message, extra=extra)
        elif level == 'error':
            self.logger.error(message, extra=extra)
        elif level == 'warning':
            self.logger.warning(message, extra=extra)

    def end_session(self):
        duration = datetime.now() - self.session_start
        self.log_with_context(
            f"Session ended - Duration: {duration}, Total interactions: {self.interaction_count}"
        )

    def get_logger(self) -> logging.Logger:
        self.logger.log_with_context = self.log_with_context
        return self.logger