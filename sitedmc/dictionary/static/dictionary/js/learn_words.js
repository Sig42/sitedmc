let word_title = document.getElementById('word').innerText;

document.getElementById('answer').onkeypress = function(e) {
if (e.keyCode === 13) {
    document.getElementById('check').click();
    }
}

function check() {
let ans = document.getElementById('answer').value
let word_level = parseInt(document.getElementById('id_level').value)

if (ans == word_title) {
  document.getElementById('answer').style.backgroundColor = 'rgba(204, 255, 230, 0.7)';
  document.getElementById('id_level').value = 1 + word_level;
  document.getElementById('next').disabled = false;
  setTimeout(function() {
    document.getElementById('next').click();
    }, 2000);
  document.getElementById('next').classList.add('get-green')
} else {
  document.getElementById('answer').style.backgroundColor = 'rgba(255, 179, 179, 0.7)';
}}

function tip() {
document.getElementById('id_level').value = -1;
window.alert("Правильный ответ -> " + word_title);
}
