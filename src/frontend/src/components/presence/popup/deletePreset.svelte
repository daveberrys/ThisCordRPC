<script>
    import { createEventDispatcher } from "svelte";
    import { fade, scale } from "svelte/transition";

    export let title;

    const dispatch = createEventDispatcher();

    function closePopup() {
        dispatch("close");
    }

    function confirmDelete() {
        dispatch("delete", { title });
    }

    function handleOverlayKeydown(event) {
        if (event.key === "Escape" || event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            closePopup();
        }
    }

    function stopDialogKeydown(event) {
        event.stopPropagation();
    }
</script>

<div
    class="overlay"
    role="button"
    tabindex="0"
    aria-label="Close delete preset dialog"
    transition:fade={{ duration: 150 }}
    on:click={closePopup}
    on:keydown={handleOverlayKeydown}
>
    <div
        class="dialog"
        role="dialog"
        aria-modal="true"
        tabindex="-1"
        transition:scale={{ duration: 180, start: 0.9 }}
        on:click|stopPropagation
        on:keydown={stopDialogKeydown}
    >
        <div class="header">
            <span class="title">Delete Preset</span>
        </div>

        <div class="content">
            <p>Delete the preset <strong>{title}</strong>?</p>
            <p class="subText">This action cannot be undone.</p>
        </div>

        <div class="actions">
            <button type="button" class="button secondary" on:click={closePopup}>Cancel</button>
            <button type="button" class="button delete" on:click={confirmDelete}>Delete</button>
        </div>
    </div>
</div>

<style>
    .overlay {
        position: fixed;
        inset: 0;
        z-index: 100;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.65);
        /*backdrop-filter: blur(6px);*/
    }

    .dialog {
        width: min(30rem, 100%);
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1.25rem;
        border: 1px solid var(--valueBorder);
        border-radius: calc(var(--radius) + 0.25rem);
        background: var(--background);
        box-shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
    }

    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    .title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text);
    }

    .content {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        color: var(--text);
    }

    .content p {
        margin: 0;
    }

    .subText {
        color: var(--extraText);
        font-size: 0.95rem;
    }

    .actions {
        display: flex;
        justify-content: flex-end;
        gap: 0.75rem;
    }

    .button {
        padding: 0.65rem 1rem;
        border-radius: var(--radius);
        border: 0;
        cursor: pointer;
        color: var(--text);
        font-size: 0.95rem;
        transition: filter 0.2s ease;
    }

    .button.secondary {
        background-color: var(--input);
        border: 1px solid var(--valueBorder);
    }

    .button.delete {
        background-color: var(--delete);
        border: 1px solid var(--deleteBorder);
    }

    .button:hover {
        filter: brightness(1.1);
    }
</style>
