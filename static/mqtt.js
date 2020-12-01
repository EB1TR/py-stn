// Create a client instance
clientID = "stn"
clientID += new Date().getUTCMilliseconds()
client = new Paho.MQTT.Client("127.0.0.1", Number(9001), clientID);

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});

// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("Connected");
  client.subscribe("pytofront");
  client.subscribe("stn1/radio1/qrg");
  client.subscribe("stn1/radio2/qrg");
  client.subscribe("stn2/radio1/qrg");
  client.subscribe("stn1/radio1/mode");
  client.subscribe("stn2/radio1/mode");
  client.subscribe("stn1/radio1/op");
  client.subscribe("stn2/radio1/op");
  client.subscribe("spots/rbn/cw");
  client.subscribe("spots/spider/spots");
  message = new Paho.MQTT.Message('0');
  message.destinationName = "update";
  client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    $("#tablestn1").addClass("blink");
    $("#tablestn2").addClass("blink");
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}


function send_command(comm, dato){
  message = new Paho.MQTT.Message(String(dato));
  message.destinationName = comm;
  client.send(message);
}


function checkBand(qrg) {
  qrg = parseFloat(qrg)
  bandcheck = 0
  if (qrg != NaN) {
    qrg = (qrg * 100)/100
    if (qrg <= 2000) bandcheck = 160
    else if (qrg <= 4000) bandcheck = 80
    else if (qrg <= 5500) bandcheck = 60
    else if (qrg <= 7300) bandcheck = 40
    else if (qrg <= 10200) bandcheck = 30
    else if (qrg <= 14350) bandcheck = 20
    else if (qrg <= 18200) bandcheck = 17
    else if (qrg <= 21450) bandcheck = 15
    else if (qrg <= 25000) bandcheck = 12
    else if (qrg <= 30000) bandcheck = 10
    else bandcheck = 6
  }
  return bandcheck
}


function isSpot(rawspot, fromrbn) {
  var jsonspot = JSON.parse(rawspot)
  var dxcall = jsonspot.dx
  if (dxcall !== "ED1B" || dxcall == "EC1A" || dxcall == "EB1TR" || dxcall == "EA1QL") {
    var spottime = jsonspot.tstamp
    var srccall = jsonspot.src
    var qrg = jsonspot.qrg
    var band = jsonspot.band
    var cmt = jsonspot.cmt
    
    var date = new Date(spottime * 1000);
    
    var hours = date.getHours();
    var minutes = "0" + date.getMinutes();
    var seconds = "0" + date.getSeconds();
    var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
    var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
    var bandstn1 = checkBand($("#stn1-r1-qrg").text())
    var bandstn2 = checkBand($("#stn2-r1-qrg").text())
    
    if (fromrbn) srccall = srccall.substr(0, (srccall.length - 3))

    if (band == bandstn1) {
      spotline = '<tr class="spotstn1"><td width="15%" align="left">' + formattedTime
       + '</td><td width="25%" align="left">' + srccall
       + '</td><td width="15%" align="left">' + qrg
       + '</td><td align="left">' + cmt + '</td></tr>'
      $("#tablestn1spot").prepend(spotline);
      while ($(".spotstn1").length > 35){
        $(".spotstn1").last().remove();
      }
    }
    if (band == bandstn2) {
      spotline = '<tr class="spotstn2"><td width="15%" align="left">' + formattedTime
       + '</td><td width="25%" align="left">' + srccall
       + '</td><td width="15%" align="left">' + qrg
       + '</td><td align="left">' + cmt + '</td></tr>'
      $("#tablestn2spot").prepend(spotline);
      while ($(".spotstn2").length > 35){
        $(".spotstn2").last().remove();
      }
    }
  }
}


