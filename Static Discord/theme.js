const themeButtonsElements = document.getElementsByClassName("themeSelectionContainer__575f5");
const htmlElement = document.getElementsByTagName("html")[0];
const themeStyleElement = document.getElementById("theme-style");
const someStupidElement = document.getElementsByClassName("container__11d72");
console.log(someStupidElement);

let selectionCircle = document.createElement("div");
selectionCircle.classList.add("selectionCircle_f4288e");
selectionCircle.innerHTML =
	' \
    <svg \
        class="checkmarkCircle__11b1b" foreground="checkmark__1577e" backgroundColor="var(--white-500)" aria-hidden="true" \
        role="img" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"> \
        <circle cx="12" cy="12" r="10" fill="var(--white-500)" class=""></circle> \
        <path fill="currentColor" fill-rule="evenodd" d="M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22Zm5.7-13.3a1 1 0 0 0-1.4-1.4L10 14.58l-2.3-2.3a1 1 0 0 0-1.4 1.42l3 3a1 1 0 0 0 1.4 0l7-7Z" \
        clip-rule="evenodd" class="checkmark__1577e"></path> \
    </svg> \
    ';

for (let i = 0; i < themeButtonsElements.length; i++) {
	themeButtonsElements[i].addEventListener("click", function () {
		let theme = this.getElementsByTagName("div")[0];
		let themeName = theme.getAttribute("aria-label");
		let themeStyle = theme.getAttribute("style");
		let themeIsDark = theme.getAttribute("class").includes("darkOverlay");

		removeSelectedTheme();
		this.getElementsByTagName("div")[0].append(selectionCircle);
		setTheme(themeStyle, themeIsDark, themeName);
	});
}

function removeSelectedTheme() {
	for (let i = 0; i < themeButtonsElements.length; i++) {
		themeButtonsElements[i].getElementsByTagName("div")[0].classList.remove("selected_e5f907");
		let selectedCircles = themeButtonsElements[i].getElementsByClassName("selectionCircle_f4288e");
		if (selectedCircles.length != 0) {
			selectedCircles[0].remove();
		}
	}
}

function setTheme(styleString, isDark, themeName) {
	// Workaround for default themes
	if (styleString === null) {
		styleString = "";
		htmlElement.classList.remove("custom-theme-background");
		someStupidElement[0].classList.remove("themed_b152");
		if (themeName == "Dark") {
			isDark = true;
		}
	}
	// Else is a normal theme
	else {
		htmlElement.classList.add("custom-theme-background");
		someStupidElement[0].classList.add("themed_b152");
		styleString = styleString.replace(
			"background: var(--bg-overlay),",
			".custom-theme-background {--custom-theme-background:"
		);
		styleString = styleString.replace(";", "}");
	}

	// Handle Dark Mode
	if (isDark) {
		htmlElement.classList.remove("theme-light");
		someStupidElement[0].classList.remove("theme-light");
		htmlElement.classList.add("theme-dark");
		someStupidElement[0].classList.add("theme-dark");
	} else {
		htmlElement.classList.remove("theme-dark");
		someStupidElement[0].classList.remove("theme-dark");
		htmlElement.classList.add("theme-light");
		someStupidElement[0].classList.add("theme-light");
	}
	// Inject CSS
	themeStyleElement.innerHTML = styleString;
}
