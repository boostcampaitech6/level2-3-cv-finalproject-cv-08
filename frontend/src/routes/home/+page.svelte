<script>
    import ButtonStyleFilled from "../join/ButtonStyleFilled.svelte";
    import ButtonStyleOutlined from "../join/ButtonStyleOutlined.svelte";
    import Header from "../../components/header/header_login.svelte";
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    onMount(() => {
    const token = sessionStorage.getItem('auth_token');
    if (!token) {
      alert(`세션이 만료되었습니다.\n다시 로그인 해주세요.`);
      goto('/');
    }
  });

  </script>
  <div
    style="{'background: var(--neutral-0, #ffffff);padding: 0px 0px 120px 0px; display: flex; flex-direction: column; gap: 180px; align-items: center; justify-content: flex-start; height: 845px; position: relative; ' }"
  >
    <Header/>
    <div
      style="
        padding: 32px 0px 0px 0px;
        display: flex;
        flex-direction: column;
        gap: 100px;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        position: relative;
      "
    >
      <div
        style="
          display: flex;
          flex-direction: column;
          gap: 24px;
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
            gap: 16px;
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
              gap: 8px;
              align-items: flex-start;
              justify-content: flex-start;
              flex-shrink: 0;
              position: relative;
            "
          >
            <div
              style="
                color: var(--6b6b6b, #000000);
                text-align: center;
                font-family: var(
                  --subtitle-large-font-family,
                  'DmSans-Medium',
                  sans-serif
                );
                font-size: var(--subtitle-large-font-size, 28px);
                line-height: var(--subtitle-large-line-height, 32px);
                font-weight: var(--subtitle-large-font-weight, 500);
                position: relative;
                align-self: stretch;
                display: flex;
                align-items: center;
                justify-content: center;
              "
            >
              <strong>무료로 경험하는</strong>
            </div>
            <div
              style="
                color: var(--6b6b6b, #000000);
                text-align: center;
                font-family: var(
                  --title-large-font-family,
                  'DmSans-Bold',
                  sans-serif
                );
                font-size: var(--title-large-font-size, 60px);
                line-height: var(--title-large-line-height, 76px);
                font-weight: var(--title-large-font-weight, 700);
                position: relative;
              "
            >
              얼굴 생성하기
            </div>
          </div>
          <div
            style="
              color: var(--7b95b7, #6b6b6b);
              text-align: center;
              font-family: var(
                --body-large-font-family,
                'DmSans-Regular',
                sans-serif
              );
              font-size: var(--body-large-font-size, 20px);
              line-height: var(--body-large-line-height, 32px);
              font-weight: var(--body-large-font-weight, 400);
              position: relative;
              align-self: stretch;
            "
          >
            목소리를 통해 나의 또 다른 얼굴을
            <br />
            찾아보세요
          </div>
        </div>
        <div
          style="
            display: flex;
            flex-direction: row;
            gap: 24px;
            align-items: flex-start;
            justify-content: flex-start;
            flex-shrink: 0;
            width: 196px;
            position: relative;
            justify-content: center;
          "
        >
          <ButtonStyleFilled
            styleVariant="filled"
            style="
              background: var(--6b6b6b, #000000);
              border-color: var(--6b6b6b, #000000);
              flex-shrink: 0;
            "
            name="생성하기"
            targetPath="/infogather"
          ></ButtonStyleFilled>
          <ButtonStyleOutlined
            style="
              border-color: var(--6b6b6b, #000000);
              flex-shrink: 0;
            "
            name="결과확인"
            targetPath="/resultlist"
          ></ButtonStyleOutlined>
        </div>
      </div>
      <div
        style="
          display: flex;
          flex-direction: column;
          gap: 20px;
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
            gap: 64px;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            position: relative;
            margin-top: 20px;
          "
        >
        
        </div>
        
      </div>
      <img
        class="group3"
        style="
          flex-shrink: 0;
          width: 300px;
          
          position: relative;
          overflow: visible;
          top: -80px;
        "
        src="/logo/boostcampLogo.jpg"
        alt="boostcamp"
      />
    </div>
  </div>



