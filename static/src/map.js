(() => {
  // src/script/map.js
  window.initMap = function() {
    const address = document.getElementById("address").value;
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ "address": address }, function(results, status) {
      if (status === "OK") {
        const map = new google.maps.Map(document.getElementById("map"), {
          zoom: 15,
          center: results[0].geometry.location
        });
        new google.maps.Marker({
          position: results[0].geometry.location,
          map
        });
      } else {
        console.error("Geocode was not successful for the following reason: " + status);
      }
    });
  };
})();
