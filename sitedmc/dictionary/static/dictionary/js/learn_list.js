document.getElementById('answer').onkeypress = function(e) {
      if (e.keyCode === 13) {
      document.getElementById('check').click();
      }
    }

let some_val = JSON.parse(document.getElementById('words').innerText);
let n = some_val.length - 1;
let current_word = some_val[n];
let cur_word_cnt = 1;
const urlParams = new URLSearchParams(window.location.search);
const qnt = urlParams.get('quantity');


document.getElementById('translation').innerText = current_word.translation;
document.getElementById('title').innerText = current_word.title;
document.getElementById('words_count').innerText = cur_word_cnt + " из " + qnt;

function check() {
  let ans = document.getElementById('answer').value
  if (ans == current_word.title) {
    document.getElementById('answer').className = 'form-control text-bg-success';
    document.getElementById('check').disabled = true;
    document.getElementById('next').disabled = false;
    current_word.level += 1;
    n -= 1;
    cur_word_cnt += 1;
    setTimeout(function() {
    document.getElementById('next').click();
    }, 2000);
    } else {
    document.getElementById('answer').className = 'form-control text-bg-danger';
  }
  if (n < 0) {
    document.getElementById('check').disabled = true;
    document.getElementById('tip').disabled = true;
    document.getElementById('next').disabled = true;
    document.getElementById('congrats').style.display = 'block';
    document.getElementById('submit').style.display = 'block';
    document.getElementById('id_only_field').value = JSON.stringify(some_val);
  } else {
    current_word = some_val[n];
  }
}

function next() {
    document.getElementById('translation').innerText = current_word.translation;
    document.getElementById('title').innerText = current_word.title;
    document.getElementById('words_count').innerText = cur_word_cnt + " из " + qnt;;
    document.getElementById('answer').value = '';
    document.getElementById('answer').className = 'form-control text-bg-dark';
    document.getElementById('check').disabled = false;
    document.getElementById('next').disabled = true;
}

function tip() {
  current_word.level = -1;
  window.alert("Правильный ответ -> " + current_word.title);
}