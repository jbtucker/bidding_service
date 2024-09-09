import quickfix as fix
import logging
from fix_engine.message_factory import FixMessageFactory

class QuoteRequestHandler:
    """
    Handler for processing QuoteRequest messages.
    """
    def __init__(self):
        self.logger = logging.getLogger('fix_logger')
        self.message_factory = FixMessageFactory()

    def handle(self, message, sessionID):
        try:
            self.logger.info("Handling QuoteRequest message")

            # Extracting necessary fields from the QuoteRequest message
            quote_req_id = message.getField(fix.QuoteReqID())
            symbol = message.getField(fix.Symbol())
            security_id = message.getField(fix.SecurityID())
            bid_size = message.getField(fix.OrderQty())
            
            # Implement the business logic to decide whether to bid
            should_bid, bid_price = self.evaluate_quote_request(symbol, security_id, bid_size)
            
            if should_bid:
                # Create and send a QuoteResponse message using the message factory
                quote_response = self.message_factory.create_quote_response(
                    quote_id=quote_req_id,
                    bid_px=bid_price,
                    offer_px=0.0,  # Assuming offer price is not applicable here
                    symbol=symbol,
                    security_id=security_id,
                    quantity=bid_size
                )
                
                fix.Session.sendToTarget(quote_response, sessionID)
                self.logger.info(f"QuoteResponse sent for QuoteReqID {quote_req_id}")
            else:
                self.logger.info(f"QuoteRequest {quote_req_id} was not pursued")
        
        except fix.FieldNotFound as e:
            self.logger.error(f"Field not found: {e}")
        except Exception as e:
            self.logger.error(f"Error handling QuoteRequest: {e}")

    def evaluate_quote_request(self, symbol, security_id, bid_size):
        """
        Evaluate whether to bid on the QuoteRequest.

        This is a placeholder for business logic.
        """
        # Implement your custom logic here
        # For demonstration, let's assume we always bid if the bid size is greater than 1000
        if int(bid_size) > 1000:
            return True, 100.25  # Return True and a bid price
        return False, 0.0  # Return False and no bid price


class MessageHandler:
    """
    Main message handler that dispatches messages to specific handlers based on message type.
    """
    def __init__(self):
        self.logger = logging.getLogger('fix_logger')
        self.quote_request_handler = QuoteRequestHandler()

    def handle_message(self, message, sessionID):
        try:
            msg_type = fix.MsgType()
            message.getHeader().getField(msg_type)

            if msg_type.getValue() == fix.MsgType_QuoteRequest:
                self.quote_request_handler.handle(message, sessionID)
            else:
                self.logger.warning(f"Unhandled message type: {msg_type.getValue()}")
        
        except fix.FieldNotFound as e:
            self.logger.error(f"Field not found in message: {e}")
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
