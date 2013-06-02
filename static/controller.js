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
  session: null,
  uid: null,
  prefs: {
    feeds: {},
    places: {}
  }
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

function saveSession(at, code) {
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
      state.session = prefs.session;
      if (prefs.prefs) {
        try {
          state.prefs = JSON.parse(prefs.prefs) || state.prefs;
        } catch(e) {}
      }
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
  if (state.prefs.places == undefined) {
    state.prefs.places = {};
  }
  for (var place in state.prefs.places) {
    var el = document.getElementById('place_' + place);
    if (el) {
      el.value = state.prefs.places[place];
    }
  }
  if (state.prefs['email_id']) {
    document.getElementById('email_id').value = state.prefs['email_id'];
  } else if(!document.getElementById('email_id').value) {
    gapi.client.load('oauth2', 'v2', function() {
      var request = gapi.client.oauth2.userinfo.get();
      request.execute(function(obj) {
        document.getElementById('email_id').value = obj['email'];
        savePrefs();
      });
    });
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
    if(prefs.status == 'good') {
      state.prefs = JSON.parse(prefs.prefs) || state.prefs;
    } else {
      console.warn("error / unexpected response: " + this.responseText);
      onSignInCallback({'error': 'Not Signed In'});
    }
    refreshPrefs();
  }
  xhr.send('token=' + state.session + '&id=' + state.uid + '&data=' + JSON.stringify(state.prefs));
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

function downloadFeeds() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/data/list', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    var data = JSON.parse(this.responseText);
    for(i=0; i < data.length; i++) {
      addEventMarker(data[i][0], data[i][1], data[i][2])
    }
  }
  xhr.send();
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
        state.prefs.feeds[el.id.substr(5)] = el.checked;
        savePrefs();
      }.bind({}, inputs[i]), true);
    }
    else if (inputs[i].id.indexOf('place_') == 0) {
      inputs[i].addEventListener('change', function(el) {
        if (state.prefs.places == undefined) {
          state.prefs.places = {};
        }
        state.prefs.places[el.id.substr(6)] = el.value;
        savePrefs();
      }.bind({}, inputs[i]), true);
    }
    else if (inputs[i].id == 'email_id') {
      inputs[i].addEventListener('change', function(el) {
        state.prefs['email_id'] = el.value;
        savePrefs();
      }.bind({}, inputs[i]), true);
    }
  }

  downloadFeeds();
}

window.addEventListener('load', init);