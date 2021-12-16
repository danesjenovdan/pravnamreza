$(document).ready(function() {
    // delete subscription
    $('.subscription').on('click', function() {
        const reqUrl = `https://podpri.djnd.si/api/segments/pravna-mreza/contact/?email=${urlParams.get('email')}&token=${urlParams.get('token')}`;
        fetch(reqUrl, {
            method: 'DELETE',
        }).then((response) => {
            return response.json();
        }).then((json) => {
            console.log(json);
        });
    });

    // submit email and subscribe
    $('#submit-managed-email').on('click', function() {
        if ($('#confirm-managed-email').is(':checked')) {
            fetch("https://podpri.djnd.si/api/subscribe/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: $('#managed-email').val(),
                    segment: 26,
                }),
            })
            .then((res) => {
                if (res.ok) {
                    return res.text();
                }
                throw new Error("Response not ok");
            })
            .then((res) => {
                alert("Na mailu te čakajo navodila za urejanje!");
            })
            .catch((error) => {
                alert('Ups, nekaj je šlo narobe. Poskusi ponovno.');
            });
        } else {
            $('.confirm-label').css({'color': 'red'});
        }
    });

    // newsletter form on landing
    $('#newsletter-btn').on('click', function(event) {
        event.preventDefault();
        $('#newsletter-btn').html('Pošiljanje...');
        $('#newsletter-btn').prop('disabled', true);
        fetch("https://podpri.djnd.si/api/subscribe/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: $('#newsletter-email').val(),
                segment: 26,
            }),
        })
        .then((res) => {
            if (res.ok) {
                return res.text();
            }
            throw new Error("Response not ok");
        })
        .then((res) => {
            $('#newsletter-btn').html('Prijavi se >>>');
            $('#newsletter-email').val('');
            $('#newsletter-terms').prop('checked', false);
            $('#newsletter-btn').prop('disabled', false);
            $('#newsletter-success-message').css('display', 'block');
        })
        .catch((error) => {
            $('#newsletter-btn').html('Prijavi se >>>');
            $('#newsletter-email').val('');
            $('#newsletter-terms').prop('checked', false);
            $('#newsletter-btn').prop('disabled', false);
            $('#newsletter-error-message').css('display', 'block');
        });
    });

    const urlParams = new URLSearchParams(document.location.search);
    if (urlParams.has('token') && urlParams.has('email')) {
        $('.manage').hide();
        const endpoint = `https://podpri.djnd.si/api/segments/my?token=${urlParams.get('token')}&email=${urlParams.get('email')}`;
        fetch(endpoint).then((response) => {
            return response.json();
        }).then((json) => {
            if (json.segments.filter((segment) => segment.id === 26).length > 0) {
                $('.subscription').text('Odjavi se od prejemanja e-novičnika');
                $('.subscription').removeAttr('disabled');
            } else {
                $('.unsubscribe').hide();
                $('.manage').show();
                $('#managed-email').focus();
            }
        });
    } else {
        $('.unsubscribe').hide();
    }
});