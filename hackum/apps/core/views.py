from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse

import time
import tempfile
import json
import numpy as np
from threading import Thread
from binascii import a2b_base64
from clarifai.client import ClarifaiApi
from .jqueue import JQueue

from functools import reduce

# Global queue to store the images that were sent to the server.
global queue
queue = JQueue()

# Global quque to store the results returned from clarifai.
global statResult
statResult = JQueue()

# Global variable defining the number of past frames that are considered for the statiscal analysis.
global eps
eps = 2

def index_view(request):
    return render(request, "index.html", {})

def vidtest_view(request):
    return render(request, "vidtest.html", {})

# Defines the request the server can handle
def api_view(request, tags=""):
    # Return the current time
    if request.GET.get("time"):
        return HttpResponse(time.time())

    # Post an image and get clarifai tags for it.
    # If the image is a url, download it into a temp file and then return the tags from clarifai
    # For debugging.
    if request.method == "POST":
        file = None
        t0 = time.time()
        if "uri" in request.POST:
            uri_data = request.POST.get("uri")
            b64_data = uri_data.split("data:image/jpeg,base64;")
            if len(b64_data) > 1:
                b64_data = b64_data[1]
                bin_data = a2b_base64(b64_data)
                file = tempfile.TemporaryFile()
                file.write(bin_data)
        elif "file" in request.FILES:
            file = request.FILES["file"]

        if file:
            print(time.time(), "loadAPI")
            clarifai_api = ClarifaiApi()
            print(time.time(), "sendAPI")
            if(tags == ""):
                json_resp = clarifai_api.tag(file)
            else:
                json_resp = clarifai_api.tag(file, select_classes=tags)
            queue.push(json_resp)
            print(queue.size())
            print(time.time(), "doneAPI")

            t1 = time.time()

            json_resp["timing"] = [t0, t1]

            return JsonResponse(json_resp)

    return JsonResponse({"error": "InvalidRequest"})

def process_file_b64(b64, classes):
    clarifai_api = ClarifaiApi()
    data = {'encoded_data': b64}
    if(classes != ""):
        data = {'encoded_data': b64, 'select_classes': classes}
    json_resp = clarifai_api._base64_encoded_data_op(data, 'tag')
    queue.push(json_resp)
    return json_resp

# json object -> (Set[Tag], Dict[Tag, Prob])
# Returns a tuple containing the set of class names and a dictionary mapping the class name
# to the respective prob.
def getKeywords(data):
    status = data["results"][0]["status_code"]
    if (status == 'OK'):
        tags = data["results"][0]["result"]["tag"]
        return (set(tags["classes"]), dict(zip(tags["classes"], tags["probs"])))
    else:
        print("Warning: Status was not OK")
        return iter(())

# List[Json] -> Map[Key, (Mean, Std)]
def calculate(queue):
    global eps
    if(queue.size() > eps):
        mapped = list(map(getKeywords, queue.toList()))
        intersectKeys = reduce(lambda x,y: x & y, map(lambda x: x[0], mapped))
        probsDict = map(lambda k: (k,np.array([l[1][k] for l in mapped])), intersectKeys)
        queue.pop()
        return dict(map(lambda k: (k[0], (np.mean(k[1]), np.std(k[1]))), probsDict))
    else:
        return None

# Global loop for observing pushes to the queue. Whenever the the size reaches epsilon + 1,
# the calculation is started for the last epsilon queues.
def top():
    global queue
    global statResult
    while(True):
        res = calculate(queue)
        if(res != None):
            statResult.push(res)
        time.sleep(0.05)

# Start the observing thread to do the calculations.
calcThread = Thread(target=top)
calcThread.start()
