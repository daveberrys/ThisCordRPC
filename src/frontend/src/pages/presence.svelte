<script lang="ts">
    import { onMount } from "svelte";

    import DiscordRPC from "../components/presence/displayRPC.svelte";
    import DeletePreset from "../components/presence/popup/deletePreset.svelte";
    import EditPreset from "../components/presence/popup/editPreset.svelte";

    type Preset = {
        title: string;
        details: string;
        state: string;
        largeImage: string;
        smallImage: string;
        largeImageText: string;
        smallImageText: string;
    };
    
    let title: string = "";
    let state: string = "";
    let details: string = "";

    let bigImage: string = "";
    let smallImage: string = "";
    let bigImageText: string = "";
    let smallImageText: string = "";

    let connectionError: string = "";
    let presetError: string = "";
    let pyAPI: any = null;
    let presets: Preset[] = [];
    let selectedPresetForEdit: Preset | null = null;
    let selectedPresetForDelete: string | null = null;

    function getErrorMessage(error: any) {
        if (error && typeof error === "object" && "message" in error) {
            return String((error as any).message);
        }

        return String(error);
    }

    const getPyAPI = () =>
        new Promise<any>((resolve) => {
            if (window.pywebview?.api) {
                resolve(window.pywebview.api);
                return;
            }

            const handleReady = () => {
                window.removeEventListener("pywebviewready", handleReady);
                resolve(window.pywebview?.api);
            };

            window.addEventListener("pywebviewready", handleReady);
        });

    async function updatePresence() {
        await clearPresence();
        await pyAPI?.updateDiscordRPC?.(
            title,
            details,
            state,
            bigImage,
            smallImage,
            bigImageText,
            smallImageText,
        );
    }
    async function clearPresence() {
        await pyAPI?.clearDiscordRPC?.();
    }

    async function loadPresets() {
        presetError = "";

        if (!pyAPI) {
            presetError = "Backend API is not ready yet. Try restarting the app.";
            presets = [];
            return;
        }

        try {
            const presetData = await pyAPI?.loadPresets?.();
            presets = Object.values((presetData?.presets ?? {}) as Record<string, Preset>);
        } catch (error) {
            presetError = "Failed to load presets: " + getErrorMessage(error);
            presets = [];
        }
    }

    async function savePresence() {
        presetError = "";

        if (!title.trim()) {
            presetError = "Preset title is required.";
            return;
        }

        try {
            await pyAPI?.savePreset?.(
                title,
                details,
                state,
                bigImage,
                smallImage,
                bigImageText,
                smallImageText,
            );
            await loadPresets();
        } catch (error) {
            presetError = "Failed to save preset: " + getErrorMessage(error);
        }
    }

    function usePreset(preset: Preset) {
        title = preset.title;
        details = preset.details;
        state = preset.state;
        bigImage = preset.largeImage;
        smallImage = preset.smallImage;
        bigImageText = preset.largeImageText;
        smallImageText = preset.smallImageText;
    }

    function openEditPreset(preset: Preset) {
        selectedPresetForEdit = preset;
    } function closeEditPreset() {
        selectedPresetForEdit = null;
    } function openDeletePreset(title: string) {
        selectedPresetForDelete = title;
    } function closeDeletePreset() {
        selectedPresetForDelete = null;
    }

    async function saveEditedPreset(event: CustomEvent<{
        oldTitle: string;
        title: string;
        details: string;
        state: string;
        largeImage: string;
        smallImage: string;
        largeImageText: string;
        smallImageText: string;
    }>) {
        const preset = event.detail;
        presetError = "";

        if (!preset.title.trim()) {
            presetError = "Preset title is required.";
            return;
        }

        try {
            await pyAPI?.editPreset?.(
                preset.oldTitle,
                preset.title,
                preset.details,
                preset.state,
                preset.largeImage,
                preset.smallImage,
                preset.largeImageText,
                preset.smallImageText,
            );
            closeEditPreset();
            await loadPresets();
            usePreset({
                title: preset.title,
                details: preset.details,
                state: preset.state,
                largeImage: preset.largeImage,
                smallImage: preset.smallImage,
                largeImageText: preset.largeImageText,
                smallImageText: preset.smallImageText,
            });
        } catch (error) {
            presetError = "Failed to update preset: " + getErrorMessage(error);
        }
    }

    async function deletePreset(event: CustomEvent<{ title: string }>) {
        presetError = "";

        try {
            await pyAPI?.deletePreset?.(event.detail.title);
            closeDeletePreset();
            await loadPresets();
        } catch (error) {
            presetError = "Failed to delete preset: " + getErrorMessage(error);
        }
    }

    let isConnected: boolean = false;
    async function checkConnected() {
        isConnected = await pyAPI?.checkConnected?.();
        connectionError = (await pyAPI?.getDiscordRPCError?.()) ?? "";
    }

    onMount(async () => {
        pyAPI = await getPyAPI();
        await pyAPI?.connectDiscordRPC?.();
        await checkConnected();
        setInterval(checkConnected, 5000);
        await loadPresets();
    });
