import os

# Set dummy env vars for testing before any other import happens
os.environ["API_ID"] = "12345"
os.environ["API_HASH"] = "abcdef123456"
os.environ["BOT_TOKEN"] = "123456789:abcdefghijklmnopqrstuvwxyz"
os.environ["BIN_CHANNEL"] = "-1001234567890"
os.environ["PORT"] = "8080"
os.environ["OWNER_ID"] = "12345"
os.environ["HASH_LENGTH"] = "6"
