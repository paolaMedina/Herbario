$(document).ready(function() {

    /* initialize the external events
     -----------------------------------------------------------------*/


    // $('#external-events div.external-event').each(function() {

    //     // store data so the calendar knows to render an event upon drop
    //     $(this).data('event', {
    //         title: $.trim($(this).text()), // use the element's text as the event title
    //         stick: true // maintain when user navigates (see docs on the renderEvent method)
    //     });

    //     // make the event draggable using jQuery UI
    //     $(this).draggable({
    //         zIndex: 1111999,
    //         revert: true,      // will cause the event to go back to its
    //         revertDuration: 0  //  original position after the drag
    //     });

    // });


    /* initialize the calendar
     -----------------------------------------------------------------*/
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    // calendar=$('#calendar').fullCalendar({
    //     header: {
    //         left: 'prev,next today',
    //         center: 'title',
    //         right: 'month,agendaWeek,agendaDay'
    //     },
    //     editable: false,
    //     locale:'es',
    //     events: [
    //         {
    //             title: 'All Day Event',
    //             start: new Date(y, m, 1)
    //         },
    //         {
    //             title: 'Click for Google',
    //             start: new Date(y, m, 28),
    //             end: new Date(y, m, 29),
    //             url: 'http://google.com/'
    //         }
    //     ]
    // });


    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['bootstrap'],
        timeZone: 'UTC',
        themeSystem: 'bootstrap',
        header: {
            left: 'prev,next',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        editable: false,
        events: [{
                title: 'All Day Event',
                start: new Date(y, m, 1, 8, 00)
            },
            {
                title: 'Click for Google',
                start: new Date(y, m, d, 10, 30),
                // end: new Date(y, m, 28),
                url: 'http://google.com/'
            },
            {
                title: 'Click for Google',
                start: new Date(y, m, d, 11, 30),
                // end: new Date(y, m, 28),
            }
        ]
    });

    calendar.setOption('locale', 'es')

    calendar.render();

    $(function() {
        $('#datetimepicker3').datetimepicker({
            format: 'LT'
        });
    });

    $(function() {
        $('#datetimepicker4').datetimepicker({
            // format: 'L'
            format: 'MM/DD/YYYY',
        });
    });

    $('#smartwizard').smartWizard({
        theme: 'dots'
    });

    //  validar solo numeros en el campo de numero de registro 
    function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
        return true;
    }


});