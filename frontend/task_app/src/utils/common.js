function capitalize (string) {
  if (string == null || typeof string == "undefined") return string;
  if (string.length < 3) return string;
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export { capitalize }
