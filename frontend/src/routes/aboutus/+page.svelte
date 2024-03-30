<script>
    import PlaceholderImage from "../../components/image/PlaceholderImage.svelte";
    import SocialProperty1Github from "../../components/image/SocialProperty1Github.svelte";
    import Header from "../../components/header/header_login.svelte";
    import HeaderNon from "../../components/header/header_non.svelte";
    import { onMount } from 'svelte';
    let className = "";
    export { className as class };
    let token;
    let isUserLoggedIn = false;

    onMount(() => {
    token = sessionStorage.getItem('auth_token');
    isUserLoggedIn = !!token; 
  });

  </script>
  <div
  style="{'background: var(--neutral-0, #ffffff);padding: 0px 0px 120px 0px; display: flex; flex-direction: column; gap: 40px; align-items: center; justify-content: flex-start; height: 2200px; position: relative; '}"
>
{#if isUserLoggedIn}
<Header />
{:else}
<HeaderNon />
{/if} <div></div>
    <div
      style="
        color: #000000;
        text-align: center;
        font-family: var(--title-large-font-family, 'DmSans-Bold', sans-serif);
        font-size: var(--title-large-font-size, 60px);
        line-height: var(--title-large-line-height, 76px);
        font-weight: var(--title-large-font-weight, 700);
        position: relative;
        width: 412px;
        height: 62px;
      "
    >
      About Us
    </div>
    <div
      style="
        color: #8c8686;
        text-align: center;
        font-family: var(--body-large-font-family, 'DmSans-Regular', sans-serif);
        font-size: var(--body-large-font-size, 20px);
        line-height: var(--body-large-line-height, 32px);
        font-weight: var(--body-large-font-weight, 400);
        position: relative;
        width: 612px;
      "
    >
    안녕하세요! <br>
    사용자의 목소리를 기반으로 가상의 얼굴을 생성하는 서비스,<br>
    Voice2Face를 개발 중인 Make Zenerator 팀입니다. <br>
    (문의&불편사항: mz240103@gmail.com)<br>


    </div>
    <img src = "/logo/MZ_aboutus.jpg" alt = "MZ_members">
    <div></div><div
    style="
      color: #000000;
      text-align: center;
      font-family: var(--title-large-font-family, 'DmSans-Bold', sans-serif);
      font-size: var(--title-large-font-size, 50px);
      line-height: var(--title-large-line-height, 76px);
      font-weight: var(--title-large-font-weight, 700);
      position: relative;
      width: 412px;
      height: 32px;
    "
  >
    MZ Members
  </div><div></div>
    <div
      style="
        display: flex;
        flex-direction: column;
        gap: 54px;
        align-items: center;
        justify-content: flex-start;
        flex-shrink: 0;
        position: relative;
      "
    >
      <div
        style="
          display: flex;
          flex-direction: row;
          gap: 10px;
          align-items: flex-start;
          justify-content: flex-start;
          flex-shrink: 0;
          position: relative;
        "
      >
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 21px;
            align-items: center;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
        <div
        style="
          display: flex;
          flex-direction: column;
          gap: 18px;
          align-items: flex-start;
          justify-content: flex-start;
          flex-shrink: 0;
          position: relative;
        "
      >
        <div
          style="
            color: #000000;
            text-align: center;
            font-family: 'DmSans-Bold', sans-serif;
            font-size: 30px;
            line-height: 40px;
            font-weight: 700;
            position: relative;
            width: 294px;
            height: 40px;
          "
        >
          신호준
        </div>
      </div>
      <SocialProperty1Github style="flex-shrink: 0" targetPath="https://github.com/internationalwe/"></SocialProperty1Github>
          
          <PlaceholderImage
            style="flex-shrink: 0;"
            targetPath="https://storage.makezenerator.com:9000/voice2face-public/site/aboutus/hojun.jpg"
          ></PlaceholderImage>
        </div>
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 21px;
            align-items: center;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 18px;
              align-items: flex-start;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
            <div
              style="
                color: #000000;
                text-align: center;
                font-family: 'DmSans-Bold', sans-serif;
                font-size: 30px;
                line-height: 40px;
                font-weight: 700;
                position: relative;
                width: 294px;
                height: 40px;
              "
            >
              김태양
            </div>
          </div>
          <SocialProperty1Github style="flex-shrink: 0" targetPath="https://github.com/taeyang916"></SocialProperty1Github>
          <PlaceholderImage
            style="flex-shrink: 0;"
            targetPath=" https://storage.makezenerator.com:9000/voice2face-public/site/aboutus/taeyang.jpg "
          ></PlaceholderImage>
        </div>
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 21px;
            align-items: center;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 18px;
              align-items: flex-start;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
            <div
              style="
                color: #000000;
                text-align: center;
                font-family: 'DmSans-Bold', sans-serif;
                font-size: 30px;
                line-height: 40px;
                font-weight: 700;
                position: relative;
                width: 294px;
                height: 40px;
              "
            >
              정소윤
            </div>
          </div>
          <SocialProperty1Github style="flex-shrink: 0" targetPath="https://github.com/soyoonjeong"></SocialProperty1Github>
          <PlaceholderImage
            style="flex-shrink: 0;"
            targetPath=" https://storage.makezenerator.com:9000/voice2face-public/site/aboutus/soyoon.jpg "
          ></PlaceholderImage>
        </div>
      </div>
      <div
        style="
          display: flex;
          flex-direction: row;
          gap: 10px;
          align-items: flex-start;
          justify-content: flex-start;
          flex-shrink: 0;
          position: relative;
        "
      >
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 21px;
            align-items: center;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 18px;
              align-items: flex-start;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
            <div
              style="
                color: #000000;
                text-align: center;
                font-family: 'DmSans-Bold', sans-serif;
                font-size: 30px;
                line-height: 40px;
                font-weight: 700;
                position: relative;
                width: 294px;
                height: 40px;
              "
            >
              김혜지
            </div>
          </div>
          <SocialProperty1Github style="flex-shrink: 0" targetPath="https://github.com/carboxaminoo"></SocialProperty1Github>
          <PlaceholderImage
            style="flex-shrink: 0;"
            targetPath=" https://storage.makezenerator.com:9000/voice2face-public/site/aboutus/hyeji.jpg "
          ></PlaceholderImage>
        </div>
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 21px;
            align-items: center;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 18px;
              align-items: flex-start;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
            <div
              style="
                color: #000000;
                text-align: center;
                font-family: 'DmSans-Bold', sans-serif;
                font-size: 30px;
                line-height: 40px;
                font-weight: 700;
                position: relative;
                width: 294px;
                height: 40px;
              "
            >
              임서현
            </div>
          </div>
          <SocialProperty1Github style="flex-shrink: 0" targetPath="https://github.com/dlatjgus0612"></SocialProperty1Github>
          <PlaceholderImage
            style="flex-shrink: 0;"
            targetPath="https://storage.makezenerator.com:9000/voice2face-public/site/aboutus/seohyun.jpg"
          ></PlaceholderImage>
        </div>
        <div
          style="
            display: flex;
            flex-direction: column;
            gap: 21px;
            align-items: center;
            justify-content: flex-start;
            flex-shrink: 0;
            position: relative;
          "
        >
          <div
            style="
              display: flex;
              flex-direction: column;
              gap: 18px;
              align-items: flex-start;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
            <div
              style="
                color: #000000;
                text-align: center;
                font-family: 'DmSans-Bold', sans-serif;
                font-size: 30px;
                line-height: 40px;
                font-weight: 700;
                position: relative;
                width: 294px;
                height: 40px;
              "
            >
              성주희
            </div>
          </div>
          <SocialProperty1Github style="flex-shrink: 0" targetPath="https://github.com/jouhy"></SocialProperty1Github>
          <PlaceholderImage
            style="flex-shrink: 0;"
            targetPath=" https://storage.makezenerator.com:9000/voice2face-public/site/aboutus/juhy.jpg "
          ></PlaceholderImage>
        </div>
      </div>
    </div>
  </div>
  