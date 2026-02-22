import os
import sys

# Set dummy env vars for testing
os.environ["API_ID"] = "12345"
os.environ["API_HASH"] = "abcdef123456"
os.environ["BOT_TOKEN"] = "123456789:abcdefghijklmnopqrstuvwxyz"
os.environ["BIN_CHANNEL"] = "-1001234567890"
os.environ["DATABASE_URL"] = "mongodb+srv://user:pass@cluster0.mongodb.net/dbname"

try:
    print("Importing WebStreamer...")
    import WebStreamer  # noqa: F401
    print("WebStreamer imported successfully.")

    # Check if plugins imported StartTime correctly
    from WebStreamer.bot.plugins import start  # noqa: F401
    print("WebStreamer.bot.plugins.start imported successfully.")

    from WebStreamer.bot.plugins import stream # noqa: F401
    print("WebStreamer.bot.plugins.stream imported successfully.")

except Exception as e:
    print(f"Error during import: {e}")
    sys.exit(1)

print("Test startup passed!")
