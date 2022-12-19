# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : handler.py              #
# ----------------------------------------------- #

import smtplib
import ssl
from email.mime.text import MIMEText

from discord_webhook import DiscordEmbed, DiscordWebhook

import config
# import logging


def send_alert(data):
    msg = data["msg"].encode("latin-1", "backslashreplace").decode("unicode_escape")
    # msg = f"{data['side']} {data['qty']} {data['symbol']} @ ${data['price']}"
    # msg = 'New Trade Executed'

    # logging.info(msg)
    desc = ""
    for key, val in data.items():
        if key == 'response':
            desc += "**Response**\n"
            for k, v in val.items():

                if k not in ('last_exec_price', 'cum_exec_qty', 'cum_exec_value', 'cum_exec_fee', 'transactTime'):
                    desc += f"      * **{k}**: `{v}`\n"
        elif key not in ('discord', 'msg', 'ticker', 'category'):
            desc += f"**{key}**: `{val}`\n"

    if config.send_discord_alerts:
        try:
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/" + data["discord"]
            )
            embed = DiscordEmbed(title=msg, description=desc, color='03b2f8')
            webhook.add_embed(embed)
            webhook.execute()
        except KeyError:
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/" + config.discord_webhook
            )
            embed = DiscordEmbed(title=msg)
            webhook.add_embed(embed)
            webhook.execute()
        except Exception as e:
            print("[X] Discord Error:\n>", e)

    if config.send_email_alerts:
        try:
            email_msg = MIMEText(
                msg.replace("*", "").replace("_", "").replace("`", "")
            )
            email_msg["Subject"] = config.email_subject
            email_msg["From"] = config.email_sender
            email_msg["To"] = config.email_sender
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                config.email_host, config.email_port, context=context
            ) as server:
                server.login(config.email_user, config.email_password)
                server.sendmail(
                    config.email_sender, config.email_receivers, email_msg.as_string()
                )
                server.quit()
        except Exception as e:
            print("[X] Email Error:\n>", e)
