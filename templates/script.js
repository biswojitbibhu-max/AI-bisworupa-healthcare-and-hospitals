/* =====================================================
   AI CHATBOT
===================================================== */

const messageInput = document.getElementById("message");


if (messageInput) {

    messageInput.addEventListener(
        "keypress",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                sendMessage();
            }
        }
    );
}


async function sendMessage() {

    const input =
        document.getElementById("message");

    const chatBox =
        document.getElementById("chatBox");


    if (!input || !chatBox) {
        return;
    }


    const message =
        input.value.trim();


    if (message === "") {
        return;
    }


    /* =================================================
       USER MESSAGE
    ================================================= */

    const userMessage =
        document.createElement("div");

    userMessage.className =
        "message user";

    userMessage.textContent =
        message;

    chatBox.appendChild(
        userMessage
    );


    input.value = "";


    /* =================================================
       LOADING MESSAGE
    ================================================= */

    const loading =
        document.createElement("div");

    loading.className =
        "message bot";

    loading.textContent =
        "Thinking...";

    chatBox.appendChild(
        loading
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;


    /* =================================================
       SEND MESSAGE TO FLASK
    ================================================= */

    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "Server error"
            );
        }


        const data =
            await response.json();


        loading.textContent =
            data.response ||
            "Sorry, I did not receive a response.";
    }


    catch (error) {

        console.error(
            "Chatbot error:",
            error
        );


        loading.textContent =
            "Sorry, I couldn't connect to the AI assistant.";
    }


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


/* =====================================================
   SIDE MENU
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* =================================================
           GET ELEMENTS
        ================================================= */

        const menuButton =
            document.getElementById(
                "menuButton"
            );


        const closeMenuButton =
            document.getElementById(
                "closeMenu"
            );


        const sideMenu =
            document.getElementById(
                "sideMenu"
            );


        const menuOverlay =
            document.getElementById(
                "menuOverlay"
            );


        /* =================================================
           CHECK ELEMENTS
        ================================================= */

        if (
            !menuButton ||
            !closeMenuButton ||
            !sideMenu ||
            !menuOverlay
        ) {

            console.error(
                "Side menu elements were not found."
            );

            return;
        }


        /* =================================================
           OPEN MENU
        ================================================= */

        function openMenu() {

            sideMenu.classList.add(
                "active"
            );


            menuOverlay.classList.add(
                "active"
            );


            sideMenu.setAttribute(
                "aria-hidden",
                "false"
            );


            menuButton.setAttribute(
                "aria-expanded",
                "true"
            );


            document.body.style.overflow =
                "hidden";
        }


        /* =================================================
           CLOSE MENU
        ================================================= */

        function closeMenu() {

            sideMenu.classList.remove(
                "active"
            );


            menuOverlay.classList.remove(
                "active"
            );


            sideMenu.setAttribute(
                "aria-hidden",
                "true"
            );


            menuButton.setAttribute(
                "aria-expanded",
                "false"
            );


            document.body.style.overflow =
                "";
        }


        /* =================================================
           MENU BUTTON
        ================================================= */

        menuButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();


                if (
                    sideMenu.classList.contains(
                        "active"
                    )
                ) {

                    closeMenu();

                } else {

                    openMenu();
                }
            }
        );


        /* =================================================
           CLOSE BUTTON
        ================================================= */

        closeMenuButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();

                closeMenu();
            }
        );


        /* =================================================
           DARK OVERLAY
        ================================================= */

        menuOverlay.addEventListener(
            "click",
            function () {

                closeMenu();
            }
        );


        /* =================================================
           ESC KEY
        ================================================= */

        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Escape"
                ) {

                    closeMenu();
                }
            }
        );


        /* =================================================
           SIDE MENU LINKS
        ================================================= */

        const menuLinks =
            sideMenu.querySelectorAll("a");


        menuLinks.forEach(
            function (link) {

                link.addEventListener(
                    "click",
                    function () {

                        closeMenu();
                    }
                );
            }
        );

    }
);