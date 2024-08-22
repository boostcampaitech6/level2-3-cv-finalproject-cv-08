<script>
    export let styleVariant = "outlined";
    let className = "";
    export { className as class };
    export let style;
    const variantsClassName = "style-variant-" + styleVariant;
    export let name = "Do something"
    import { goto } from '$app/navigation';
    export let targetPath = "/";
    function handleClick() {
      goto(targetPath); // 버튼 클릭 시 targetPath로 이동
    }
  </script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Titan+One&display=swap" rel="stylesheet">


  <button on:click={handleClick}
    style="{'border-radius: 50px; border-style: solid; border-color: var(--neutral-10, #ffffff); border-width: 1px; padding: 12px 20px 12px 20px; display: flex; flex-direction: row; gap: 10px; align-items: center; justify-content: center; position: relative; overflow: hidden;' + style}"
  >
    <div
      style="
        color: var(--neutral-10, #6b6b6b);
        text-align: left;
        font-family: var(--body-small-font-family, 'DmSans-Regular', sans-serif);
        font-size: var(--body-small-font-size, 22px);
        line-height: var(--body-small-line-height, 24px);
        font-weight: var(--body-small-font-weight, 400);
        position: relative;
      "
    >
      {name}
    </div>
  </button>