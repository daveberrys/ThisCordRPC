<script lang="ts">
  import Sidebar from './components/sidebar.svelte';
  import Topbar from './components/topbar.svelte';

  import Presence from './pages/presence.svelte';
  import Settings from './pages/settings.svelte';
  import Profile from './pages/profile.svelte';
  import Status from './pages/status.svelte';

  let currentPage = 'presence';
</script>

<main class="flex">
    <div class="left">
        <Sidebar bind:currentPage />
    </div>
    
    <div class="right">
        <Topbar/>
        <div class="content">
            {#if currentPage === "presence"}
                <Presence />
            {:else if currentPage === "settings"}
                <Settings />
            {:else if currentPage === "profile"}
                <Profile />
            {:else if currentPage === "status"}
                <Status />
            {/if}
        </div>
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
        
        .content {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
    }
</style>
