var reloading;
var period = 3000;

function checkReloading() {
    if (window.location.hash=="#autoreload") {
        reloading=setTimeout("window.location.reload();", period);
        document.getElementById("reloadCB").checked=true;
        console.log('Auto-reload...');
    }
}

function toggleAutoRefresh(cb) {
    if (cb.checked) {
        window.location.replace("#autoreload");
        reloading=setTimeout("window.location.reload();", period);
    } else {
        window.location.replace("#");
        clearTimeout(reloading);
    }
}

window.onload=checkReloading;