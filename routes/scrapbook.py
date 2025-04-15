"""
Display my hackclub scrapbook
see https://scrapbook.hackclub.com/about
"""

from flask import Blueprint, render_template
from datetime import datetime
import requests
import time
import json
import re

sp_routes = Blueprint('scrapbook', __name__, template_folder='templates')

lastScrapbookUpdate = 0
scrapbookPosts = []

try:
    channels_maps = json.load(open('channels.json', 'r', encoding="utf-8"))
except:
    print("channels.json not found")
    channels_maps = {}

@sp_routes.app_template_filter('formatDate')
def format_date(date_str):
    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return date_obj.strftime('%d/%m/%Y @ %Hh%M')

@sp_routes.app_template_filter('formatContent')
def convert_slack_references(text):
    # Convert channel references
    channel_pattern = r'<#(C[A-Z0-9]+)\|>'
    
    def channel_replacement(match):
        channel_id = match.group(1)
        channel_name = channels_maps.get(channel_id, channel_id)
        return f'<a href="https://hackclub.slack.com/archives/{channel_id}">#{channel_name}</a>'
    
    result = re.sub(channel_pattern, channel_replacement, text)
    
    return result

@sp_routes.route("/scrapbook")
def scrapbook():
    """Page linking to my scrapbook articles"""
    global lastScrapbookUpdate, scrapbookPosts
    if lastScrapbookUpdate+3600 < time.time():
        try:
            r = requests.get("https://scrapbook.hackclub.com/api/users/mathias")
            data = r.json()
            scrapbookPosts = data["posts"]
            lastScrapbookUpdate = time.time()
        except: pass

    return render_template("scrapbook.html", posts=scrapbookPosts)