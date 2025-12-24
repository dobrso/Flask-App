const ACTIVATION_CHANCE = 0.1;
const COOLDOWN = 1000 * 30;
const DURATION = 5000;

const JUMPSCARE_IMAGE = [
    "/static/jumpscare/image/jumpscare_image_1.png",
    "/static/jumpscare/image/jumpscare_image_2.png",
    "/static/jumpscare/image/jumpscare_image_3.png",
    "/static/jumpscare/image/jumpscare_image_4.png",
    "/static/jumpscare/image/jumpscare_image_5.png"
];

const JUMPSCARE_SOUND = [
    "/static/jumpscare/sound/jumpscare_sound_1.mp3",
    "/static/jumpscare/sound/jumpscare_sound_2.mp3",
    "/static/jumpscare/sound/jumpscare_sound_3.mp3",
    "/static/jumpscare/sound/jumpscare_sound_4.mp3",
    "/static/jumpscare/sound/jumpscare_sound_5.mp3"
];

let isUserInteracted = false;
let isJumpscareActive = false;
let lastJumpscareActivation = 0;
let jumpscareInterval = null;

document.addEventListener("DOMContentLoaded", () => {
    jumpscareInterval = setInterval(activateJumpscare, 1000);
    
    console.log("Система скримеров инициализирована");
    console.log(`Вероятность: ${(ACTIVATION_CHANCE * 100).toFixed(1)}% каждую секунду`);
    console.log(`Задержка после скримера: ${COOLDOWN/1000} секунд`);
});

document.addEventListener("click", () => {
    isUserInteracted = true;
}, { once: true });

function getRandomJumpscare() {
    const randomImageIndex = Math.floor(Math.random() * JUMPSCARE_IMAGE.length);
    const randomSoundIndex = Math.floor(Math.random() * JUMPSCARE_SOUND.length);

    return {
        image: JUMPSCARE_IMAGE[randomImageIndex],
        sound: JUMPSCARE_SOUND[randomSoundIndex]
    };
}

function checkJumpscareActivationConditions() {
    if (isJumpscareActive) {
        return false;
    }

    const time = Date.now();
    if (time - lastJumpscareActivation < COOLDOWN) {
        return false;
    }

    return Math.random() < ACTIVATION_CHANCE;
}

function activateJumpscare() {
    if (!checkJumpscareActivationConditions()) {
        return;
    }

    isJumpscareActive = true;
    lastJumpscareActivation = Date.now();

    const jumpscare = getRandomJumpscare();

    showJumpscare(jumpscare.image, jumpscare.sound);
}

function showJumpscare(imageSrc, soundSrc) {
    const overlay = document.getElementById("jumpscare-overlay");
    const image = document.createElement("img");
    const audio = new Audio(soundSrc);

    image.src = imageSrc;
    image.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.1);
        max-width: 90vw;
        max-height: 90vh;
        z-index: 10000;
        pointer-events: none;
        opacity: 0;
        transition: transform 0.2s, opacity 0.2s;
    `;

    overlay.style.cssText = `
        display: block;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.95);
        z-index: 9999;
        cursor: pointer;
        opacity: 0;
        transition: opacity 0.3s;
    `;

    overlay.innerHTML = "";
    overlay.appendChild(image);

    setTimeout(() => {
        overlay.style.opacity = "1";
        setTimeout(() => {
            image.style.opacity = "1";
            image.style.transform = "translate(-50%, -50%) scale(1)";
        }, 50);
    }, 10);

    if (isUserInteracted) {
        audio.volume = 1.0;
        audio.play().catch(e => {
            console.log("Ошибка воспроизведения звука:", e.message);
        });
    } else {
        console.log("Звук не воспроизводится - пользователь еще не взаимодействовал");
    }

    const jumpscareTimeout = setTimeout(() => {
        deactivateJumpscare(overlay, audio);
    }, DURATION);

    const closeHandler = () => {
        clearTimeout(jumpscareTimeout);
        deactivateJumpscare(overlay, audio);
        overlay.removeEventListener("click", closeHandler);
    };

    overlay.addEventListener("click", closeHandler);
}

function deactivateJumpscare(overlay, audio) {
    if (!overlay) return;

    overlay.style.opacity = "0";
    const image = overlay.querySelector("img");
    if (image) {
        image.style.opacity = "0";
        image.style.transform = "translate(-50%, -50%) scale(0.1)";
    }

    setTimeout(() => {
        overlay.style.display = "none";
        overlay.innerHTML = "";
        isJumpscareActive = false;
    }, 300);

    if (audio) {
        audio.pause();
        audio.currentTime = 0;
    }
}

setInterval(() => {
    if (isJumpscareActive) {
        const overlay = document.getElementById("jumpscare-overlay");
        if (overlay && overlay.style.display !== "none") {
            console.log("Принудительный сброс скримера");
            deactivateJumpscare(overlay, null);
        }
    }
}, COOLDOWN);

window.addEventListener("beforeunload", () => {
    if (jumpscareInterval) {
        clearInterval(jumpscareInterval);
    }
});
