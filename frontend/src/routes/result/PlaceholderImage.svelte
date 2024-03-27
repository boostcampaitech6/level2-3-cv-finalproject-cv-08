<script>
  let className = "";
  export { className as class };
  export let style;
  export let targetPath = "/join/placeholder-image.svg"
</script>
<img
  class="{'placeholder-image ' + className}"
  style="{'border-radius: 24px;padding: 10px; display: flex; flex-direction: row; gap: 10px; align-items: center; justify-content: center; flex-shrink: 0;height: 393px; position: relative; overflow: visible;' + style}"
  src={targetPath}
/>
