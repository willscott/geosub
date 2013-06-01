// Include google auth client API.
var plusone = document.createElement('script');
plusone.type = 'text/javascript';
plusone.async = true;
plusone.src = 'https://plus.google.com/js/client:plusone.js';
var head = document.getElementsByTagName('script')[0];
head.parentNode.insertBefore(plusone, head);

// Authentication / preference state.
var state = {
  uid: null,
  prefs: {}
};

function onSignInCallback(authResult) {
  if (authResult['access_token']) {
    //hide button
    document.getElementById('overlay').style.top = '-100%';
    saveSession(authResult.access_token, authResult.code)
  } else if (authResult['error']) {
    //show button
    document.getElementById('overlay').style.top='0';
    
    console.log('There was an error: ' + authResult['error']);
  }
  console.log(authResult);
}

function saveSession(id, code) {
  state.uid = id;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/user/connect', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    state.prefs = JSON.parse(this.responseText);
    refreshPrefs();
  }
  xhr.send('data=' + code);
}

/**
 * Respond to sensitivity measurements.
 */
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

/**
 * Hook up event listeners.
 */
function init() {
  var sensitivity = document.getElementById('sensitivity');
  sensitivity.addEventListener('change', function() {
    document.getElementById('sizeestimate').innerHTML = getSizeEstimate(sensitivity.value);
  });
}

window.addEventListener('load', init);