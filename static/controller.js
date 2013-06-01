// Include google auth client API.
var plusone = document.createElement('script');
plusone.type = 'text/javascript';
plusone.async = true;
plusone.src = 'https://plus.google.com/js/client:plusone.js';
var head = document.getElementsByTagName('script')[0];
head.parentNode.insertBefore(plusone, head);

// Authentication / preference state.
var state = {
  at: null,
  uid: null,
  prefs: {
    feeds: {}
  }
};

function onSignInCallback(authResult) {
  console.log(authResult);
  if (authResult['access_token']) {
    //hide button
    document.getElementById('overlay').style.top = '-100%';
    saveSession(authResult.uid, authResult.access_token, authResult.code)
  } else if (authResult['error']) {
    //show button
    document.getElementById('overlay').style.top='0';
    
    console.log('There was an error: ' + authResult['error']);
  }
  console.log(authResult);
}

function saveSession(uid, at, code) {
  state.uid = uid;
  state.at = at;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/user/connect', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    var prefs = JSON.parse(this.responseText);
    if(prefs.status == 'new' || prefs.status == 'existing') {
      if (!state.uid && prefs.uid) {
        state.uid = prefs.uid;
      }
      state.prefs = prefs.prefs || state.prefs;
    }
    refreshPrefs();
  }
  xhr.send('data=' + code);
}

function refreshPrefs() {
  for (var feed in state.prefs.feeds) {
    var el = document.getElementById('feed_' + feed);
    if (el) {
      el.checked = state.prefs.feeds[feed];
    }
  }
}

function savePrefs() {
  if (!state.uid) {
    return onSignInCallback({'error': 'Not Signed In'});
  }
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/user/sync', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    var prefs = JSON.parse(this.responseText);
    if(prefs.status == 'new' || prefs.status == 'existing') {
      state.prefs = prefs.prefs || state.prefs;
    } else {
      console.warn("error / unexpected response: " + this.responseText);
    }
    refreshPrefs();
  }
  xhr.send('token=' + state.at + '&id=' + state.uid + '&data=' + JSON.stringify(state.prefs));
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
  var inputs = document.getElementsByTagName('input');
  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].id.indexOf('feed_') == 0) {
      inputs[i].addEventListener('change', function(el) {
        console.log(state.prefs);
        state.prefs.feeds[el.id.substr(5)] = el.checked;
        savePrefs();
      }.bind({}, inputs[i]), true);
    }
  }
}

window.addEventListener('load', init);