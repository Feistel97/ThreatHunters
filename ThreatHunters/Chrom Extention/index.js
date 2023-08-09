//URL접속시 동작할 페이지
//바디에 존재하는 텍스트를 가져와 URL형태 텍스트를 TextUrl의 저장
var bodyText = document.querySelector("body").innerText;
const words = bodyText.split(/[\s\n]+/);
const TextUrl = [];

for (let i = 0; i < words.length; i++) {
    //http형식을 가지는 텍스트형태의 URL을 저장
    if (words[i].startsWith("http://") || words[i].startsWith("https://")) {
      TextUrl.push(words[i]);
    }
}
console.log(TextUrl);

//하이퍼링크의 존재하는 링크를 LinkUrl에 가져와서 저장
var links = document.getElementsByTagName("a");
const LinkUrl = [];

for (let i = 0; i < links.length; i++) {
    //getAttribute를 사용하여 하이퍼링크의 URL을 가져온다
    const url = links[i].getAttribute("href");
    //가져온 링크를 push를 이용하여 저장
    LinkUrl.push(url);
}
console.log(LinkUrl);

//DB blacklisturl의 값이 존재하는 검사
var AI_Url_list = TextUrl.concat(LinkUrl);
const blackurl = [];

for (let i = 0; i < TextUrl.length; i++) {
  const url = TextUrl[i];
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost/db1/check.php', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.send('url=' + encodeURIComponent(url));
  xhr.onload = function() {
    if (xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      if (response.indexOf(url) !== -1) {
        blackurl.push(url);
      }
      if (i === TextUrl.length - 1 && blackurl.length > 0) {
        alert("현재 페이지에서 악성 URL이 확인되었습니다.\n" + blackurl);
        console.log(blackurl);
    }
  };
 }
}


const loadPyodide = () => {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js';
    script.async = true;
    script.onload = () => {
      languagePluginLoader.then(() => {
        resolve();
      });
    };
    script.onerror = () => {
      reject(new Error('Failed to load Pyodide'));
    };
    document.head.appendChild(script);
  });
};

//데이터를 한 번에 요청으로 처리하기 위해 리스트를 합쳐 전송
var AI_Black = [];

console.log(AI_Url_list);
// AI 결과값을 받기 위한 API 요청
function sendDataToAPI(data) {
  var url = 'https://192.168.15.128:5000/translate';
var data = { 'text': 'asd10621621' };
var headers = { 'Content-Type': 'application/json' };

fetch(url, {
  method: 'POST',
  headers: headers,
  body: JSON.stringify(data),
  agent: new (function () {
    this.fetch = function (input, init) {
      return fetch(input, { ...init, insecure: true });
    };
  })()
})
  .then(function (response) {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Request failed with status code: ' + response.status);
    }
  })
  .then(function (jsonResponse) {
    try {
      var result = jsonResponse.result;
      console.log(result);
    } catch (error) {
      console.error('Error decoding JSON:', error);
    }
  })
  .catch(function (error) {
    console.error('Error:', error);
  });
}

// text, link를 AI_url_API에 요청
if (AI_Url_list.length > 0) {
  sendDataToAPI({ url: AI_Url_list });
}
