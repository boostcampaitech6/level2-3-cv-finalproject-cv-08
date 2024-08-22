<script>
  import { goto } from '$app/navigation';
  import { page } from '$app/stores'; // SvelteKit의 페이지 정보에 접근하기 위해 import
  import { get } from 'svelte/store'; // store 값을 직접 읽기 위해 import
  export let styleVariant = "outlined";
  let className = "";
  export { className as class };
  export let style;
  const variantsClassName = "style-variant-" + styleVariant;
  export let name = "Do something";
  
  export let targetPath = "/";
  export let type="button";
  
  function handleClick() {
    const currentPath = get(page).url.pathname; // 현재 페이지의 경로를 가져옴
    if (currentPath === targetPath) {
      window.location.reload(); // 현재 경로와 targetPath가 같으면 페이지 새로고침
    } else {
      goto(targetPath); // 다르면 targetPath로 이동
    }
  }
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Titan+One&display=swap" rel="stylesheet">


<button
on:click={handleClick} type={type}
  style="{'background: var(--neutral-10, #486284);border-radius: 50px; border-style: solid; border-color: var(--neutral-10, #486284); border-width: 1px; padding: 12px 20px 12px 20px; display: flex; flex-direction: row; gap: 10px; align-items: center; justify-content: center; position: relative; overflow: hidden;' + style}"
>
  <div
    style="
      color: var(--neutral-0, #ffffff);
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