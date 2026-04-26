export function getDesktopAPI() {
    return new Promise((resolve) => {
        if (window.pywebview && window.pywebview.api) {
            resolve(window.pywebview.api);
            return;
        }

        function handleReady() {
            window.removeEventListener("pywebviewready", handleReady);

            if (window.pywebview && window.pywebview.api) {
                resolve(window.pywebview.api);
                return;
            }

            resolve(null);
        }

        window.addEventListener("pywebviewready", handleReady);
    });
}
