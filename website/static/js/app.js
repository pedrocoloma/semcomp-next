// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();

(function ($, window, document) {
    var ScheduleData = {
        anchorURL: null,
        modal: null,
        baseURL: location.pathname,
        triggeredByPop: false,
    };

    function configModals() {
        $('a[data-reveal-id]')
            .off('click.semcomp')
            .on('click.semcomp', function() {
                var anchor = $(this);
                ScheduleData.anchorURL = anchor.attr('href');
                ScheduleData.modal = getOpenModal();
        });
    }

    function getOpenModal() {
        var selected = $('.reveal-modal.open[data-reveal]');
        if (selected.length == 1)
            return selected.attr('id');
        else
            return null;
    }

    configModals();

    $(document).on('opened.fndtn.reveal', '[data-reveal]', function(e) {
        configModals();

        if (ScheduleData.triggeredByPop) {
            ScheduleData.triggeredByPop = false;
        } else {
            window.history.pushState(
                {
                    modalID: $(this).attr('id'),
                }, null,
                ScheduleData.anchorURL
            );
        }
    });

    $(document).on('close.fndtn.reveal', '[data-reveal]', function(e) {
        configModals();

        if (ScheduleData.triggeredByPop) {
            ScheduleData.triggeredByPop = false;
        } else {
            window.history.pushState(
                {
                    modalID: $(this).attr('id'),
                }, null,
                ScheduleData.baseURL
            );
        }
    });

    window.onpopstate = function(e) {
        configModals();
        ScheduleData.triggeredByPop = true;

        if (e.state && e.state.modalID) {
            ScheduleData.anchorURL = location.pathname;
            $('#' + e.state.modalID).foundation('reveal', 'open', location.pathname);
        } else {
            var modal = getOpenModal();
            if (modal) {
                $('#' + modal).foundation('reveal', 'close')
            }
        }
    };
}(jQuery, window, window.document));