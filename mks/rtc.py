import pickle
import io
import asyncio
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRelay

def obj_to_bytes(obj):
    bytes_output = io.BytesIO()
    pickle.dump(obj, bytes_output)
    return bytes_output.getvalue()

class FrameTrack(VideoStreamTrack):
    def __init__(self, frame):
        self.frame = frame
        super().__init__()

    async def recv(self):
        return self.frame

class Rtc:
    def __init__(self):
        self.connections = {}

    async def emit_frame(self, camera_label: str, dat: object):
        if camera_label in self.connections:
            connection = self.connections[camera_label]
            frame_bytes = obj_to_bytes(dat)
            connection.track = FrameTrack(frame_bytes)
        else:
            print(f"Camera '{camera_label}' not connected")

    async def listen_frame(self, camera_label):
        pc = RTCPeerConnection()
        self.connections[camera_label] = pc

        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            async def on_message(message):
                if isinstance(message, str) and message == "start":
                    await channel.send("ready")

        await pc.setLocalDescription(await pc.createOffer())
        offer = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        
        return offer

    async def connect_listener(self, camera_label, offer):
        pc = RTCPeerConnection()
        self.connections[camera_label] = pc

        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            async def on_message(message):
                if isinstance(message, str) and message == "ready":
                    frame = await self.connections[camera_label].track.recv()
                    await channel.send(frame)

        await pc.setRemoteDescription(RTCSessionDescription(sdp=offer["sdp"], type=offer["type"]))
        await pc.setLocalDescription(await pc.createAnswer())
        answer = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

        return answer

    async def disconnect(self, camera_label):
        if camera_label in self.connections:
            await self.connections[camera_label].close()
            del self.connections[camera_label]

    async def close_all_connections(self):
        for camera_label in self.connections.keys():
            await self.disconnect(camera_label)

# Usage
async def main():
    rtc = Rtc()

    camera_label = "camera_1"
    dat = b"your_binary_frame_data_here"

    offer = await rtc.listen_frame(camera_label)
    print("Offer:", offer)

    answer = await rtc.connect_listener(camera_label, offer)
    print("Answer:", answer)

    await rtc.emit_frame(camera_label, dat)
    await asyncio.sleep(5)  # Allow time for data transmission

    await rtc.disconnect(camera_label)
    await rtc.close_all_connections()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
