<script>
    import { onMount } from "svelte";
    import { getDesktopAPI } from "../lib/getDesktopAPI.js";

    export let currentPage;

    import gameSVG from "/public/icon/game.svg?raw";
    import profileSVG from "/public/icon/profile.svg?raw";
    import settingsSVG from "/public/icon/settings.svg?raw";
    import editSVG from "/public/icon/edit.svg?raw";

    let version = "";
    let os = "";

    const sidebarPages = [
      {
        "name": "Presence",
        "icon": gameSVG,
        "page": "presence",
      },
      {
        "name": "Profile",
        "icon": profileSVG,
        "page": "profile",
      },
      {
        "name": "Status",
        "icon": editSVG,
        "page": "status",
      },
      {
        "name": "Settings",
        "icon": settingsSVG,
        "page": "settings",
      },
    ];
    
    onMount(async () => {
        const desktopAPI = await getDesktopAPI();
        const result = await desktopAPI?.getVer?.();
        const osResult = await desktopAPI?.getOS?.();
        version = result ?? "desktop bridge missing";
        os = osResult ?? "unknown";
    });

    const selectPage = (page) => {
        currentPage = page;
    };
</script>

<section class="sidebar">
    <section class="content">
        {#each sidebarPages as page}
            <button
                type="button"
                class:selected={currentPage === page.page}
                class="item"
                on:click={() => selectPage(page.page)}
            >
                <div class="content">
                    {@html page.icon}
                    <span>{page.name}</span>
                </div>
            </button>
        {/each}
    </section>

    <section class="footer">
        <span class="content">
            <span>{version} - {os}</span>
            <span>(c) 2026 - MIT License</span>
            <span>
                <a
                    href="https://github.com/daveberrys/thiscordrpc"
                    target="_blank"
                >
                    GitHub
                </a>
            </span>
        </span>
    </section>
</section>

<style>
    .sidebar {
        display: flex;
        flex-direction: column;
        padding: 10px;
        background-color: var(--sidebar);

        height: 100vh;
        width: 200px;
        min-width: 200px;
        max-width: 200px;

        .content {
            display: flex;
            flex-direction: column;
            gap: var(--gap);

            .item {
                .content {
                    flex-direction: row;
                }
            }
        }
    }

    .item {
        color: var(--unselected);
        padding: 0.45rem 3rem;
        border-radius: var(--radius);
        font-size: 1rem;
        cursor: pointer;

        border: 0;
        background: transparent;
        text-align: left;

        .content {
            display: flex;
            align-items: center;
            transform: translateX(-2.4rem);
        }

        .content :global(svg) {
            width: 1.75rem !important;
            height: 1.75rem !important;
            max-width: 1.75rem;
            max-height: 1.75rem;
        }
    }
    .item:hover {
        background-color: var(--unselectedHover);
        color: var(--text);
    }

    .item.selected {
        background-color: var(--selected);
        .content {
            color: var(--text);
            opacity: 1;
        }
    }

    .footer {
        margin-top: auto;
        transform: translateY(-1rem);
        color: var(--extraText);
        font-size: 0.75rem;

        .content {
            display: flex;
            flex-direction: column;
            gap: 0.2.5rem;
        }
    }
</style>
