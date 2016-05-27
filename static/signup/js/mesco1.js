$(function() {

              $("#43").autocomplete({
                source: "/api/get_institutes/",
                minLength: 2,
              });
            });
$( "#16" ).wrap( "<div class='ui-widget'></div>" );

$("#heading").text('Mesco-Ed Aid College Level - Application Form')