// called when a message arrives
function onMessageArrived(message) {
    if (message.destinationName == "stn1/radio1/qrg") {
        $('#stn1-r1-qrg').text((message.payloadString/100).toFixed(2))
    } else if (message.destinationName == "stn2/radio1/qrg") {
        $('#stn2-r1-qrg').text((message.payloadString/100).toFixed(2))
    } else if (message.destinationName == "stn1/radio1/mode") {
        $('#stn1-r1-mode').text(message.payloadString)
    } else if (message.destinationName == "stn2/radio1/mode") {
        $('#stn2-r1-mode').text(message.payloadString)
    } else if (message.destinationName == "stn1/radio1/op") {
        $('#stn1-op').text(message.payloadString)
    } else if (message.destinationName == "stn2/radio1/op") {
        $('#stn2-op').text(message.payloadString)
    } else if (message.destinationName == "spots/rbn/cw") {
      isSpot(message.payloadString, true)
    } else if (message.destinationName == "spots/spider/spots") {
      isSpot(message.payloadString, false)
    } else {
        json = JSON.parse(message.payloadString)
        if (json.stn1 != undefined) {
            json = JSON.parse(message.payloadString)
            astn1 = "#stn1-a"+json.stn1.ant
            astn2 = "#stn2-a"+json.stn2.ant
            fstn1 = "#stn1-f"+json.stn1.fil
            fstn2 = "#stn2-f"+json.stn2.fil
            bstn1 = "#stn1-b"+json.stn1.band
            bstn2 = "#stn2-b"+json.stn2.band
            asstn1 = json.stn1.auto
            asstn2 = json.stn2.auto
            fsstn1 = json.stn1.bpf
            fsstn2 = json.stn2.bpf
            $('#stn1-an').text(json.stn1.antname)
            $('#stn2-an').text(json.stn2.antname)
            $("#stn1-a0").removeClass("spanitemselected");
            $("#stn1-a1").removeClass("spanitemselected");
            $("#stn1-a2").removeClass("spanitemselected");
            $("#stn1-a3").removeClass("spanitemselected");
            $("#stn1-a4").removeClass("spanitemselected");
            $("#stn1-a5").removeClass("spanitemselected");
            $("#stn1-a6").removeClass("spanitemselected");
            $("#stn2-a0").removeClass("spanitemselected");
            $("#stn2-a1").removeClass("spanitemselected");
            $("#stn2-a2").removeClass("spanitemselected");
            $("#stn2-a3").removeClass("spanitemselected");
            $("#stn2-a4").removeClass("spanitemselected");
            $("#stn2-a5").removeClass("spanitemselected");
            $("#stn2-a6").removeClass("spanitemselected");
            $("#stn1-b0").removeClass("spanitemselected");
            $("#stn1-b160").removeClass("spanitemselected");
            $("#stn1-b80").removeClass("spanitemselected");
            $("#stn1-b40").removeClass("spanitemselected");
            $("#stn1-b20").removeClass("spanitemselected");
            $("#stn1-b15").removeClass("spanitemselected");
            $("#stn1-b10").removeClass("spanitemselected");
            $("#stn2-b0").removeClass("spanitemselected");
            $("#stn2-b160").removeClass("spanitemselected");
            $("#stn2-b80").removeClass("spanitemselected");
            $("#stn2-b40").removeClass("spanitemselected");
            $("#stn2-b20").removeClass("spanitemselected");
            $("#stn2-b15").removeClass("spanitemselected");
            $("#stn2-b10").removeClass("spanitemselected");
            $("#stn1-f0").removeClass("spanitemselected");
            $("#stn1-f1").removeClass("spanitemselected");
            $("#stn1-f2").removeClass("spanitemselected");
            $("#stn1-f3").removeClass("spanitemselected");
            $("#stn1-f4").removeClass("spanitemselected");
            $("#stn1-f5").removeClass("spanitemselected");
            $("#stn1-f6").removeClass("spanitemselected");
            $("#stn2-f0").removeClass("spanitemselected");
            $("#stn2-f1").removeClass("spanitemselected");
            $("#stn2-f2").removeClass("spanitemselected");
            $("#stn2-f3").removeClass("spanitemselected");
            $("#stn2-f4").removeClass("spanitemselected");
            $("#stn2-f5").removeClass("spanitemselected");
            $("#stn2-f6").removeClass("spanitemselected");
            $("#stn1-as").removeClass("spanitemselected");
            $("#stn1-fs").removeClass("spanitemselected");
            $("#stn2-as").removeClass("spanitemselected");
            $("#stn2-fs").removeClass("spanitemselected");
            $(astn1).addClass("spanitemselected")
            $(astn2).addClass("spanitemselected")
            $(bstn1).addClass("spanitemselected")
            $(bstn2).addClass("spanitemselected")
            $(fstn1).addClass("spanitemselected")
            $(fstn2).addClass("spanitemselected")
            if (asstn1 == true) $("#stn1-as").addClass("spanitemselected")
            if (asstn2 == true) $("#stn2-as").addClass("spanitemselected")
            if (fsstn1 == true) $("#stn1-fs").addClass("spanitemselected")
            if (fsstn2 == true) $("#stn2-fs").addClass("spanitemselected")
        }
    }
}