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
    padding: 1rem;
  }
</style>
