<script>
    import minimizeSvg from "/public/topbar/minimize.svg?raw";
    import exitSvg from "/public/topbar/exit.svg?raw";
    import { onMount } from "svelte";
    import { getDesktopAPI } from "../lib/getDesktopAPI.js";
    
    let desktopAPI = null;
    
    function exitApp() {
        desktopAPI?.exitApp?.();
    }
    
    function minimizeApp() {
        desktopAPI?.minimizeApp?.();
    }
    
    onMount(async () => {
        desktopAPI = await getDesktopAPI();
    });
</script>

<main>
    <div class="dragArea pywebview-drag-region" aria-label="Drag window"></div>

    <div class="right">
        <button type="button" class="button minimize" aria-label="Minimize" on:click={minimizeApp}>
            {@html minimizeSvg}
        </button>

        <button type="button" class="button exit" aria-label="Exit" on:click={exitApp}>
            {@html exitSvg}
        </button>
    </div>
</main>

<style>
    main {
        background-color: var(--background);
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        box-sizing: border-box;
    }

    .dragArea {
        flex: 1;
        height: 2.5rem;
        cursor: move;
    }

    .right {
        margin-left: auto;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-end;
        gap: 0.25rem;
    }

    .button {
        width: 2.5rem;
        height: 2.5rem;
        padding: 0;
        border: 0;
        background-color: var(--background);
        color: var(--text);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0.5;
    }

    .button :global(svg) {
        width: 1rem;
        height: 1rem;
        display: block;
        fill: currentColor;
    }

    .minimize:hover {
        background-color: var(--unselectedHover);
        opacity: 0.95;
    } .exit:hover {
        background-color: var(--delete);
        opacity: 0.95;
    }
</style>
