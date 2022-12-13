var id = null;


createHTML();

async function createHTML(){
  var myJsonX = await getJson("../api/lap_progression.json");
  console.log(myJsonX);
  for (let key in myJsonX[0]){
      console.log(key);
      var newDiv = document.createElement("div");
      newDiv.setAttribute("id",key.replace(/\s+/g, ''));
      newDiv.style.width = "200px";
      newDiv.style.height = "20px";
      newDiv.style.position = "absolute";
      var newContent = document.createTextNode(key);
      newDiv.appendChild(newContent);
      document.getElementById("myContainer").appendChild(newDiv);
    }
  
}

const header = document.querySelector('header');

//getJson("../api/lap_progression.json","../api/ranking_data.json")

async function getJson(fileX) {
  let myObjectX = await fetch(fileX);
  var myJsonX = await myObjectX.json();
  return myJsonX;
}


/*
async function getJson(fileX, fileY) {
  let myObjectX = await fetch(fileX);
  var myJsonX = await myObjectX.json();

  let myObjectY = await fetch(fileY);
  var myJsonY = await myObjectY.json();

  for (let key in myJsonX[0]){
    console.log(key);
    var newDiv = document.createElement("div");
    newDiv.setAttribute("id",key.replace(/\s+/g, ''));
    newDiv.style.width = "200px";
    newDiv.style.height = "20px";
    newDiv.style.position = "absolute";
    var newContent = document.createTextNode(key);
    newDiv.appendChild(newContent);
    document.getElementById("myContainer").appendChild(newDiv);
  }


}*/




/*function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}


readTextFile("../api/ranking_data.json", function(text){
    var data = JSON.parse(text); //parse JSON
    
    populateHeader(data);
    console.log(data);
  kartMove(data);
});
*/

function populateHeader(obj) {
  const myH1 = document.createElement('h1');
	myH1.textContent = obj["0"]["Gary"];
  header.appendChild(myH1);
}

async function kartMove() {
  
  var objX = await getJson("../api/lap_progression.json");
  var objY = await getJson("../api/ranking_data.json");

  var elem = document.getElementById("myAnimation");

  clearInterval(id);
  id = setInterval(frame, 10);
  iter =0

  function frame() {
    console.log(iter);
    if(iter >= Object.keys(objX).length)
    {
      clearInterval(id);
    }
    else
    {
      console.log(objX[iter]);
      for (let key in objX[iter]){
        
        console.log(key.replace(/\s+/g, ''));
        elem = document.getElementById(key.replace(/\s+/g, ''));
        elem.style.top = objY[iter][key] * 20;
        elem.style.left = objX[iter][key] * 10;
      }
      iter++;
    }
  }
}


function myMove() {
  var elem = document.getElementById("Gator");
  var pos = 0;
  clearInterval(id);
  id = setInterval(frame, 10);
  function frame() {
    if (pos == 350) {
      clearInterval(id);
    } else {
      pos++;
      elem.style.top = pos + 'px';
      elem.style.left = pos + 'px';
    }
  }
}