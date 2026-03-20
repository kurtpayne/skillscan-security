---
name: ios-app-info-summary
description: Extracts detailed iOS app information from the iTunes API using an app URL or name.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: kowird342/ios-app-info-summary
# corpus-url: https://github.com/kowird342/ios-app-info-summary/blob/aeb7bd76fb8e70f6077dca9bfdeaf9339f53b1cb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# iOS App Info Summary Skill

This skill allows you to extract detailed information about an iOS app from the iTunes Store.

## Description
When a user asks for information about an iOS app (by providing an App Store URL or the app's name), use the provided Python scripts to fetch the details from the iTunes API.

## Usage Instructions

1. **Run the Fetch Script:**
   Depending on the user's input, execute the appropriate script located in the `scripts` directory of this skill.
   
   If the user provides a URL or App ID:
   ```bash
   python3 scripts/fetch_app_by_url.py "https://apps.apple.com/us/app/spotify-music-and-podcasts/id324684580"
   ```
   
   If the user provides an app name:
   ```bash
   python3 scripts/search_app_by_name.py "spotify"
   ```

2. **Handle Multiple Results:**
   If the user searched by name and the script returns multiple applications (up to 5), DO NOT guess. Present a concise list of the matched apps (Name, Artist, and a short identifier) to the user and ask them to clarify which exact app they meant.
   *Wait for their response before proceeding.*

3. **Process the JSON Output:**
   Once you have the JSON data for the specific target app, extract the `description` field.

4. **Generate the Description Summary & Keywords:**
   Read the raw `description` text and synthesize a structured summary containing:
   *   **Keywords**: Extract a relevant list of keywords based on the app's name and description.
   *   **Hook (Optional)**: A catchy 1-2 sentence overview of the app's main purpose. *Only extract/generate this if it is truly clear from the text, do not infer or make it up.*
   *   **Key Value**: The primary benefit or unique selling proposition of the app.
   *   **Feature List**: A concise bulleted list of the top 3-5 key features.

5. **Format the Final Final Output:**
   Present the extracted and generated information to the user in a well-formatted Markdown response. 
   **You MUST include the following fields:**
   *   **App Name & ID:** (e.g., Spotify - Music and Podcasts - ID: 324684580)
   *   **Artwork (or logo):** Display the image using the `artworkUrl100` (or the highest resolution available in the JSON). Render as an image link: `![App Icon](url)`.
   *   **Artist Name & URL:** (e.g., [Spotify Ltd.](https://apps.apple.com/...))
   *   **Primary Genre Name:** (e.g., Music)
   *   **Extracted Keywords:** (The keywords you extracted in step 4).
   *   **App Description Summary:** (The structured summary you generated in step 4, containing Hook (if clear), Key Value, and Feature List).
   *   **Average User Rating:** (e.g., 4.8 out of 5 - based on X ratings)
   *   **First Release Date:** (Format as readable date)
   *   **Last Update Date:** (Format as readable date)

## Requirements
- Python 3.x
- `requests` library (ensure it is installed or run `pip install requests` if missing).