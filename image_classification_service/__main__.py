import base64
import logging
from pathlib import Path

import tensorflow
from aiohttp import web
from jsonrpcserver.aio import methods
from jsonrpcserver.exceptions import InvalidParams
import sys
sys.path.append(str(Path(__file__).absolute().parent.parent))

from image_classification_service import configuration as config
from image_classification_service.imagenet.node_lookup import NodeLookup

logger = logging.getLogger(__name__)
app = web.Application()

graph_path = Path(__file__).parent.joinpath("imagenet", "model_data", "classify_image_graph_def.pb")
with tensorflow.gfile.FastGFile(str(graph_path), "rb") as f:
    graph_def = tensorflow.GraphDef()
    graph_def.ParseFromString(f.read())
    tensorflow.import_graph_def(graph_def, name="")
node_lookup = NodeLookup()
session = tensorflow.Session()
softmax_tensor = session.graph.get_tensor_by_name("softmax:0")


@methods.add
async def classify(**kwargs):
    image = kwargs.get("image", None)
    image_type = kwargs.get("image_type", None)

    if image is None:
        raise InvalidParams("image is required")

    if image_type is None:
        raise InvalidParams("image_type is required")

    binary_image = base64.b64decode(image)
    if image_type == 'jpeg' or image_type == 'jpg':
        decoder_key = 'DecodeJpeg/contents:0'
    elif image_type == 'png':
        decoder_key = 'DecodeJpeg/contents:0'
    elif image_type == 'gif':
        raise RuntimeError("TensorflowImageNet - cannot decode gif images")
    elif image_type == 'bmp':
        raise RuntimeError("TensorflowImageNet - cannot decode bmp images")
    else:
        decoder_key = 'DecodeJpeg/contents:0'
        logger.warning("Missing image type {0}".format(image_type))

    logger.debug("classifying '{0}' image".format(image_type))

    raw_predictions = session.run(softmax_tensor, {decoder_key: binary_image})

    # Pull the predicted scorces out of the raw predictions.
    predicted_scores = raw_predictions[0]

    # Sort and strip off the top 5 predictions.
    top_predictions = predicted_scores.argsort()[-5:][::-1]
    image_predictions = []
    image_scores = []
    for predicted_node_id in top_predictions:
        # Get a text description for the top predicted node.
        description = node_lookup.id_to_string(predicted_node_id)

        # Cast to a float so JSON can serialize it. Normal Tensorflow float32 are not serializable.
        score = float(predicted_scores[predicted_node_id])

        logger.debug("        prediction = '{0}', score = {1}".format(description, score))

        # Add only those that exceed our minimum score to the predictions and scores lists.
        if score > config.MINIMUM_SCORE:
            image_predictions.append(description)
            image_scores.append(score)

    return {"predictions": image_predictions, "confidences": image_scores}


async def handle(request):
    request = await request.text()
    response = await methods.dispatch(request)
    if response.is_notification:
        return web.Response()
    else:
        return web.json_response(response, status=response.http_status)


if __name__ == '__main__':
    logging.basicConfig(level=config.LOG_LEVEL, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
    app.router.add_post('/', handle)
    web.run_app(app, host="127.0.0.1", port=config.SERVER_PORT)
