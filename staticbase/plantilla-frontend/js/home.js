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





function busqueda(){
  var especimen = document.getElementById('especimen').value;
  var seleccion=radioValue();
  
  $.ajax({
    type: 'GET',
    url: '/especimen/testing/',
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
}
      

// autocompletado en la busqueda
$('#especimen').on('keyup', function(){
    var value = $(this).val();
    var type= radioValue();
    $.ajax({
        url: "especimen/api/get_especimenes",
        data: {
          'search': value,
          'type': type
        },
        async: false,
        dataType: 'json',
        success: function (data) {
            console.log(data)
            list = data.list;
            $('#especimen').autocomplete({
            source: list,
            minLength: 1,
            });       
        }, error: function (data){
            console.log('error')
        }
        
    });  
});
    