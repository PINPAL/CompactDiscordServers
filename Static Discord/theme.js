const themeButtonsElements = document.getElementsByClassName("themeSelectionContainer__575f5");
const htmlElement = document.getElementsByTagName("html")[0];
const themeStyleElement = document.getElementById("theme-style");

for (let i = 0; i < themeButtonsElements.length; i++) {
	themeButtonsElements[i].addEventListener("click", function () {
		let theme = this.getElementsByTagName("div")[0];
		let themeName = theme.getAttribute("aria-label");
		let themeStyle = theme.getAttribute("style");
		let themeIsDark = theme.getAttribute("class").includes("darkOverlay");

		setTheme(themeStyle, themeIsDark, themeName);
	});
}

function setTheme(styleString, isDark, themeName) {
	// Workaround for default themes
	if (styleString === null) {
		styleString = "";
		htmlElement.classList.remove("custom-theme-background");
		if (themeName == "Dark") {
			isDark = true;
		}
	}
	// Else is a normal theme
	else {
		htmlElement.classList.add("custom-theme-background");
		styleString = styleString.replace(
			"background: var(--bg-overlay),",
			".custom-theme-background {--custom-theme-background:"
		);
		styleString = styleString.replace(";", "}");
	}

	// Handle Dark Mode
	if (isDark) {
		htmlElement.classList.remove("theme-light");
		htmlElement.classList.add("theme-dark");
	} else {
		htmlElement.classList.remove("theme-dark");
		htmlElement.classList.add("theme-light");
	}
	// Inject CSS
	themeStyleElement.innerHTML = styleString;
}
