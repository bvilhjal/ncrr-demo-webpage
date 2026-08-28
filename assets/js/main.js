// NCRR demo webpage scripts

document.addEventListener("DOMContentLoaded", function () {
  // Footer year.
  document.querySelectorAll("#year").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  // Generic list filter: input[data-filter-target] hides items in the target
  // list whose text does not match the query.
  var inputs = document.querySelectorAll("[data-filter-target]");
  inputs.forEach(function (input) {
    var list = document.querySelector(input.getAttribute("data-filter-target"));
    if (!list) return;

    var note = document.querySelector(input.getAttribute("data-filter-note"));
    var items = Array.prototype.slice.call(
      list.querySelectorAll("[data-filter-item]")
    );

    function applyFilter() {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (item) {
        var match = item.textContent.toLowerCase().indexOf(q) !== -1;
        item.classList.toggle("hidden-by-filter", !match);
        if (match) shown++;
      });
      if (note) {
        note.textContent = q
          ? shown + " of " + items.length + " match \u201c" + input.value.trim() + "\u201d"
          : "";
      }
    }

    input.addEventListener("input", applyFilter);
  });
});
