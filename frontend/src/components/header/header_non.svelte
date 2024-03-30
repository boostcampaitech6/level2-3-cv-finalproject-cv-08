<script>
    import ButtonStyleFilled from "../../routes/join/ButtonStyleFilled.svelte";
    let className = "";
    export { className as class };

    
  </script>
<style global>
     a {
    text-decoration: none;
  }

  @font-face {
    font-family: 'yg-jalnan';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_four@1.2/JalnanOTF00.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
</style>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Titan+One&display=swap" rel="stylesheet">


<div
  style="
    background: var(--neutral-0, #ffffff);
    border-style: solid;
    border-color: var(--neutral-2, #dee5ed);
    border-width: 0px 0px 0.5px 0px;
    padding: 8px 98px 8px 98px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
    width: 1440px;
    height: 72px;
    position: relative;
    overflow: hidden;
  "
>
<div>
  <a href="/" style="flex-shrink: 0; width: 299px; height: 55px; position: static">
      <div
    style="
    color: var(--7b95b7, #6b6b6b);
    text-align: center;
    font-family: 'yg-jalnan';
    line-height: 28px;
    font-weight: 400;
    font-size: 23px;
    position: absolute;
    left: 173px;
    top: 25px;
    "
  >
    <strong>Make Zenerator</strong>
  </div>
  <img
  class="{'image-2 ' + className}"
  style="
    width: 70px;
    position: absolute;
    left: 100px;
    top: 5px;
    object-fit: cover;
  "
  src="./logo/logo.png"
  alt="logo"
/>
    </a>
    </div>
  <div
    style="
      display: flex;
      flex-direction: row;
      gap: 48px;
      align-items: center;
      justify-content: flex-start;
      flex-shrink: 0;
      position: relative;
    "
  >
    <a href="/aboutus"
    style="
    color: var(--7b95b7, #6b6b6b);
    text-align: center;
    font-family: var(
      --body-small-font-family,
      'DmSans-Regular',
      sans-serif
    );
    font-size: var(--body-small-font-size, 24px);
    line-height: var(--body-small-line-height, 24px);
    font-weight: var(--body-small-font-weight, 400);
    position: relative;
  "
>
      About us
</a>
    <a href="/login" 
    style="
    color: var(--7b95b7, #6b6b6b);
    text-align: center;
    font-family: var(
      --body-small-font-family,
      'DmSans-Regular',
      sans-serif
    );
    font-size: var(--body-small-font-size, 22px);
    line-height: var(--body-small-line-height, 24px);
    font-weight: var(--body-small-font-weight, 400);
    position: relative;
  "
>
      로그인  
</a>
    <ButtonStyleFilled
      styleVariant="filled"
      style="
        background: var(--6b6b6b, #000000);
        border-color: var(--7b95b7, #6b6b6b);
        flex-shrink: 0;
      "
      name ="회원가입"
      targetPath="/join"
      
    ></ButtonStyleFilled>
  </div>
</div>