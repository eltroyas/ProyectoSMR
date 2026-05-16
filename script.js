
// MENÚ SLIDER
$(document).ready(function() {
    // 1. Preparamos el array para el menú (si decides usarlo en el futuro)
    var menu = [];
    $('.swiper-slide').each(function(index) {
        // Usamos una alternativa por si "data-text" no existe en el HTML
        var text = $(this).find('.slide-inner').attr("data-text") || "Slide " + (index + 1);
        menu.push(text);
    });

    // 2. Configuración de efectos de transición (Parallax manual)
    var interleaveOffset = 0.5;

    var swiperOptions = {
        loop: true,
        speed: 1000,
        parallax: true,
        autoplay: {
            delay: 6500,
            disableOnInteraction: false,
        },
        watchSlidesProgress: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        on: {
            progress: function() {
                var swiper = this;
                for (var i = 0; i < swiper.slides.length; i++) {
                    var slideProgress = swiper.slides[i].progress;
                    var innerOffset = swiper.width * interleaveOffset;
                    var innerTranslate = slideProgress * innerOffset;
                    
                    // Aplicamos el movimiento al fondo para el efecto suave
                    var innerElement = swiper.slides[i].querySelector(".slide-inner");
                    if (innerElement) {
                        innerElement.style.transform = "translate3d(" + innerTranslate + "px, 0, 0)";
                    }
                }
            },
            touchStart: function() {
                var swiper = this;
                for (var i = 0; i < swiper.slides.length; i++) {
                    swiper.slides[i].style.transition = "";
                }
            },
            setTransition: function(speed) {
                var swiper = this;
                for (var i = 0; i < swiper.slides.length; i++) {
                    swiper.slides[i].style.transition = speed + "ms";
                    var innerElement = swiper.slides[i].querySelector(".slide-inner");
                    if (innerElement) {
                        innerElement.style.transition = speed + "ms";
                    }
                }
            }
        }
    };

    // 3. Inicializar Swiper
    // Nota: Asegúrate de que en tu HTML la clase sea "swiper-container"
    var swiper = new Swiper(".swiper-container", swiperOptions);

    // 4. Manejo de Imágenes de Fondo (Data Background)
    // Esto busca el atributo data-background y lo pone como fondo real
    $(".slide-bg-image").each(function() {
        var bg = $(this).attr("data-background");
        if (bg) {
            $(this).css("background-image", "url(" + bg + ")");
        }
    });

    console.log("¡Opalo E-Learning JS cargado correctamente!");
});