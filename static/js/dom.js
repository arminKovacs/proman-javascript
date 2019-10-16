// It uses data_handler.js to visualize elements
import {dataHandler} from "./data_handler.js";

export let dom = {
    init: function () {
        // This function should run once, when the page is loaded.
    },
    loadBoards: function () {
        // retrieves boards and makes showBoards called
        dataHandler.getBoards(function (boards) {
            dom.showBoards(boards);
        });
    },
    showBoards: function (boards) {
        // shows boards appending them to #boards div
        // it adds necessary event listeners also

        let boardList = '';
        for (let board of boards) {
            boardList += `
                <li class="board">
                    <section class="board" id="${board.board_id}">
                        <div class="board-header"><span class="board-title">${board.board_title}</span>
                            <button class="board-add">Add Card</button>
                            <button class="board-toggle"><i class="fas fa-chevron-down"></i></button>
                        </div>
                        <div class="board-columns">
                            <div class="board-column">
                                <div class="board-column-title">Status New</div>
                                    <div class="board-column-content"></div>
                            </div>
                        </div>
                    </section>
                </li>`;
            dom.loadCards(board.board_id)
            console.log(board.board_id)
        }
        const outerHtml = `
            <ul class="board-container">
                ${boardList}
            </ul>
        `;

        let boardsContainer = document.querySelector('#boards');
        boardsContainer.insertAdjacentHTML("beforeend", outerHtml);

    },
    loadCards: function (boardId) {
        // retrieves cards and makes showCards called
        dataHandler.getCardsByBoardId(boardId, function (cards) {
            console.log(cards)
                dom.showCards(cards);
            })
    },


    showCards: function (cards) {
            // shows the cards of a board
            // it adds necessary event listeners also
            let cardList = '';
            for (let card of cards) {
                console.log(card)
                cardList += `
            <div class="card">
                <div class="card-remove"><i class="fas fa-trash-alt"></i></div>
                <div class="card-title">${card.title}</div>
            </div>`;
            }

        let cardsToShow = document.querySelector('${card.board_id').querySelector('.board-column-content');
        cardsToShow.insertAdjacentHTML("beforeend", cardList);

    },
    // here comes more features
};
