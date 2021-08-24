---
title: Export-YouTube-subscriptions
description: How to export YouTube channel subscriptions.
published: true
date: 2021-04-17T00:00:00.000Z
tags: 
editor: markdown
dateCreated: 2021-01-28T20:39:23.334Z
---

**Some details may differ based on your Google language settings.**

**This process won't work if you go directly to [Google Takeout](https://takeout.google.com/). You must enter the Takeout process via YouTube as described below.**

1. Make sure you are signed into YouTube with the account you want to export subscriptions from. 
2. Open https://takeout.google.com/takeout/custom/youtube?continue=https%3A%2F%2Fmyaccount.google.com%2Fyourdata%2Fyoutube%3Fhl%3Det%26authuser%3D0
6. Click `All YouTube data included`.
7. Click `Deselect all`.
8. Choose `channel-memberships`.
9. Click `OK`.
10. Click `Next step`.
11. Click `Create export`.
12. Wait for the export to complete, it should be fairly quick.
13. Download the export, it will be a .zip file. 
14. Expand the ZIP file. 
15. Go to Invidious, click on the gear in the upper-right corner.
16. Scroll down and click "Import/export data"
17. Click the "Browse" button next to "Import YouTube subscriptions"
18. Browse to the path you expanded the ZIP file to, there should be a "Takeout" folder.
19. Open "./Takeout/YouTube and YouTube Music/subscriptions/subscriptions.json".
20. Choose "Import"
