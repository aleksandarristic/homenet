$(function(){
    $(".menuItemBtn").click(function(){
        let msg = $(this).data('msg');
        if (confirm(msg)) {
        	let $f = $(this).parents('form:first');
        	let b = $f.attr('action');
        	$f.attr('action', b + location.hash);
        	$f.submit();
        }
    });
});
