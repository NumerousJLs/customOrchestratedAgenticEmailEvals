#!/usr/bin/env python3
"""
Email Analysis System - Local Application Launcher

This script starts the Flask web application for the email analysis system.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['flask', 'flask_socketio', 'openai']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print("❌ Missing required packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install them with:")
        print("   pip install flask flask-socketio openai python-socketio")
        return False

    return True

def main():
    print("=" * 60)
    print("📧 Email Analysis System - Local Web Application")
    print("=" * 60)
    print()

    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)

    print("✅ All dependencies installed!")
    print()

    # Start the application
    print("🚀 Starting the application...")
    print("📍 The app will be available at: http://localhost:5000")
    print()
    print("💡 Tips:")
    print("   - Use the example emails to get started quickly")
    print("   - Watch the agents communicate in real-time")
    print("   - Press Ctrl+C to stop the server")
    print()
    print("=" * 60)
    print()

    try:
        # Import and run the Flask app
        from app import app, socketio
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down... Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
