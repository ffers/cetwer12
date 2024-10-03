function toggleField() {
    var warRadio = document.querySelector('input[value="warehouse"]');
    var postRadio = document.querySelector('input[value="poshtomat"]');
    var AdrRadio = document.querySelector('input[value="address"]');
    var hiddenFieldWar = document.getElementById("hiddenFieldWar");
    var hiddenFieldPost = document.getElementById("hiddenFieldPost");
    var hiddenFieldAdr = document.getElementById("hiddenFieldAdr");

    if (warRadio.checked) {
        hiddenFieldWar.style.display = "block";
        hiddenFieldPost.style.display = "none";
        hiddenFieldAdr.style.display = "none";
        $('#postSelect').val(null).trigger('change');
        document.getElementById("addressText").value = "";
    } else if (postRadio.checked) {
        hiddenFieldWar.style.display = "none";
        hiddenFieldPost.style.display = "block";
        hiddenFieldAdr.style.display = "none";
        $('#warhousSelect').val(null).trigger('change');
        document.getElementById("addressText").value = "";
    } else {
        hiddenFieldWar.style.display = "none";
        hiddenFieldPost.style.display = "none";
        hiddenFieldAdr.style.display = "block";
        $('#postSelect').val(null).trigger('change');
        $('#warhousSelect').val(null).trigger('change');
    }
     if (warRadio.checked) {
        localStorage.setItem('radioState', 'warehouse');
    } else if (postRadio.checked) {
        localStorage.setItem('radioState', 'poshtomat');
    } else if (AdrRadio.checked) {
        localStorage.setItem('radioState', 'address');
    }
};
window.onload = function () {
    var radioState = localStorage.getItem('radioState');
    var AddressState = localStorage.getItem('AddressState');
    var warRadio = document.querySelector('input[value="warehouse"]');
    var postRadio = document.querySelector('input[value="poshtomat"]');
    var AdrRadio = document.querySelector('input[value="address"]');
    if (radioState === 'warehouse') {
        document.querySelector('input[value="warehouse"]').checked = true;
        document.getElementById("hiddenFieldWar").style.display = "block";
        document.getElementById("hiddenFieldPost").style.display = "none";
        document.getElementById("hiddenFieldAdr").style.display = "none";
    } else if (radioState === 'poshtomat') {
        document.querySelector('input[value="poshtomat"]').checked = true;
        document.getElementById("hiddenFieldWar").style.display = "none";
        document.getElementById("hiddenFieldPost").style.display = "block";
        document.getElementById("hiddenFieldAdr").style.display =   "none";

    } else if (AddressState === 'address') {
        document.querySelector('input[value="address"]').checked = true;
        document.getElementById("hiddenFieldWar").style.display = "none";
        document.getElementById("hiddenFieldPost").style.display = "none";
        document.getElementById("hiddenFieldAdr").style.display = "block";
    }
};

var hiddenFieldPay = document.getElementById("hiddenFieldPay");


function togglePaybefore() {
    var payRadio = document.querySelector('input[id="peredpalata"]');
    var cardRadio = document.querySelector('input[id="card_pay"]');
    var nalogkaRadio = document.querySelector('input[id="nalogka"]');
    if (payRadio.checked) {
        hiddenFieldPay.style.display = "block";
    } else if (cardRadio.checked) {
        hiddenFieldPay.style.display = "none";
    } else if (nalogkaRadio.checked) {
        hiddenFieldPay.style.display = "none";
    }
}
    // $('#peredpalata100').on('change', function() {
    //     var payRadio = $(this);
    //     if (payRadio.checked) {
    //         hiddenFieldPay.style.display = "block";        
    //     } });

$(document).ready(function() {
    if ($('#peredpalata').prop('checked')) {
        togglePaybefore();
    
    };
    $('#peredpalata').on('change', function() {
        togglePaybefore();
    });
    
});