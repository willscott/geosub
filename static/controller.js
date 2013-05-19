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