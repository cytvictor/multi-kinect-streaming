import pika
import io
import pickle
from pika.channel import Channel
from typing import Mapping


MERGER_IP_ADDR = '192.168.2.200'

def obj_to_bytes(obj):
    bytes_output = io.BytesIO()
    pickle.dump(obj, bytes_output)
    return bytes_output


def bytes_to_obj(bytes_input):
    bytes_io = io.BytesIO(bytes_input)
    obj = pickle.load(bytes_io)
    return obj


class MQComm:
  def __init__(self) -> None:
    self.channels: Mapping[str, Channel] = {}
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(MERGER_IP_ADDR))
    pass

  def emit_frame(self, camera_label: str, dat: object):
    if camera_label not in self.channels.keys():
      chnl = self.connection.channel()
      chnl.queue_declare(camera_label)
      self.channels[camera_label] = chnl
    
    chnl = self.channels[camera_label]

    # encap packet
    pkt = obj_to_bytes(dat)
    chnl.basic_publish(exchange='',
      routing_key=camera_label,
      body=pkt.getvalue())
    
  def recv_frame(self, camera_label: str):
    if camera_label not in self.channels.keys():
        raise ValueError(f"Channel for camera '{camera_label}' not initialized.")

    chnl = self.channels[camera_label]

    method_frame, header_frame, body = chnl.basic_get(queue=camera_label)

    if method_frame:
        frame_data = bytes_to_obj(body)
        return frame_data
    else:
        return None
