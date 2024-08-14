console.log("Script.js is working")
const works = ["programmer ", "student ", "developer ", "learner ", "problem solver ", "dreamer ", "thinker"];
const element = document.getElementById("what_am_i");
let workIndex = 0;
let letterIndex = 0;
let isDeleting = false;
let typingSpeed = 450;


particlesJS.load('particles-js', 'static/json/particlesjs-config.json', function() {
    console.log('callback - particles.js config loaded');
  });

function typeEffect() {
    const currentWork = works[workIndex];
    const fullText = "I am a " + currentWork;

    if (isDeleting) {
        letterIndex--;
        typingSpeed = 50;  // Speed up for deletion
    } else {
        letterIndex++;
        typingSpeed = 50;  // Normal speed for typing
    }

    element.innerHTML = fullText.substring(0, letterIndex) + '<span class="typing"></span>';

    if (!isDeleting && letterIndex === fullText.length) {
        isDeleting = true;
        typingSpeed = 1000;  // Pause before deleting
    } else if (isDeleting && letterIndex === 7) {  // Keep "I am a " when deleting
        isDeleting = false;
        workIndex = (workIndex + 1) % works.length;  // Move to the next word
    }

    setTimeout(typeEffect, typingSpeed);
}

typeEffect();
