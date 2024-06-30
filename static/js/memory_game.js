document.addEventListener("DOMContentLoaded", () => {
    const gameBoard = document.getElementById('gameBoard');
    const startGameButton = document.getElementById('startGame');
    const backdrop = document.getElementById('backdrop');
    const finalScoreElement = document.getElementById('finalScore');
    const finalTimeElement = document.getElementById('finalTime');
    const scoreElement = document.getElementById('score');
    const timeElement = document.getElementById('time');
    const backToAppArrow = document.getElementById('backToAppArrow');

    let cards = [];
    let flippedCards = [];
    let score = 0;
    let timeRemaining = 60;
    let timerInterval;

    const cardCount = 6; // You can change this value to increase/decrease number of cards

    startGameButton.addEventListener('click', startGame);
    backToAppArrow.addEventListener('click', () => alert('Going back to the app'));

    async function startGame() {
        backdrop.style.display = "none";
        resetGame();
        const signals = await fetchSignals();
        initializeGameBoard(signals);
        startTimer();
    }

    function resetGame() {
        cards = [];
        flippedCards = [];
        score = 0;
        timeRemaining = 60;
        scoreElement.textContent = score;
        timeElement.textContent = timeRemaining;
        finalScoreElement.style.display = 'none';
        finalTimeElement.style.display = 'none';
        gameBoard.innerHTML = ''; // Clear game board
        if (timerInterval) {
            clearInterval(timerInterval);
        }
    }

    async function fetchSignals() {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/signals/');
            const data = await response.json();
            const signals = data.signals;
            const responses = data.responses;

            return signals.map(signal => {
                const response = responses.find(r => r.id === signal.id);
                return {
                    ...signal,
                    name: response.name
                };
            }).slice(0, cardCount);
        } catch (error) {
            console.error('Error fetching signals:', error);
        }
    }

    function initializeGameBoard(signals) {
        const doubledSignals = [...signals, ...signals];
        const shuffledSignals = shuffleArray(doubledSignals);

        gameBoard.innerHTML = '';
        shuffledSignals.forEach(signal => {
            const card = createCardElement(signal);
            gameBoard.appendChild(card);
            cards.push(card);
        });
    }

    function createCardElement(signal) {
        const card = document.createElement('div');
        card.classList.add('card');
        card.dataset.name = signal.name;
        card.innerHTML = `
            <div class="card-inner">
                <div class="card-front"></div>
                <div class="card-back">
                    <img src="${signal.image}" alt="${signal.name}">
                    <p>${signal.name}</p>
                </div>
            </div>
        `;
        card.addEventListener('click', handleCardClick);
        return card;
    }

    function handleCardClick(event) {
        const card = event.currentTarget;
        if (flippedCards.length < 2 && !card.classList.contains('flipped')) {
            flipCard(card);
            flippedCards.push(card);

            if (flippedCards.length === 2) {
                setTimeout(checkForMatch, 1000);
            }
        }
    }

    function flipCard(card) {
        card.classList.add('flipped');
    }

    function unflipCards() {
        flippedCards.forEach(card => card.classList.remove('flipped'));
        flippedCards = [];
    }

    function checkForMatch() {
        const [card1, card2] = flippedCards;
        if (card1.dataset.name === card2.dataset.name) {
            score++;
            scoreElement.textContent = score;
            flippedCards = [];
            if (cards.every(card => card.classList.contains('flipped'))) {
                endGame();
            }
        } else {
            unflipCards();
        }
    }

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    function startTimer() {
        timerInterval = setInterval(() => {
            timeRemaining--;
            timeElement.textContent = timeRemaining;
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                endGame();
            }
        }, 1000);
    }

    function endGame() {
        finalScoreElement.textContent = `Your score is ${score}`;
        finalTimeElement.textContent = `Time taken: ${60 - timeRemaining} seconds`;
        finalScoreElement.style.display = 'block';
        finalTimeElement.style.display = 'block';
        backdrop.style.display = "flex"; // Show the backdrop again for restarting the game
    }
});
