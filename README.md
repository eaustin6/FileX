
# TG-FileStreamBot

A high-performance Telegram File Stream Bot that allows you to stream files directly from Telegram without downloading them. It includes advanced features like traffic quotas, premium access, and a secure lock mode.

## Features

*   **Fast Streaming**: Stream files directly from Telegram with high speed.
*   **Database Integration**: Uses MongoDB for persistent user data and access management.
*   **Traffic Quota System**: Limit usage for free users, with unlimited access for the owner and premium users.
*   **Premium Mode**: Grant specific bandwidth limits to users.
*   **Lock Mode**: Restrict bot usage to authorized users via a generated passkey or master key.
*   **Web Status Page**: Check bot uptime, version, and server stats via a beautiful web interface.
*   **Multi-Client Support**: Load balance traffic across multiple Telegram accounts.
*   **Deployable Anywhere**: Ready for Heroku, Railway, Render, Koyeb, and Docker.

## Commands

*   `/start` - Check if the bot is running and register.
*   `/status` - Show your user ID, traffic usage, quota, and server stats.
*   `/login <passkey>` - Authorize yourself to use the bot (if Lock Mode is enabled).
*   `/premium` - Get information on how to upgrade to premium.
*   `/ping` - Check bot latency.

### Admin Commands (Owner Only)

*   `/broadcast` - Reply to a message to broadcast it to all users.
*   `/add_premium <user_id> <limit_bytes>` - Grant premium status and set a traffic limit (in bytes) for a user.
*   `/remove_premium <user_id>` - Remove premium status from a user.
*   `/generate_key <key> [description]` - Create a new access key for users to login.

## Deployment Guides

### Prerequisites

*   **API ID & Hash**: Get them from [my.telegram.org](https://my.telegram.org).
*   **Bot Token**: Get it from [@BotFather](https://t.me/BotFather).
*   **MongoDB URL**: Get a free database from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
*   **Bin Channel**: Create a private channel and add the bot as an admin.

### 1. Deploy on Koyeb

1.  Click the button below to deploy on Koyeb.
    [![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/YourUsername/TG-FileStreamBot&branch=main&env[API_ID]&env[API_HASH]&env[BOT_TOKEN]&env[BIN_CHANNEL]&env[DATABASE_URL]&env[OWNER_ID]&env[FQDN]&name=tg-filestreambot)
2.  Fill in the required Environment Variables:
    *   `API_ID`
    *   `API_HASH`
    *   `BOT_TOKEN`
    *   `BIN_CHANNEL`
    *   `DATABASE_URL`
    *   `OWNER_ID`
    *   `FQDN` (Your App URL, e.g., `https://your-app.koyeb.app`)
3.  Click **Deploy**.

### 2. Deploy on Heroku

1.  Fork this repository.
2.  Create a new Heroku app.
3.  Connect your GitHub repository.
4.  Go to **Settings** -> **Reveal Config Vars** and add the required variables.
5.  Deploy the branch.

### 3. Deploy on Railway

1.  Fork this repository.
2.  Login to [Railway](https://railway.app/).
3.  Create a new project -> Deploy from GitHub repo.
4.  Add variables in the **Variables** tab.

### 4. Deploy with Docker

```bash
git clone https://github.com/YourUsername/TG-FileStreamBot
cd TG-FileStreamBot
# Edit .env file with your variables
docker build -t tg-filestreambot .
docker run -d --env-file .env -p 8080:8080 tg-filestreambot
```

## Environment Variables

*   `API_ID`: Your Telegram API ID.
*   `API_HASH`: Your Telegram API Hash.
*   `BOT_TOKEN`: Your Bot Token.
*   `BIN_CHANNEL`: ID of the channel where files will be stored.
*   `DATABASE_URL`: MongoDB Connection String.
*   `OWNER_ID`: Your Telegram User ID (for admin commands and unlimited access).
*   `FQDN`: The full URL of your deployed app (e.g., `https://myapp.com`).
*   `PORT`: Port to run the server on (Default: 8080).
*   `LOCK_MODE`: Set to `True` to enable Lock Mode (Default: `False`).
*   `PASSKEY`: Master key for `/login` (Required if Lock Mode is `True`).
*   `WORKERS`: Number of workers (Default: 6).
*   `SLEEP_THRESHOLD`: FloodWait sleep threshold (Default: 60).

## Credits

Developed and maintained by the Open Source Community.
Special thanks to the user for the feature concepts and design.
