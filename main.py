import datetime as dt
import time
import update
import utils
import xbmc

def init():
    # Get the path to the mc2xml executable
    pathToExecutable = utils.getSetting('path_to_mc2xml')
    if(not utils.isNullOrEmpty(pathToExecutable)):
        # Set the xmltv output path
        xmltvPath = os.path.join(path, "xmltv.xml")

        # See if the file does not exist
        if(not os.path.isfile(xmltvPath)):
            # Log
            utils.log("[Init] The tv guide information hasn't been set. Clearing the last run time to ensure it runs at startup.")

            # Clear the last run time
            utils.setSetting("last_run_time", "")

def startService():
    # Log
    utils.log("Main loop execution started.")

    # Run until XBMC exits
    while(not xbmc.abortRequested):
        # Get the update interval
        updateInterval = int(utils.getSetting("update_interval"))

        # Get the current time
        now = dt.datetime.now()

        # Get the last run time
        lastRunTimeString = utils.getSetting("last_run_time")

        # Ensure a run time exists and is in the correct format
        if(utils.isNullOrEmpty(lastRunTimeString) or len(lastRunTimeString) != 14):
            # Set the last run time to now minus the update interval + 1 hour to ensure it runs now
            lastRunTimeString = utils.convertDateToString(now - dt.timedelta(hours = updateInterval + 1))

            # Update the settings
            utils.setSetting("last_run_time", lastRunTimeString)

        # Convert the string to datetime
        lastRunTime = utils.convertStringToDate(lastRunTimeString)

        # Set the next run time
        nextRunTime = lastRunTime + dt.timedelta(hours = updateInterval)

        # See if an update is required
        if(nextRunTime < now):
            # Run the update
            update.UpdateGuideInformation()

            # Update the settings
            utils.log("Updating the TV Guide Information")
            utils.setSetting("last_run_time", utils.convertDateToString(dt.datetime.now()))

        # Sleep
        time.sleep(1)

    # Log
    utils.log("Main loop execution ended.")
