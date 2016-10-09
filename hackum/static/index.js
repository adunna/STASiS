
window.addEventListener("load", function() {

    var video = document.querySelector("#videl");
    var imgs = document.querySelector("#imgs");
    var canvas = document.createElement("canvas");
    var width, height;
    window.navigator = window.navigator || {};
    navigator.getUserMedia = (navigator.getUserMedia ||
                              navigator.webkitGetUserMedia ||
                              navigator.mozGetUserMedia ||
                              null);
    if(navigator.getUserMedia) {
        var createSrc = window.URL ? window.URL.createObjectURL : function(stream) {return stream;};
        navigator.getUserMedia({
            video: true,
            audio: true
        }, function(stream) {
            vidstream = stream;
            video.src = createSrc(vidstream);
            video.play();
        }, function(err) {
            //console.error("getUserMedia", err);
        })
    }

    var desiredWidth = 640;

    video.addEventListener('canplay', function(ev) {
        width = desiredWidth;
        height = video.videoHeight / (video.videoWidth / desiredWidth);

        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);

    });

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat/" + parseInt(+new Date()));
    chatsock.open();
    chatsock.onmessage = function(message) {
        //console.debug(message);
        var data = JSON.parse(message.data);
        //alert(data["response"]["desk"][0]);
        parseResp(data["response"]);
    }

    takePic = function() {
        if(width && height) {
            var context = canvas.getContext('2d');
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);
            var data = canvas.toDataURL('image/jpeg', 0.5);
            return data;
        }
    }

    showPic = function(data) {
        var e = document.createElement('img');
        e.src = data;
        imgs.appendChild(e);
    }

    showTxt = function(txt) {
        var p = document.createElement('p');
        p.innerHTML = txt;
        imgs.appendChild(p);
    }

    var send_format = "websocket";

    sendPic = function(classeslist) {
        st = +new Date/1000;
        var pic = takePic();
        pt = +new Date/1000;
        var fmt = pic.split("data:")[1];
        var fmt = fmt.split(";base64,");
        var b64 = fmt[1];
        fmt = fmt[0];

        chatsock.send(JSON.stringify({'b64': b64, 'classes_selection': classeslist}));

        /*if(send_format == 'postform') {
            var blob = b64toblob(b64, fmt);
            //console.debug(blob);
            var formData = new FormData();
            formData.append('file', blob);
            //console.info(formData);
            //showPic(pic);
            showTxt("pictureCap");
            filePOST(apiEndpoint, formData, function(data) {
                var jdata = JSON.parse(data);
                //console.info(jdata);
                parseResp(jdata);
            });
        } else if(send_format == 'websocket') {
            //console.info("Sending "+b64.length)

        }*/
    }

    timeDiff = function() {
        httpGET(apiEndpoint, "?time=1", function(data) {
            console.info((+new Date/1000) - parseFloat(data));
        })
    }

    parseResp = function(data) {
        // var now = +new Date/1000;
        // var tim = [pt-st, data["timing"][0]-pt, data["timing"][1]-data["timing"][0], now-data["timing"][1]];
        // showTxt("sendPic: "+tim[0]);
        // showTxt("netlag: "+tim[1]);
        // showTxt("Clarifi: "+tim[2]);
        // showTxt("parseResp: "+tim[3]);
        // showTxt("overall: "+(now-st));
        // var ares = data["results"];
        // var data = [];
        var wordList = [];
        var weightsList = [];
        for(var feature in data) {
          wordList.push(feature);
          weightsList.push(data[feature][0]);
        }
        // console.log(ares);
        // var res = ares[0];
        //     var txt = "";
        //     var tags = res["result"]["tag"];
        //     for(var j=0; j<tags["classes"].length; j++) {
        //         var p = (tags["probs"][j] - 0.5) * 2;
        //         wordList.push(tags["classes"][j]);
        //         weightsList.push(tags["probs"][j]);
        //         txt += "<span style='opacity: " + p + ";'>" + tags["classes"][j] + "</span> ";
        //         data.push([tags["classes"][j], tags["probs"][j]]);
        //     }
        //     showTxt(txt);
        // console.info(data);
        updateWordCloud(wordList, weightsList);
        updateResultsList(wordList, weightsList);
    }

});
