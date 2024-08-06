document.addEventListener('DOMContentLoaded', () => {
    const prelistedCards = document.getElementById('prelisted-cards');
    const column = document.querySelector('.cards');
    const submitButton = document.getElementById('submit-button');
    const fetchButton = document.getElementById('fetch-button');
    const loadingContainer = document.getElementById('loading-container');
    const loadingBar = document.getElementById('loading-bar');
    const fetchedCardsContainer = document.getElementById('fetched-cards');

    // Initialize sortable lists
    new Sortable(column, {
        group: 'shared',
        animation: 150,
        onAdd: function (evt) {
            evt.item.setAttribute('data-dragged', 'true');
            addDeleteButton(evt.item);
            console.log('Card added to column:', evt.item);
        }
    });

    new Sortable(prelistedCards, {
        group: {
            name: 'shared',
            pull: 'clone',
            put: false
        },
        animation: 150,
        onStart: function (evt) {
            evt.clone.querySelector('.delete-btn')?.remove();
        },
        onAdd: function (evt) {
            evt.item.setAttribute('data-dragged', 'true');
            console.log('Card added to prelisted cards:', evt.item);
        }
    });

    // Event listener for delete button
    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('delete-btn')) {
            event.target.parentElement.remove();
        }
    });

    // Submit button click event
    submitButton.addEventListener('click', () => {
        const cards = document.querySelectorAll('.cards .card[data-dragged="true"]');
        console.log('Dragged cards:', cards);

        const cardDetails = Array.from(cards).map(card => {
            const title = card.querySelector('h3').innerText;
            const description = card.querySelector('p').innerText;
            const audioUrl = card.querySelector('audio source').src;
            const imageUrl = card.querySelector('img').src;

            return {
                title,
                description,
                audioUrl,
                imageUrl
            };
        });

        console.log('Card details to be submitted:', cardDetails);

        fetch('http://localhost:8080/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cards: cardDetails })
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
    });

    // Fetch button click event
    fetchButton.addEventListener('click', () => {
        fetchCards();
    });

    // Function to fetch cards
    function fetchCards() {
        showLoadingBar();
    
        fetch('http://localhost:8080/cards')
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data.cards)) {
                    displayFetchedCards(data.cards); // Pass the array of cards
                } else {
                    console.error('Unexpected response format:', data);
                }
                hideLoadingBar();
            })
            .then(data => console.log('fetching data Successfully:'))
            .catch(error => {
                console.error('Error fetching cards:', error);
                hideLoadingBar();
            });
    }
    

    // Function to show loading bar
    function showLoadingBar() {
        loadingBar.style.width = '0%';
        loadingContainer.style.display = 'block';

        let width = 0;
        const interval = setInterval(() => {
            if (width >= 100) {
                clearInterval(interval);
            } else {
                width += 10;
                loadingBar.style.width = width + '%';
            }
        }, 200);
    }

    // Function to hide loading bar
    function hideLoadingBar() {
        loadingContainer.style.display = 'none';
    }

    // Function to display fetched cards
    function displayFetchedCards(cards) {
        fetchedCardsContainer.innerHTML = ''; // Clear current fetched cards

        cards.forEach(card => {
            const cardElement = document.createElement('div');
            cardElement.classList.add('card');
            cardElement.dataset.title = card.title;
            cardElement.dataset.description = card.description;
            cardElement.innerHTML = `
                <div class="card-header">
                    <h3>${card.title}</h3>
                    <img src="${card.imageUrl}" alt="${card.title} Image">
                </div>
                <p>${card.description}</p>
                <audio controls>
                    <source src="${card.audioUrl}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            `;
            fetchedCardsContainer.appendChild(cardElement);
        });
    }

    // Function to add delete button to a card
    function addDeleteButton(card) {
        let deleteBtn = card.querySelector('.delete-btn');
        if (!deleteBtn) {
            deleteBtn = document.createElement('button');
            deleteBtn.classList.add('delete-btn');
            deleteBtn.textContent = 'Delete';
            card.appendChild(deleteBtn);
        }
    }

    // Function to add a new card
    function addNewCard(status) {
        const title = prompt('Enter card title');
        const description = prompt('Enter card description');
        const audioUrl = prompt('Enter audio URL');
        const imageUrl = prompt('Enter image URL');

        if (title && description && audioUrl && imageUrl) {
            const card = document.createElement('div');
            card.classList.add('card');
            card.setAttribute('draggable', 'true');
            card.setAttribute('data-dragged', 'true'); // Ensure new cards are marked as dragged
            card.innerHTML = `
                <div class="card-header">
                    <h3>${title}</h3>
                    <img src="${imageUrl}" alt="${title} Image">
                </div>
                <p>${description}</p>
                <audio controls>
                    <source src="${audioUrl}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                <button class="delete-btn">Delete</button>
            `;
            document.getElementById(status).appendChild(card);
            addDeleteButton(card);
            addNewPrelistedCard(title, description, audioUrl, imageUrl);
        }
    }

    // Function to add a new prelisted card
    function addNewPrelistedCard(title, description, audioUrl, imageUrl) {
        if (!title) {
            title = prompt('Enter card title');
            description = prompt('Enter card description');
            audioUrl = prompt('Enter audio URL');
            imageUrl = prompt('Enter image URL');
        }

        if (title && description && audioUrl && imageUrl) {
            const card = document.createElement('div');
            card.classList.add('card');
            card.setAttribute('draggable', 'true');
            card.setAttribute('data-dragged', 'true'); // Ensure new cards are marked as dragged
            card.innerHTML = `
                <div class="card-header">
                    <h3>${title}</h3>
                    <img src="${imageUrl}" alt="${title} Image">
                </div>
                <p>${description}</p>
                <audio controls>
                    <source src="${audioUrl}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                <button class="delete-btn">Delete</button>
            `;
            prelistedCards.appendChild(card);
            addDeleteButton(card);
        }
    }
});
