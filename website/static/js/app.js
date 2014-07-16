// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();

$('a[data-reveal-id="modal-reveal"]').each(function(){
    console.log($(this));
    var link = $(this);
    $(this).click(function(){
        console.log($(this).attr("href"));
        var url = $(this).attr("href");
        window.history.pushState("A semcomp é foda!","Semcomp 17",url);
    });
});

// quando clicar em Voltar ele deve fechar o modal e quando fechar o modal ele deve voltar. Para resolver este conflito foi feito uma bela gambiarra a seguir
var trigger = 0; //  Serve para guardar o estado e se estiver fechando, volta no histórico mas nao tenta fechar de novo. E se estiver voltando no histórico, fecha o modal e não tenta voltar de novo.

$(document).on('close', '#modal-reveal', function () {
    if(trigger == 0){
        trigger = 1;
        history.back();
    }
    else{
        trigger = 0;
    }
});

window.onpopstate = function(event) {
    if(trigger == 1){
        trigger = 0;
    }
    else{
        trigger = 1;
        $("#modal-reveal").foundation('reveal', 'close');
    }
};