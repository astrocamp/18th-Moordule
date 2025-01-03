
const openMeetingRulesModalButton = document.getElementById("openMeetingRulesModal");
const agree = document.getElementById("agree");
const meetingRulesModal = document.getElementById("meetingRulesModal");

// 顯示模態框
openMeetingRulesModalButton.addEventListener("click", () => {
    meetingRulesModal.classList.remove("hidden");
});

// 關閉模態框
agree.addEventListener("click", () => {
    meetingRulesModal.classList.add("hidden");
});

// 點擊模態框外部關閉
meetingRulesModal.addEventListener("click", (e) => {
    if (e.target === meetingRulesModal) {
        meetingRulesModal.classList.add("hidden");
    }
});
