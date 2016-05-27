$(function() {

              $("#43").autocomplete({
                source: "/api/get_institutes/",
                minLength: 2,
              });
            });
$( "#16" ).wrap( "<div class='ui-widget'></div>" );

$("#heading").text('EDUCATIONAL AID COLLEGE LEVEL');
	



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
    z = z.toFixed(2);
    $("input[name=52]").val(z);
    
     
   };
 cal_exp= function()
{
    var a = document.getElementById('53').value;
    var b = document.getElementById('54').value;
    var c = document.getElementById('55').value; 
    var d = parseInt(a)+ parseInt(b)+parseInt(c);
    d = parseInt(d);
    $("input[name=56]").val(d);
     
   };

