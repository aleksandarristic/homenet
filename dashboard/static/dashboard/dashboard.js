$(function(){
    $(".menuItemBtn").click(function(){
        console.log('.menuItemBtn clicked');
        let msg = $(this).data('msg');
        if (confirm(msg)) {
            console.log("sure i'm sure");
        	let $f = $(this).parents('form:first');

        	let b = $f.attr('action');
        	$f.attr('action', b + location.hash);
        	$f.submit();
        } else {
            console.log("no i'm not sure");
        }
    });
});
