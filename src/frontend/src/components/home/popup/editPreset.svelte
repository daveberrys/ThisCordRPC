<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { fade, scale } from "svelte/transition";

    type Preset = {
        title: string;
        details: string;
        state: string;
        largeImage: string;
        smallImage: string;
        largeImageText: string;
        smallImageText: string;
    };

    export let preset: Preset;

    const dispatch = createEventDispatcher<{
        close: void;
        save: {
            oldTitle: string;
            title: string;
            details: string;
            state: string;
            largeImage: string;
            smallImage: string;
            largeImageText: string;
            smallImageText: string;
        };
    }>();

    let title = "";
    let details = "";
    let state = "";
    let largeImage = "";
    let smallImage = "";
    let largeImageText = "";
    let smallImageText = "";

    $: if (preset) {
        title = preset.title;
        details = preset.details;
        state = preset.state;
        largeImage = preset.largeImage;
        smallImage = preset.smallImage;
        largeImageText = preset.largeImageText;
        smallImageText = preset.smallImageText;
    }

    function closePopup() {
        dispatch("close");
    }

    function handleOverlayKeydown(event: KeyboardEvent) {
        if (event.key === "Escape" || event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            closePopup();
        }
    }

    function stopDialogKeydown(event: KeyboardEvent) {
        event.stopPropagation();
    }

    function savePreset() {
        dispatch("save", {
            oldTitle: preset.title,
            title,
            details,
            state,
            largeImage,
            smallImage,
            largeImageText,
            smallImageText,
        });
    }
</script>

<div
    class="overlay"
    role="button"
    tabindex="0"
    aria-label="Close edit preset dialog"
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
            <span class="title">Edit Preset</span>
        </div>

        <div class="fields">
            <input class="input" type="text" placeholder="Title" bind:value={title} />

            <div class="row">
                <input class="input" type="text" placeholder="Details" bind:value={details} />
                <input class="input" type="text" placeholder="State" bind:value={state} />
            </div>

            <div class="row">
                <input class="input" type="text" placeholder="Big Image" bind:value={largeImage} />
                <input class="input" type="text" placeholder="Big Image Text" bind:value={largeImageText} />
            </div>

            <div class="row">
                <input class="input" type="text" placeholder="Small Image" bind:value={smallImage} />
                <input class="input" type="text" placeholder="Small Image Text" bind:value={smallImageText} />
            </div>
        </div>

        <div class="actions">
            <button type="button" class="button secondary" on:click={closePopup}>Cancel</button>
            <button type="button" class="button" on:click={savePreset}>Save Changes</button>
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
        width: min(42rem, 100%);
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

    .fields {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .row {
        display: flex;
        gap: 0.75rem;
    }

    .input {
        width: 100%;
        box-sizing: border-box;
        padding: 0.65rem 0.75rem;
        border: 1px solid var(--valueBorder);
        border-radius: var(--radius);
        background-color: var(--input);
        color: var(--text);
        outline: none;
        box-shadow: none;
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

    .button {
        background-color: var(--booleanEnabled);
    }

    .button.secondary {
        background-color: var(--input);
        border: 1px solid var(--valueBorder);
    }

    .button:hover {
        filter: brightness(1.1);
    }
</style>
