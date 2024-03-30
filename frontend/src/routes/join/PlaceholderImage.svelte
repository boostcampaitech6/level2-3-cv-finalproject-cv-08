<script>
    let className = "";
    export let targetPath = "/join/placeholder-image.svg"
    export { className as class };
    export let style;
  </script>
  <img
    class="{'placeholder-image ' + className}"
    style="{'border-radius: 24px;padding: 10px; display: flex; flex-direction: row; gap: 10px; align-items: center; justify-content: center; align-self: stretch;flex: 1;height: auto; position: relative; overflow: visible;' + style}"
    src= {targetPath}
    alt= "placeholder"
  />