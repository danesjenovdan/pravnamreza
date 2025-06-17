$(document).ready(function() {
  // newsletter form on landing
  $('#newsletter-btn').on('click', function (event) {
    console.log('Subscribing se začne');
    event.preventDefault();
    if ($('#newsletter-terms').is(':checked')) {
      // $('#newsletter-btn').html('Pošiljanje...');
      // reset form
      $('.newsletter-checkbox-label').css({ color: 'white' });
      $('#newsletter-success-message').css('display', 'none');
      $('#newsletter-error-message').css('display', 'none');
      // disable form while processing
      $('#newsletter-btn').prop('disabled', true);
      $('#newsletter-email').prop('disabled', true);
      $('#newsletter-terms').prop('disabled', true);
      fetch('https://podpri.lb.djnd.si/api/subscribe/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: $('#newsletter-email').val(),
          segment_id: 25,
        }),
      })
        .then((res) => {
          if (res.ok) {
            return res.text();
          }
          throw new Error('Response not ok');
        })
        .then((res) => {
          // $('#newsletter-btn').html('Prijavi se');
          $('#newsletter-email').val('');
          $('#newsletter-terms').prop('checked', false);
          $('#newsletter-btn').prop('disabled', false);
          $('#newsletter-email').prop('disabled', false);
          $('#newsletter-terms').prop('disabled', false);
          $('#newsletter-success-message').css('display', 'block');
        })
        .catch((error) => {
          // $('#newsletter-btn').html('Prijavi se');
          $('#newsletter-btn').prop('disabled', false);
          $('#newsletter-email').prop('disabled', false);
          $('#newsletter-terms').prop('disabled', false);
          $('#newsletter-error-message').css('display', 'block');
        });
    } else {
      $('.newsletter-checkbox-label').css({ color: 'red' });
    }
  });
});
