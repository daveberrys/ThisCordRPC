<script>
    export let title;
    export let details;
    export let state;
    export let bigImage;
    export let smallImage;
    export let bigImageText;
    export let smallImageText;
</script>

<div class="displayRPC">
    <section class="left">
        <section class="imageTooltipParent bigTooltipParent">
            <img src={bigImage} alt={title} class="bigImage"/>
            {#if bigImageText}
                <section class="imageTooltipChild big">
                    {bigImageText}
                </section>
            {/if}
        </section>

        {#if smallImage}
            <section class="imageTooltipParent">
                <img src={smallImage} alt={title} class="smallImage"/>
                {#if smallImageText}
                    <section class="imageTooltipChild small">
                        {smallImageText}
                    </section>
                {/if}
            </section>
        {/if}
    </section>
    
    <section class="right">
        <span class="title">{title}</span>
        <span>{details}</span>
        <span>{state}</span>
    </section>
</div>

<style>
    .displayRPC {
        display: flex;
        flex-direction: row;
        gap: 0.5rem;
        
        .left {
            .bigImage {
                width: 100px;
                height: auto;
                border-radius: var(--radius);
            }
            
            .smallImage {
                width: 35px;
                height: auto;
                
                position: absolute;
                top: -25px;
                left: -30px;
                border: 2px solid var(--background);
                background-color: var(--background);
                border-radius: 100%;
            }
            
            .imageTooltipParent {
                position: relative;
                display: inline-block;
            }
            
            .imageTooltipChild.big,
            .imageTooltipChild.small {
                margin-bottom: 0.5rem;
            }
            
            .imageTooltipChild {
                position: absolute;
                z-index: 1;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background-color: var(--input);
                border: 1px solid var(--valueBorder);
                color: var(--text);
                padding: 0.5rem;
                border-radius: var(--radius);
                white-space: nowrap;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.2s ease;
            }
            
            .imageTooltipParent:hover .imageTooltipChild {
                opacity: 1;
            }
        }
        
        .right {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            
            .title {
                font-weight: bold;
                font-size: 1.25rem;
            }
        }
    }
</style>
