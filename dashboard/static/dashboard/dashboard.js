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

    let reloading, $reloadCB = $("#reloadCB"), $reloadCBLabel = $("label[for='reloadCB']"),
        period = $reloadCB.data('refresh') * 1000;
    let msgNotReloading = "Click to automatically reload every " + period / 1000 + " seconds.",
        msgReloading = "Page will reload in " + period / 1000 + " seconds."

    function reload(){
        console.log('Reloading the page now!');
        window.location.reload();
    }

    // check initial state on load
    if (window.location.hash=="#autoreload") {
        reloading=setTimeout(reload, period);
        $reloadCB.prop("checked", true);
    }

    // handle click event
    $reloadCB.click(function(){
        if ($(this).is(":checked")){
            window.location.replace("#autoreload");
            reloading=setTimeout(reload, period);
            console.log(msgReloading);
            $reloadCBLabel.prop('title', msgReloading);
        } else {
            window.location.replace("#");
            clearTimeout(reloading);
            console.log('No longer auto refreshing');
            $reloadCBLabel.prop('title', msgNotReloading);
        }
    });

    function updateTime() {
        $('.update-time').each(function(){
            let timestamp = $(this).data('time');
            let naturalTime = moment.unix(timestamp).fromNow();
            $(this).html(naturalTime);
        });
    }

    $(function() {
        updateTime();
        setInterval(updateTime, 1000);
    });

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });


});
