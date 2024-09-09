import quickfix as fix
import quickfix44 as fix44

class FixMessageFactory:
    def __init__(self):
        pass

    def create_quote_response(self, quote_id, bid_px, offer_px, symbol, security_id, quantity):
        """
        Create a QuoteResponse message in response to a QuoteRequest.
        
        Args:
            quote_id (str): Unique identifier of the quote.
            bid_px (float): The bid price.
            offer_px (float): The offer price.
            symbol (str): The symbol of the security.
            security_id (str): The security identifier (e.g., CUSIP or ISIN).
            quantity (float): The quantity for the bid.
        
        Returns:
            quickfix.Message: A FIX message object representing the QuoteResponse.
        """
        message = fix44.Quote()
        
        # Set the necessary fields in the FIX message
        message.setField(fix.QuoteID(quote_id))
        message.setField(fix.BidPx(bid_px))
        message.setField(fix.OfferPx(offer_px))
        message.setField(fix.Symbol(symbol))
        message.setField(fix.SecurityID(security_id))
        message.setField(fix.OrderQty(quantity))

        return message

    def create_order(self, order_id, side, symbol, security_id, order_qty, price, order_type=fix.OrdType_LIMIT):
        """
        Create an Order message (New Order Single).

        Args:
            order_id (str): Unique identifier of the order.
            side (str): Side of the order ('1' for buy, '2' for sell).
            symbol (str): The symbol of the security.
            security_id (str): The security identifier (e.g., CUSIP or ISIN).
            order_qty (float): The quantity of the order.
            price (float): The price at which to execute the order.
            order_type (char): The type of order (default is LIMIT).

        Returns:
            quickfix.Message: A FIX message object representing the New Order Single.
        """
        message = fix44.NewOrderSingle()

        # Set the necessary fields in the FIX message
        message.setField(fix.ClOrdID(order_id))
        message.setField(fix.Side(side))
        message.setField(fix.Symbol(symbol))
        message.setField(fix.SecurityID(security_id))
        message.setField(fix.OrderQty(order_qty))
        message.setField(fix.Price(price))
        message.setField(fix.OrdType(order_type))
        
        # Set additional standard fields
        message.setField(fix.TransactTime())
        message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))

        return message

    def create_execution_report(self, order_id, exec_id, exec_type, ord_status, symbol, security_id, quantity, last_px):
        """
        Create an ExecutionReport message.

        Args:
            order_id (str): The order ID to which this report relates.
            exec_id (str): Unique identifier of the execution.
            exec_type (char): Type of execution (e.g., '0' for New, '1' for Partial Fill).
            ord_status (char): The current status of the order (e.g., '0' for New, '2' for Filled).
            symbol (str): The symbol of the security.
            security_id (str): The security identifier (e.g., CUSIP or ISIN).
            quantity (float): The quantity executed.
            last_px (float): The price at which the last quantity was executed.

        Returns:
            quickfix.Message: A FIX message object representing the ExecutionReport.
        """
        message = fix44.ExecutionReport()

        # Set the necessary fields in the FIX message
        message.setField(fix.ClOrdID(order_id))
        message.setField(fix.ExecID(exec_id))
        message.setField(fix.ExecType(exec_type))
        message.setField(fix.OrdStatus(ord_status))
        message.setField(fix.Symbol(symbol))
        message.setField(fix.SecurityID(security_id))
        message.setField(fix.LastQty(quantity))
        message.setField(fix.LastPx(last_px))
        message.setField(fix.LeavesQty(0 if ord_status == fix.OrdStatus_FILLED else quantity))
        message.setField(fix.CumQty(quantity if ord_status == fix.OrdStatus_FILLED else 0))

        return message

    # Add more methods here for creating different types of FIX messages
