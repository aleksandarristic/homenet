var reloading;
var period = 45000;

function checkReloading() {
    if (window.location.hash=="#autoreload") {
        reloading=setTimeout("window.location.reload();", period);
        document.getElementById("reloadCB").checked=true;
    }
}

function toggleAutoRefresh(checkbox) {
    if (checkbox.checked) {
        window.location.replace("#autoreload");
        reloading=setTimeout("window.location.reload();", period);
    } else {
        window.location.replace("#");
        clearTimeout(reloading);
    }
}

window.onload=checkReloading;