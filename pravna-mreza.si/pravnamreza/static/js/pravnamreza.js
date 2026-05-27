$(document).ready(function () {
  // newsletter form on landing
  $("#newsletter-btn").on("click", function (event) {
    event.preventDefault();

    const campaign_slug = "pravna-mreza";
    const segment_id = 25;
    const email = $("#newsletter-email").val();

    let url = `https://moj.djnd.si/${campaign_slug}/prijava?segment_id=${segment_id}`;
    url += `&email=${encodeURIComponent(email)}`;
    window.open(`${url}`, `_blank`);
    this.loading = false;
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
    const parentPageId = parent.data("load-more-parent");
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
    const currentParams = new URLSearchParams(window.location.search);
    currentParams.forEach((value, key) => {
      loadMoreUrl.searchParams.set(key, value);
    });
    if (parentPageId) {
      loadMoreUrl.searchParams.set("parent", parentPageId);
    }
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
