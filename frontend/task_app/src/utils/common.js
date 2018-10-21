function capitalize (string) {
  if (string == null || typeof string == "undefined") return string;
  if (string.length < 3) return string;
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function addQueryParam (url, params) {
  let urls = url.split('?')
  for (var key in params) {
    if (urls.length > 1) {
      urls.push(`&${key}=${params[key]}`);
    } else {
      urls.push(`?${key}=${params[key]}`);
    }
  }
  return urls.join('');
}

export { capitalize, addQueryParam };
