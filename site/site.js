const navigation = document.querySelector("[data-navigation]");

if (navigation) {
  const toggle = navigation.querySelector("button");
  const links = navigation.querySelectorAll("a");

  const closeNavigation = ({ restoreFocus = false } = {}) => {
    navigation.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");

    if (restoreFocus) {
      toggle.focus();
    }
  };

  toggle.addEventListener("click", () => {
    const willOpen = !navigation.classList.contains("is-open");
    navigation.classList.toggle("is-open", willOpen);
    toggle.setAttribute("aria-expanded", String(willOpen));
  });

  links.forEach((link) => {
    link.addEventListener("click", () => {
      closeNavigation();
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !navigation.classList.contains("is-open")) {
      return;
    }

    closeNavigation({ restoreFocus: true });
  });
}

const copyText = async (value) => {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(value);
    return;
  }

  const previousFocus = document.activeElement;
  const fallback = document.createElement("textarea");
  fallback.value = value;
  fallback.setAttribute("readonly", "");
  fallback.style.position = "fixed";
  fallback.style.opacity = "0";
  document.body.append(fallback);
  let copied = false;

  try {
    fallback.select();
    copied = document.execCommand("copy");
  } finally {
    fallback.remove();
    if (previousFocus instanceof HTMLElement) {
      previousFocus.focus({ preventScroll: true });
    }
  }

  if (!copied) {
    throw new Error("Copy command was unavailable");
  }
};

document.querySelectorAll("[data-copy-target]").forEach((button) => {
  const label = button.querySelector("span");
  const status = document.getElementById(button.getAttribute("aria-describedby"));
  const target = document.getElementById(button.dataset.copyTarget);
  const defaultLabel = label.textContent;
  let isCopying = false;
  let resetTimer;

  button.addEventListener("click", async () => {
    if (isCopying) {
      return;
    }

    isCopying = true;
    window.clearTimeout(resetTimer);
    button.setAttribute("aria-busy", "true");

    try {
      await copyText(target.textContent.trim());
      label.textContent = "Copied";
      status.textContent = "Command copied.";
      button.dataset.state = "success";
    } catch {
      label.textContent = "Copy failed";
      status.textContent = "Copy failed. Select the command manually.";
      button.dataset.state = "error";
    } finally {
      isCopying = false;
      button.removeAttribute("aria-busy");
      resetTimer = window.setTimeout(() => {
        label.textContent = defaultLabel;
        status.textContent = "";
        delete button.dataset.state;
      }, 2200);
    }
  });
});
