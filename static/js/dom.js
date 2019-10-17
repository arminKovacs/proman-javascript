// It uses data_handler.js to visualize elements
import {dataHandler} from "./data_handler.js";

export let dom = {
    init: function () {
        let createBoardBtn = document.getElementById('create-board');
        createBoardBtn.addEventListener('click', function () {
            dataHandler.getBoards(function (boards) {
                let newBoardTitle = 'Board ' + (boards.length + 1);
                dataHandler.createNewBoard(newBoardTitle, function (newBoardId) {
                    dataHandler.getBoard(newBoardId, function (boardToShow) {
                            console.log(boardToShow);
                        dom.showBoards(boardToShow);
                    })
                });
            });
        });
        $("#logout").on("click", function () {
            sessionStorage.clear();
        });
        $("#nav-container").on("mouseleave", function (navbar) {
            $("#nav-container").animate({opacity: 0})
        });
        $("#nav-container").on("mouseenter", function (navbar) {
            $("#nav-container").animate({opacity: 0.7})

        });
    },


    loadBoards: function () {
        // retrieves boards and makes showBoards called
        dataHandler.getBoards(function (boards) {

            dom.showBoards(boards);
            for (let board of boards) {
                let boardTitleToChange = $(`#bt-id-${board.id}`);
                dom.clickBoardTitle(boardTitleToChange, board.title, board.id);
            }
        });
    },
    showBoards: function (boards) {
        // shows boards appending them to #boards div
        // it adds necessary event listeners also
        let boardList = '';
        for (let board of boards) {
            boardList += `
               <section class="board">
                    <div class="board-header"><span class="board-title" id="bt-id-${board.id}">${board.title}</span>
                        <button class="board-add">Add Card</button>
                        <button id="board${board.id}-column-add" class="column-add">Add Column</button>
                        <button id="board${board.id}-delete" class="delete-board">Delete board</button>
                        <button id="toggle${board.id}" class="board-toggle"><i class="fas fa-chevron-down"></i></button>
                    </div>
                    <div id="board-body${board.id}">
                        <div id="board${board.id}-column" class="board-columns">
                            <div class="board-column">
                                <div class="board-column-title">New</div>
                                <div class="board-column-content" id="board-id-${board.id}-status-id-0"></div>
                            </div>
                            <div class="board-column">
                                <div class="board-column-title">In Progress</div>
                                <div class="board-column-content" id="board-id-${board.id}-status-id-1"></div>
                            </div>
                            <div class="board-column">
                                <div class="board-column-title">Testing</div>
                                <div class="board-column-content" id="board-id-${board.id}-status-id-2"></div>
                            </div>
                            <div class="board-column">
                                <div class="board-column-title">Done</div>
                                <div class="board-column-content" id="board-id-${board.id}-status-id-3"></div>
                            </div>
                        </div>
                    </div>
                </section>`;
            dom.loadCards(board.id);
        }
        const outerHtml = `
            <ul class="board-container">
                ${boardList}
            </ul>
        `;

        let boardsContainer = document.querySelector('#boards');
        boardsContainer.insertAdjacentHTML("beforeend", outerHtml);
        for (let board of boards) {
            let toggle = document.getElementById(`toggle${board.id}`);
            toggle.addEventListener("click", function () {
                $(`#board-body${board.id}`).fadeToggle();
            });

            let columnAdder = document.getElementById(`board${board.id}-column-add`);
            columnAdder.addEventListener("click", function () {
                let columnHtml = `
                        <div class="board-column">
                            <div class="board-column-title">Done</div>
                            <div class="board-column-content" id = "board-id-${board.id}-status-id-3"></div>
                        </div>`;
                let columnContainer = document.getElementById(`board${board.id}-column`);
                columnContainer.insertAdjacentHTML("beforeend", columnHtml)
            })
        }
    },
    loadCards: function (boardId) {
        // retrieves cards and makes showCards called
        dataHandler.getCardsByBoardId(boardId, function (cards) {
            dom.showCards(cards);
            for (let card of cards) {
                let cardTitleToChange = $(`#ct-id${card.id}`);
                dom.clickBoardTitle(cardTitleToChange, card.title, card.id, "cards");
            }
        });
    },
    showCards: function (cards) {
        for (let card of cards) {
            let parentBoardColumn = document.querySelector(`#board-id-${card.board_id}-status-id-${card.status_id}`);
            let cardTemplate = `
                <div id=card-id-${card.id} class="card">
                    <div id="remove-card-id${card.id}" class="card-remove"><i class="fas fa-trash-alt"></i></div>
                    <div id="ct-id${card.id}" class="card-title">${card.title}</div>
                </div>
                `;
            parentBoardColumn.insertAdjacentHTML('beforeend', cardTemplate);
            let deleteCardButton = document.getElementById(`remove-card-id${card.id}`);
            deleteCardButton.addEventListener("click", function () {
                dataHandler.deleteCard(`${card.id}`, function (response) {
                        $(`#card-id-${response}`).fadeOut().remove();
                        });
                });
            }

        // shows the cards of a board
        // it adds necessary event listeners also
    },
    clickBoardTitle : function (titleToChange, originalTitle, boardId, table="boards") {
        var chosenTitle = 'in func';
        titleToChange.bind('dblclick', function () {
            $(this).attr('contentEditable', true);
        }).blur(
            function () {
                if (confirm('Are you sure you want to change?')){
                    chosenTitle = titleToChange.html();
                    dataHandler.changeBoardTitle(chosenTitle, boardId, table)
                } else {
                    chosenTitle = originalTitle;
                    dataHandler.changeBoardTitle(chosenTitle, boardId, table)
                }
                $(this).attr('contentEditable', false);
                return chosenTitle
            });
        return chosenTitle
    }

    // here comes more features
};
