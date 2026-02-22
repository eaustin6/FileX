# TG-FileStreamBot

A powerful Telegram Bot to stream files directly to the web with Quota Management and Premium features.

## Features

- **Direct Stream Links:** Generate direct download/stream links for Telegram files.
- **Quota Management:** Users have a specific data quota (default 2GB).
- **Premium System:** Owner can grant extra quota (Premium) to users.
- **Pass Key System:** Secure access with pass keys for claiming premium credits.
- **Owner Dashboard:** Broadcast messages, manage users, and generate keys.
- **Web Interface:** Simple status page showing system health.
- **Multi-Client Support:** Use multiple bot tokens to distribute load.

## Commands

### User Commands
- `/start` - Start the bot.
- `/status` - Check your quota usage and remaining data.
- `/premium` - Information on how to upgrade your plan.
- `/premium <key>` - Redeem a premium key.

### Owner Commands
- `/status` - View system status and total users.
- `/broadcast` - Broadcast a message to all users (Reply to a message).
- `/add_premium <user_id> <gb_amount>` - Add quota to a specific user.
- `/genkey <amount_gb>` - Generate a Premium Key for a specific amount of GB.

## Deployment

### Prerequisites
- `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
- `BOT_TOKEN` from [@BotFather](https://t.me/BotFather).
- `BIN_CHANNEL` ID (Create a private channel, add the bot as admin, and get the ID).
- `DATABASE_URL` (MongoDB Connection String).
- `OWNER_ID` (Your Telegram User ID).
- `FQDN` (Your public domain/IP, e.g., `https://myapp.koyeb.app`).

### Deploy on Koyeb

1. Create an account on [Koyeb](https://koyeb.com).
2. Create a new App.
3. Select **GitHub** as the source and choose this repository.
4. Set the **Environment Variables** listed above. **FQDN is mandatory.**
5. Click **Deploy**.

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/Owner/TG-FileStreamBot&branch=main&env[API_ID]&env[API_HASH]&env[BOT_TOKEN]&env[BIN_CHANNEL]&env[DATABASE_URL]&env[OWNER_ID]&env[FQDN])

### Deploy with Docker

```bash
# Clone the repo
git clone https://github.com/yourusername/TG-FileStreamBot
cd TG-FileStreamBot

# Build the image
docker build -t text-stream-bot .

# Run the container
docker run -d -p 8080:8080 \
  -e API_ID=12345 \
  -e API_HASH=abcdef... \
  -e BOT_TOKEN=123:ABC... \
  -e BIN_CHANNEL=-100... \
  -e DATABASE_URL=mongodb://... \
  -e OWNER_ID=12345 \
  -e FQDN=your-public-ip-or-domain \
  text-stream-bot
```

## Environment Variables

- `API_ID`: Your Telegram API ID.
- `API_HASH`: Your Telegram API Hash.
- `BOT_TOKEN`: Your Bot Token.
- `BIN_CHANNEL`: Channel ID for storing files.
- `DATABASE_URL`: MongoDB Connection URL.
- `OWNER_ID`: Your Telegram User ID.
- `FQDN`: Your server URL (e.g., `https://myapp.koyeb.app` or `http://your-ip`). Required for valid links.
- `DEFAULT_QUOTA`: Default quota in bytes (Default 2GB).
- `PORT`: Port to run the server on (Default 8080).
- `HAS_SSL`: Set to `True` if using HTTPS (Default `False` unless on cloud providers).
- `NO_PORT`: Set to `True` if you don't want the port in the URL.
- `MULTI_TOKENS`: Comma-separated list of additional bot tokens for multi-client support.
- `WORKERS`: Number of workers (Default 6).
- `SLEEP_THRESHOLD`: FloodWait sleep threshold (Default 60s).

## Credits

Maintained by **Owner** (Contact via Telegram).

---
*Based on TG-FileStreamBot.*
