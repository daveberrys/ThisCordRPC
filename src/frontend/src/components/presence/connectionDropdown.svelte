<script>
    import { onMount } from "svelte";
    import { getDesktopAPI } from "../../lib/getDesktopAPI.js";
    export let status = false
    
    const buttons = [
        { label: 'Connect', onClick: () => desktopAPI?.connectDiscordRPC?.(), class: '' },
    ]
    
    let dropdownToggle = false;
    function showDropdown() {
        dropdownToggle = !dropdownToggle;
    }
    
    let desktopAPI = null;
    onMount(async () => {
      desktopAPI = await getDesktopAPI();
    })
</script>

<main>
    <button on:click={showDropdown} class="secondary">
        {status ? 'Connected' : 'Disconnected'}
    </button>
    
    {#if dropdownToggle}
        <section class="dropdown">
            {#each buttons as button}
                <button
                    on:click={button.onClick}
                    class="{button.class}"
                >
                    {button.label}
                </button>
            {/each}
        </section>
    {/if}
</main>

<style>
    main {
        display: flex;
        position: relative;
        
        .dropdown {
            position: absolute;
            top: 120%;
            left: 0;
            z-index: 10;
            background: var(--input);
            border: 1px solid var(--valueBorder);
            display: flex;
            flex-direction: column;
            width: 100%;
            border-radius: var(--radius);
            overflow: hidden;
            
            button {
                border: none;
                padding: 0.5rem 0;
                border-radius: 0;
            }
        }
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
    
    button.secondary:hover {
        filter: brightness(125%);
    } button:hover {
        filter: brightness(85%);
    }
</style>