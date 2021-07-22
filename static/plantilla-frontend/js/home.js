function radioValue(){
    
    var radios = document.getElementsByName('option');
    var seleccion="";
    
    for (var i = 0, length = radios.length; i < length; i++) {
      if (radios[i].checked) {
        seleccion=radios[i].value
          //alert(especimen);
          break;
      }
    }
    return seleccion;
    
}




/* function busqueda(){
  var especimen = document.getElementById('especimen').value;
  var seleccion=radioValue();
  
  $.ajax({
    type: 'GET',
    url: '/especimen/busqueda/',
    data: {
      'especimen': especimen,
      'seleccion': seleccion,
    },
    success: function(data){
      alert('success');
      console.log(data);
      document.write(data.html);
      //window.location = data;
    },
    error: function(error) { 
      // if ajax fails display error alert
      console.log(error)
      alert('error');
    }
  });
} */

// autocompletado en la busqueda
$('#especimen').on('keyup', function(){
    var value = $(this).val();
    var type= radioValue();
    $.ajax({
        url: "/especimen/api/get_especimenes",
        data: {
          'search': value,
          'type': type
        },
        async: false,
        dataType: 'json',
        success: function (data) {
            // console.log(data)
            // console.log('f')
            list = data.list;
            $('#especimen').autocomplete({
              maxShowItems: 5,
              minLength: 1,
              // source: list,
              source: function(request, response) {
                var results = $.ui.autocomplete.filter(list, request.term);
                
                response(results.slice(0, 10));
            }
            });       
        }, error: function (data){
            console.log('error')
        }
        
    });  
});
    