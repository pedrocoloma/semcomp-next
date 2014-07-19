// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();

var count_modal_opened = 0;

$('a[data-reveal-id="modal-reveal"]').each(function(){
    var link = $(this);
    $(this).click(function(){
        console.log(">"+$(this).attr("href"));
        var url = $(this).attr("href");
        window.history.pushState("A semcomp é foda!","Semcomp 17",url);
        count_modal_opened=1;
        console.log("pushState - count_modal_opened : "+count_modal_opened);
    });
});

$(document).on('opened', '#modal-reveal', function () {
    setConfigCourseModal();
});

function setConfigCourseModal(){
    $('a[data-reveal-id="course-modal"]').each(function(){
        //console.log($(this).attr("href"));
        var link = $(this);
        $(this).click(function(){
            console.log(">>"+$(this).attr("href"));
            var url = $(this).attr("href");
            window.history.pushState("A semcomp é foda!","Semcomp 17",url);
            count_modal_opened = 2;
        });
    });
    $(document).on('close', '#course-modal', function () {
        backModal(1);
    });
    $(document).on('closed', '#course-modal', function () {
        console.log("on closed modal minicurso");
        $("#modal-reveal").foundation('reveal', 'open');
    });
}


// quando clicar em Voltar ele deve fechar o modal e quando fechar o modal ele deve voltar. Para resolver este conflito foi feito uma bela gambiarra a seguir
var trigger = 0; //  Serve para guardar o estado e se estiver fechando, volta no histórico mas nao tenta fechar de novo. E se estiver voltando no histórico, fecha o modal e não tenta voltar de novo.
var trigger2 = 0;
$(document).on('close', '#modal-reveal', function () {
    backModal(0);
});

function backModal(minicurso){
    if(trigger == 0){
        console.log("close modal minicurso : "+ minicurso);
        count_modal_opened = minicurso;
        if(trigger2 == 0)
        {
            trigger = 1;
            history.back();
            console.log("history.back()");
        }else{
            trigger2 = 0;
        }
    }
    else{
        console.log("close modal - parou trigger - minicurso: "+ minicurso);
        trigger = 0;
    }
}


window.onpopstate = function(event) {
    console.log("popstate trigger: "+ trigger);
    if(trigger == 0){
        if(count_modal_opened == 1){
            trigger2 =1;
            $("#modal-reveal").foundation('reveal', 'close');
        }else if(count_modal_opened == 2){
            trigger2 =1;
            $("#course-modal").foundation('reveal', 'close');
        }
    }
    else{
        trigger = 0;
    }
};