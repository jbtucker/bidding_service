import quickfix as fix
import quickfix44 as fix44
import logging
from fix_engine.message_handlers import QuoteRequestHandler
from utils.error_handling import log_and_raise, ConfigurationError, ConnectionError

class FixServiceApplication(fix.Application):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('fix_logger')
        self.quote_request_handler = QuoteRequestHandler()

    def onCreate(self, sessionID):
        self.logger.info(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        self.logger.info(f"Logon - Session connected: {sessionID}")

    def onLogout(self, sessionID):
        self.logger.info(f"Logout - Session disconnected: {sessionID}")

    def toAdmin(self, message, sessionID):
        self.logger.debug(f"To Admin: {message}")

    def fromAdmin(self, message, sessionID):
        self.logger.debug(f"From Admin: {message}")

    def toApp(self, message, sessionID):
        self.logger.debug(f"To App: {message}")
        self.logger.debug(f"Sent: {message}")
        #will use message factory here to send bid

    def fromApp(self, message, sessionID):
        self.logger.debug(f"From App: {message}")
        try:
            msg_type = fix.MsgType()
            message.getHeader().getField(msg_type)
            if msg_type.getValue() == fix.MsgType_QuoteRequest:
                self.quote_request_handler.handle(message, sessionID)
            else:
                self.logger.warning(f"Unhandled message type: {msg_type.getValue()}")
        except fix.FieldNotFound as e:
            self.logger.error(f"Field not found in message: {e}")

def start_fix_service(self):
    try:
        # Load the FIX settings from the configuration file
        settings = fix.SessionSettings('config/fix_settings.cfg')
        
        # Initialize the application
        application = FixServiceApplication()
        
        # Initialize the store factory (for message storage)
        storeFactory = fix.FileStoreFactory(settings)
        
        # Initialize the log factory (for logging)
        logFactory = fix.FileLogFactory(settings)
        
        # Create the FIX acceptor or initiator
        initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
        
        # Start the service
        initiator.start()
        
        # Keep the service running
        self.logger.info("FIX service started and running.")
        while True:
            pass  # This keeps the service running. Use a more graceful method in production.

    except fix.ConfigError as e:
        logging.getLogger('fix_logger').error(f"Configuration error: {e}")
        ConfigurationError(e)
    except fix.RuntimeError as e:
        logging.getLogger('fix_logger').error(f"Runtime error: {e}")

if __name__ == "__main__":
    start_fix_service()
