(function() {

              $("#43").autocomplete({
                source: "/api/get_institutes/",
                minLength: 2,
              });
            });
$( "#16" ).wrap( "<div class='ui-widget'></div>" );

$("#heading").text('Mesco-Ed Aid College Level - Application Form')
	



function showfield(name){
  if(name=='OTHERS')
  	{
  		document.getElementById('div1').innerHTML='<input type="text" class="Required form-control" id= "others" onblur= "show()" placeholder= "OTHERS Specify" name="" />';
  	}
  else document.getElementById('div1').innerHTML='';
}


function show(){
		var b = 'OTHERS-' + document.getElementById('others').value;
    	$("#OTHERS").val(b);
}

 cal= function()
{
    var x = document.getElementById('51').value;
    var y = document.getElementById('48').value; 
    var z = parseInt(x)/parseInt(y);
    var a = parseInt(z);
    $("input[name=52]").val(a);
     
   };

