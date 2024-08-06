var loader = document.getElementById("preloader");
        window.addEventListener("load", function () {
            setTimeout(function () {
                loader.style.display = "none";
            }, 1000); // 9-second delay
        });
        // loader.style.display = "none";
        //   })