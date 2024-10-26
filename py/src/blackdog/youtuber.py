import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

def main():
    # Initialize GStreamer
    Gst.init(None)

    # Create the pipeline
    pipeline = Gst.parse_launch("v4l2src ! videoconvert ! autovideosink")

    # Start playing
    pipeline.set_state(Gst.State.PLAYING)

    # Wait until error or EOS (End of Stream)
    bus = pipeline.get_bus()
    msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

    # Free resources
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    main()