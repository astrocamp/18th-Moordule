import Alpine from "alpinejs";
import htmx from "htmx.org";
import zxcvbn from "zxcvbn";

import initMap from "./map";
window.zxcvbn = zxcvbn;

setTimeout(() => {
	initMap();
});
Alpine.start();
