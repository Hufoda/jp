const words = ["kanji", "crossword", "listening", "grammar", "vocabulary"];
let index = 0;

function changeWord() {
    index = (index + 1) % words.length;
    document.getElementById("changing-word").textContent = words[index];
}

setInterval(changeWord, 2000); // Change word every 2 seconds
