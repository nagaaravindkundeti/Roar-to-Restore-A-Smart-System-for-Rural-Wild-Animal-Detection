function showTable(month) {
  // hide all tables except for the one corresponding to the clicked button
  var tables = document.getElementsByTagName("table");
  for (var i = 0; i < tables.length; i++) {
    if (tables[i].id === month + "-table") {
      tables[i].style.display = "table";
    } else {
      tables[i].style.display = "none";
    }
  }
}