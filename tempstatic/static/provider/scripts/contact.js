$(function(){$("#contactForm").validate({errorElement:"label",wrapper:"div",errorPlacement:function(e,t){e.insertAfter(t.parent());e.wrap("<div class='error-msg'></div>")},rules:{name:{required:true,minlength:2},email:{required:true,email:true},message:{required:true,minlength:10}},messages:{name:{required:"Please enter your name.",minlength:jQuery.format("At least {0} characters required.")},email:{required:"Please enter your email.",email:"Please enter a valid email."},message:{required:"Please enter a message.",minlength:jQuery.format("At least {0} characters required.")}},submitHandler:function(e){$("#send").attr("value","Sending...");$(e).ajaxSubmit({success:function(t,n,r,i){$(e).slideUp("fast");$("#response").html(t).hide().slideDown("fast")}});return false}})});$(function(){$("#subscribeForm").validate({errorElement:"label",wrapper:"div",errorPlacement:function(e,t){e.insertAfter(t.parent());e.wrap("<div class='error-msg'></div>")},rules:{email:{required:true,email:true}},messages:{email:{required:"Please enter your email.",email:"Please enter a valid email."}},submitHandler:function(e){$("#subSend").text("Sending...");$(e).ajaxSubmit({success:function(t,n,r){$(e).slideUp("fast");$("#subscriptionResponse").html(t).hide().slideDown("fast")}});return false}})});$(function(){$("#downloadForm").validate({errorElement:"label",wrapper:"div",errorPlacement:function(e,t){e.insertAfter(t.parent());e.wrap("<div class='error-msg'></div>")},rules:{email:{required:true,email:true}},messages:{email:{required:"Please enter your email.",email:"Please enter a valid email."}},submitHandler:function(e){$("#dLoad").text("Processing...");$(e).ajaxSubmit({success:function(t,n,r){$(e).slideUp("fast");$("#dLoadResponse").html(t).hide().slideDown("fast")}});return false}})})