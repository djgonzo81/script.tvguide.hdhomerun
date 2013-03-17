import datetime as dt
import os
import subprocess
import time
import utils
import xbmcvfs
import xml.etree.ElementTree as ET

def GetSubscribedChannelStreams():
    channels = {}

    # Log
    utils.log("[Get Subscribed Channels] Started")

    # Get the HD Homerun UPnP address
    upnpAddress = utils.getSetting('pnp_address')
    if(utils.isNullOrEmpty(upnpAddress)):
        return channels

    # Ensure it's the cable tv folder
    if(not upnpAddress.endswith("CableTV")):
        upnpAddress += "CableTV"

    # Get the subscribed channels in the hdhomerun cable tv folder
    folders, files = xbmcvfs.listdir(upnpAddress)

    # Parse the channel folders
    if(folders is not None):
        # Log
        utils.log("[Get Subscribed Channels] # of channels found: " + str(len(folders)))

        # Parse the folders
        for folder in folders:
            channelNumber = None

            # Format of the folder is CableTV%2fv[Channel Number]
            if(folder.startswith("CableTV%2f")):
                channelNumber = folder[10:]
            elif(folder.startswith("CableTV/")):
                channelNumber = folder[8:]
            else:
                continue

            # Add the channel number to the list
            channels[channelNumber[1:]] = upnpAddress + '/' + channelNumber

    # Log
    utils.log("[Get Subscribed Channels] Completed")

    # Return the subscribed channels
    return channels

def GetTvGuideInformationFile():
    # Get the path to the mc2xml executable
    pathToExecutable = utils.getSetting('path_to_mc2xml')
    if(utils.isNullOrEmpty(pathToExecutable)):
        # Log
        utils.log("[Get Tv Guide Information File] The path to the mc2xml executable hasn't been set.")
        return None

    # Set the path of the executable and redirect to it
    path = os.path.dirname(pathToExecutable)
    os.chdir(path)

    # Get the mc2xml parameters
    mc2xmlParameters = utils.getSetting('mc2xml_parameters').strip()

    # Set the xmltv output path
    xmltvPath = os.path.join(path, "xmltv.xml")
    if(os.path.isfile(xmltvPath)):
        # Set the time difference to be 4 hours for now
        minUpdateDate = dt.datetime.now() - dt.timedelta(hours=4)

        # Get the last modify date of the output file
        lastModifiedDate = dt.datetime.fromtimestamp(os.path.getmtime(xmltvPath))

        # Ensure it hasn't been written to in the past 4 hours
        if(lastModifiedDate > minUpdateDate):
            # Log
            utils.log("[Get Tv Guide Information File] Last update was w/in 4 hours. No need to download the guide data.")
            return xmltvPath

    # Run the mc2xml command
    utils.log('[Get Tv Guide Information File] Executing the mc2xml method: ' +  pathToExecutable + ' ' + mc2xmlParameters)
    subprocess.Popen([pathToExecutable, mc2xmlParameters], stdout = subprocess.PIPE)
    utils.log('[Get Tv Guide Information File] The mc2xml execution completed.')

    # Ensure the xmltv.xml output file exists
    if(not os.path.isfile(xmltvPath)):
        # Log
        utils.log("[Get Tv Guide Information File] The xmltv.xml output file does not exist.")
        return None

    return xmltvPath

def UpdateGuideInformation():
    # Log
    utils.log("[Update Guide Information] Started")

    # Get the tv guide information file
    xmltvPath = GetTvGuideInformationFile()
    if(xmltvPath is None):
        return

    # Get the subscribed channel streams
    subscribedChannels = GetSubscribedChannelStreams()

    # Read the xmltv output file
    utils.log('[Update Guide Information] Reading the xmltv file.')
    xmlDoc = ET.parse(xmltvPath)
    utils.log('[Update Guide Information] Read completed.')

    # Get the root
    root = xmlDoc.getroot()

    # Parse the channel nodes
    channelNodes = root.findall("./channel")
    for channelNode in channelNodes:
        channelNumber = None
        
        # Find the channel number
        displayNodes = channelNode.findall("./display-name")
        if(displayNodes is None):
            utils.log("No display node exists for channel: " + channelNode.get("id"))
            continue
        for displayNode in displayNodes:
            if(displayNode.text.isdigit()):
                channelNumber = displayNode.text
                break

        # Ensure the channel number was found
        if(channelNumber is None):
            continue

        try:
            # Get the stream url for this channel
            streamUrl = subscribedChannels[channelNumber]

            # Get the stream node
            streamNode = channelNode.find('stream')

            # Ensure it exists
            if(streamNode is None):
                streamNode = ET.Element('stream')
                channelNode.append(streamNode)

            # Set the channel stream node
            streamNode.text = streamUrl
        except:
            # Set the visible tag
            channelNode.set('visible', '0')

    # Save the xml doc
    utils.log('[Update Guide Information] Writing the updated xmltv file.')
    with open(xmltvPath, 'w') as writer:
        writer.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n<!DOCTYPE tv SYSTEM "xmltv.dtd">\n\n')
        xmlDoc.write(writer)
    utils.log('[Update Guide Information] Write completed.')

    # Log
    utils.log("[Update Guide Information] Completed")