</script>

<main>
    <div class="changers">
        <section class="s1">
            <input class="input" id="title" type="text" placeholder="Title" bind:value={title} />
        </section>

        <section class="s2">
            <input class="input" id="details" type="text" placeholder="Details" bind:value={details} />
            <input class="input" id="state" type="text" placeholder="State" bind:value={state} />
        </section>

        <section class="s3">
            <input class="input" id="bigImage" type="text" placeholder="Big Image" bind:value={bigImage} />
            <input class="input" id="bigImageText" type="text" placeholder="Big Image Text" bind:value={bigImageText} />
            <input class="input" id="smallImage" type="text" placeholder="Small Image" bind:value={smallImage} />
            <input class="input" id="smallImageText" type="text" placeholder="Small Image Text" bind:value={smallImageText} />
        </section>

        <section class="s4">
            <button on:click={pyAPI?.connectDiscordRPC?.()} class="button secondary">Reconnect</button>
            <button on:click={clearPresence} class="button secondary">Clear</button>
            <button on:click={savePresence} class="button">Save</button>
            <button on:click={updatePresence} class="button">Update</button>
            {#if connectionError}
                <span class="errorText">{connectionError}</span>
            {/if}
            {#if presetError}
                <span class="errorText">{presetError}</span>
            {/if}
        </section>
    </div>
    
    <DiscordRPC
        title={title}
        state={state}
        details={details}
        bigImage={bigImage}
        smallImage={smallImage}
        bigImageText={bigImageText}
        smallImageText={smallImageText}
    />
    
    <div class="displayAllPreset">
        {#if presets.length === 0}
            <span class="emptyState">No presets saved yet.</span>
        {:else}
            {#each presets as preset (preset.title)}
                <div class="programs">
                    <DiscordRPC
                        title={preset.title}
                        state={preset.state}
                        details={preset.details}
                        bigImage={preset.largeImage}
                        smallImage={preset.smallImage}
                        bigImageText={preset.largeImageText}
                        smallImageText={preset.smallImageText}
                    />
                    
                    <section class="bottom">
                        <button on:click={() => usePreset(preset)}>Use</button>
                        <button class="secondary" on:click={() => openEditPreset(preset)}>Edit</button>
                        <button class="delete" on:click={() => openDeletePreset(preset.title)}>Delete</button>
                    </section>
                </div>
            {/each}
        {/if}
    </div>

    {#if selectedPresetForEdit}
        <EditPreset
            preset={selectedPresetForEdit}
            on:close={closeEditPreset}
            on:save={saveEditedPreset}
        />
    {/if}

    {#if selectedPresetForDelete}
        <DeletePreset
            title={selectedPresetForDelete}
            on:close={closeDeletePreset}
            on:delete={deletePreset}
        />
    {/if}
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }
    
    .changers {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        width: 35rem;
        /*background-color: white;*/
        
        section.s2, section.s3 {
            display: flex;
            flex-direction: row;
            gap: 0.5rem;
            
            .input {
                width: 100%;
            }
        }
        
        section.s4 {
            display: flex;
            flex-direction: row;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
    }
    
    .displayAllPreset {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        box-sizing: border-box;

        padding-right: 0.5rem;
        padding-bottom: 2.75rem;

        max-height: 60vh;
        scrollbar-width: thin;
        scrollbar-color: var(--scrollbar) var(--background);
        overflow-y: scroll;

        .programs {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            
            background-color: var(--input);
            border: 1px solid var(--valueBorder);
            padding: 1rem;
            border-radius: var(--radius);
        }

        .bottom {
            display: flex;
            gap: 0.75rem;
        }
    }
    
    .emptyState {
        color: var(--extraText);
    }

    .errorText {
        color: #ffb4b4;
        font-size: 0.9rem;
    }
    
    /* ============= global! ============= */
    /* input values */
    .input {
        padding: 0.5rem;
        border: 1px solid var(--valueBorder);
        border-radius: var(--radius);
        background-color: var(--input);
        color: var(--text);
        outline: none;
        box-shadow: none;
    }
    
    .input {
        width: 100%;
        box-sizing: border-box;
    }
    
    /* buttons */
    button {
        padding: 0.65rem 1.5rem;
        border: 0;
        border-top: 1px solid var(--faintGradientButton);
        border-bottom: 1px solid var(--faintGradientButton);
        border-radius: var(--radius);
        background-color: var(--booleanEnabled);
        color: var(--text);
        font-size: 1rem;
        filter: brightness(100%);
        transition: filter 0.2s ease;
        cursor: pointer;
    }
    
    button.secondary {
        background-color: var(--input);
        color: var(--text);
        border: 1px solid var(--valueBorder);
    }
    
    button.delete {
        background-color: var(--delete);
        color: var(--text);
        border: 1px solid var(--deleteBorder);
    }
    
    button.secondary:hover {
        filter: brightness(125%);
    } button:hover {
        filter: brightness(85%);
    }
</style>
