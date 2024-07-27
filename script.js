document.addEventListener('DOMContentLoaded', () => {
    const prelistedCards = document.getElementById('prelisted-cards');
    const column = document.querySelector('.cards');

    new Sortable(column, {
        group: 'shared',
        animation: 150,
        onAdd: function (evt) {
            addDeleteButton(evt.item);
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
        }
    });

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('delete-btn')) {
            event.target.parentElement.remove();
        }
    });
});

function addDeleteButton(card) {
    let deleteBtn = card.querySelector('.delete-btn');
    if (!deleteBtn) {
        deleteBtn = document.createElement('button');
        deleteBtn.classList.add('delete-btn');
        deleteBtn.textContent = 'Delete';
        card.appendChild(deleteBtn);
    }
}

function addNewCard(status) {
    const title = prompt('Enter card title');
    const description = prompt('Enter card description');
    const audioUrl = prompt('Enter audio URL');
    const imageUrl = prompt('Enter image URL');

    if (title && description && audioUrl && imageUrl) {
        const card = document.createElement('div');
        card.classList.add('card');
        card.setAttribute('draggable', 'true');
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
        card.dataset.title = title;
        card.dataset.description = description;
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
        `;
        document.getElementById('prelisted-cards').appendChild(card);
    }
}
