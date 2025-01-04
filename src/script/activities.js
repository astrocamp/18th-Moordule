document.addEventListener("DOMContentLoaded", function() {
    const openActivitiesRules = document.getElementById("openActivitiesRules");
    const rulesAgree = document.getElementById("rulesAgree");
    const activitiesRules = document.getElementById("activitiesRules");
    

    openActivitiesRules.addEventListener("click", () => {
        activitiesRules.classList.remove("hidden");
    });
    
   
    rulesAgree.addEventListener("click", () => {
        activitiesRules.classList.add("hidden");
    });
    
    
    activitiesRules.addEventListener("click", (e) => {
        if (e.target === activitiesRules) {
            activitiesRules.classList.add("hidden");
        }
    });
    });