const capitalize = (string) => {
  if (string == null || typeof string == 'undefined') return '';
  return string.charAt(0).toUpperCase() + string.slice(1);
}

const addQueryParam = (url, params) => {
  var urls = url.split('?');
  if (urls.length > 1) {
    urls[1] = `?${urls[1]}`;
  }
  for (var key in params) {
    if (urls.length > 1) {
      urls.push(`&${key}=${params[key]}`);
    } else {
      urls.push(`?${key}=${params[key]}`);
    }
  }
  return urls.join('');
}

const toggleFullScreen = () => {
  let doc = window.document;
  let docEl = doc.documentElement;

  let requestFullScreen =
    docEl.requestFullscreen ||
    docEl.mozRequestFullScreen ||
    docEl.webkitRequestFullScreen ||
    docEl.msRequestFullscreen;
  let cancelFullScreen =
    doc.exitFullscreen ||
    doc.mozCancelFullScreen ||
    doc.webkitExitFullscreen ||
    doc.msExitFullscreen;

  if (
    !doc.fullscreenElement &&
    !doc.mozFullScreenElement &&
    !doc.webkitFullscreenElement &&
    !doc.msFullscreenElement
  ) {
    requestFullScreen.call(docEl);
  } else {
    cancelFullScreen.call(doc);
    window.location.reload();
  }
};

export { capitalize, addQueryParam , toggleFullScreen};
