import Alpine from "alpinejs";
import htmx from "htmx.org";
import zxcvbn from "zxcvbn";
window.zxcvbn = zxcvbn;
import initMap from "./map";
window.initMap = initMap;
Alpine.start();
