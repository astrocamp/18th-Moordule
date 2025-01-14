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
    document.getElementById('photo').addEventListener('change', function(event) {
        const file = event.target.files[0]; 
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('preview');
                preview.src = e.target.result;
                preview.style.display = 'block'; 
            };
            reader.readAsDataURL(file); 
        }
    });