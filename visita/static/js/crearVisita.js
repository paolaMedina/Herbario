$(document).ready(function() {

    $(function () {
        $('#datetimepicker3').datetimepicker({
            format: 'LT'
        });
    });

    $(function () {
        $('#datetimepicker4').datetimepicker({
            format: 'L'
        });
    });

    $('#smartwizard').smartWizard({
        theme: 'dots'
    });


    function isNumberKey(evt) {
        var charCode = (evt.which) ? evt.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
        return true;
    }

    $(function() {
        $('#datetimepicker3').datetimepicker({
            format: 'HH:mm'
        });
    });
    $(function() {
        var dateFormat = "DD-MM-YYYY";
        var MinDate = new Date();

        dateMin = moment(MinDate, dateFormat);

        $("#datetimepicker4").datetimepicker({
            format: dateFormat,
            minDate: dateMin
        });
    });


});