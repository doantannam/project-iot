// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.11/firebase-app.js";
// import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.6.11/firebase-analytics.js";
import { getDatabase, ref, set, onValue } from "https://cdnjs.cloudflare.com/ajax/libs/firebase/9.6.11/firebase-database.min.js";
// import { getDatabase, ref, onValue } from 'https://cdnjs.cloudflare.com/ajax/libs/firebase/9.6.11/firebase-database.min.js'

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyCFnwGKU2T3P8dpTaN0KZpDotLwXDjaBxY",
    authDomain: "project-iot-64a3a.firebaseapp.com",
    databaseURL: "https://project-iot-64a3a-default-rtdb.firebaseio.com",
    projectId: "project-iot-64a3a",
    storageBucket: "project-iot-64a3a.appspot.com",
    messagingSenderId: "1044925443271",
    appId: "1:1044925443271:web:9ab084b8c433e3f4ae22e2",
    measurementId: "G-9LB8NG9Z8T"
  };
// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);

function writeUserData(rel1, rel2, rel3, rel4) {
    const db = getDatabase();
    set(ref(db, 'raspberry/module-Relay/'), {
        Relay1: rel1,
        Relay2: rel2,
        Relay3: rel3,
        Relay4: rel4,
    });
}

var rel1 = 0;
var rel2 = 0;
var rel3 = 0;
var rel4 = 0;

document.getElementById("1").onclick = function(){ valueClick1(rel1) };
document.getElementById("2").onclick = function(){ valueClick2(rel2) };
document.getElementById("3").onclick = function(){ valueClick3(rel3) };
document.getElementById("4").onclick = function(){ valueClick4(rel4) };

function valueClick1(data) {
    if (data == 0){
        rel1 = 1;
    }else{
        rel1 = 0;
    }
    writeUserData(rel1, rel2, rel3, rel4);

    console.log(rel1);
}
function valueClick2(data) {
    if (data == 0){
        rel2 = 1;
    }else{
        rel2 = 0;
    }
    writeUserData(rel1, rel2, rel3, rel4);
    console.log(rel2);
}
function valueClick3(data) {
    if (data == 0){
        rel3 = 1;
    }else{
        rel3 = 0;
    }
    writeUserData(rel1, rel2, rel3, rel4);
    console.log(rel3);
}
function valueClick4(data) {
    if (data == 0){
        rel4 = 1;
    }else{
        rel4 = 0;
    }
    writeUserData(rel1, rel2, rel3, rel4);
    console.log(rel4);
}


const db1 = getDatabase();
  const RaspberryRef = ref(db1, 'raspberry/sensor-DHT11/');
  onValue(RaspberryRef, (snapshot) => {
    const dataOne = snapshot.val();
    document.getElementById('temperature').innerText = dataOne.temperature + String(" °C");
    document.getElementById('humidity').innerText = dataOne.humidity + String(" %");
  });

  const db2 = getDatabase();
  const datetime = ref(db2, 'raspberry/datetime/');
  onValue(datetime, (snapshot) => {
    const datatime = snapshot.val();
    document.getElementById('hour').innerText = datatime.hour;
    document.getElementById('minute').innerText = datatime.minute;
  });

  
  const db4 = getDatabase();
  const dateClosedoor = ref(db4, 'raspberry/distance/Door/');
  onValue(dateClosedoor, (snapshot) => {
      const dateClosedoor = snapshot.val();
      document.getElementById('the-door').innerText = dateClosedoor.this;
    });
