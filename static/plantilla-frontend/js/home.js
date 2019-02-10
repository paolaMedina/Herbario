function busqueda(){
  var radios = document.getElementsByName('option');
  var especimen = document.getElementById('especimen').value;
  var seleccion="";
  
  for (var i = 0, length = radios.length; i < length; i++) {
      if (radios[i].checked) {
        seleccion=radios[i].value
          //alert(especimen);
          break;
      }
  }
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
      
      
$(function() {
  $("#especimen").autocomplete({
    source: "/especimen/api/get_places/",
    select: function (event, ui) { //item selected
      AutoCompleteSelectHandler(event, ui)
    },
    minLength: 2,
  });
});

function AutoCompleteSelectHandler(event, ui)
{
  var selectedObj = ui.item;
}
