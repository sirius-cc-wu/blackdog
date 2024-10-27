import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import Gst, GObject, GLib, GstVideo
import tkinter as tk
from tkinter import Frame

def main():
    # Initialize GStreamer
    Gst.init(None)

    # Create the Tkinter window
    root = tk.Tk()
    root.title("Camera Viewer")

    # Create a frame
    frame = Frame(root, width=800, height=600)
    frame.pack()

    def on_message(bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            loop.quit()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error: {err}, Debug: {debug}")
            loop.quit()

        structure = message.get_structure()
        if structure is not None:
            name = structure.get_name()
            if name == 'prepare-window-handle':
                message.src.set_window_handle(frame.winfo_id())
        
    # Create the pipeline
    pipeline = Gst.parse_launch("v4l2src ! videoconvert ! autovideosink")

    # Start playing
    pipeline.set_state(Gst.State.PLAYING)

    # Create a GLib Main Loop to handle gstreamer bus events
    loop = GLib.MainLoop()

    # Wait until error or EOS (End of Stream)
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message, loop)

    # Run the GLib main loop in a separate thread
    import threading
    threading.Thread(target=loop.run).start()

    # Run the Tkinter main loop
    root.mainloop()

    # Free resources
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    main()