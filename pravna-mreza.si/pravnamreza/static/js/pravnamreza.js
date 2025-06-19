$(document).ready(function () {
  // newsletter form on landing
  $("#newsletter-btn").on("click", function (event) {
    console.log("Subscribing se začne");
    event.preventDefault();
    if ($("#newsletter-terms").is(":checked")) {
      // $('#newsletter-btn').html('Pošiljanje...');
      // reset form
      $(".newsletter-checkbox-label").css({ color: "white" });
      $("#newsletter-success-message").css("display", "none");
      $("#newsletter-error-message").css("display", "none");
      // disable form while processing
      $("#newsletter-btn").prop("disabled", true);
      $("#newsletter-email").prop("disabled", true);
      $("#newsletter-terms").prop("disabled", true);
      fetch("https://podpri.lb.djnd.si/api/subscribe/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: $("#newsletter-email").val(),
          segment_id: 25,
        }),
      })
        .then((res) => {
          if (res.ok) {
            return res.text();
          }
          throw new Error("Response not ok");
        })
        .then((res) => {
          // $('#newsletter-btn').html('Prijavi se');
          $("#newsletter-email").val("");
          $("#newsletter-terms").prop("checked", false);
          $("#newsletter-btn").prop("disabled", false);
          $("#newsletter-email").prop("disabled", false);
          $("#newsletter-terms").prop("disabled", false);
          $("#newsletter-success-message").css("display", "block");
        })
        .catch((error) => {
          // $('#newsletter-btn').html('Prijavi se');
          $("#newsletter-btn").prop("disabled", false);
          $("#newsletter-email").prop("disabled", false);
          $("#newsletter-terms").prop("disabled", false);
          $("#newsletter-error-message").css("display", "block");
        });
    } else {
      $(".newsletter-checkbox-label").css({ color: "red" });
    }
  });

  // load more buttons
  $(".blog-grid-more-button").on("click", function (event) {
    const button = $(this); // this is the button (<a> link) that was clicked

    if (button.hasClass("loading")) {
      return;
    }

    const parent = button.closest("[data-load-more-container]");
    const containerSelector = parent.data("load-more-container");
    const container = parent.find(containerSelector);
    const url = parent.data("load-more-url");
    const shownNumElem = parent.find(".blog-grid-show-count").find(".shown");
    const totalNumElem = parent.find(".blog-grid-show-count").find(".total");
    const offset = Number.parseInt(shownNumElem.text(), 10);
    const total = Number.parseInt(totalNumElem.text(), 10);

    if (!container.length || !shownNumElem.length || offset >= total) {
      return;
    }

    event.preventDefault();

    button.prop("disabled", true);
    button.addClass("loading");

    const loadMoreUrl = new URL(url, window.location.href);
    loadMoreUrl.searchParams.set("offset", offset);

    fetch(loadMoreUrl.toString())
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((html) => {
        container.append(html);
        const newOffset = container.children().length;
        shownNumElem.text(newOffset);

        button.prop("disabled", false);
        button.removeClass("loading");

        if (newOffset >= total) {
          button.parent().remove();
        }
      })
      .catch((error) => {
        console.error("Error loading more posts:", error);
        button.text("Napaka");
      });
  });

  $("body").on("click", ".blog-grid-item", function (event) {
    const item = $(this);

    // Don't navigate if text is selected
    const selectedText = window.getSelection().toString();
    if (selectedText) return;

    if (!event.target.closest("a")) {
      const link = item.find(".blog-grid-title a");
      if (link.length) {
        link[0].click();
      }
    }
  });
});
