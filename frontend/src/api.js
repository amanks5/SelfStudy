import axios from "axios";

function getCookie(key) {
  var b = document.cookie.match("(^|;)\\s*" + key + "\\s*=\\s*([^;]+)");
  return b ? b.pop() : "";
}

const api = axios.create({
    headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token")
    },
    withCredentials: true
});

export default api;
