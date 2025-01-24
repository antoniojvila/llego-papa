document.addEventListener("DOMContentLoaded", () => {
    const leftColumn = document.querySelector('.left-column');
    const rightColumn = document.querySelector('.right-column');
    const scoreElement = document.getElementById('score');
    const successElement = document.getElementById('success');
    const errorsElement = document.getElementById('errors');
    const timeElement = document.getElementById('time');
    const restartButton = document.getElementById('restart');
    const FirstStartButton = document.getElementById('firstStart');
    const backdrop = document.getElementById('backdrop');
    const retryStart = document.getElementById('retryStart');
    const resultBackdrop = document.getElementById('resultBackdrop');
    const finalScore = document.getElementById('finalScore');
    const backToApp = document.getElementById('backToApp');
    const backToAppArrow = document.getElementById('backToAppArrow');

    let selectedLeft = null;
    let data = {};
    let timerInterval;
    let timeRemaining = 60;
    let roundNumber = 0;

    const username = getCookie('username') || 'admin';
    const password = getCookie('password') || 'admin';

    login(username, password).then(() => {
        initializeData();
    }).catch(error => {
        console.error('Login with cookie credentials failed, trying with admin credentials:', error);
        login('admin', 'admin').then(() => {
            initializeData();
        }).catch(error => console.error('Login with admin credentials failed:', error));
    });

    async function login(username, password) {
        const response = await fetch('http://localhost:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        console.log('Login successful');
    }

    async function authenticatedFetch(url, method = 'GET', body = null) {
        let accessToken = localStorage.getItem('access_token');

        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + accessToken,
            },
            body: body ? JSON.stringify(body) : null,
        };

        let response = await fetch(url, options);

        if (response.status === 401) {
            const refreshResponse = await fetch('http://localhost:8000/api/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: localStorage.getItem('refresh_token') }),
            });

            if (!refreshResponse.ok) {
                throw new Error('Failed to refresh token');
            }

            const refreshData = await refreshResponse.json();
            localStorage.setItem('access_token', refreshData.access);
            accessToken = refreshData.access;

            options.headers['Authorization'] = 'Bearer ' + accessToken;
            response = await fetch(url, options);
        }

        return response.json();
    }

    function initializeData() {
        fetchSignals();
        fetchScore();
    }

    function fetchSignals() {
        authenticatedFetch('http://127.0.0.1:8000/api/signals/')
            .then(jsonData => {
                data = jsonData;
            })
            .catch(error => console.error('Error loading signals:', error));
    }

    async function fetchScore() {
        try {
            var scores = await authenticatedFetch('http://127.0.0.1:8000/api/scores/');
            const totalScore = scores.length > 0 ? scores[0]['score'] : 0;
            scoreElement.textContent = totalScore;
            roundNumber = scores.length;
        } catch (error) {
            console.error('Error fetching score:', error);
        }
    }

    function saveScore(success, errors) {
        roundNumber += 1;
        const totalScore = parseInt(scoreElement.textContent) + success;
        const newScore = {
            game: 1,
            hits: success,
            time: 60 - timeRemaining,
            errors: errors
        };

        authenticatedFetch('http://127.0.0.1:8000/api/round-history/', 'POST', newScore)
            .then(data => fetchScore())
            .catch(error => console.error('Error saving score:', error));
    }

    function startGame() {
        backdrop.style.display = "none";
        resultBackdrop.style.display = "none";

        resetScore();
        resetTimer();
        fillContainers();
        startTimer();
        leftColumn.addEventListener('click', handleLeftClick);
        rightColumn.addEventListener('click', handleRightClick);
    }

    function resetGame() {
        resetScore();
        resetTimer();
        fillContainers();
        leftColumn.removeEventListener('click', handleLeftClick);
        rightColumn.removeEventListener('click', handleRightClick);
    }

    function resetScore() {
        successElement.textContent = 0;
        errorsElement.textContent = 0;
    }

    function resetTimer() {
        timeRemaining = 60;
        timeElement.textContent = timeRemaining;
        if (timerInterval) {
            clearInterval(timerInterval);
        }
    }

    function startTimer() {
        timerInterval = setInterval(() => {
            timeRemaining -= 1;
            timeElement.textContent = timeRemaining;
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                endGame();
            }
        }, 1000);
    }

    function endGame() {
        const success = parseInt(successElement.textContent);
        const errors = parseInt(errorsElement.textContent);
        resultBackdrop.style.display = "block";
        finalScore.innerHTML = success;
        saveScore(success, errors);
        resetGame();
    }

    function shuffle(my_array) {
        for (let i = my_array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [my_array[i], my_array[j]] = [my_array[j], my_array[i]];
        }
        return my_array;
    }

    function fillContainers() {
        const shuffledSignals = shuffle([...data.signals]);
        const shuffledResponses = shuffle([...data.responses]);

        const signalsSubset = shuffledSignals.slice(0, 10);
        const responsesSubset = shuffledResponses.slice(0, 10);

        const commonElementIndex = Math.floor(Math.random() * signalsSubset.length);
        const commonElement = signalsSubset[commonElementIndex];

        const responseIndex = responsesSubset.findIndex(response => response.id === commonElement.id);

        if (responseIndex !== -1) {
            responsesSubset[responseIndex] = { id: commonElement.id, name: responsesSubset[responseIndex].name };
        }

        const signalElements = leftColumn.querySelectorAll('.signal');
        const responseElements = rightColumn.querySelectorAll('.response');
        for (let i = 0; i < 10; i++) {
            signalElements[i].innerHTML = `<img src="${signalsSubset[i].image}" item="${signalsSubset[i].id}" class="sign-icon"></img>`;
            responseElements[i].innerHTML = `<div class="sign-icon" item="${responsesSubset[i].id}">${responsesSubset[i].name}</div>`;
        }
    }

    function handleLeftClick(event) {
        handleClick(event, 'left');
    }

    function handleRightClick(event) {
        handleClick(event, 'right');
    }

    function handleClick(event, column) {
        if (timeRemaining <= 0) return; // Ignore clicks if time is up

        const target = event.target;

        if (column === 'left') {
            if (selectedLeft === target) {
                selectedLeft = null;
                removeHighlight();
            } else {
                selectedLeft = target;
                highlightSelected(target, column);
            }
        } else if (column === 'right' && selectedLeft) {
            if (selectedLeft === target) {
                selectedLeft = null;
                removeHighlight();
            } else {
                if (compareElements(selectedLeft, target)) {
                    updateScore('success');
                } else {
                    updateScore('errors');
                }
                fillContainers();
                selectedLeft = null;
                removeHighlight();
            }
        }
    }

    function highlightSelected(element, column) {
        removeHighlight();
        element.classList.add('selected');
    }

    function removeHighlight() {
        const selectedElements = document.querySelectorAll('.selected');
        selectedElements.forEach(el => el.classList.remove('selected'));
    }

    function compareElements(left, right) {
        return left.textContent === right.textContent;
    }

    function updateScore(type) {
        const score = parseInt(scoreElement.textContent);
        const success = parseInt(successElement.textContent);

        if (type === 'success') {
            successElement.textContent = success + 1;
            scoreElement.textContent = score + 1;
        } else if (type === 'errors') {
            errorsElement.textContent = parseInt(errorsElement.textContent) + 1;
        }
    }

    const backtoAppFunction = () => {
        alert("Aquí te lleva pa la aplicación");
    }

    restartButton.addEventListener('click', startGame);
    FirstStartButton.addEventListener('click', startGame);
    retryStart.addEventListener('click', startGame);

    backToApp.addEventListener('click', backtoAppFunction);

    backToAppArrow.addEventListener('click', backtoAppFunction);

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});
