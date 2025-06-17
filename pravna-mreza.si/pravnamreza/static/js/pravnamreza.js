$(document).ready(function() {
  // delete subscription
  // DEPRECATED: NewsletterPage and old mautic are no longer in use
//   $('.subscription').on('click', function () {
//     const reqUrl = `https://podpri.djnd.si/api/segments/pravna-mreza/contact/?email=${urlParams.get(
//       'email'
//     )}&token=${urlParams.get('token')}`;
//     fetch(reqUrl, {
//       method: 'DELETE',
//     })
//       .then((response) => {
//         return response.json();
//       })
//       .then((json) => {
//         $('.unsubscribe').hide();
//         $('.manage').show();
//       });
//   });

  // submit email and subscribe
  // DEPRECATED: NewsletterPage and old mautic are no longer in use
  // $('#submit-managed-email').on('click', function() {
  //     if ($('#newsletter-terms').is(':checked')) {
  //         // reset form
  //         $('.newsletter-checkbox-label').css({'color': '#212529'});
  //         $('#newsletter-success-message').css('display', 'none');
  //         $('#newsletter-error-message').css('display', 'none');
  //         // disable form while processing
  //         $('#submit-managed-email').prop('disabled', true);
  //         $('#managed-email').prop('disabled', true);
  //         $('#newsletter-terms').prop('disabled', true);
  //         // -----
  //         fetch("https://podpri.djnd.si/api/subscribe/", {
  //             method: "POST",
  //             headers: {
  //                 "Content-Type": "application/json",
  //             },
  //             body: JSON.stringify({
  //                 email: $('#managed-email').val(),
  //                 segment: 26,
  //             }),
  //         })
  //         .then((res) => {
  //             if (res.ok) {
  //                 return res.text();
  //             }
  //             throw new Error("Response not ok");
  //         })
  //         .then((res) => {
  //             $('#managed-email').val('');
  //             $('#newsletter-terms').prop('checked', false);
  //             $('#submit-managed-email').prop('disabled', false);
  //             $('#managed-email').prop('disabled', false);
  //             $('#newsletter-terms').prop('disabled', false);
  //             $('#newsletter-success-message').css('display', 'block');
  //         })
  //         .catch((error) => {
  //             $('#submit-managed-email').prop('disabled', false);
  //             $('#managed-email').prop('disabled', false);
  //             $('#newsletter-terms').prop('disabled', false);
  //             $('#newsletter-error-message').css('display', 'block');
  //         });
  //     } else {
  //         $('.newsletter-checkbox-label').css({'color': 'red'});
  //     }
  // });

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

//   DEPRECATED: NewsletterPage and old mautic are no longer in use
//   const urlParams = new URLSearchParams(document.location.search);
//   if (urlParams.has('token') && urlParams.has('email')) {
//     $('.manage').hide();
//     const endpoint = `https://podpri.djnd.si/api/segments/my?token=${urlParams.get(
//       'token'
//     )}&email=${urlParams.get('email')}`;
//     fetch(endpoint)
//       .then((response) => {
//         return response.json();
//       })
//       .then((json) => {
//         if (json.segments.filter((segment) => segment.id === 26).length > 0) {
//           $('.subscription').text('Odjavi se od prejemanja e-novičnika');
//           $('.subscription').removeAttr('disabled');
//         } else {
//           $('.unsubscribe').hide();
//           $('.manage').show();
//           $('#managed-email').focus();
//         }
//       });
//   } else {
//     $('.unsubscribe').hide();
//     $('#managed-email').focus();
//   }
});
