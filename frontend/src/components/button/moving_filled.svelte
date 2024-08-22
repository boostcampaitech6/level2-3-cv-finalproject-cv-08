<script>
    import { goto } from '$app/navigation';
    export let styleVariant = "outlined";
    const variantsClassName = "style-variant-" + styleVariant;
    export let name = "Do something";
    export let type = "button";
    export let targetPath = "/";
    export let id;
    export let latest_id;
    export let gender;

    async function handleClick() {
        // id와 latest_id를 sessionStorage에 저장
        sessionStorage.setItem('id', id);
        sessionStorage.setItem('latest_id', latest_id);
        sessionStorage.setItem('gender', gender);
        // targetPath로 페이지 이동
        goto(targetPath);
    }
    
  </script>
  
  <button
  type = {type}
  on:click={handleClick}
    style="{'background: var(--neutral-10, #6b6b6b);border-radius: 50px; border-style: solid; border-color: var(--neutral-10, #486284); border-width: 1px; padding: 12px 20px 12px 20px; display: flex; flex-direction: row; gap: 10px; align-items: center; justify-content: center; position: relative; overflow: hidden;'}"
  >
    <div
      style="
        color: var(--neutral-0, #ffffff);
        text-align: left;
        font-family: var(--body-small-font-family, 'DmSans-Regular', sans-serif);
        font-size: var(--body-small-font-size, 18px);
        line-height: var(--body-small-line-height, 18px);
        font-weight: var(--body-small-font-weight, 400);
        position: relative;

      "
    >
      <strong>{name}</strong>
    </div>
  </button>