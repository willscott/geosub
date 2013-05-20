var po = document.createElement('script');
po.type = 'text/javascript'; po.async = true;
po.src = 'https://plus.google.com/js/client:plusone.js';
var s = document.getElementsByTagName('script')[0];
s.parentNode.insertBefore(po, s);

function onSignInCallback(authResult) {
  if (authResult['access_token']) {
    //hide button
    document.getElementById('gConnect').style.display='none';
    saveSession(authResult.code)
  } else if (authResult['error']) {
    //show button
    document.getElementById('gConnect').style.display='block';
    
    console.log('There was an error: ' + authResult['error']);
  }
  console.log(authResult);
}

function saveSession(id, code) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/user/connect', true);
  xhr.onload = function() {
    console.log(this.responseText);
  }
  xhr.send('data=' + code);
}

function init() {
  var sensitivity = document.getElementById('sensitivity');
  sensitivity.addEventListener('change', function() {
    document.getElementById('sizeestimate').innerHTML = getSizeEstimate(sensitivity.value);
  });
}

function getSizeEstimate(val) {
  if (val > 50) {
    n = Math.round((1 + (val - 50)/10))
    return "Targeting ~" + n + " events per hour."
  } else if (val > 9) {
    n = Math.round((1 + (val-10)/2))
    return "Targeting ~" + n + " events per day."
  } else {
    return "Targeting ~" + val + " events per week."
  }
}

window.addEventListener('load', init);