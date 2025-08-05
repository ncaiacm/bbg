"""
Simple Data Retrieval for a Single Ticker

This script demonstrates how to retrieve a single data point for a stock ticker
from the Bloomberg Terminal.

Prerequisites:
- Bloomberg Terminal installed and running
- Bloomberg API (blpapi) Python package installed
- Successfully ran 01_basic_connection.py

What this script does:
1. Establishes a connection to Bloomberg Terminal
2. Opens the reference data service
3. Creates a request for a single field (LAST_PRICE) for a single ticker (AAPL US Equity)
4. Sends the request and processes the response
5. Displays the retrieved data
6. Properly closes the session

This is a basic building block for more complex Bloomberg data retrieval operations.
"""

import blpapi
import sys

def main():
    print("Retrieving data for a single ticker...")
    
    # Create and configure session options
    session_options = blpapi.SessionOptions()
    session_options.setServerHost('localhost')
    session_options.setServerPort(8194)
    
    # Create a session
    session = blpapi.Session(session_options)
    
    try:
        # Start the session
        if not session.start():
            print("Failed to start session.")
            return
        
        print("Successfully connected to Bloomberg Terminal!")
        
        # Open the reference data service
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata service")
            return
            
        print("Reference data service opened successfully")
        
        # Get the reference data service
        refdata_service = session.getService("//blp/refdata")
        
        # Create the request
        request = refdata_service.createRequest("ReferenceDataRequest")
        
        # Add a ticker - using Apple as an example
        # Note: Bloomberg tickers typically end with " Equity" for stocks
        ticker = "AAPL US Equity"
        request.getElement("securities").appendValue(ticker)
        
        # Add a field - requesting the last price
        field = "LAST_PRICE"
        request.getElement("fields").appendValue(field)
        
        print(f"Requesting {field} for {ticker}...")
        
        # Send the request
        session.sendRequest(request)
        
        # Process the response
        while True:
            event = session.nextEvent()
            
            # Print the event type
            print(f"Event Type: {event.eventType()}")
            
            # Process messages in the event
            for msg in event:
                # Check if this is the response we're looking for
                if msg.messageType() == blpapi.Name("ReferenceDataResponse"):
                    # Get the security data
                    security_data = msg.getElement("securityData")
                    
                    # For each security in the response
                    for i in range(security_data.numValues()):
                        security = security_data.getValue(i)
                        ticker_name = security.getElementAsString("security")
                        
                        # Check if there was an error
                        if security.hasElement("securityError"):
                            error_msg = security.getElement("securityError").getElementAsString("message")
                            print(f"Error for {ticker_name}: {error_msg}")
                            continue
                        
                        # Get the field data
                        field_data = security.getElement("fieldData")
                        
                        # Check if the field exists
                        if field_data.hasElement(field):
                            value = field_data.getElement(field).getValue()
                            print(f"\nResult: {ticker_name} {field} = {value}")
                        else:
                            print(f"Field {field} not found for {ticker_name}")
            
            # Check if this is the final response
            if event.eventType() == blpapi.Event.RESPONSE:
                break
                
    except Exception as e:
        print(f"Exception occurred: {e}")
        
    finally:
        # Always properly close the session
        print("\nStopping session...")
        session.stop()
        print("Session stopped.")

if __name__ == "__main__":
    main()
    print("\nScript completed. If you see a LAST_PRICE value, the data retrieval was successful.")