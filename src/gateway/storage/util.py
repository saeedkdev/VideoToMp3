import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except:
        return "Internal Server Error", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        # put message on the queue
        channel.basic_publish(
                exchange="",
                routing_key="video",
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    # make sure the message is persistent
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                ),
        )
    except:
        fs.delete(fid)
        return "Internal Server Error", 500
