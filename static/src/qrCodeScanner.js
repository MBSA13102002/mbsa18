
 function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(showPosition);
  } else {
    div.innerHTML = "The Browser Does not Support Geolocation";
  }
}
function showPosition(position) {
  div.innerHTML = "Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude;
}



const qrcode_ = window.qrcode;

const video = document.createElement("video");
const canvasElement = document.getElementById("qr-canvas");
const canvas = canvasElement.getContext("2d");

const qrResult = document.getElementById("qr-result");
const outputData = document.getElementById("outputData");
const btnScanQR = document.getElementById("btn-scan-qr");

let scanning = false;
var verification_key = 0
var Imp_Data = firebase.database().ref("__Generated__")
Imp_Data.on('value', (snapshot) => {
  all_values = snapshot.val()
  verification_key = Object.keys(all_values)[Object.keys(all_values).length - 1]
})

qrcode_.callback = res => {
  if (res==verification_key) {
    console.log(`res = ${res}   verification_key = ${verification_key}   hence true was followed`)
    var currentdate = new Date(); 
    var datetime = "Last Sync: " + currentdate.getDate() + "-"
                + (currentdate.getMonth()+1)  + "-" 
                + currentdate.getFullYear() + "--"  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();
    outputData.innerText = res;

    scanning = false;
    
    video.srcObject.getTracks().forEach(track => {
      track.stop();
    });

    qrResult.hidden = false;
    canvasElement.hidden = true;
    btnScanQR.hidden = false;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/verify", false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        key:res,
        date:datetime,
        


    }));
var response = xhr.responseText;
   if(response=='1'){
    firebase.database().ref("__Generated__").child(res).set({
      'verified':1
    })
     window.location.replace('/success')
   }
   else if(response=='0'){
     window.location.replace('/danger')
   }
  }
  else{
    window.location.replace('/error')
  }
};

btnScanQR.onclick = () => {
  navigator.mediaDevices
    .getUserMedia({ video: { facingMode: "environment" } })
    .then(function(stream) {
      scanning = true;
      qrResult.hidden = true;
      btnScanQR.hidden = true;
      canvasElement.hidden = false;
      video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
      video.srcObject = stream;
      video.play();
      tick();
      scan();
    });
};

function tick() {
  canvasElement.height = video.videoHeight;
  canvasElement.width = video.videoWidth;
  canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);

  scanning && requestAnimationFrame(tick);
}

function scan() {
  try {
    qrcode_.decode();
  } catch (e) {
    setTimeout(scan, 300);
  }
}
