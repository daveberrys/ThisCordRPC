<script lang="ts">
  import Sidebar from './components/sidebar.svelte';
  import Home from './pages/home.svelte';
  import Settings from './pages/settings.svelte';
  
  let currentPage = 'home';
</script>

<main class="flex">
    <div class="left">
        <Sidebar bind:currentPage />
    </div>
    
    <div class="right">
        {#if currentPage === "home"}
            <Home />
        {:else if currentPage === "settings"}
            <Settings />
        {/if}
    </div>
</main>

<style>
    .flex {
        display: flex;
    }
    
    .right {
        height: 100vh;
        width: 100vw;
        min-height: 100vh;
        max-height: 100vh;
        
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
</style>
