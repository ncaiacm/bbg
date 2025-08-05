"""
Basic Bloomberg Terminal Connection Test

This script demonstrates how to establish a basic connection to the Bloomberg Terminal.
It's the first step in working with the Bloomberg API.

Prerequisites:
- Bloomberg Terminal installed
- Bloomberg API (blpapi) Python package installed
- Bloomberg Terminal running and logged in

What this script does:
1. Creates a session options object
2. Sets the connection parameters (localhost:8194 is the default)
3. Creates a session
4. Attempts to start the session
5. Prints success or failure message
6. Properly closes the session

Run this script to verify that your Bloomberg Terminal is properly set up
and that you can connect to it from Python.
"""

import blpapi
import sys

def main():
    print("Attempting to connect to Bloomberg Terminal...")
    
    # Create session options
    session_options = blpapi.SessionOptions()
    
    # Configure session options
    session_options.setServerHost('localhost')  # Default Bloomberg Terminal host
    session_options.setServerPort(8194)         # Default Bloomberg Terminal port
    
    # Create a session
    session = blpapi.Session(session_options)
    
    try:
        # Start the session
        if not session.start():
            print("Failed to start session.")
            return
        
        print("Successfully connected to Bloomberg Terminal!")
        
        # At this point, you could open services and make requests
        # But for this basic test, we'll just verify the connection
        
    except Exception as e:
        print(f"Exception occurred: {e}")
        
    finally:
        # Always properly close the session
        print("Stopping session...")
        session.stop()
        print("Session stopped.")

if __name__ == "__main__":
    main()
    print("\nScript completed. If you see 'Successfully connected to Bloomberg Terminal!',")
    print("your connection is working properly.")