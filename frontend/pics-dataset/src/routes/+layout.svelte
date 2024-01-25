<script lang="ts">
  import { ensureWSConnected } from '$lib/wslib'
  import { onMount } from 'svelte'
  import WSIndicator from '$lib/components/WSIndicator.svelte'

  onMount(ensureWSConnected)
</script>

<div class="app">
  <main>
    <nav>
      <a href="">Dataset</a>
      <a href="">Browser</a>

      <WSIndicator />
    </nav>
    <slot />
  </main>
</div>

<style>
  nav {
    display: flex;
    align-items: center;
  }
  nav a {
    padding-right: 5px;
    border-left: 1px solid #000;
    padding-left: 5px;
  }
</style>
