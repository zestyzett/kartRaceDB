
async function kartMove(objX, objY) {
  
  var id = null

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