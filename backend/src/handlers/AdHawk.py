import sys
sys.path.append('../')
import adhawkapi
import adhawkapi.frontend
from adhawkapi import Events, MarkerSequenceMode, PacketType
import time
#from src.utils.GazeBuffer import GazeBuffer
from src.classes.Event import Event
#from src.classes.Database import Database
from src.utils import utils
import numpy as np
import cv2

class GazeBuffer:
    MAX_SIZE = 87
    def __init__(self):
        self.buffer = []
    
    def append(self, array):
        if len(self.buffer) < 20:
            self.buffer.append(array)
        else:
            self.buffer.pop(0)
            self.buffer.append(array)

    def getBuffer(self):
        return self.buffer
    
    def getCoordsForTimeStamp(self, timestamp):
        timestamps = [row[0] for row in self.buffer]
        idx = min(range(len(timestamps)), key=lambda i: abs(timestamps[i]-timestamp))
        return [[self.buffer[idx][1], self.buffer[idx][2]],[self.buffer[idx-1][1], self.buffer[idx-1][2]]]


class AdHawkHandler:
    #def __init__(self, handle_gaze_in_screen, handle_event_stream):
    MARKER_DIC = cv2.aruco.DICT_4X4_50  # pylint: disable=no-member
    ARUCO_MARKER_SIZE_MM = 20
    ARUCO_MARKER_BORDER_MM = 10
    EDGE_OFFSETS_MM = np.array([[10, 10], [10, 10]])  # Marker offsets: [[left, right], [top, bottom]]
    SCREEN_WIDTH_CM = 35.93
    SCREEN_HEIGHT_CM = 20.95
    _screen_size_mm = [359.5, 209.5]

    def _calculate_marker_positions(self):
        margin_size = self.EDGE_OFFSETS_MM * 1e-3
        screen_size = self._screen_size_mm * 1e-3
        marker_size = self.ARUCO_MARKER_SIZE_MM * 1e-3

        positions = np.array([
            [margin_size[0, 0], - margin_size[1, 0] - marker_size],
            [screen_size[0] - margin_size[0, 1] - marker_size, - margin_size[1, 0] - marker_size],
            [margin_size[0, 0], - screen_size[1] + margin_size[1, 1]],
            [screen_size[0] - margin_size[0, 1] - marker_size, - screen_size[1] + margin_size[1, 1]],
        ])
        markers = []
        for marker_pos in positions:
            markers.append([*marker_pos, marker_size])
        return markers

    def __init__(self, Database):

        self.Database = Database
        self._screen_size_mm = np.array([359.5, 209.5])
        self._marker_positions = self._calculate_marker_positions()
        self.MARKER_DIC = cv2.aruco.DICT_4X4_50
        self._marker_ids = [0,1,2,3]
        self.BUFFER = GazeBuffer()
        
        # Instantiate an API object
        self._api = adhawkapi.frontend.FrontendApi()

        # Tell the api that we wish to tap into the GAZE_IN_IMAGE data stream with the given callback as the handler
        self._api.register_stream_handler(PacketType.GAZE_IN_SCREEN, self._handle_gaze_in_screen)

        # Tell the api that we wish to tap into the EVENTS stream
        # with self._handle_event_stream as the handler
        self._api.register_stream_handler(PacketType.EVENTS, self._handle_event_stream)

        # Start the api and set its connection callback to self._handle_connect. When the api detects a connection to a
        # tracker, this function will be run.
        self._api.start(connect_cb=self._handle_connect_response)

        # Flags the frontend as not connected yet
        self.connected = False

    def shutdown(self):
        ''' Shuts down the backend connection '''
        # Disables screen tracking
        self.enable_screen_tracking(False)

        # Stops api camera capture
        self._api.stop_camera_capture(lambda *_args: None)

        # Stop the log session
        self._api.stop_log_session(lambda *_args: None)

        # Shuts down the api
        self._api.shutdown()

    def quickstart(self):
        ''' Runs a Quick Start using AdHawk Backend's GUI '''

        # The tracker's camera will need to be running to detect the marker that the Quick Start procedure will display
        self._api.quick_start_gui(mode=MarkerSequenceMode.FIXED_GAZE, marker_size_mm=35,
                                  callback=(lambda *_args: None))
        self._allow_output = True

    def calibrate(self):
        ''' Runs a Calibration using AdHawk Backend's GUI '''

        # Two calibration modes are supported: FIXED_HEAD and FIXED_GAZE
        # With fixed head mode you look at calibration markers without moving your head
        # With fixed gaze mode you keep looking at a central point and move your head as instructed during calibration.
        self._api.start_calibration_gui(mode=MarkerSequenceMode.FIXED_HEAD, n_points=9, marker_size_mm=35,
                                        randomize=False, callback=(lambda *_args: None))   

    def register_screen(self, screen_width, screen_height, aruco_dic, marker_ids, markers):
        ''' Registers the screen and starts tracking on a successful discovery'''
        # screen_width = self._screen_size_mm[0]* 1e-3
        # screen_height = self._screen_size_mm[1]* 1e-3
        # marker_ids = self._marker_ids
        # markers = self.positions
        # aruco_dic = self.MARKER_DIC

        # Tells the api to search for the screen displaying ArUco (tracking) markers with the given parameters.
        # We set self._handle_screen_registered_response as the handler for the api's response to this request.
        self._api.register_screen_board(screen_width, screen_height, aruco_dic, marker_ids, markers,
                                        self._handle_screen_registered_response)

    def enable_screen_tracking(self, enable):
        ''' Utility function to enable or disable screen tracking '''

        # Note that the GAZE_IN_SCREEN data stream will only output when screen tracking is enabled
        if enable:
            print('Starting screen tracking')
            self._api.start_screen_tracking(lambda *_args: None)
        else:
            print('Stopping screen tracking')
            self._api.stop_screen_tracking(lambda *_args: None)

    def _handle_gaze_in_screen(self, _timestamp, xpos, ypos):
        self.BUFFER.append([_timestamp, xpos, ypos])
        print([_timestamp, xpos, ypos])
    
    def _handle_event_stream(self, event_type, _timestamp, *_args):
        ''' Handler for the event stream '''
        #TODO: decide how to handle this since we want events to be handled to 
        #change the DB value. easy option: no calibration so no renabling needed

        # if event_type == Events.SACCADE:
        #     print('saccade' + str(_timestamp) + str(_args[0]))
        #     print(_args)
        #     print('before' + str(self.BUFFER.getCoordsForTimeStamp(_timestamp)[1]))
        #     print('after' + str(self.BUFFER.getCoordsForTimeStamp(_timestamp)[0]))

        #     before = self.BUFFER.getCoordsForTimeStamp(_timestamp)[1]
        #     after = self.BUFFER.getCoordsForTimeStamp(_timestamp)[0]
        #     fancy_ML_regression_fitting_magic = (after[1]-before[1]) - (after[0] - before[0])
        #     print("g = " + str(fancy_ML_regression_fitting_magic))
        #     if fancy_ML_regression_fitting_magic < 0:
        #         print("TURN!!")

        if event_type == Events.TRACKLOSS_END:
            print(str(_timestamp) + str(_args))

            if _args[0] == 0:
                event = Event({"timestamp": time.time(), "command": "right"})
            else:
                event = Event({"timestamp": time.time(), "command": "left"})

            utils.log_event(self.Database, event)

        if event_type == Events.PROCEDURE_ENDED:
            # Screen tracking gets disabled when we start a marker sequence procedure, such as a Quick Start or
            # calibration, so we re-enable it upon receiving a PROCEDURE_ENDED event
            self.enable_screen_tracking(True)

    def _handle_camera_start_response(self, error):
        print('Camera started')
        # screen_width = self._screen_size_mm[0]* 1e-3
        # screen_height = self._screen_size_mm[1]* 1e-3
        # marker_ids = self._marker_ids
        # markers = self.positions
        # aruco_dic = self.MARKER_DIC
        #TODO: hardcode the screen sizing stuff!!!!
        self.register_screen(self._screen_size_mm[0] * 1e-3, self._screen_size_mm[1] * 1e-3,
                                        self.MARKER_DIC, self._marker_ids, self._marker_positions)

        # # Handles the response after starting the tracker's camera
        # if error:
        #     # End the program if there is a camera error
        #     print(f'Camera start error: {error}')
        #     self.shutdown()
        #     sys.exit()
        # else:
        #     # Otherwise, starts the video stream, streaming to the address of the video receiver
        #     self._api.start_video_stream(*self._video_receiver_address, lambda *_args: None)
         

    def _handle_connect_response(self, error):
        ''' Handler for backend connections '''

        # Starts the camera and sets the stream rate
        if not error:
            print('Connected to AdHawk Backend Service')

            # Sets the GAZE data stream rate to 125Hz
            self._api.set_stream_control(PacketType.GAZE_IN_SCREEN, 125, callback=(lambda *_args: None))

            # Tells the api which event streams we want to tap into. In this case, we wish to tap into the BLINK and
            # SACCADE data streams.
            self._api.set_event_control(adhawkapi.EventControlBit.PRODECURE_START_END, 1, callback=(lambda *args: None))
            #self._api.set_event_control(adhawkapi.EventControlBit.BLINK, 1, callback=(lambda *_args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.SACCADE, 1, callback=(lambda *_args: None))
            #self._api.set_event_control(adhawkapi.EventControlBit.SACCADE_START_END, 1, callback=(lambda *_args: None))
            self._api.set_event_control(adhawkapi.EventControlBit.TRACKLOSS_START_END, 1, callback=(lambda *_args: None))
            # Starts the MindLink's camera so that a Quick Start can be performed. Note that we use a camera index of 0
            # here, but your camera index may be different, depending on your setup. On windows, it should be 0.
            self._api.start_camera_capture(camera_index=0, resolution_index=adhawkapi.CameraResolution.MEDIUM,
                                           correct_distortion=False, callback=self._handle_camera_start_response)

            # Starts a logging session which saves eye tracking signals. This can be very useful for troubleshooting
            self._api.start_log_session(log_mode=adhawkapi.LogMode.BASIC, callback=lambda *args: None)

            # Flags the frontend as connected
            self.connected = True

    def getState(self):
        return self.connected

    def _handle_screen_registered_response(self, error):
        ''' Handler for the screen register response '''
        # If the screen was registered successfully, we enable screen tracking to start the GAZE_IN_SCREEN stream
        if not error:
            print('ArUco markers registered')
            self.enable_screen_tracking(True)



def main():
    handler = AdHawkHandler()
    try:
        print('Plug in your MindLink and ensure AdHawk Backend is running.')
        while not handler.getState:
            pass  # Waits for the frontend to be connected before proceeding


        #input('Press Enter to run a Quick Start.')

        # Runs a Quick Start at the user's command. This tunes the scan range and frequency to best suit the user's eye
        # and face shape, resulting in better tracking data. For the best quality results in your application, you
        # should also perform a calibration before using gaze data.
        #frontend.quickstart()

        while True:
            # Loops while the data streams come in
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):

        # Allows the frontend to be shut down robustly on a keyboard interrupt
        handler.shutdown()    

if __name__ == '__main__':
    main()
       

        


        
