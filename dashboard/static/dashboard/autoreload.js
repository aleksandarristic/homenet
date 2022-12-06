var reloading;
var period = 45000;

function checkReloading() {
    if (window.location.hash=="#autoreload") {
        reloading=setTimeout("window.location.reload();", period);
        document.getElementById("reloadCB").checked=true;
        console.log('Page reloaded automatically');
    }
}

function toggleAutoRefresh(checkbox) {
    if (checkbox.checked) {
        window.location.replace("#autoreload");
        reloading=setTimeout("window.location.reload();", period);
        console.log('Page will reload in ' + period/1000 + ' seconds');
    } else {
        window.location.replace("#");
        clearTimeout(reloading);
        console.log('Giving up on autoreload.')
    }
}

window.onload=checkReloading;