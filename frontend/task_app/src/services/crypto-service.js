import CryptoJS from 'crypto-js';

export default {
  encrypt(data) {
    const encrypted_data = CryptoJS.AES.encrypt(data, 'TaskApp El Psy Congroo');
    return encrypted_data.toString()
  },
  decrypt(data) {
    var bytes = CryptoJS.AES.decrypt(data, 'TaskApp El Psy Congroo');
    return bytes.toString(CryptoJS.enc.Utf8);
  },
  randomString(len) {
    let text = ' ';
    let chars = '.abcdefghijklmnopqr.stuvwxyz1234567890.';

    for (let i = 0; i < len; i++) {
      text += chars.charAt(Math.floor(Math.random() * chars.length));
    }

    return text;
  }
};
