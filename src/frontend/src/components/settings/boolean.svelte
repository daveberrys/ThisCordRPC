<script>
    import { onMount } from "svelte";

    export let name;
    export let desc;
    export let value;

    let temporaryValue;
    let temporaryPositionCircle;
    let animating = false;
    
    function toggle() {
        value = !value;
        animating = true;
        console.log(`${name}: ${value}`)

        if (!value) {
            temporaryValue = "var(--booleanDisabled)";
            temporaryPositionCircle = '-12px';
        } else {
            temporaryValue = "var(--booleanEnabled)";
            temporaryPositionCircle = '12px';
        }
    }

    function onAnimEnd() {
        animating = false;
    }

    onMount(() => {
        toggle()
    })
</script>

<main on:click={toggle}>
    <section class="info">
        <span class="name">{name}</span>
        <span class="desc">{desc}</span>
    </section>

    <div
        class="boolean"
        style="background-color: {temporaryValue}"
    >
        <div
            class="circleWrapper"
            style="transform: translateX({temporaryPositionCircle})"
        >
            <div
                class="circle"
                class:squish={animating}
                on:animationend={onAnimEnd}
            ></div>
        </div>
    </div>
</main>

<style>
    @keyframes squishAnim {
        0% {
            transform: scaleY(1);
        }
        50% {
            transform: scaleY(0.75);
        }
        100% {
            transform: scaleY(1);
        }
    }

    main {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 50px;
        
        padding: 10px 15px;
        border-radius: var(--radius);
        cursor: pointer;

        .info {
            display: flex;
            flex-direction: column;
            gap: var(--gap);

            .name {
                font-size: 1.5rem;
                font-weight: bold;
            }

            .desc {
                font-size: 1rem;
            }
        }

        .boolean {
            border: 1px solid var(--valueBorder);
            padding: 3px 15px;
            border-radius: 999px;
            height: fit-content;
            width: fit-content;

            .circleWrapper {
                transition: transform 0.2s ease-in-out;
            }
            
            .circle {
                padding: 10px;
                background-color: var(--booleanCircle);
                border-radius: 999px;
                
                &.squish {
                    animation: squishAnim 0.2s ease-in-out;
                }
            }
        }
    }
</style>