tvguide.hdhomerun
=================

[XBMC-AddOn] TV Guide Add-On Extension for HD Homerun Devices

This will require you to update the TV Guide source.py script file manually for now. I'm not sure if this change will be put in or not.
After installing the add-on, edit the source.py file manually. In windows it will be in the "~\AppData\Roaming\XBMC\addons\script.tvguide" directory.

Edit the source.py script file:
	Replace line 876:
	result = Channel(id, title, logo)

With the following code:
    streamElement = elem.find("stream")
    streamUrl = None
    if streamElement is not None:
        streamUrl = streamElement.get("url")
    visible = elem.get("visible")
    if visible == "0":
        visible = False
    else:
        visible = True
    result = Channel(id, title, logo, streamUrl, visible)
