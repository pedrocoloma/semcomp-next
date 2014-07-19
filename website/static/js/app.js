// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();

$('a[data-reveal-id="modal-reveal"]').each(function(){
    var link = $(this);
    $(this).click(function(){
        //console.log(">"+$(this).attr("href"));
        var url = $(this).attr("href");
        window.history.pushState("A semcomp é foda!","Semcomp 17",url);
    });
});
setConfigCourseModal();

$(document).on('opened', '#modal-reveal', function () {
    setConfigCourseModal();
});

function setConfigCourseModal(){
    $('a[data-reveal-id="course-modal"]').each(function(){
        var link = $(this);
        $(this).click(function(){
            //console.log(">>"+$(this).attr("href"));
            var url = $(this).attr("href");
            window.history.replaceState("A semcomp é foda!","Semcomp 17",url);
        });
    });
}
window.onpopstate = function(event) {
    $("#modal-reveal").foundation('reveal', 'close');
    $("#course-modal").foundation('reveal', 'close');
};